#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نمایش خلاصه ارزشگذاری‌ها و توضیح اختلاف با بازار
"""

import json
import pandas as pd

# خواندن داده‌ها
with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*100)
print(" " * 30 + "چرا ارزشگذاری با قیمت بازار اختلاف دارد؟")
print("="*100)

print("\n📌 توضیح مهم:")
print("   ارزشگذاری بنیادی بر اساس صورت‌های مالی و عملکرد واقعی شرکت محاسبه می‌شود.")
print("   قیمت بازار تحت تأثیر عوامل روانی، عرضه و تقاضا، و انتظارات آینده است.")
print("   اختلاف بین این دو می‌تواند به معنی overvalued یا undervalued بودن سهم باشد.\n")

# جدول خلاصه
summary_data = []

for symbol, stock in data.items():
    pred = stock['analysis']['prediction']
    val_per_share = stock.get('valuations_per_share', {})
    tech = stock['analysis']['technical']
    fund = stock['analysis']['fundamentals']
    
    price_df = pd.read_csv(f'Data/PriceHistory/{symbol}.csv')
    current_price = price_df['Adj Close'].iloc[-1]
    
    intrinsic = val_per_share.get('خنثی', 0)
    diff_pct = ((intrinsic - current_price) / current_price) * 100 if current_price > 0 else 0
    
    # تشخیص وضعیت
    if diff_pct < -40:
        status = "بیش‌ارزش‌گذاری شدید ⚠️"
        action = "فروش"
    elif diff_pct < -20:
        status = "بیش‌ارزش‌گذاری متوسط ⚠️"
        action = "نگهداری یا فروش"
    elif diff_pct < -10:
        status = "بیش‌ارزش‌گذاری جزئی"
        action = "نگهداری"
    elif diff_pct < 10:
        status = "ارزش‌گذاری منصفانه ✅"
        action = "نگهداری"
    elif diff_pct < 25:
        status = "کم‌ارزش‌گذاری جزئی 💎"
        action = "خرید تدریجی"
    elif diff_pct < 50:
        status = "کم‌ارزش‌گذاری متوسط 💎"
        action = "خرید"
    else:
        status = "کم‌ارزش‌گذاری شدید 💎💎"
        action = "خرید قوی"
    
    summary_data.append({
        'نماد': symbol,
        'قیمت فعلی': f"{current_price:,.0f}",
        'ارزش ذاتی': f"{intrinsic:,.0f}",
        'اختلاف %': f"{diff_pct:+.1f}%",
        'وضعیت': status,
        'توصیه': action,
        'امتیاز بنیادی': f"{fund['score']}/100",
        'روند': tech['trend']
    })

# نمایش جدول
df = pd.DataFrame(summary_data)
print(df.to_string(index=False))

print("\n" + "="*100)
print(" " * 35 + "توضیحات تکمیلی")
print("="*100)

print("\n🔍 چگونه از این اطلاعات استفاده کنیم:\n")

print("1️⃣  سهام بیش‌ارزش‌گذاری شده (Overvalued):")
print("    • قیمت بازار بیشتر از ارزش ذاتی است")
print("    • احتمال کاهش قیمت در بلندمدت وجود دارد")
print("    • مناسب برای فروش یا عدم خرید")

print("\n2️⃣  سهام با ارزش‌گذاری منصفانه (Fair Value):")
print("    • قیمت بازار نزدیک به ارزش ذاتی است")
print("    • مناسب برای نگهداری")
print("    • بررسی عوامل تکنیکال برای زمان‌بندی")

print("\n3️⃣  سهام کم‌ارزش‌گذاری شده (Undervalued):")
print("    • قیمت بازار کمتر از ارزش ذاتی است")
print("    • فرصت خرید با پتانسیل رشد")
print("    • توجه به امتیاز بنیادی و روند تکنیکال")

print("\n⚠️  هشدارها:")
print("    • ارزشگذاری بنیادی تنها یک ابزار است، نه تصمیم نهایی")
print("    • باید شرایط کلی بازار، صنعت، و روند را نیز در نظر گرفت")
print("    • اختلاف زیاد ممکن است دلایل خاصی داشته باشد (مثلاً انتظارات رشد)")
print("    • همیشه ریسک را مدیریت کنید\n")

print("="*100)

# ذخیره در فایل
df.to_csv('output/valuation_summary.csv', index=False, encoding='utf-8-sig')
print("\n✅ خلاصه ذخیره شد: output/valuation_summary.csv")
