
# Week 07: Variant calling using human mitochondrial DNA
# Reference genome: NC_012920.1 (16,569 bp)
# Download 1,500 paired-end reads to target approximately 20x coverage.
# Actual coverage will be calculated after alignment.

SRA_ACCESSION := SRR10069469
READ_LIMIT := 1500
SAMPLE_NAME := SRR10069469
THREADS ?= 4

# Reference
REFERENCE_SOURCE := ../week02/data/human_mtDNA.fa
REFERENCE_DIR := data/reference
REFERENCE_FASTA := $(REFERENCE_DIR)/NC_012920.1.fa
BWA_INDEX := $(REFERENCE_FASTA).bwt
FASTA_INDEX := $(REFERENCE_FASTA).fai

# Raw reads
RAW_DIR := data/raw
RAW_R1 := $(RAW_DIR)/$(SAMPLE_NAME)_R1.fastq
RAW_R2 := $(RAW_DIR)/$(SAMPLE_NAME)_R2.fastq

# Trimmed reads
TRIM_DIR := data/trimmed
TRIM_R1 := $(TRIM_DIR)/$(SAMPLE_NAME)_trimmed_R1.fastq
TRIM_R2 := $(TRIM_DIR)/$(SAMPLE_NAME)_trimmed_R2.fastq

# Quality control
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
COVERAGE_SUMMARY := $(ALIGN_DIR)/coverage_summary.txt

# Variant calling
VCF_DIR := results/variants
VCF := $(VCF_DIR)/$(SAMPLE_NAME).vcf.gz
VCF_INDEX := $(VCF).csi
VCF_STATS := $(VCF_DIR)/variant_stats.txt

.PHONY: all clean

all: $(RAW_QC) $(TRIM_QC) $(FLAGSTAT) $(COVERAGE_SUMMARY) $(VCF_STATS) $(VCF_INDEX)


# Download 1,500 paired-end reads
$(RAW_R1) $(RAW_R2) &: 
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
$(TRIM_R1) $(TRIM_R2) &: $(RAW_R1) $(RAW_R2)
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


# Copy mitochondrial reference
$(REFERENCE_FASTA): $(REFERENCE_SOURCE)
	mkdir -p $(REFERENCE_DIR)
	cp $(REFERENCE_SOURCE) $(REFERENCE_FASTA)


# Index reference for BWA
$(BWA_INDEX): $(REFERENCE_FASTA)
	bwa index $(REFERENCE_FASTA)


# Index reference for bcftools
$(FASTA_INDEX): $(REFERENCE_FASTA)
	samtools faidx $(REFERENCE_FASTA)


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


# Summarize mean coverage and breadth
$(COVERAGE_SUMMARY): $(COVERAGE)
	awk '{total += $$3; n++; if ($$3 > 0) covered1++; if ($$3 >= 10) covered10++} \
	END {if (n > 0) { \
	printf "Genome positions: %d\n", n; \
	printf "Mean coverage: %.2fx\n", total/n; \
	printf "Breadth at 1x: %.2f%%\n", 100*covered1/n; \
	printf "Breadth at 10x: %.2f%%\n", 100*covered10/n \
	} else {print "No coverage data"}}' $(COVERAGE) > $(COVERAGE_SUMMARY)


# Call variants and generate compressed VCF
$(VCF): $(BAM) $(BAI) $(FASTA_INDEX)
	mkdir -p $(VCF_DIR)
	bcftools mpileup -d 1000 -Ou -f $(REFERENCE_FASTA) $(BAM) | \
		bcftools call --ploidy 1 -mv -Ou | \
		bcftools norm -f $(REFERENCE_FASTA) -d all -Ou | \
		bcftools sort -Oz -o $(VCF)


# Index VCF
$(VCF_INDEX): $(VCF)
	bcftools index -f -c $(VCF)


# Generate variant statistics
$(VCF_STATS): $(VCF)
	bcftools stats $(VCF) > $(VCF_STATS)


# Remove generated data and results
clean:
	rm -rf data results $(SRA_ACCESSION)
