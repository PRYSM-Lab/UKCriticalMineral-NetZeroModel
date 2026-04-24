import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

plt.rcParams['font.family'] = 'serif'

# =========================
# زمان‌ها
# =========================
years = np.array([2030, 2040, 2050])
x_smooth = np.linspace(years.min(), years.max(), 200)

materials = [
    'Al','Co','Cr','Cu','Li','Mn','Ni','Pb','Si','Sn','Ti','Zn'
]

colors = {
    "Recycling": "#32cd32",
    "Domestic": "#ffff00",
    "Import": "#ff0000"
}

# =========================
# 📌 داده واقعی
# =========================
data = {
    "Al": {"imp":[8.1,1,3.26], "dom":[0.1,0,0], "rec":[0,0,0.5]},
    "Co": {"imp":[0.0005,0.0002,0.0009], "dom":[0.0015,0.0028,0.0026], "rec":[0,0,0]},
    "Cr": {"imp":[0,0.014,0.023], "dom":[0.01,0.009,0], "rec":[0,0,0]},
    "Cu": {"imp":[1.9,0.77,1.11], "dom":[0.1,0.01,0], "rec":[0,0,0.1]},
    "Li": {"imp":[0.003,0.02,0.019], "dom":[0.001,0,0], "rec":[0,0,0.002]},
    "Mn": {"imp":[0.02, 0.096, 0.1], "dom":[0.043,0,0], "rec":[0,0,0]},
    "Ni": {"imp":[0.09, 0.19, 0.22], "dom":[0.01,0.01,0], "rec":[0,0,0]},
    "Pb": {"imp":[0,0.15,0.15], "dom":[0.03,0,0], "rec":[0,0,0]},
    "Si": {"imp":[0,0,0.056], "dom":[0.001,0.033,0.028], "rec":[0,0,0]},
    "Sn": {"imp":[0,0.003,0.004], "dom":[0,0,0], "rec":[0,0,0]},
    "Ti": {"imp":[0,0,0], "dom":[0.003,0.0002,0.004], "rec":[0,0,0]},
    "Zn": {"imp":[0,0.126,0.129], "dom":[0.028,0,0], "rec":[0,0,0]}
}
from scipy.interpolate import make_interp_spline
# =========================
# Smooth function (CubicSpline)
# =========================
def smooth(y):
    spline = make_interp_spline(years, y, k=2)
    return spline(x_smooth)

# =========================
# Figure
# =========================
fig, axes = plt.subplots(3, 4, figsize=(14, 10))


axes = axes.flatten()

x_offset = 0.5

# =========================
# Plot loop
# =========================
for i, ax in enumerate(axes[:len(materials)]):
    mat = materials[i]

    imp = np.array(data[mat]["imp"])
    dom = np.array(data[mat]["dom"])
    rec = np.array(data[mat]["rec"])

    # smoothing
    imp_s = smooth(imp)
    dom_s = smooth(dom)
    rec_s = smooth(rec)

    total_s = imp_s + dom_s + rec_s

    # =========================
    # stacked smooth areas
    # =========================
    ax.fill_between(x_smooth, 0, rec_s,
                    color=colors["Recycling"], alpha=0.9)

    ax.fill_between(x_smooth, rec_s, rec_s + dom_s,
                    color=colors["Domestic"], alpha=0.3)

    ax.fill_between(x_smooth, rec_s + dom_s, total_s,
                    color=colors["Import"], alpha=0.3)

    # total line
    ax.plot(x_smooth, total_s, color='black', linewidth=1.5)

    # original data points (clean markers)
    ax.plot(years, imp + dom + rec,
            'o',
            markersize=5,
            markerfacecolor='white',
            markeredgecolor='black',
            markeredgewidth=1)

    ax.set_xlim(years.min() - x_offset, years.max() + x_offset)
    ax.set_ylim(0)
    ax.set_xticks(years)
    ax.set_title(mat, fontsize=10)
    ax.set_ylabel("Demand (Mt)", fontsize=12)



# =========================
# legend
# =========================
handles = [
    plt.Line2D([0],[0], color=colors["Import"], lw=6,alpha=0.3),
    plt.Line2D([0],[0], color=colors["Domestic"], lw=6, alpha=0.3),
    plt.Line2D([0],[0], color=colors["Recycling"], lw=6, alpha=0.9)
]

labels = ['Import', 'Domestic', 'Recycling']

fig.legend(handles, labels, loc='lower center',
           ncol=3, frameon=False)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.subplots_adjust(hspace=0.4)
plt.show()