ACCESSION = NC_012920.1

FASTA_URL = https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=$(ACCESSION)&rettype=fasta&retmode=text
GFF_URL = https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=$(ACCESSION)&rettype=gff3&retmode=text

FASTA = data/human_mtDNA.fa
GFF = data/human_mtDNA.gff3
FAI = $(FASTA).fai

all: $(FASTA) $(GFF) $(FAI)

$(FASTA):
	mkdir -p data
	curl -L "$(FASTA_URL)" -o $(FASTA)

$(GFF):
	mkdir -p data
	curl -L "$(GFF_URL)" -o $(GFF)

$(FAI): $(FASTA)
	samtools faidx $(FASTA)

clean:
	rm -f $(FASTA) $(GFF) $(FAI)

.PHONY: all clean
