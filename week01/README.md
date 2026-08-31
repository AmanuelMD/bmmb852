# BMMB 852 - Week 1 Assignment

## AI-Ready Code Editor

I chose Visual Studio Code as my AI-ready code editor.

## Samtools Version

I used the following command to check the version of Samtools in the `bioinfo` environment:

```bash
samtools --version
```

Output:

```text
samtools 1.24
Using htslib 1.24
```

## Creating a Nested Directory Structure

I created nested directories using:

```bash
mkdir -p data/raw data/processed results
```

I checked the directory structure using:

```bash
find . -type d
```

Output:

```text
.
./data
./data/raw
./data/processed
./results
```

## Creating Files in Different Directories

I created files in different directories using:

```bash
touch data/raw/sample.txt
touch data/processed/processed.txt
touch results/results.txt
```

I checked the files using:

```bash
find . -type f
```

Output:

```text
./README.md
./data/raw/sample.txt
./data/processed/processed.txt
./results/results.txt
```

## Relative and Absolute Paths

I added text to the sample file:

```bash
echo "This is a sample file." > data/raw/sample.txt
```

I accessed the file using a relative path:

```bash
cat data/raw/sample.txt
```

Output:

```text
This is a sample file.
```

I accessed the same file using an absolute path:

```bash
cat /Users/aba6573/edu/bmmb852/week01/data/raw/sample.txt
```

Output:

```text
This is a sample file.
```
