import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ---------------------------
# Input data
# ---------------------------
cols = [2025,2030,2035,2040,2045,2050]  # iterations
data = {
    "WindOn":             [77, 77, 80, 82, 88, 63],
    "WindOFF":            [227,225,233,258,245,214],
    "Solar":              [80, 69, 50, 30, 0, 11],
    "Nuclear":            [200,200,201,194,203,212],
    "CCGTCCS":            [78, 83, 83, 79, 82, 93],
    "CCGT":                 [0.8,1,1,0.8,5,4],
    "H2CCGT":             [0.8,1,1,0.8,2,1],
    "Biomass":            [0.5,1,1,1,0.0,0],
    "Hydro":            [0.5,1,1,1,0.0,0],
    "Storage Charge":     [-62,-59,-48,-43,-35,-26],
    "Storage discharge":  [40,38,31,27,22,18],
}
heat_elec = [440,434,433,426,402,377]

df = pd.DataFrame(data, index=cols).T
iterations = cols

# ---------------------------
# Colors
# ---------------------------
palette = {
    "WindOn": "#008F2D",
    "WindOFF": "#8FD9A8",
    "Solar": "#FFD34E",
    "Nuclear": "#A9A9A9",
    "CCGTCCS": "#E4572E",
    "CCGT": "#4C84C6",
    "H2CCGT": "#F29E4C",
    "Biomass": "#B068A6",
    "Hydro": "#B068A6",
    "Storage Charge": "#7F4F24",
    "Storage discharge": "#BFA2DE",
    "Heat": "#000000"
}

# ---------------------------
# Stack order (for legend / visual clarity)
# ---------------------------
stack_order = [
    "WindOn","WindOFF","Solar","Nuclear","CCGTCCS",
    "Biomass","CCGT","H2CCGT","Hydro", "Storage Charge",
    "Storage discharge",
]

# ---------------------------
# Create figure
# ---------------------------
plt.rcParams.update({
    "font.size": 12,
    "legend.fontsize": 11,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
})
fig, ax = plt.subplots(figsize=(18,10))

# Initialize positive and negative bottoms
pos_bottom = np.zeros(len(iterations), dtype=float)
neg_bottom = np.zeros(len(iterations), dtype=float)
bar_width = 3.5
# Draw all techs
for tech in stack_order:
    vals = np.array(df.loc[tech].values, dtype=float)
    
    # Positive part
    pos_vals = np.where(vals > 0, vals, 0.0)
    ax.bar(iterations, pos_vals, bottom=pos_bottom, color=palette[tech],width=bar_width, edgecolor='none', label=tech)
    pos_bottom += pos_vals
    
    # Negative part
    neg_vals = np.where(vals < 0, vals, 0.0)
    ax.bar(iterations, neg_vals, bottom=neg_bottom, color=palette[tech], width=bar_width, edgecolor='none')
    neg_bottom += neg_vals
    

# Horizontal baseline
ax.axhline(0, color="#444444", linewidth=0.1)

# Secondary axis for heat
ax2 = ax.twinx()
ax2.plot(iterations, heat_elec, color=palette["Heat"], linewidth=2.5,
         linestyle='--', marker='o', markersize=8, label="Heat Demand Met by Electricity")
ax2.set_ylim(min(heat_elec)-10, max(heat_elec)+10)
ax2.tick_params(axis='y')

# ---------------------------
# Legend
# ---------------------------
legend_handles = []
legend_labels = []

for tech in stack_order:
    patch = Line2D([0],[0], color=palette[tech], marker='s', markersize=12, lw=0)
    legend_handles.append(patch)
    legend_labels.append(tech)

legend_handles.append(Line2D([0],[0], color=palette["Heat"], lw=2.5, ls='--', marker='o'))
legend_labels.append("AI Demand")

ax.legend(legend_handles, legend_labels, loc='upper center', bbox_to_anchor=(0.5,1.14),
          ncol=6, frameon=False, handletextpad=0.4,fontsize=12, columnspacing=1.0)

# ---------------------------
# Labels and aesthetics
# ---------------------------
ax.set_xlabel("Iteration", fontsize=18)
ax.set_ylabel("Electricity Generation (TWh)", fontsize=18)
ax2.set_ylabel("AI Energy Concumption(TWh)", fontsize=18)

ax.set_xticks(iterations)
ax.set_xticklabels([str(i) for i in iterations])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.9)
ax.spines['bottom'].set_linewidth(0.9)

# ---------------------------
# Layout and save
# ---------------------------
plt.tight_layout(rect=[0,0,1,0.95])

plt.show()
