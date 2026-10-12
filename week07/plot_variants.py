import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("images").mkdir(exist_ok=True)

vcf = "results/variants/SRR10069469.vcf.gz"

result = subprocess.run(
    ["bcftools", "query", "-f", "%POS\t%REF\t%ALT\n", vcf],
    capture_output=True,
    text=True,
    check=True
)

variants = []
for line in result.stdout.strip().splitlines():
    pos, ref, alt = line.split("\t")
    kind = "SNP" if len(ref) == len(alt) == 1 else "Indel"
    variants.append((int(pos), kind))

df = pd.DataFrame(variants, columns=["Position", "Type"])

# Figure 1: Variant distribution
fig, ax = plt.subplots(figsize=(12, 3.5))

for kind, color, level in [
    ("SNP", "steelblue", 1),
    ("Indel", "darkorange", 0)
]:
    subset = df[df["Type"] == kind]
    ax.scatter(
        subset["Position"],
        [level] * len(subset),
        label=kind,
        color=color,
        s=65
    )

ax.set_xlim(0, 16569)
ax.set_yticks([0, 1], ["Indel", "SNP"])
ax.set_xlabel("Mitochondrial genome position (bp)")
ax.set_title("Distribution of Candidate Variants Across Human mtDNA")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig("images/variant_distribution.png", dpi=300)
plt.close(fig)

# Figure 2: Variant types
counts = df["Type"].value_counts().reindex(["SNP", "Indel"], fill_value=0)

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(
    counts.index,
    counts.values,
    color=["steelblue", "darkorange"],
    width=0.55
)

ax.bar_label(bars, padding=3)
ax.set_ylabel("Number of variants")
ax.set_title("Variant Types Identified by bcftools")
ax.set_ylim(0, max(counts.values) * 1.2)
fig.tight_layout()
fig.savefig("images/variant_types.png", dpi=300)
plt.close(fig)

print(f"Total variants: {len(df)}")
print(counts.to_string())
print("Saved: images/variant_distribution.png")
print("Saved: images/variant_types.png")
