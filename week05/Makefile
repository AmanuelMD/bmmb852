SRA_ACCESSION := SRR40580480

# Human mtDNA is 16,569 bp. For 10x coverage with 151 bp paired-end reads:
# N = (16,569 * 10) / (151 * 2) ≈ 549 read pairs
READ_LIMIT := 549

SAMPLE_NAME := mtND4_ND5_base_editing
THREADS ?= 4

# Reference
REFERENCE_SOURCE := ../week02/data/human_mtDNA.fa
REFERENCE_DIR := data/reference
REFERENCE_FASTA := $(REFERENCE_DIR)/NC_012920.1.fa
BWA_INDEX := $(REFERENCE_FASTA).bwt

# Raw reads
RAW_DIR := data/raw
RAW_R1 := $(RAW_DIR)/$(SAMPLE_NAME)_R1.fastq
RAW_R2 := $(RAW_DIR)/$(SAMPLE_NAME)_R2.fastq

# Trimmed reads
TRIM_DIR := data/trimmed
TRIM_R1 := $(TRIM_DIR)/$(SAMPLE_NAME)_trimmed_R1.fastq
TRIM_R2 := $(TRIM_DIR)/$(SAMPLE_NAME)_trimmed_R2.fastq

# QC
FASTQC_RAW_DIR := results/fastqc_raw
FASTQC_TRIM_DIR := results/fastqc_trimmed
FASTP_DIR := results/fastp

RAW_QC := $(FASTQC_RAW_DIR)/$(SAMPLE_NAME)_R1_fastqc.html
TRIM_QC := $(FASTQC_TRIM_DIR)/$(SAMPLE_NAME)_trimmed_R1_fastqc.html
FASTP_HTML := $(FASTP_DIR)/fastp_report.html
FASTP_JSON := $(FASTP_DIR)/fastp_report.json

# Alignment
ALIGN_DIR := results/alignment
BAM := $(ALIGN_DIR)/$(SAMPLE_NAME).sorted.bam
BAI := $(BAM).bai
FLAGSTAT := $(ALIGN_DIR)/$(SAMPLE_NAME).flagstat.txt
COVERAGE := $(ALIGN_DIR)/coverage.txt


.PHONY: all clean

all: $(RAW_QC) $(TRIM_QC) $(FLAGSTAT) $(COVERAGE)


# Download a subset of 549 paired-end reads
$(RAW_R1) $(RAW_R2):
	mkdir -p $(RAW_DIR)
	prefetch $(SRA_ACCESSION) --max-size 1G
	fastq-dump --split-files -X $(READ_LIMIT) --outdir $(RAW_DIR) $(SRA_ACCESSION)
	mv $(RAW_DIR)/$(SRA_ACCESSION)_1.fastq $(RAW_R1)
	mv $(RAW_DIR)/$(SRA_ACCESSION)_2.fastq $(RAW_R2)


# FastQC on raw reads
$(RAW_QC): $(RAW_R1) $(RAW_R2)
	mkdir -p $(FASTQC_RAW_DIR)
	fastqc --threads $(THREADS) --outdir $(FASTQC_RAW_DIR) $(RAW_R1) $(RAW_R2)


# Trim and filter reads
$(TRIM_R1) $(TRIM_R2): $(RAW_R1) $(RAW_R2)
	mkdir -p $(TRIM_DIR) $(FASTP_DIR)
	fastp \
		--in1 $(RAW_R1) \
		--in2 $(RAW_R2) \
		--out1 $(TRIM_R1) \
		--out2 $(TRIM_R2) \
		--detect_adapter_for_pe \
		--thread $(THREADS) \
		--qualified_quality_phred 20 \
		--length_required 50 \
		--html $(FASTP_HTML) \
		--json $(FASTP_JSON)


# FastQC on trimmed reads
$(TRIM_QC): $(TRIM_R1) $(TRIM_R2)
	mkdir -p $(FASTQC_TRIM_DIR)
	fastqc --threads $(THREADS) --outdir $(FASTQC_TRIM_DIR) $(TRIM_R1) $(TRIM_R2)


# Copy the Week 02 mitochondrial reference
$(REFERENCE_FASTA): $(REFERENCE_SOURCE)
	mkdir -p $(REFERENCE_DIR)
	cp $(REFERENCE_SOURCE) $(REFERENCE_FASTA)


# Index reference for BWA
$(BWA_INDEX): $(REFERENCE_FASTA)
	bwa index $(REFERENCE_FASTA)


# Align reads and create sorted BAM
$(BAM): $(TRIM_R1) $(TRIM_R2) $(BWA_INDEX)
	mkdir -p $(ALIGN_DIR)
	bwa mem -t $(THREADS) $(REFERENCE_FASTA) $(TRIM_R1) $(TRIM_R2) | \
		samtools sort -o $(BAM) -


# Index BAM
$(BAI): $(BAM)
	samtools index $(BAM)


# Alignment statistics
$(FLAGSTAT): $(BAM)
	samtools flagstat $(BAM) > $(FLAGSTAT)


# Per-base coverage
$(COVERAGE): $(BAM)
	samtools depth -a $(BAM) > $(COVERAGE)


clean:
	rm -rf data results $(SRA_ACCESSION)