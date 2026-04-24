
import matplotlib.pyplot as plt
import numpy as np

# Data
imports = np.array([5.63,  4.78, 4.22, 3.66, 2.81, 2.53, 2.25])
costs   = np.array([388, 392, 397, 408, 419, 434, 440])

# Professional font
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 14

plt.figure(figsize=(14, 12))

# Plot
plt.plot(imports, costs, marker='o',color="black", linewidth=2.5, markersize=8)

# Labels and title
plt.xlabel("Import Mineral (Mtons)", fontsize=30)
plt.ylabel("Cost (£ b)", fontsize=30)


# Remove top and right borders
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Professional grid
plt.grid(True, linestyle='--', linewidth=0.6, alpha=0.6)

# Tight layout
plt.tight_layout()
plt.grid(False)
plt.show()


#%%
import matplotlib.pyplot as plt
import numpy as np

# Data
imports = np.array([5.63, 4.78, 4.22, 3.66, 2.81, 2.53, 2.25])
costs   = np.array([388, 392, 397, 408, 419, 434, 440])

# Style
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 14

fig, ax = plt.subplots(figsize=(14, 12))

# Plot
ax.plot(
    imports,
    costs,
    marker='o',
    color="black",
    linewidth=2.5,
    markersize=8,
    label="Cost vs Import Mineral"
)

# Labels
ax.set_xlabel("Import Mineral (Mtons)", fontsize=30)
ax.set_ylabel("Cost (£ b)", fontsize=30)

# -----------------------------
# ✅ EXTEND AXES + OFFSET
# -----------------------------

x_min, x_max = imports.min(), imports.max()
y_min, y_max = costs.min(), costs.max()

x_pad = (x_max - x_min) * 0.15   # 15% padding
y_pad = (y_max - y_min) * 0.15

ax.set_xlim(x_min - x_pad, x_max + x_pad)
ax.set_ylim(y_min - y_pad, y_max + y_pad)

# -----------------------------
# Grid + style
# -----------------------------
ax.grid(True, linestyle='--', linewidth=0.6, alpha=0.6)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)



plt.tight_layout()
plt.grid(False)
plt.show()