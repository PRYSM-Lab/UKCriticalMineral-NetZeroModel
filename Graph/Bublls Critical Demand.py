import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Data Setup ---
elements = ['Co','Cr','Li','Mn','Ni','Pb','Si','Sn','Ti','Zn']
years = [2030, 2040, 2050]
demand = [
    [189, 308, 316],
    [9586, 23321, 19533],
    [4960, 20880, 20880],
    [58548, 100339, 101903],
    [100575, 199280, 226691],
    [30351, 151266, 102330],
    [1553, 33945, 84000],
    [485, 3036, 3448],
    [1600, 1600, 2400],
    [26920, 133072, 90248]
]

# Flatten and structure the data into a DataFrame
demand_array = np.array(demand)
elements_col = np.repeat(elements, len(years))
years_col = np.tile(years, len(elements))
demand_col = demand_array.flatten()

df = pd.DataFrame({
    'Element': elements_col,
    'Year': years_col,
    'Demand': demand_col
})

# --- 2. Styling ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(12, 8))

# Bubble size scaling
max_demand = df['Demand'].max()
size_factor = 5000
df['Scaled_Demand'] = (df['Demand'] / max_demand) * size_factor

# --- 3. Colors using Seaborn Set3 Palette ---
elements_unique = df['Element'].unique()
palette = sns.color_palette('Set3', n_colors=len(elements_unique))
color_map = {element: palette[i] for i, element in enumerate(elements_unique)}

# --- 4. Plot the Bubbles ---
for element in elements_unique:
    subset = df[df['Element'] == element]
    ax.scatter(
        subset['Year'],
        subset['Element'],
        s=subset['Scaled_Demand'],
        color=color_map[element],
        edgecolors='none',
        alpha=0.6
    )

# --- 5. Annotate each bubble with demand value ---
x_offset = 1.1
for _, row in df.iterrows():
    ax.text(
        row['Year'] + x_offset,
        row['Element'],
        f"{int(row['Demand']):,}",
        ha='left',
        va='center',
        fontsize=12,
        color='black'
    )

# --- 6. Axes and Spines ---
ax.set_xlabel('Year', fontsize=20)
ax.set_ylabel('Critical Mineral Demand (ton)', fontsize=20)

ax.set_xticks(years)
ax.set_xticklabels(years)
ax.set_xlim(2025, 2055)

# Black tick labels for x
ax.tick_params(axis='x', colors='black')

# --- Make y-axis labels large and match bubble colors ---
y_labels = ax.get_yticklabels()
for label in y_labels:
    element = label.get_text()
    label.set_fontsize(16)
    label.set_color(color_map[element])
    label.set_weight("bold")

# Spines
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.grid(False)

# --- 7. Element Color Legend ---
ax.legend(
    title='Element',
    loc='center left',
    bbox_to_anchor=(1.05, 0.5),
    frameon=False,
    fontsize=14,
    title_fontsize=14
)

# --- 8. Size Legend ---
legend_demands = [1000, 25000, 100000]
legend_sizes = (np.array(legend_demands) / max_demand) * size_factor
legend_labels = [f'{int(d):,}' for d in legend_demands]

handles = [
    plt.scatter([], [], s=size, color='black', alpha=0.8, edgecolors='none')
    for size in legend_sizes
]

size_legend = ax.legend(
    handles,
    legend_labels,
    loc='upper left',
    bbox_to_anchor=(1.05, 0.25),
    title='Demand Size Key (MT)',
    scatterpoints=1,
    frameon=False,
    labelspacing=1.5,
    fontsize=10,
    title_fontsize=12
)

ax.add_artist(size_legend)

plt.tight_layout(rect=[0, 0.03, 1, 1])

# --- 9. Show ---
plt.show()
