from Bio import SeqIO
from Bio.Seq import Seq
import gzip
import csv

reference = SeqIO.read(
    "week08/data/reference/NC_012920.1.gb", "genbank"
)

vcf_path = "week08/results/variants/multisample.vcf.gz"
output_path = "week08/results/variants/variant_effects.tsv"

with gzip.open(vcf_path, "rt") as vcf, open(output_path, "w") as out:
    writer = csv.writer(out, delimiter="\t")
    writer.writerow([
        "Position", "REF", "ALT", "Gene",
        "Reference_Codon", "Alternative_Codon",
        "Reference_AA", "Alternative_AA",
        "Protein_Change", "Effect"
    ])

    for line in vcf:
        if line.startswith("#"):
            continue

        fields = line.strip().split("\t")
        pos = int(fields[1])
        ref = fields[3]
        alt = fields[4]

        if len(ref) != 1 or len(alt) != 1 or alt not in "ACGT":
            continue

        for feature in reference.features:
            if feature.type != "CDS":
                continue

            if pos - 1 not in feature.location:
                continue

            gene = feature.qualifiers.get("gene", ["Unknown"])[0]
            table = int(feature.qualifiers.get("transl_table", ["2"])[0])
            sequence = str(feature.extract(reference.seq)).upper()

            genomic_positions = list(feature.location)
            offset = genomic_positions.index(pos - 1)
            codon_start = (offset // 3) * 3

            ref_codon = sequence[codon_start:codon_start + 3]

            if len(ref_codon) != 3:
                continue

            if feature.location.strand == -1:
                alt_base = str(Seq(alt).reverse_complement())
            else:
                alt_base = alt

            alt_codon = list(ref_codon)
            alt_codon[offset % 3] = alt_base
            alt_codon = "".join(alt_codon)

            ref_aa = str(Seq(ref_codon).translate(table=table))
            alt_aa = str(Seq(alt_codon).translate(table=table))

            aa_position = offset // 3 + 1

            if ref_aa == alt_aa:
                effect = "synonymous"
            elif alt_aa == "*":
                effect = "stop_gained"
            elif ref_aa == "*":
                effect = "stop_lost"
            else:
                effect = "missense"

            writer.writerow([
                pos, ref, alt, gene,
                ref_codon, alt_codon,
                ref_aa, alt_aa,
                f"p.{ref_aa}{aa_position}{alt_aa}",
                effect
            ])

print(f"Annotation saved to {output_path}")
