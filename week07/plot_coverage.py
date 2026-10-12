import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("images").mkdir(exist_ok=True)

coverage = pd.read_csv(
    "results/alignment/coverage.txt",
    sep="\t",
    header=None,
    names=["Chromosome", "Position", "Depth"]
)

mean_depth = coverage["Depth"].mean()
breadth_10x = (coverage["Depth"] >= 10).mean() * 100

plt.figure(figsize=(12, 4))

plt.plot(
    coverage["Position"],
    coverage["Depth"],
    color="steelblue",
    linewidth=0.8
)

plt.axhline(
    10,
    color="red",
    linestyle="--",
    label="10x coverage threshold"
)

plt.axhline(
    mean_depth,
    color="darkgreen",
    linestyle=":",
    label=f"Mean coverage: {mean_depth:.2f}x"
)

plt.xlabel("Mitochondrial genome position (bp)")
plt.ylabel("Sequencing depth (x)")
plt.title("Sequencing Coverage Across the Human Mitochondrial Genome")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig("images/coverage_plot.png", dpi=300)
plt.close()

print(f"Mean coverage: {mean_depth:.2f}x")
print(f"Genome covered at >=10x: {breadth_10x:.2f}%")
print("Saved: images/coverage_plot.png")
