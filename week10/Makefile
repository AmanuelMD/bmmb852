.RECIPEPREFIX := >

# BMMB 852 - Week 10: ChIP-seq peak calling

REFERENCE := data/reference/chr3.fa
DESIGN := design.csv

THREADS ?= 2
JOBS ?= 2
READ_LIMIT ?= 1500000

SRR ?= SRR949136
SAMPLE_NAME ?= ChIP_H3K4me1_rep1

CONTROL := results/alignment/ChIP_Input.sorted.bam
BAM := results/alignment/$(SAMPLE_NAME).sorted.bam
PEAK := results/peaks/$(SAMPLE_NAME)_peaks.narrowPeak

.PHONY: all batch background peaks

all: $(BAM).bai

data/raw/$(SRR).fastq:
>mkdir -p data/raw
>prefetch $(SRR)
>fastq-dump -X $(READ_LIMIT) --outdir data/raw $(SRR)

results/trimmed/$(SAMPLE_NAME).fastq: data/raw/$(SRR).fastq
>mkdir -p results/trimmed results/fastp
>fastp -i $< -o $@ -q 20 -l 50 -w $(THREADS) --html results/fastp/$(SAMPLE_NAME).html --json results/fastp/$(SAMPLE_NAME).json

$(BAM): results/trimmed/$(SAMPLE_NAME).fastq $(REFERENCE).bwt
>mkdir -p results/alignment
>bwa mem -t $(THREADS) $(REFERENCE) $< | samtools sort -@ $(THREADS) -o $@ -

$(BAM).bai: $(BAM)
>samtools index $<

background:
>$(MAKE) SRR=SRR949142 SAMPLE_NAME=ChIP_Input all

batch: background
>parallel --halt soon,fail=1 --colsep , --header : -j $(JOBS) make SRR={run} SAMPLE_NAME={sample} THREADS=$(THREADS) all :::: $(DESIGN)

peaks: background
>mkdir -p results/peaks
>parallel --halt soon,fail=1 --colsep , --header : -j $(JOBS) 'if [ "{type}" != "Input" ]; then make SRR={run} SAMPLE_NAME={sample} THREADS=$(THREADS) callpeak; fi' :::: $(DESIGN)

.PHONY: callpeak

callpeak: $(PEAK)

$(PEAK): $(BAM).bai $(CONTROL).bai
>mkdir -p results/peaks
>macs3 callpeak -t $(BAM) -c $(CONTROL) -f BAM -g 3e8 -q 0.01 -n $(SAMPLE_NAME) --outdir results/peaks
