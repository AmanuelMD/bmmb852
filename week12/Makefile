# Week 12: Transcript-based RNA-seq count matrices

SAMPLES = HBR_1 HBR_2 HBR_3 UHR_1 UHR_2 UHR_3
QUANTS = $(addprefix counts/,$(addsuffix /quant.sf,$(SAMPLES)))

.PHONY: all matrices clean

all: matrices

salmon_index/complete: fasta/chr22.transcripts.fa
	salmon index -t $< -i salmon_index -k 31
	touch $@

counts/%/quant.sf: ../week11/fastq/%_R1.fq salmon_index/complete
	mkdir -p counts/$*
	salmon quant -i salmon_index -l A -r $< -o counts/$* --validateMappings

results/transcript_counts.csv: $(QUANTS) src/combine_transcript_counts.r
	mkdir -p results
	Rscript src/combine_transcript_counts.r

results/transcripts_as_genes.csv: results/transcript_counts.csv src/combine_transcripts_as_genes.r ../week11/gtf/chr22.gtf
	Rscript src/combine_transcripts_as_genes.r

matrices: results/transcripts_as_genes.csv

clean:
	rm -rf counts salmon_index results
