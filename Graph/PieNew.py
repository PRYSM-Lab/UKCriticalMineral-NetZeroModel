import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge

plt.rcParams["font.family"] = "serif"

# -----------------------------
# MAIN DATA
# -----------------------------

labels = [
    "Solar","Wind Onshore","Wind Offshore","Battery","Hydro",
    "Nuclear","H2CCGT","FC","CCGTCCS","BECCS","Biomass",
]


values = [55, 25, 60, 60, 6, 29, 40, 21, 15, 30, 5]

colors = [
    "#FFFF00","#00FF00","#228b22","#00FFFF","#0080FF",
    "#0000FF","#8000FF","#FF00FF","#FF0080","#FF0000","#ffa54f",
]

# -----------------------------
# FIGURE
# -----------------------------
fig, ax = plt.subplots(figsize=(8,8))

# -----------------------------
# MAIN DONUT
# -----------------------------
wedges, _ = ax.pie(
    values,
    startangle=90,
    colors=colors,
    radius=0.75,
    wedgeprops=dict(width=0.35, edgecolor="#0B1330")
)

ax.set(aspect="equal")

# values inside donut
for i, wedge in enumerate(wedges):
    angle = (wedge.theta1 + wedge.theta2) / 2
    x = 0.58 * np.cos(np.deg2rad(angle))
    y = 0.58 * np.sin(np.deg2rad(angle))

    ax.text(x, y, f"{values[i]}", ha="center", va="center", fontsize=14)

# center text
ax.text(0, 0, f"{sum(values)} GW",
        ha="center", va="center",
        fontsize=22, fontweight="bold")

# -----------------------------
# ARC 1
# -----------------------------

labels2 = [
    "SMRCCS","ATRCCS","BGCCS","WE"
]
deep_values1 = [49, 49, 8, 1]
deep_colors = ["#6c7b8b", "#9fb6cd", "#afeeee", "#f5fffa"]

start_angle1 = -300
total_angle1 = 100

total1 = sum(deep_values1)
current_angle = start_angle1

for i, val in enumerate(deep_values1):
    angle = val / total1 * total_angle1

    wedge = Wedge((0, 0), 1.2,
                  current_angle, current_angle + angle,
                  width=0.35,
                  facecolor=deep_colors[i],
                  edgecolor="#0B1330")
    ax.add_patch(wedge)

    mid = current_angle + angle/2
    x = 1.05 * np.cos(np.deg2rad(mid))
    y = 1.05 * np.sin(np.deg2rad(mid))

    ax.text(x, y, f"{val}", ha="center", va="center", fontsize=13)

    current_angle += angle

# 👉 مجموع ARC 1
mid_arc1 = start_angle1 + total_angle1 / 2
x1 = 1.5 * np.cos(np.deg2rad(mid_arc1))
y1 = 1.5 * np.sin(np.deg2rad(mid_arc1))

ax.text(x1, y1, f"{total1} GW",
        ha="center", va="center",
        fontsize=18, fontweight="bold")

# -----------------------------
# ARC 2
# -----------------------------

labels3 = [
    "ASHP","HyBoiler"
]

deep_values2 = [98, 182]
deep_colors2 = ["#8b5a00", "#cd8500"]
start_angle2 = 250
total_angle2 = 90

total2 = sum(deep_values2)
current_angle = start_angle2

for i, val in enumerate(deep_values2):
    angle = val / total2 * total_angle2

    wedge = Wedge((0, 0), 1.2,
                  current_angle, current_angle + angle,
                  width=0.35,
                  facecolor=deep_colors2[i],
                  edgecolor="#0B1330")
    ax.add_patch(wedge)

    mid = current_angle + angle/2
    x = 1.05 * np.cos(np.deg2rad(mid))
    y = 1.05 * np.sin(np.deg2rad(mid))

    ax.text(x, y, f"{val}", ha="center", va="center", fontsize=13)

    current_angle += angle

# 👉 مجموع ARC 2
mid_arc2 = start_angle2 + total_angle2 / 2
x2 = 1.5 * np.cos(np.deg2rad(mid_arc2))
y2 = 1.5 * np.sin(np.deg2rad(mid_arc2))

ax.text(x2, y2, f"{total2} GW",
        ha="center", va="center",
        fontsize=18, fontweight="bold")

# -----------------------------
# CLEAN
# -----------------------------
ax.axis("off")

plt.savefig("final_arc_chart.png", dpi=300, bbox_inches="tight")
plt.show()