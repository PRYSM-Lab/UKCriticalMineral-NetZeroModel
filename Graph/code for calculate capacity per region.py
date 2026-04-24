import pandas as pd
import ast

# خواندن فایل اکسل
input_file = "Installed Capacity Base.xlsx"
df = pd.read_excel(input_file)

# تبدیل ستون Index از string به tuple
df['Index'] = df['Index'].apply(ast.literal_eval)

# جدا کردن تکنولوژی، منطقه و سال
df['Technology'] = df['Index'].apply(lambda x: x[0])
df['Region'] = df['Index'].apply(lambda x: x[1])
df['Year'] = df['Index'].apply(lambda x: x[2])

# لیست سال‌ها
years = df['Year'].unique()

# ساخت فایل خروجی
output_file = "output.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for year in years:
        # فیلتر داده برای هر سال
        df_year = df[df['Year'] == year]
        
        # ساخت جدول pivot
        pivot = df_year.pivot_table(
            index='Region',
            columns='Technology',
            values='Value',
            aggfunc='sum'
        )
        
        # ذخیره در شیت مربوطه
        sheet_name = f"Year_{year}"
        pivot.to_excel(writer, sheet_name=sheet_name)

print("Done! Output saved to", output_file)