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

write.csv(counts, OUTPUT, row.names = FALSE)

cat("# Transcripts:", nrow(counts), "\n")
cat("# Samples:", length(SAMPLES), "\n")
cat("# Saved:", OUTPUT, "\n")
