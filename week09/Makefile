
.RECIPEPREFIX := >
# BMMB 852 - Week 09: Automated variant calling
# Run from week09 using: make batch

REFERENCE := data/reference/NC_012920.1.fa
DESIGN := design.csv
THREADS ?= 2
JOBS ?= 2
READ_LIMIT ?= 1500

SRR ?= SRR10069469
SAMPLE_NAME ?= Sample1

VCF := results/variants/$(SAMPLE_NAME).vcf.gz
SAMPLES := $(shell tail -n +2 $(DESIGN) | cut -d, -f3)
VCFS := $(addprefix results/variants/,$(addsuffix .vcf.gz,$(SAMPLES)))

.PHONY: all batch merge clean

all: $(VCF).csi

$(REFERENCE).bwt: $(REFERENCE)
>bwa index $(REFERENCE)

$(REFERENCE).fai: $(REFERENCE)
>samtools faidx $(REFERENCE)

data/raw/$(SRR)_1.fastq data/raw/$(SRR)_2.fastq &: 
>mkdir -p data/raw
>prefetch $(SRR) --max-size 1G
>fastq-dump --split-files -X $(READ_LIMIT) --outdir data/raw $(SRR)

results/trimmed/$(SAMPLE_NAME)_R1.fastq results/trimmed/$(SAMPLE_NAME)_R2.fastq &: data/raw/$(SRR)_1.fastq data/raw/$(SRR)_2.fastq
>mkdir -p results/trimmed results/fastp
>fastp --in1 data/raw/$(SRR)_1.fastq --in2 data/raw/$(SRR)_2.fastq --out1 results/trimmed/$(SAMPLE_NAME)_R1.fastq --out2 results/trimmed/$(SAMPLE_NAME)_R2.fastq --detect_adapter_for_pe --qualified_quality_phred 20 --length_required 50 --thread $(THREADS) --html results/fastp/$(SAMPLE_NAME).html --json results/fastp/$(SAMPLE_NAME).json

results/alignment/$(SAMPLE_NAME).sorted.bam: results/trimmed/$(SAMPLE_NAME)_R1.fastq results/trimmed/$(SAMPLE_NAME)_R2.fastq $(REFERENCE).bwt
>mkdir -p results/alignment
>bwa mem -t $(THREADS) -R '@RG\tID:$(SRR)\tSM:$(SAMPLE_NAME)' $(REFERENCE) results/trimmed/$(SAMPLE_NAME)_R1.fastq results/trimmed/$(SAMPLE_NAME)_R2.fastq | samtools sort -o $@ -

results/alignment/$(SAMPLE_NAME).sorted.bam.bai: results/alignment/$(SAMPLE_NAME).sorted.bam
>samtools index $<

$(VCF): results/alignment/$(SAMPLE_NAME).sorted.bam results/alignment/$(SAMPLE_NAME).sorted.bam.bai $(REFERENCE).fai
>mkdir -p results/variants
>bcftools mpileup -d 1000 -Ou -f $(REFERENCE) results/alignment/$(SAMPLE_NAME).sorted.bam | bcftools call --ploidy 1 -mv -Ou | bcftools norm -f $(REFERENCE) -d all -Oz -o $@

$(VCF).csi: $(VCF)
>bcftools index -f -c $<

batch: $(REFERENCE).bwt $(REFERENCE).fai
>parallel --halt soon,fail=1 --colsep , --header : -j $(JOBS) make SRR={run_accession} SAMPLE_NAME={sample_alias} THREADS=$(THREADS) all :::: $(DESIGN)
>$(MAKE) merge

merge: results/variants/multisample.vcf.gz.csi

results/variants/multisample.vcf.gz: $(VCFS)
>bcftools merge -0 -Oz -o $@ $(VCFS)

results/variants/multisample.vcf.gz.csi: results/variants/multisample.vcf.gz
>bcftools index -f -c $<

clean:
>rm -f data/raw/*.fastq
>rm -f results/trimmed/*.fastq
>rm -f results/alignment/*.bam results/alignment/*.bai

