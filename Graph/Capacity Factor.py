import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
plt.rcParams['font.family'] = 'Serif'

# -----------------------------
# Data
# -----------------------------

tech = ["Nuclear", "CCGTCCS", "SMRCCS", "ATRCCS", "BECCS", "BGCCS", "H2CCGT", "FC", "WE"]


Nuclear  = [71, 72, 73, 76, 79, 80, 83]
CCGTCCS = [30, 32, 33,31, 35, 36, 38]
SMRCCS   = [6, 6,6,7 , 7, 10, 12.5]
ATRCCS    = [42.6, 43, 43, 45, 47.3, 52.4, 54]
BECCS    = [0, 0, 3, 4, 5, 7, 10]
BGCCS    = [65, 60, 50, 43, 33, 30, 27]
H2CCGT    = [1, 1, 1.2, 2, 2,2, 2]
FC    = [1, 1, 4, 4, 5, 5, 7]
WE   =[0,0,0,1,3,4,7]

scenario_data = [Nuclear, CCGTCCS, SMRCCS, ATRCCS, BECCS, BGCCS, H2CCGT, FC, WE]

# -----------------------------
# Plot
# -----------------------------

fig, ax = plt.subplots(figsize=(6,5))

x = np.arange(len(tech))

box = ax.boxplot(
    scenario_data,
    positions=x-0.15,
    widths=0.3,
    patch_artist=True,
    showfliers=False
)

# All boxes same color
for patch in box['boxes']:
    patch.set_facecolor("#2CB9FF")
    patch.set_alpha(0.7)
    patch.set_edgecolor("black")

for median in box['medians']:
    median.set_color("black")

# -----------------------------
# Mean of scenarios
# -----------------------------



# -----------------------------
# Labels
# -----------------------------

ax.set_ylabel("Capacity Factor (%)", fontsize=20)
ax.set_xlabel("Technology", fontsize=20)

ax.set_xticks(x)
ax.set_xticklabels(tech)

# -----------------------------
# Legend
# -----------------------------

legend_elements = [

    

    Line2D([0],[0],
           color="black",
           lw=3,
           label="Mean of FES scenarios"),

    
]

ax.legend(handles=legend_elements, frameon=False)

# -----------------------------
# Style
# -----------------------------

ax.grid(axis="y", linestyle="--", alpha=0.4)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams['font.family'] = 'Serif'

# -----------------------------
# Data
# -----------------------------
tech = ["Nuclear", "CCGTCCS", "SMRCCS", "ATRCCS", "BECCS", "BGCCS", "H2CCGT", "FC", "WE"]

Nuclear = [71, 72, 73, 76, 79, 80, 83]
CCGTCCS = [30, 32, 33, 31, 35, 36, 40]
SMRCCS  = [6, 6, 6, 7, 7, 10, 12.5]
ATRCCS  = [42.6, 43, 43, 45, 47.3, 52.4, 54]
BECCS   = [0, 0, 3, 4, 5, 7, 10]
BGCCS   = [65, 60, 50, 43, 33, 30, 27]
H2CCGT  = [1, 1, 1.2, 2, 2, 2, 2]
FC      = [1, 1, 4, 4, 5, 5, 7]
WE      = [0, 0, 0, 1, 3, 4, 7]

scenario_data = [Nuclear, CCGTCCS, SMRCCS, ATRCCS, BECCS, BGCCS, H2CCGT, FC, WE]

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(8, 6)) # کمی عریض‌تر برای خوانایی بهتر نام تکنولوژی‌ها

x = np.arange(len(tech))
width = 0.4 # عرض باکس‌ها

box = ax.boxplot(
    scenario_data,
    positions=x,
    widths=width,
    patch_artist=True,
    showfliers=False,
    manage_ticks=False
)

# استایل باکس‌ها
for patch in box['boxes']:
    patch.set_facecolor("#0000cd")
    patch.set_alpha(0.9)
    
    patch.set_linewidth(1.2)

for median in box['medians']:
    median.set_color("#00ffff")
    median.set_linewidth(2)

# --- اضافه کردن خط میانگین و Base Case ---
for i, data in enumerate(scenario_data):
    # محاسبه میانگین
    mean_val = np.mean(data)
    # دیتای اول (Base Case)
    base_val = data[0]
    
    # رسم خط میانگین (سفید)
    
    # رسم خط Base Case (قرمز)
    ax.hlines(base_val, i - width/2, i + width/2, color="#E63946", 
              linewidth=2, linestyle='-', zorder=4, label='Base case' if i == 0 else "")

# -----------------------------
# Labels
# -----------------------------
ax.set_ylabel("Capacity Factor (%)", fontsize=20)
ax.set_xlabel("Technology", fontsize=20)

ax.set_xticks(x)
ax.set_xticklabels(tech, rotation=0) # اگر نام‌ها طولانی بود rotation=45 بگذارید

# -----------------------------
# Legend
# -----------------------------
legend_elements = [
    Line2D([0], [0], color="#00ffff", lw=2.5, label="Median"),
    
    Line2D([0], [0], color="#E63946", lw=2.5, label="Base case")
]

# اصلاح ظاهر لجند برای نمایش بهتر خط سفید
ax.legend(handles=legend_elements, frameon=False, loc='upper right', fontsize=14)

# -----------------------------
# Style
# -----------------------------
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-5, 90) # فضای کافی برای نمایش

plt.tight_layout()
plt.show()