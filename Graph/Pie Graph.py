import matplotlib.pyplot as plt
import math

# Data
labels = ['Solar','Wind Offshore', 'Wind Onshore', 'CCGTCCS', 'H2CCGT', 'Hydro', 'Nuclear', 'Fuel Cell', 'Biomass', 'Battery', 'PumpHy']
sizes = [59, 60, 25, 30, 49, 1, 31, 17, 2, 61, 3]  # Approximate small percentages for remaining
colors = [
    '#FFD700',  # Solar
    '#C7FF3F',  # Wind Offshore
    '#006400',  # Wind Onshore
    '#D62828',  # CCGTCCS
    '#C0C0C0',  # H2CCGT
    '#00008B',  # Hydro
    '#9370DB',  # Nuclear
    '#1E90FF',  # Fuel Cell
    '#64E0DB',  # Biomass
    '#FFC0CB',  # Battery
    '#D95F02'   # PumpHy (new color)
]

plt.rcParams["font.family"] = "serif"

# Create a donut chart
fig, ax = plt.subplots(figsize=(8,8))
wedges, texts, autotexts = ax.pie(
    sizes, 
    labels=None,  # We'll manually add percentages
    autopct='',   # Turn off default
    startangle=90, 
    colors=colors,
    wedgeprops={'width':0.4, 'edgecolor':'white'}
)

# Add central text
plt.text(0, 0, "Total:\n339 GW", ha='center', va='center', fontsize=30, fontweight='normal')

# Add percentage labels outside
percentages = ['17.3%', '17.6%','8.8', '9.8%', '5.3%']
angles = [w.theta2 - (w.theta2-w.theta1)/2 for w in wedges[:1]]  # Get angle for first four major wedges

for i, angle in enumerate(angles):
    x = 1.07 * math.cos(angle * math.pi / 180)
    y = 1.07 * math.sin(angle * math.pi / 180)
    ax.text(x, y, sizes[i], ha='center', va='center', fontsize=22)

# Add legend
ax.legend(labels, loc="upper center",fontsize=20, bbox_to_anchor=(0.5, 1.1), ncol=5)

# Equal aspect ratio ensures the pie chart is circular
ax.axis('equal')  
plt.show()


#%%
fig, ax = plt.subplots(figsize=(8, 2))

# Create invisible handles for legend
handles = [plt.Line2D([0], [0], marker='o', color='w', 
                      label=label, markerfacecolor=color, markersize=18) 
           for label, color in zip(labels, colors)]

# Only draw legend
ax.legend(handles=handles, loc="center", fontsize=20, ncol=5)

# Remove axes
ax.axis('off')

plt.show()

#%%
import matplotlib.pyplot as plt
import math

# Data
labels = ['Solar','Wind Offshore', 'Wind Onshore', 'CCGTCCS', 'H2CCGT', 'Hydro', 'Nuclear', 'Fuel Cell', 'Biomass', 'Battery', 'PumpHy']
sizes = [59, 60, 25, 30, 49, 1, 31, 17, 2, 61, 3]
colors = [
    '#FFD700', '#C7FF3F', '#006400', '#D62828', '#C0C0C0',
    '#00008B', '#9370DB', '#1E90FF', '#64E0DB', '#FFC0CB', '#D95F02'
]

plt.rcParams["font.family"] = "serif"

fig, ax = plt.subplots(figsize=(8,8))
wedges, texts, autotexts = ax.pie(
    sizes, 
    labels=None,
    autopct='',
    startangle=90,
    colors=colors,
    wedgeprops={'width':0.4, 'edgecolor':'white'}
)

plt.text(0, 0, "Total:\n339 GW", ha='center', va='center', fontsize=30)

percentages = ['17.3%', '17.6%','8.8', '9.8%', '5.3%']
angles = [w.theta2 - (w.theta2-w.theta1)/2 for w in wedges[:1]]

for i, angle in enumerate(angles):
    x = 1.07 * math.cos(angle * math.pi / 180)
    y = 1.07 * math.sin(angle * math.pi / 180)
    ax.text(x, y, sizes[i], ha='center', va='center', fontsize=22)

# ONLY THIS LINE IS UPDATED → two columns
ax.legend(labels, loc="upper center", fontsize=20, bbox_to_anchor=(0.5, 1.1), ncol=2)

ax.axis('equal')
plt.show()
