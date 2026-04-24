import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon
import numpy as np
plt.rcParams["font.family"] = "serif"

# ---------------- Load shapefile ----------------
nuts1 = gpd.read_file("NUTS1_Jan_2018_SGCB_in_the_UK.shp")

# ---------------- Map NUTS codes to LDZ ----------------
ldz_map = {
    'UKC': 'NO', 'UKD': 'NW', 'UKE': 'NE', 'UKF': 'EM', 'UKG': 'WM',
    'UKH': 'EA', 'UKI': 'NT', 'UKJ': 'SO & SE', 'UKK': 'SW',
    'UKL': 'WS & WN', 'UKM': 'SC',
}
nuts1['LDZ'] = nuts1['nuts118cd'].map(ldz_map)

# ---------------- Split Functions ----------------
def split_polygon_vertically(geom):
    polygons = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    left_parts, right_parts = [], []
    for poly in polygons:
        minx, miny, maxx, maxy = poly.bounds
        mid_x = (minx + maxx) / 2
        left_coords = [(x, y) for x, y in poly.exterior.coords if x <= mid_x]
        right_coords = [(x, y) for x, y in poly.exterior.coords if x > mid_x]
        if len(left_coords) > 2: left_parts.append(Polygon(left_coords))
        if len(right_coords) > 2: right_parts.append(Polygon(right_coords))
    return MultiPolygon(left_parts) if len(left_parts) > 1 else left_parts[0], \
           MultiPolygon(right_parts) if len(right_parts) > 1 else right_parts[0]

def split_polygon_horizontally(geom):
    polygons = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    bottom_parts, top_parts = [], []
    for poly in polygons:
        minx, miny, maxx, maxy = poly.bounds
        mid_y = (miny + maxy) / 2
        bottom_coords = [(x, y) for x, y in poly.exterior.coords if y <= mid_y]
        top_coords = [(x, y) for x, y in poly.exterior.coords if y > mid_y]
        if len(bottom_coords) > 2: bottom_parts.append(Polygon(bottom_coords))
        if len(top_coords) > 2: top_parts.append(Polygon(top_coords))
    return MultiPolygon(bottom_parts) if len(bottom_parts) > 1 else bottom_parts[0], \
           MultiPolygon(top_parts) if len(top_parts) > 1 else top_parts[0]

# Split Regions
ukj_geom = nuts1.loc[nuts1['nuts118cd'] == 'UKJ', 'geometry'].values[0]
poly_so_final, poly_se_final = split_polygon_vertically(ukj_geom)
ukl_geom = nuts1.loc[nuts1['nuts118cd'] == 'UKL', 'geometry'].values[0]
poly_ws_final, poly_wn_final = split_polygon_horizontally(ukl_geom)

nuts1 = nuts1[~nuts1['nuts118cd'].isin(['UKJ', 'UKL'])].copy()
new_rows = gpd.GeoDataFrame([
    {'nuts118cd': 'UKJ_SO', 'LDZ': 'SO', 'geometry': poly_so_final},
    {'nuts118cd': 'UKJ_SE', 'LDZ': 'SE', 'geometry': poly_se_final},
    {'nuts118cd': 'UKL_WS', 'LDZ': 'WS', 'geometry': poly_ws_final},
    {'nuts118cd': 'UKL_WN', 'LDZ': 'WN', 'geometry': poly_wn_final},
], geometry='geometry', crs=nuts1.crs)
nuts1 = pd.concat([nuts1, new_rows], ignore_index=True)

# ---------------- DATA ----------------
# ---------------- DATA ----------------

# لیست LDZ ها (ثابت)
ldz_list = ['EA','EM','WM','NT','NO','NW','NE','SO','SE','SW','WS','WN','SC']


# -------- Panel 1: Heating (3 technologies) --------
heating_techs = ['GasBoiler', 'HyBoiler', 'Heat Pump']

data_heat = {
    'EA': [50, 40, 44],
    'EM': [5, 5, 5],
    'WM': [6, 4, 6],
    'NT': [400, 300, 406],
    'NO': [4, 4, 4],
    'NW': [15, 15, 13],
    'NE': [4, 3, 4],
    'SO': [300, 250, 255],
    'SE': [50, 40, 50],
    'SW': [15, 15, 21],
    'WS': [60, 60, 64],
    'WN': [1, 1, 1],
    'SC': [5, 5, 5]
}


# -------- Panel 2: Hydrogen (4 technologies) --------
hydrogen_techs = ['H2-Tech1', 'H2-Tech2', 'H2-Tech3', 'H2-Tech4']

data_h2 = {
    'EA': [10, 20, 30, 40],
    'EM': [2, 3, 4, 5],
    'WM': [3, 4, 5, 6],
    'NT': [80, 90, 100, 110],
    'NO': [2, 2, 3, 3],
    'NW': [8, 9, 10, 11],
    'NE': [3, 3, 4, 4],
    'SO': [60, 70, 80, 90],
    'SE': [20, 25, 30, 35],
    'SW': [10, 12, 14, 16],
    'WS': [25, 30, 35, 40],
    'WN': [1, 1, 2, 2],
    'SC': [5, 6, 7, 8]
}


# -------- Panel 3: Electricity (8 technologies) --------
electricity_techs = ['E1','E2','E3','E4','E5','E6','E7','E8']

data_el = {
    'EA': [5,10,15,20,25,30,35,40],
    'EM': [2,4,6,8,10,12,14,16],
    'WM': [3,6,9,12,15,18,21,24],
    'NT': [50,60,70,80,90,100,110,120],
    'NO': [2,3,4,5,6,7,8,9],
    'NW': [10,12,14,16,18,20,22,24],
    'NE': [3,4,5,6,7,8,9,10],
    'SO': [40,50,60,70,80,90,100,110],
    'SE': [15,20,25,30,35,40,45,50],
    'SW': [8,10,12,14,16,18,20,22],
    'WS': [20,25,30,35,40,45,50,55],
    'WN': [1,2,3,4,5,6,7,8],
    'SC': [4,5,6,7,8,9,10,11]
}

# ---------------- DRAW FUNCTION ----------------
def draw_panel(ax, data, colors, title, legend_labels):

    nuts1.plot(ax=ax, color='#eeeeee', edgecolor='grey', linewidth=0.8)

    def draw_pie(ax, ratios, center, size):
        xy = np.asarray(center)
        ratios = np.array(ratios) / sum(ratios)
        start = 0
        for r, color in zip(ratios, colors):
            x = [0] + np.cos(np.linspace(2 * np.pi * start, 2 * np.pi * (start + r), 30)).tolist()
            y = [0] + np.sin(np.linspace(2 * np.pi * start, 2 * np.pi * (start + r), 30)).tolist()
            ax.fill(xy[0] + np.array(x) * size, xy[1] + np.array(y) * size, color=color, ec='white', lw=0.5)
            start += r

    for _, row in nuts1.dropna(subset=['LDZ']).iterrows():
        ldz_name = row['LDZ']
        if ldz_name not in data: continue
        
        centroid = row.geometry.centroid
        cx, cy = centroid.x, centroid.y
        
        total_val = sum(data[ldz_name])
        base_size = 15000
        pie_size = base_size + (np.sqrt(total_val) * 2500)

        if ldz_name == 'NT' and 'SO':
            target_x, target_y = 1.1*cx + 150000, cy 
            ax.annotate("", xy=(cx, cy), xytext=(target_x, target_y),
                        arrowprops=dict(arrowstyle="-", color="gray", lw=0.8))
            draw_pie(ax, data[ldz_name], (target_x, target_y), pie_size)
            ax.text(target_x, target_y - pie_size - 20000, ldz_name, ha='center', fontsize=9)
        else:
            draw_pie(ax, data[ldz_name], (cx, cy), pie_size)
            ax.text(cx, cy - pie_size - 20000, ldz_name, ha='center', fontsize=10, alpha=0.7)

    ax.axis('off')
    ax.set_title(title, fontsize=16)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l) for c, l in zip(colors, legend_labels)]
    ax.legend(handles=legend_elements, loc='upper right',
              title="Technologies", title_fontsize=14, fontsize=12, frameon=False)

# ---------------- PLOT 3 PANELS ----------------
fig, axes = plt.subplots(1, 3, figsize=(24, 10))

# Panel 1: Heating
draw_panel(
    axes[0],
    data_heat,
    ['#ff9999', '#66b3ff', '#99ff99'],
    "Heating Technologies",
    ['GasBoiler', 'HyBoiler', 'Heat Pump']
)

# Panel 2: Hydrogen
draw_panel(
    axes[1],
    data_h2,
    ["#6c7b8b","#9fb6cd","#afeeee", "#00ff7f"],
    "Hydrogen Technologies",
    ['SMRCCS','ATRCCS','BGCCS','WE']
)

# Panel 3: Electricity
draw_panel(
    axes[2],
    data_el,
    ["#228b22","#00FF00","#FFFF00","#00FFFF","#FF0080","#0000FF","#8000FF","#FF00FF"],
    "Electricity Technologies",
    ['WindOff','WindOn','Solar','Battery','CCGTCCS','Nuclear','H2CCGT','FC']
)



plt.tight_layout()
plt.show()