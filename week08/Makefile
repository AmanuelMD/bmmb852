.RECIPEPREFIX := >
# BMMB 852 - Week 08: Predict Variant Effects
# Three human mitochondrial DNA samples
# Run with: make -C week08

SAMPLES := SRR10069469 SRR10069441 SRR10069450
REFERENCE := ../week07/data/reference/NC_012920.1.fa
GENBANK := data/reference/NC_012920.1.gb
THREADS ?= 4
READ_LIMIT := 1500

BAMS := $(addprefix results/alignment/,$(addsuffix .sorted.bam,$(SAMPLES)))
BAIS := $(addsuffix .bai,$(BAMS))

.PHONY: all stats clean
all: results/variants/multisample.vcf.gz.csi results/variants/variant_effects.tsv

# Reference indexing
$(REFERENCE).bwt: $(REFERENCE)
>bwa index $(REFERENCE)

$(REFERENCE).fai: $(REFERENCE)
>samtools faidx $(REFERENCE)

# Download and trim reads for samples 2 and 3
OTHER_SAMPLES := SRR10069441 SRR10069450

data/raw/%_1.fastq data/raw/%_2.fastq &:
>prefetch $* --max-size 1G
>fastq-dump --split-files -X $(READ_LIMIT) --outdir data/raw $*

data/trimmed/%_trimmed_R1.fastq data/trimmed/%_trimmed_R2.fastq &: data/raw/%_1.fastq data/raw/%_2.fastq
>fastp --in1 data/raw/$*_1.fastq --in2 data/raw/$*_2.fastq --out1 data/trimmed/$*_trimmed_R1.fastq --out2 data/trimmed/$*_trimmed_R2.fastq --detect_adapter_for_pe --qualified_quality_phred 20 --length_required 50 --thread $(THREADS) --html results/fastp/$*_fastp.html --json results/fastp/$*_fastp.json

results/alignment/%.sorted.bam: data/trimmed/%_trimmed_R1.fastq data/trimmed/%_trimmed_R2.fastq $(REFERENCE).bwt
>bwa mem -t $(THREADS) -R '@RG\tID:$*\tSM:$*' $(REFERENCE) data/trimmed/$*_trimmed_R1.fastq data/trimmed/$*_trimmed_R2.fastq | samtools sort -o $@ -

# First sample reuses Week 07 trimmed reads
results/alignment/SRR10069469.sorted.bam: ../week07/data/trimmed/SRR10069469_trimmed_R1.fastq ../week07/data/trimmed/SRR10069469_trimmed_R2.fastq $(REFERENCE).bwt
>bwa mem -t $(THREADS) \
>-R '@RG\tID:SRR10069469\tSM:SRR10069469' \
>$(REFERENCE) \
>../week07/data/trimmed/SRR10069469_trimmed_R1.fastq \
>../week07/data/trimmed/SRR10069469_trimmed_R2.fastq | \
>samtools sort -o $@ -

%.sorted.bam.bai: %.sorted.bam
>samtools index $<

# Joint variant calling
results/variants/multisample.vcf.gz: $(BAMS) $(BAIS) $(REFERENCE).fai
>bcftools mpileup -d 1000 -Ou -f $(REFERENCE) $(BAMS) | \
>bcftools call --ploidy 1 -mv -Ou | \
>bcftools norm -f $(REFERENCE) -d all -Oz -o $@

results/variants/multisample.vcf.gz.csi: results/variants/multisample.vcf.gz
>bcftools index -f -c $<

# Predict coding consequences
results/variants/variant_effects.tsv: results/variants/multisample.vcf.gz $(GENBANK) scripts/annotate_variants.py
>cd .. && python week08/scripts/annotate_variants.py

stats: all
>bcftools query -l results/variants/multisample.vcf.gz
>bcftools view -H results/variants/multisample.vcf.gz | wc -l
>awk -F '\t' 'NR>1 {count[$$10]++} END {for (effect in count) print effect, count[effect]}' results/variants/variant_effects.tsv

# Remove intermediate files only; preserve final results
clean:
>rm -f data/raw/*.fastq
>rm -f data/trimmed/*.fastq
>rm -f results/alignment/*.bam results/alignment/*.bam.bai
