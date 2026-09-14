# BMMB 852 - Week 03 Assignment

## Repository Collaboration and Pull Request

For this assignment, I reviewed and forked Shraman Jana’s Week 2 repository:

- [Original repository](https://github.com/shraman2000/bmmb852/tree/main/week02)
- [My fork](https://github.com/AmanuelMD/shraman-bmmb852)
- [My pull request](https://github.com/shraman2000/bmmb852/pull/2)

I inspected the Makefile before running it and found no suspicious or broadly dangerous operations. It downloads the *Caenorhabditis elegans* genome and annotation from NCBI, organizes the files inside a dedicated `refs/` directory, and calculates genome statistics using standard command-line tools. Although the `clean` target uses `rm -rf`, it is restricted to the project-specific `refs/` directory. I ran `make stats` and reproduced the results reported in the README: a genome size of 100,286,401 bp, seven FASTA sequences, 547,615 annotation records, and 44,795 genes. The README clearly explains how to run the workflow and interpret its outputs.

Compared with my human mitochondrial genome project, Shraman’s solution provides more automated statistics and examines a much larger and more complex eukaryotic genome. My solution is smaller, faster to reproduce, and medically focused. Overall, Shraman’s workflow is stronger in automation, while mine is simpler and more lightweight. I identified one issue in the reading-frame section: it explained the six-frame concept but did not report the exact codons at coordinate 1,020,030. I verified the surrounding sequence using `samtools faidx` and added the three forward codons (`TTG`, `TGG`, and `GGT`) and three reverse codons (`CAA`, `CCA`, and `ACC`), together with their amino-acid translations. I committed the correction to my fork and submitted it to the original repository as [Pull Request #2](https://github.com/shraman2000/bmmb852/pull/2).