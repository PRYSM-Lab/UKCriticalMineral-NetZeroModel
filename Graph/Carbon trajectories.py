import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# ---------- Global Style ----------
plt.rcParams.update({
    "font.family": "serif",
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

x_points = np.array([2030, 2040, 2050])
x_smooth = np.linspace(x_points.min(), x_points.max(), 300)

# ---------- Data ----------
y_elec = {
    'Base': [9.9, 13.6, 7],
    '1% reduction': [7.8, 12.3, 8.5],
    '3% reduction': [10, 13.6, 8.7],
    '5% reduction': [10, 12, 8.2],
    '10% reduction': [5, 11.6, 9],
}

y_hydro = {
    'Base': [-11, -13, -18],
    '1% reduction': [-6, -12, -17],
    '3% reduction': [-8.4, -13, -18],
    '5% reduction': [-7.5, -12, -17],
    '10% reduction': [-6.8, -14, -18],
}

y_heat = {
    'Base': [47, 6, 0],
    '1% reduction': [49.5, 6.2, 0],
    '3% reduction': [55, 7, 0],
    '5% reduction': [57, 8, 0],
    '10% reduction': [65, 9.3, 0],
}

# ---------- Style Maps ----------
colors = {
    'Base': 'gray',
    '1% reduction': 'black',
    '3% reduction': 'goldenrod',
    '5% reduction': 'blue',
    '10% reduction': 'red',
}

markers = {
    'Base': 'v',
    '1% reduction': 'o',
    '3% reduction': 's',
    '5% reduction': '^',
    '10% reduction': 'p',
}

# ---------- Figure ----------
fig, axs = plt.subplots(1, 3, figsize=(11, 5))

panels = [
    ('Electricity', y_elec, axs[0]),
    ('Hydrogen', y_hydro, axs[1]),
    ('Heating', y_heat, axs[2])
]

legend_handles = []
legend_labels = []

for title, data, ax in panels:

    # ---- compute global y range for THIS panel ----
    all_vals = np.array([v for vals in data.values() for v in vals])
    y_min = all_vals.min()
    y_max = all_vals.max()
    margin = (y_max - y_min) * 0.15

    ax.set_ylim(y_min - margin, y_max + margin)

    for label, y_vals in data.items():

        spl = make_interp_spline(x_points, y_vals, k=2)
        y_smooth = spl(x_smooth)

        line, = ax.plot(
            x_smooth, y_smooth,
            color=colors[label],
            linewidth=2,
            label=label
        )

        ax.scatter(
            x_points, y_vals,
            color=colors[label],
            marker=markers[label],
            s=55,
            zorder=5
        )

        if title == "Electricity":
            legend_handles.append(line)
            legend_labels.append(label)

    ax.set_title(title, pad=10)
    ax.set_ylabel('Mt CO2eq', fontsize=14)

    ax.set_xticks([2030, 2040, 2050])
    ax.set_xlim(2028, 2052)

    # ---------- show ALL y tick labels ----------
    ax.tick_params(axis='y', labelleft=True)

    # ---------- boxed style ----------
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.2)

    ax.grid(True, linestyle='--', alpha=0.25)

# ---------- Legend ----------
fig.legend(
    legend_handles,
    legend_labels,
    loc='lower center',
    ncol=5,
    frameon=False,
    bbox_to_anchor=(0.5, -0.02)
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.18, wspace=0.25)
plt.show()