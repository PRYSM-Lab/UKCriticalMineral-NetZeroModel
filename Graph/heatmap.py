import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
import pandas as pd

plt.rcParams["font.family"] = "serif"
# -----------------------------
# Labels
# -----------------------------
materials = ["Al", "Co", "Cr", "Cu", "Li", "Mn", "Ni", "Pb", "Si", "Sn", "Zn",]

technologies = [
    "Solar", "Wind Off", "Wind On", "Battery", "BECCS", "FC",
    "Nuclear", "CCGTCCS", "SMRCCS", "ATRCCS",
    "WE", "BGCCS", "ASHP", "HyBoiler"
]

df = pd.read_excel("Inividual.xlsx", sheet_name="Sheet1")
df["Scenario"] = (df["Scenario"] * 100).astype(int).astype(str) + "%"
scenarios = ["5%", "10%", "20%"]
# index maps
mat_idx = np.arange(len(materials))
tech_idx = np.arange(len(technologies))



# enforce ordering
df.columns = df.columns.str.strip()
df["Scenario"] = df["Scenario"].astype(str).str.strip()
df["Technology"] = df["Technology"].astype(str).str.strip()
df["Material"] = df["Material"].astype(str).str.strip()

import numpy as np

data = []

for scen in scenarios:
    pivot = (
        df[df["Scenario"] == scen]
        .pivot(index="Technology", columns="Material", values="Value")
        .reindex(index=technologies, columns=materials)
    )
    data.append(pivot.values)

data = np.array(data)

# -----------------------------
# Example data (replace with yours)
# shape: (scenario, tech, material)
# -----------------------------

# -----------------------------
# Plot
# -----------------------------
cmap = LinearSegmentedColormap.from_list(
    "Spectral",
    ["#ff0000", "white", "#0000ff"]  # قرمز، سفید، سبز
)

fig, axes = plt.subplots(1, 3, figsize=(14, 6), sharey=False)
plt.subplots_adjust(wspace=0.4, right=0.88)
# یک norm مشترک برای همه سناریوها (خیلی مهم برای مقایسه درست)
vmax = np.nanmax(np.abs(data))
norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

for i, ax in enumerate(axes):
    Z = data[i]

    # انتخاب ستون‌ها بر اساس سناریو
    if scenarios[i] == "10%":
        keep_mask = [m != "Cu" for m in materials]

    elif scenarios[i] == "20%":
        keep_mask = [m not in ["Cu", "Ni"] for m in materials]

    else:
        keep_mask = [True] * len(materials)

    # اعمال فیلتر
    Z_filtered = Z[:, keep_mask]
    materials_filtered = [m for m, k in zip(materials, keep_mask) if k]

    im = ax.imshow(
        Z_filtered,
        cmap=cmap,
        norm=norm,
        aspect='auto'
    )

    # ticks جدید
    ax.set_xticks(np.arange(len(materials_filtered)))
    ax.set_xticklabels(materials_filtered, rotation=90, ha='right', fontsize=9)

    ax.set_yticks(np.arange(len(technologies)))
    ax.set_yticklabels(technologies, fontsize=9)

    ax.set_title(f"{scenarios[i]} Import Reduction", fontweight='bold')

    # annotations
    for y in range(Z_filtered.shape[0]):
        for x in range(Z_filtered.shape[1]):
            if not np.isnan(Z_filtered[y, x]):
                ax.text(x, y, f"{Z_filtered[y,x]:.0f}",
                        ha='center', va='center',
                        fontsize=6)
cbar_ax = fig.add_axes([0.90, 0.15, 0.015, 0.7])  # [left, bottom, width, height]

cbar = fig.colorbar(im, cax=cbar_ax)
#cbar = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.01)
cbar.set_label(r'$\Delta$ Capacity Compared to Baseline (GW)', fontsize=15)
fig.savefig('heatmap_results.png', dpi=300)
plt.subplots_adjust(wspace=0.3)
#plt.tight_layout()
plt.show()