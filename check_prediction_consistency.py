#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# خواندن نتایج
with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("بررسی همخوانی ارزشگذاری و پیش‌بینی:")
print("="*80)

for symbol, stock in data.items():
    pred = stock['analysis']['prediction']
    val_per_share = stock.get('valuations_per_share', {})
    
    current = pred['current_price']
    intrinsic = pred['intrinsic_value']
    target = pred['target_3month']
    expected_return = pred['expected_return_3month']
    valuation_neutral = val_per_share.get('خنثی', 0)
    
    print(f"\n📊 {symbol}:")
    print(f"   قیمت فعلی: {current:,} ریال")
    print(f"   ارزش ذاتی (در prediction): {intrinsic:,.0f} ریال")
    print(f"   ارزش ذاتی (در valuations): {valuation_neutral:,.0f} ریال")
    
    # بررسی همخوانی
    if abs(intrinsic - valuation_neutral) < 1:
        print(f"   ✅ همخوانی کامل!")
    else:
        print(f"   ⚠️ عدم همخوانی: {abs(intrinsic - valuation_neutral):,.0f} ریال")
    
    print(f"   هدف 3 ماهه: {target:,.0f} ریال")
    print(f"   بازده پیش‌بینی: {expected_return:+.1f}%")
    
    # محاسبه اختلاف ارزش ذاتی با قیمت
    if current > 0:
        intrinsic_diff = ((intrinsic - current) / current) * 100
        print(f"   اختلاف ارزش/قیمت: {intrinsic_diff:+.1f}%")
        
        # بررسی منطقی بودن
        if abs(intrinsic_diff - expected_return) < 20:
            print(f"   ✅ بازده منطقی است (نزدیک به اختلاف ارزش)")
        else:
            print(f"   ⚠️ بازده با اختلاف ارزش همخوانی ندارد")

print("\n" + "="*80)
