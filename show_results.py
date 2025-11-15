"""
خلاصه نتایج تحلیل و توصیه‌های تخصیص منابع
"""

import pandas as pd
import sys
sys.path.append('src')
from persian_utils import format_number, format_percentage

# خواندن ماتریس تخصیص
df = pd.read_csv('output/allocation_matrix.csv')

print("="*70)
print("خلاصه تحلیل تخصیص منابع")
print("="*70)

# 1. خلاصه تصمیمات
print("\n1. توزیع تصمیمات:")
decisions = df['decision'].value_counts()
total = len(df)
for decision, count in decisions.items():
    pct = (count / total) * 100
    print(f"   • {decision}: {count} حالت ({pct:.1f}%)")

# 2. میانگین upside هر شرکت
print("\n2. پتانسیل رشد (Upside) شرکت‌ها:")
print("\n   شرکت‌های دارای مازاد منابع:")
for source in df['source'].unique():
    avg_upside = df[df['source'] == source]['source_upside'].mean()
    status = "✓ خوب" if avg_upside > 0 else "✗ ضعیف"
    print(f"   • {source}: {avg_upside:,.1f}% {status}")

print("\n   شرکت‌های نیازمند منابع:")
for target in df['target'].unique():
    avg_upside = df[df['target'] == target]['target_upside'].mean()
    status = "✓ خوب" if avg_upside > 0 else "✗ ضعیف"
    print(f"   • {target}: {avg_upside:,.1f}% {status}")

# 3. بهترین فرصت‌های تخصیص
print("\n3. بهترین فرصت‌های تخصیص (بیشترین اختلاف upside):")
allocations = df[df['decision'] == 'تخصیص'].copy()
if not allocations.empty:
    allocations['diff'] = allocations['target_upside'] - allocations['source_upside']
    top_5 = allocations.nlargest(5, 'diff')
    
    for idx, row in top_5.iterrows():
        print(f"\n   {row['source']} → {row['target']}")
        print(f"   سناریو منبع: {row['source_scenario']}, سناریو هدف: {row['target_scenario']}")
        print(f"   Upside منبع: {row['source_upside']:,.1f}%")
        print(f"   Upside هدف: {row['target_upside']:,.1f}%")
        print(f"   اختلاف: {row['diff']:,.1f}%")
else:
    print("   هیچ فرصت تخصیصی یافت نشد!")

# 4. توصیه کلی
print("\n" + "="*70)
print("4. توصیه کلی:")
print("="*70)

# شمارش تخصیص‌ها برای هر جفت
pairs = df.groupby(['source', 'target'])['decision'].apply(lambda x: (x == 'تخصیص').sum() / len(x) * 100)
pairs_sorted = pairs.sort_values(ascending=False)

print("\nاحتمال تخصیص برای هر جفت (از 9 سناریو):")
for (source, target), pct in pairs_sorted.head(10).items():
    if pct > 0:
        confidence = "قوی" if pct > 66 else "متوسط" if pct > 33 else "ضعیف"
        print(f"   {source} → {target}: {pct:.0f}% ({confidence})")

print("\n" + "="*70)
print("⚠️  توجه:")
print("="*70)
print("""
اگر اعداد Upside خیلی بزرگ یا منفی هستند، به معنی:
1. داده‌های مالی ناقص یا اشتباه استخراج شده‌اند
2. قیمت‌های فعلی خیلی پایین یا بالا هستند  
3. نیاز به بررسی دستی داده‌های اولیه دارد

توصیه: گزارش HTML (reports/summary_all_companies.html) را باز کنید
و اعداد را با صورت‌های مالی واقعی مقایسه کنید.
""")
