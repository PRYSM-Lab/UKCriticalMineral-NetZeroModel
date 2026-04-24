import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ---------------------------
# Input data
# ---------------------------
cols = [1,2,3,4,5,6,7]  # iterations
data = {
    "WindOn":             [80, 80, 74, 71, 59,59, 53],
    "WindOFF":            [236,212,212,195,180,178, 161],
    "Solar":              [80, 63, 48, 29, 16,10, 2],
    "Nuclear":            [180,190,189,194,203,207, 212],
    "CCGTCCS":            [69, 79, 81, 79, 82,81, 95],
    "FC":                 [0.8,0.8,3,3,4,4,4.6],
    "H2CCGT":             [1,1.1,1,1,1,1.2,1.2],
    "BECCS":            [0,0,3,5,6.4,10,14],
    "Hydro":            [6,6,6,6,6,6,6],
    "Storage Charge":     [-62,-58,-53,-48,-43,-35,-26],
    "Net Trading":  [-20,-18,-12,-8,-2,5,7],
    "Load Shedding":  [0,0,0,0,0,1,3],
}
heat_elec = [440,435,431,426,412,395,377]

df = pd.DataFrame(data, index=cols).T
iterations = cols

# ---------------------------
# Colors
# ---------------------------
palette = {
    "WindOn": "#66FF66",
    "WindOFF": "#5FAF5F",
    "Solar": "#ffff00",
    "Nuclear": "#912cee",
    "CCGTCCS": "#FF6666",
    "BECCS": "#ababab",
    "FC": "#FF66FF",
    "H2CCGT": "#8b795e",

    "Hydro": "#66B2FF",
    "Storage Charge": "#66FFFF",
    "Load Shedding": "#000000",
    "Net Trading": "#FFC285",
    "Heat Line": "#000000"
}

# ---------------------------
# Stack order (for legend / visual clarity)
# ---------------------------
stack_order = [
    "Solar", "WindOn","WindOFF","Hydro","CCGTCCS","Nuclear",
   "H2CCGT","FC","BECCS","Load Shedding", 
    "Net Trading","Storage Charge"
]
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
fig, ax = plt.subplots(figsize=(18,10))

# Initialize positive and negative bottoms
pos_bottom = np.zeros(len(iterations), dtype=float)
neg_bottom = np.zeros(len(iterations), dtype=float)
bar_width = 0.8
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
ax.axhline(0, color="#444444", linewidth=0.6)
ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin, ymax * 1.05)  # 10% فضای خالی بالا
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
legend_labels.append("Heat Met by Electricity")

ax.legend(legend_handles, legend_labels, loc='upper center', bbox_to_anchor=(0.5,1.14),
          ncol=7, frameon=False, handletextpad=0.4,fontsize=14, columnspacing=1.0)
# ---------------------------
# Labels
# ---------------------------
ax.set_xlabel("Iteration", fontsize=20)
ax.set_ylabel("Electricity Generation (TWh)", fontsize=20)
ax2.set_ylabel("Heat Demand Met by Electricity (TWh)", fontsize=20)

ax.set_xticks(iterations)
ax.set_xticklabels([str(i) for i in iterations])

# aesthetic cleanup
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.9)
ax.spines['bottom'].set_linewidth(0.9)

plt.tight_layout(rect=[0,0,1,0.99])
plt.show()
