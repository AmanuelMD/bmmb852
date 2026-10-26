# Week 09: Automated Variant Calling Across Multiple Samples

## Overview

This workflow automates mitochondrial DNA variant calling for 10 human samples from NCBI BioProject **PRJNA563929**, which investigates mitochondrial DNA in type 2 diabetes. It extends the previous variant-calling workflow by using a metadata design file and GNU Parallel to process multiple samples.

The reference genome is the human mitochondrial sequence **NC_012920.1**.

## Requirements

Run the workflow in the course `bioinfo` environment. It uses GNU Make, GNU Parallel, SRA Toolkit (`prefetch`, `fastq-dump`), fastp, BWA, SAMtools, and BCFtools. No tools are installed automatically.

## Reproduce the analysis

From the `week09` directory, run:

```bash
make batch JOBS=2 THREADS=2
```

To preview the workflow without executing it:

```bash
make -n SRR=SRR10069469 SAMPLE_NAME=Sample1 all
```

The `design.csv` file contains 10 sequencing run accessions, BioSample identifiers, and unique sample names. GNU Parallel reads this file to run the same analysis for each sample.

Each sample is processed using 1,500 paired-end sequencing spots, fastp quality filtering (Phred 20; minimum read length 50 bp), BWA alignment, and haploid variant calling with BCFtools.

## Outputs

Individual sample VCF files are written to `results/variants/`. The final combined VCF is:

`results/variants/multisample.vcf.gz`

The 10-sample analysis produced **174 VCF records**. These records are not necessarily 174 unique genomic positions.

**Limitation:** The merge command uses `bcftools merge -0`, which fills missing calls with reference genotypes. These should not be interpreted as independently verified reference calls.

## Reproducibility

The Makefile uses the included mitochondrial reference genome, and the design file determines which samples are processed. No files from previous assignment weeks are required.
