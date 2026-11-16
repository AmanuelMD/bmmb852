# Sum Salmon transcript counts into gene-level counts.

INPUT <- "results/transcript_counts.csv"
GTF <- "../week11/gtf/chr22.gtf"
OUTPUT <- "results/transcripts_as_genes.csv"

# Extract a named attribute from a GTF annotation.
get_attribute <- function(x, key) {
  pattern <- paste0('(?:^|;[[:space:]]*)', key, ' "([^"]+)"')
  m <- regexec(pattern, x, perl = TRUE)
  matches <- regmatches(x, m)
  vapply(matches, function(z) {
    if (length(z) >= 2) z[2] else NA_character_
  }, character(1))
}

# Read transcript annotations from the GTF.
gtf <- read.delim(
  GTF, header = FALSE, comment.char = "#",
  quote = "", stringsAsFactors = FALSE
)

gtf <- gtf[gtf[[3]] == "transcript", ]

annotation <- data.frame(
  transcript_id = get_attribute(gtf[[9]], "transcript_id"),
  gene_id = get_attribute(gtf[[9]], "gene_id"),
  gene_name = get_attribute(gtf[[9]], "gene_name")
)

annotation <- annotation[!duplicated(annotation$transcript_id), ]

# Read the Salmon transcript count matrix.
counts <- read.csv(INPUT, check.names = FALSE)

# Match each transcript to its gene.
idx <- match(counts$transcript_id, annotation$transcript_id)

if (anyNA(idx)) {
  stop(sum(is.na(idx)), " transcripts have no GTF annotation")
}

mapped <- cbind(
  annotation[idx, c("gene_id", "gene_name")],
  counts[-1]
)

# Sum counts for transcripts belonging to the same gene.
sample_columns <- names(counts)[-1]

gene_counts <- aggregate(
  mapped[sample_columns],
  by = list(gene_id = mapped$gene_id),
  FUN = sum
)

# Add gene names.
gene_names <- mapped[!duplicated(mapped$gene_id),
                     c("gene_id", "gene_name")]

gene_counts <- merge(
  gene_names, gene_counts,
  by = "gene_id",
  sort = FALSE
)

write.csv(gene_counts, OUTPUT, row.names = FALSE)

cat("# Genes:", nrow(gene_counts), "\n")
cat("# Samples:", length(sample_columns), "\n")
cat("# Saved:", OUTPUT, "\n")
