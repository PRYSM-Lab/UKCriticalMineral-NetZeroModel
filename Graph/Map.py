import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon
import numpy as np
plt.rcParams["font.family"] = "serif"

# ---------------- Load shapefile ----------------
# فرض بر این است که فایل در مسیر جاری قرار دارد
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

# ---------------- Data for Pie Charts ----------------
# مقادیر فرضی برای ۳ تکنولوژی (میتوانید با داده‌های واقعی جایگزین کنید)
data = {
    'EA': [50, 40, 44], 'EM': [5, 5, 5], 'WM': [6, 4, 6], 'NT': [400, 300, 406],
    'NO': [4, 4, 4], 'NW': [15, 15, 13], 'NE': [4, 3, 4], 'SO': [300, 250, 255],
    'SE': [50, 40, 50], 'SW': [15, 15, 21], 'WS': [60, 60, 64], 'WN': [1, 1, 1], 'SC': [5, 5, 5]
}

# ---------------- Plotting ----------------
fig, ax = plt.subplots(figsize=(12, 14))

# رسم نقشه با تم طوسی بسیار روشن
nuts1.plot(ax=ax, color='#eeeeee', edgecolor='grey', linewidth=0.8)

# تنظیمات رنگ تکنولوژی‌ها
colors = ['#ff9999', '#66b3ff', '#99ff99'] # صورتی ملایم، آبی آسمانی، سبز بهاری

def draw_pie(ax, ratios, center, size):
    # رسم نمودار دایره‌ای در مختصات نقشه
    xy = np.asarray(center)
    ratios = np.array(ratios) / sum(ratios)
    start = 0
    for r, color in zip(ratios, colors):
        x = [0] + np.cos(np.linspace(2 * np.pi * start, 2 * np.pi * (start + r), 30)).tolist()
        y = [0] + np.sin(np.linspace(2 * np.pi * start, 2 * np.pi * (start + r), 30)).tolist()
        ax.fill(xy[0] + np.array(x) * size, xy[1] + np.array(y) * size, color=color, ec='white', lw=0.5)
        start += r

# استخراج سنترویدها و رسم نمودارها
for ldz, row in nuts1.dropna(subset=['LDZ']).iterrows():
    ldz_name = row['LDZ']
    if ldz_name not in data: continue
    
    centroid = row.geometry.centroid
    cx, cy = centroid.x, centroid.y
    
    total_val = sum(data[ldz_name])
    # محاسبه شعاع بر اساس مجموع (با مقیاس‌بندی برای زیبایی)
    base_size = 15000 # مقدار پایه برای ابعاد نقشه UK
    pie_size = base_size + (np.sqrt(total_val) * 2500) 
    
    # مدیریت مناطق خاص (مثل لندن NT که خیلی کوچک است)
    if ldz_name == 'NT' and 'SO':
        # انتقال دایره به سمت راست برای دیده شدن
        target_x, target_y = 1.1*cx + 150000, cy 
        ax.annotate("", xy=(cx, cy), xytext=(target_x, target_y),
                    arrowprops=dict(arrowstyle="-", color="gray", lw=0.8))
        draw_pie(ax, data[ldz_name], (target_x, target_y), pie_size)
        ax.text(target_x, target_y - pie_size - 20000, ldz_name, ha='center', fontsize=9, fontweight='bold')
    else:
        draw_pie(ax, data[ldz_name], (cx, cy), pie_size)
        # نمایش نام منطقه زیر دایره
        ax.text(cx, cy - pie_size - 20000, ldz_name, ha='center', fontsize=10, alpha=0.7)

# حذف محورها و اضافات
ax.axis('off')
ax.set_title("UK Technology Distribution by Region (2030)", fontsize=16, pad=20)

# افزودن راهنمای دستی برای تکنولوژی‌ها (به جای لجنت خودکار)
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[0], label='Tech A'),
                   Patch(facecolor=colors[1], label='Tech B'),
                   Patch(facecolor=colors[2], label='Tech C')]
ax.legend(handles=legend_elements, loc='upper right', title="Technologies", frameon=False)

plt.tight_layout()
plt.show()