import pandas as pd
import matplotlib.pyplot as plt

# Load coverage data
targeted = pd.read_csv(
    "results/alignment/coverage.txt",
    sep="\t",
    header=None,
    names=["chrom", "position", "depth"]
)

comparison = pd.read_csv(
    "data/comparison/coverage.txt",
    sep="\t",
    header=None,
    names=["chrom", "position", "depth"]
)

# Create figure
fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

# Original dataset
axes[0].plot(targeted["position"], targeted["depth"])
axes[0].set_ylabel("Depth")
axes[0].set_title("SRR40580480 — Targeted sequencing")
axes[0].set_ylim(bottom=0)

# Comparison dataset
axes[1].plot(comparison["position"], comparison["depth"])
axes[1].set_xlabel("Mitochondrial genome position (bp)")
axes[1].set_ylabel("Depth")
axes[1].set_title("SRR10069469 — Mitochondrial genome capture")
axes[1].set_ylim(bottom=0)

plt.tight_layout()

# Save figure
plt.savefig("coverage_comparison.png", dpi=300)
plt.close()

print("Saved coverage_comparison.png")