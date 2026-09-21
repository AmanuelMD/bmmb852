SRA_ACCESSION := SRR40580480
READ_LIMIT := 10000
SAMPLE_NAME ?= mtND4_ND5_base_editing
OUTDIR := data/raw
TRIMMED_OUTDIR := data/trimmed
FASTQC_OUTDIR := results/fastqc_raw
FASTQC_TRIMMED_OUTDIR := results/fastqc_trimmed
FASTP_OUTDIR := results/fastp
THREADS ?= 4

.PHONY: all download qc_raw trim qc_trimmed clean

all: download qc_raw trim qc_trimmed

download: $(OUTDIR)
	prefetch $(SRA_ACCESSION) --max-size 1G
	fastq-dump --split-files -X $(READ_LIMIT) --outdir $(OUTDIR) $(SRA_ACCESSION)
	mv $(OUTDIR)/$(SRA_ACCESSION)_1.fastq $(OUTDIR)/$(SAMPLE_NAME)_R1.fastq
	mv $(OUTDIR)/$(SRA_ACCESSION)_2.fastq $(OUTDIR)/$(SAMPLE_NAME)_R2.fastq

qc_raw: download $(FASTQC_OUTDIR)
	fastqc --threads $(THREADS) --outdir $(FASTQC_OUTDIR) \
		$(OUTDIR)/$(SAMPLE_NAME)_R1.fastq \
		$(OUTDIR)/$(SAMPLE_NAME)_R2.fastq

trim: qc_raw $(TRIMMED_OUTDIR) $(FASTP_OUTDIR)
	fastp \
		--in1 $(OUTDIR)/$(SAMPLE_NAME)_R1.fastq \
		--in2 $(OUTDIR)/$(SAMPLE_NAME)_R2.fastq \
		--out1 $(TRIMMED_OUTDIR)/$(SAMPLE_NAME)_trimmed_R1.fastq \
		--out2 $(TRIMMED_OUTDIR)/$(SAMPLE_NAME)_trimmed_R2.fastq \
		--detect_adapter_for_pe \
		--thread $(THREADS) \
		--qualified_quality_phred 20 \
		--length_required 50 \
		--html $(FASTP_OUTDIR)/fastp_report.html \
		--json $(FASTP_OUTDIR)/fastp_report.json

qc_trimmed: trim $(FASTQC_TRIMMED_OUTDIR)
	fastqc --threads $(THREADS) --outdir $(FASTQC_TRIMMED_OUTDIR) \
		$(TRIMMED_OUTDIR)/$(SAMPLE_NAME)_trimmed_R1.fastq \
		$(TRIMMED_OUTDIR)/$(SAMPLE_NAME)_trimmed_R2.fastq

clean:
	rm -rf data results $(SRA_ACCESSION)

$(OUTDIR):
	mkdir -p $@

$(TRIMMED_OUTDIR):
	mkdir -p $@

$(FASTQC_OUTDIR):
	mkdir -p $@

$(FASTQC_TRIMMED_OUTDIR):
	mkdir -p $@

$(FASTP_OUTDIR):
	mkdir -p $@