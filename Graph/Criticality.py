import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1.5

materials = ['Al','Co','Cr','Cu','Fe','Li','Mn','Ni','Pb','Si','Sn','Ti','Zn']
importance = [3.857, 4.557, 6.161, 3.3503, 3.31, 3, 5.978, 5.5572, 7.136, 4, 5.672, 4, 7.1616]
import_dependency = [10, 6, 10, 10, 0, 10, 9, 8, 9, 8, 9, 0, 10]

# ایجاد صفحه نمودار
fig, ax = plt.subplots(figsize=(6, 8), dpi=150)

x = np.linspace(0, 11, 500)
y = np.linspace(0, 11, 500)
X, Y = np.meshgrid(x, y)
Z = np.sqrt(X * Y) 

colors = ['#ffffff', '#fce4ec', '#f8bbd0', '#f06292', '#e91e63', '#c2185b', '#880e4f']
n_bins = 20
cmap = LinearSegmentedColormap.from_list('custom_reds', colors, N=n_bins)

# نمایش گرادینت در پس‌زمینه
extent = [0, 11, 0, 11]
ax.imshow(Z, extent=extent, origin='lower', cmap=cmap, alpha=0.8, aspect='auto')

sizes = np.array(importance) * 30 
scatter = ax.scatter(import_dependency, importance, s=sizes, 
                     c='white', edgecolor='black', linewidth=1.5, zorder=3)

# ۳. اضافه کردن لیبل مواد (نسخه اصلاح شده)
for i, txt in enumerate(materials):
    ax.annotate(txt, 
                (import_dependency[i], importance[i]), 
                xytext=(18, -6),            # عدد اول فاصله افقی، عدد دوم فاصله عمودی (منفی یعنی پایین بابل)
                textcoords='offset points',
                fontsize=10, 
                fontweight='normal',       # حذف حالت بولد
                family='serif',
                ha='center')               # تراز شدن متن دقیقاً در وسط بابل

ax.set_ylabel('Importance to Energy ', fontsize=14, fontweight='bold', labelpad=15)
ax.set_xlabel('Net Import Reliance', fontsize=14, fontweight='bold', labelpad=15)

#ax.spines['left'].set_position(('outward', 10))
#ax.spines['bottom'].set_position(('outward', 10))
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)

# اضافه کردن فلش و متن "Increasing criticality"
#ax.annotate('Increasing criticality', xy=(9, 9), xytext=(4, 4),
            #arrowprops=dict(arrowstyle='->', lw=2, color='black'),
            #fontsize=14, fontweight='bold', rotation=45, ha='center')
from matplotlib.patches import FancyArrowPatch

# --- تنظیمات فلش‌های منحنی (جایگزین بخش قبلی شود) ---

# تعریف مشخصات فلش‌ها (نقطه شروع، نقطه پایان، میزان انحنا)
arrows_data = [
   
    {'start': (5, 4),     'end': (9, 9.6), 'rad': 0}, # فلش وسطی
   
]

for arrow in arrows_data:
    p = FancyArrowPatch(arrow['start'], arrow['end'],
                        connectionstyle=f"arc3,rad={arrow['rad']}",
                        arrowstyle='-|>', 
                        mutation_scale=20, # اندازه نوک فلش
                        color='black',
                        linewidth=1.5,
                        zorder=4)
    ax.add_patch(p)

# اضافه کردن متن مورب روی فلش وسطی
ax.text(6.5, 6.8, 'Increasing Criticality', 
        fontsize=12, 
        fontfamily='serif',
        fontweight='bold', 
        rotation=40, # زاویه متن متناسب با شیب فلش
        ha='center', 
        va='center',
        zorder=5)

# --- پایان بخش فلش‌ها ---
# تنظیم بازه نمایش
ax.set_xlim(-1, 10.5)
ax.set_ylim(-1, 10.5)

ax.grid(False)

plt.tight_layout()
plt.subplots_adjust(left=0.15, bottom=0.15)
plt.show()
fig.savefig('criticality_map.png', dpi=300, bbox_inches='tight')