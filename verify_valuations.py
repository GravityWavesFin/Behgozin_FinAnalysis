#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd

# خواندن نتایج تحلیل
with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("بررسی ارزش‌گذاری‌های محاسبه شده:")
print("="*80)

for symbol, stock in data.items():
    shares = stock.get('shares_outstanding', 0)
    val_per_share = stock.get('valuations_per_share', {})
    
    # گرفتن قیمت فعلی از فایل CSV
    try:
        price_df = pd.read_csv(f'Data/PriceHistory/{symbol}.csv')
        current_price = price_df['Adj Close'].iloc[-1]
    except:
        current_price = 0
    
    if shares > 0 and val_per_share:
        print(f"\n📊 {symbol}:")
        print(f"   تعداد سهام: {shares:,.0f}")
        print(f"   قیمت فعلی: {current_price:,.0f} ریال")
        
        # بررسی سناریوی خنثی
        neutral_val = val_per_share.get('خنثی', 0)
        if neutral_val > 0:
            diff_pct = ((neutral_val - current_price) / current_price) * 100
            ratio = neutral_val / current_price if current_price > 0 else 0
            
            print(f"   ارزش (خنثی): {neutral_val:,.0f} ریال")
            print(f"   اختلاف: {diff_pct:+.1f}%")
            
            if abs(diff_pct) > 1000:
                print(f"   ⚠️ مشکل: اختلاف خیلی زیاد است! ({ratio:.1f}x)")
            elif abs(diff_pct) < 100:
                print(f"   ✅ منطقی: اختلاف معقول است")
            else:
                print(f"   ⚠️ نکته: اختلاف قابل توجه است")

print("\n" + "="*80)
print("✅ بررسی کامل شد")
