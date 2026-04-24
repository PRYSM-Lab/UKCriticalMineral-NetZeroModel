import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ---------------------------
# Input data
# ---------------------------
cols = [1,2,3,4,5,6, 7]  # iterations
data = {
    "SMRCCS":             [24, 24, 25, 25, 27,44, 54],
    "ATRCCS":            [180,184,182,193,203,225,230],
    "BGCCS":              [46, 45, 43, 35, 32, 17, 13],
    "WE":                [0,0,0,1,3,5,6],
}
heat_elec = [220,226,227,234,245,258,283]   # <-- secondary axis line

df = pd.DataFrame(data, index=cols).T
iterations = cols

# ---------------------------
# Colors
# ---------------------------
palette = {
    "SMRCCS": "#6c7b8b",
    "ATRCCS": "#9fb6cd",
    "BGCCS": "#96cdcd",
    "WE": "#00ff7f",
    "Heat Line": "#000000",
}
# ---------------------------
# Stack order
# ---------------------------
stack_order = ["SMRCCS","ATRCCS","BGCCS","WE"]

# ---------------------------
# Create figure
# ---------------------------
plt.rcParams["font.family"] = "serif"

plt.rcParams.update({
    "font.size": 12,
    "legend.fontsize": 11,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
})
fig, ax = plt.subplots(figsize=(16,9))

# Initialize positive and negative bottoms
pos_bottom = np.zeros(len(iterations), dtype=float)
neg_bottom = np.zeros(len(iterations), dtype=float)

# Draw all techs
for tech in stack_order:
    vals = np.array(df.loc[tech].values, dtype=float)

    pos_vals = np.where(vals > 0, vals, 0.0)
    ax.bar(iterations, pos_vals, bottom=pos_bottom,
           color=palette[tech], edgecolor='none', label=tech)
    pos_bottom += pos_vals

# Horizontal baseline
ax.axhline(0, color="#444444", linewidth=0.6)

# ---------------------------
# Secondary axis for heat met by electricity
# ---------------------------
ax2 = ax.twinx()
ax2.plot(iterations, heat_elec, color=palette["Heat Line"],
         linewidth=2.5, linestyle='--', marker='o', markersize=8,
         label="Heat Met by Electricity")
ax2.set_ylim(min(heat_elec)-10, max(heat_elec)+10)

# ---------------------------
# Legend
# ---------------------------
legend_handles = [Line2D([0],[0], color=palette[tech], marker='s',
                          markersize=12, lw=0) for tech in stack_order]
legend_labels = stack_order.copy()

# add heat line
legend_handles.append(Line2D([0],[0], color=palette["Heat Line"],
                             lw=2.5, ls='--', marker='o'))
legend_labels.append("Heat Met by Hydrogen")

ax.legend(legend_handles, legend_labels, loc='upper center',
          bbox_to_anchor=(0.5,1.08),fontsize=18, ncol=5, frameon=False)

# ---------------------------
# Labels
# ---------------------------
ax.set_xlabel("Iteration", fontsize=20)
ax.set_ylabel("Hydrogen Generation (TWh)", fontsize=20)
ax2.set_ylabel("Heat Demand Met by Hydrogen (TWh)", fontsize=20)

ax.set_xticks(iterations)
ax.set_xticklabels([str(i) for i in iterations])

# aesthetic cleanup
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.9)
ax.spines['bottom'].set_linewidth(0.9)

plt.tight_layout(rect=[0,0,1,0.95])
plt.show()
