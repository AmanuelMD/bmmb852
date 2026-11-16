# Combine Salmon transcript counts across six RNA-seq samples.

SAMPLES <- c("HBR_1", "HBR_2", "HBR_3",
             "UHR_1", "UHR_2", "UHR_3")

OUTPUT <- "results/transcript_counts.csv"

# Read the first sample to establish transcript IDs.
first <- read.delim(file.path("counts", SAMPLES[1], "quant.sf"))

counts <- data.frame(transcript_id = first$Name)

# Add estimated read counts from each sample.
for (sample in SAMPLES) {
  path <- file.path("counts", sample, "quant.sf")
  quant <- read.delim(path)

  if (anyDuplicated(quant$Name)) {
    stop("Duplicate transcript IDs in ", sample)
  }

  idx <- match(counts$transcript_id, quant$Name)

  if (anyNA(idx) || nrow(quant) != nrow(counts)) {
    stop("Transcript IDs do not match for ", sample)
  }

  counts[[sample]] <- quant$NumReads[idx]

  cat("# Processed:", sample, "\n")
}


# Read transcript-to-gene annotations from the GTF.
gtf <- read.delim(
  "../week11/gtf/chr22.gtf",
  header = FALSE,
  comment.char = "#",
  quote = "",
  stringsAsFactors = FALSE
)

gtf <- gtf[gtf[[3]] == "transcript", ]

get_attribute <- function(x, key) {
  pattern <- paste0('(?:^|;[[:space:]]*)', key, ' "([^"]+)"')
  matches <- regmatches(x, regexec(pattern, x, perl = TRUE))
  vapply(matches, function(z) {
    if (length(z) >= 2) z[2] else NA_character_
  }, character(1))
}

annotation <- data.frame(
  transcript_id = get_attribute(gtf[[9]], "transcript_id"),
  gene_id = get_attribute(gtf[[9]], "gene_id"),
  gene_name = get_attribute(gtf[[9]], "gene_name")
)

annotation <- annotation[!duplicated(annotation$transcript_id), ]

idx <- match(counts$transcript_id, annotation$transcript_id)

if (anyNA(idx)) {
  stop("Some transcripts have no GTF annotation")
}

counts <- cbind(
  counts["transcript_id"],
  annotation[idx, c("gene_id", "gene_name")],
  counts[-1]
)

write.csv(counts, OUTPUT, row.names = FALSE)

cat("# Transcripts:", nrow(counts), "\n")
cat("# Samples:", length(SAMPLES), "\n")
cat("# Saved:", OUTPUT, "\n")
