#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
پیدا کردن بهترین جایگزین‌ها برای سهام با تحلیل 9 سناریو
"""

import json
import pandas as pd
from itertools import product

# خواندن داده‌ها
with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*120)
print(" " * 40 + "تحلیل جایگزین با 9 سناریو")
print("="*120)

# سهام هدف (که می‌خواهیم جایگزین پیدا کنیم)
target_stocks = ['زفجر', 'گکوثر', 'کاوه']

# سهام کاندید (برای جایگزینی)
candidate_stocks = ['رنیک', 'قشیر', 'زدشت', 'وسنا', 'کگاز', 'تلیسه']

# سناریوها
scenarios = ['خوشبینانه', 'خنثی', 'بدبینانه']

def get_stock_data(symbol):
    """دریافت اطلاعات سهم"""
    stock = data[symbol]
    price_df = pd.read_csv(f'Data/PriceHistory/{symbol}.csv')
    current_price = price_df['Adj Close'].iloc[-1]
    
    valuations = stock.get('valuations_per_share', {})
    fund_score = stock['analysis']['fundamentals']['score']
    tech_score = stock['analysis']['technical']['momentum_score']
    trend = stock['analysis']['technical']['trend']
    
    return {
        'symbol': symbol,
        'price': current_price,
        'valuations': valuations,
        'fund_score': fund_score,
        'tech_score': tech_score,
        'trend': trend
    }

def calculate_scenario_score(stock_data, scenario):
    """محاسبه امتیاز برای یک سناریو"""
    valuation = stock_data['valuations'].get(scenario, 0)
    price = stock_data['price']
    
    if price == 0:
        return 0
    
    # پتانسیل رشد (upside)
    upside = ((valuation - price) / price) * 100
    
    # امتیاز کلی (ترکیب upside، بنیادی، تکنیکال)
    # وزن‌ها: upside (50%), بنیادی (30%), تکنیکال (20%)
    score = (
        upside * 0.5 +  # پتانسیل رشد
        stock_data['fund_score'] * 0.3 +  # بنیادی
        stock_data['tech_score'] * 0.2  # تکنیکال
    )
    
    return score, upside

def analyze_alternatives(target_symbol):
    """تحلیل جایگزین‌های یک سهم با 9 سناریو"""
    print(f"\n{'='*120}")
    print(f"📊 جایگزین برای: {target_symbol}")
    print(f"{'='*120}")
    
    target_data = get_stock_data(target_symbol)
    print(f"\nوضعیت {target_symbol}:")
    print(f"  قیمت فعلی: {target_data['price']:,.0f} ریال")
    print(f"  امتیاز بنیادی: {target_data['fund_score']}/100")
    print(f"  امتیاز تکنیکال: {target_data['tech_score']}/100")
    print(f"  روند: {target_data['trend']}")
    
    # محاسبه امتیاز سهم هدف در هر سناریو
    print(f"\n  ارزش‌گذاری {target_symbol}:")
    target_scenarios = {}
    for scenario in scenarios:
        score, upside = calculate_scenario_score(target_data, scenario)
        target_scenarios[scenario] = {'score': score, 'upside': upside}
        val = target_data['valuations'].get(scenario, 0)
        print(f"    {scenario}: {val:,.0f} ریال (upside: {upside:+.1f}%, امتیاز: {score:.1f})")
    
    print(f"\n{'─'*120}")
    print(f"🔍 تحلیل 9 سناریو برای هر کاندید:")
    print(f"{'─'*120}")
    
    # تحلیل هر کاندید با 9 سناریو
    all_results = []
    
    for candidate in candidate_stocks:
        candidate_data = get_stock_data(candidate)
        
        print(f"\n🏢 {candidate}:")
        print(f"  قیمت: {candidate_data['price']:,.0f} | بنیادی: {candidate_data['fund_score']}/100 | تکنیکال: {candidate_data['tech_score']}/100 | روند: {candidate_data['trend']}")
        
        # محاسبه امتیاز برای هر ترکیب سناریو
        for target_scenario in scenarios:
            for candidate_scenario in scenarios:
                score, upside = calculate_scenario_score(candidate_data, candidate_scenario)
                val = candidate_data['valuations'].get(candidate_scenario, 0)
                
                # مقایسه با سهم هدف
                target_score = target_scenarios[target_scenario]['score']
                target_upside = target_scenarios[target_scenario]['upside']
                
                score_diff = score - target_score
                upside_diff = upside - target_upside
                
                all_results.append({
                    'target': target_symbol,
                    'target_scenario': target_scenario,
                    'candidate': candidate,
                    'candidate_scenario': candidate_scenario,
                    'scenario_combo': f"{target_symbol}({target_scenario}) → {candidate}({candidate_scenario})",
                    'candidate_price': candidate_data['price'],
                    'candidate_value': val,
                    'upside': upside,
                    'upside_diff': upside_diff,
                    'score': score,
                    'score_diff': score_diff,
                    'fund_score': candidate_data['fund_score'],
                    'tech_score': candidate_data['tech_score'],
                    'trend': candidate_data['trend']
                })
    
    # مرتب‌سازی بر اساس امتیاز
    df = pd.DataFrame(all_results)
    df_sorted = df.sort_values('score', ascending=False)
    
    # نمایش 10 بهترین گزینه
    print(f"\n{'='*120}")
    print(f"🏆 10 بهترین جایگزین برای {target_symbol} (بر اساس امتیاز کلی):")
    print(f"{'='*120}")
    
    top_10 = df_sorted.head(10)
    for idx, row in top_10.iterrows():
        print(f"\n{row.name - top_10.index[0] + 1}. {row['scenario_combo']}")
        print(f"   قیمت: {row['candidate_price']:,.0f} | ارزش: {row['candidate_value']:,.0f} | upside: {row['upside']:+.1f}%")
        print(f"   امتیاز کل: {row['score']:.1f} (بهتر از {target_symbol}: {row['score_diff']:+.1f})")
        print(f"   بنیادی: {row['fund_score']}/100 | تکنیکال: {row['tech_score']}/100 | روند: {row['trend']}")
        
        # توضیح
        if row['upside'] > 0:
            if row['upside'] > 20:
                quality = "عالی 💎💎"
            elif row['upside'] > 10:
                quality = "خوب 💎"
            else:
                quality = "متوسط"
            print(f"   ✅ فرصت کم‌ارزش‌گذاری - {quality}")
        else:
            print(f"   ⚠️ بیش‌ارزش‌گذاری - احتمال کاهش قیمت")
    
    # خلاصه برای هر کاندید (میانگین در تمام سناریوها)
    print(f"\n{'='*120}")
    print(f"📊 خلاصه کاندیدها (میانگین تمام 9 سناریو):")
    print(f"{'='*120}")
    
    summary = df.groupby('candidate').agg({
        'score': 'mean',
        'upside': 'mean',
        'fund_score': 'first',
        'tech_score': 'first',
        'trend': 'first'
    }).sort_values('score', ascending=False)
    
    for candidate, row in summary.iterrows():
        print(f"\n🏢 {candidate}:")
        print(f"   میانگین امتیاز: {row['score']:.1f}")
        print(f"   میانگین upside: {row['upside']:+.1f}%")
        print(f"   بنیادی: {row['fund_score']}/100 | تکنیکال: {row['tech_score']}/100 | روند: {row['trend']}")
        
        # توصیه
        if row['score'] > 20:
            print(f"   ✅ توصیه قوی برای جایگزینی")
        elif row['score'] > 10:
            print(f"   ✅ توصیه متوسط برای جایگزینی")
        elif row['score'] > 0:
            print(f"   ⚠️ توصیه ضعیف - بررسی بیشتر نیاز است")
        else:
            print(f"   ❌ توصیه نمی‌شود - از {target_symbol} بدتر است")
    
    return df_sorted

# تحلیل برای هر سهم هدف
print("\n" + "="*120)
print(" " * 35 + "شروع تحلیل جامع با 9 سناریو")
print("="*120)

all_recommendations = {}

for target in target_stocks:
    df = analyze_alternatives(target)
    all_recommendations[target] = df.head(3)  # 3 توصیه برتر

# خلاصه نهایی
print("\n" + "="*120)
print(" " * 40 + "خلاصه توصیه‌های نهایی")
print("="*120)

for target, recommendations in all_recommendations.items():
    print(f"\n📌 به جای {target}:")
    for idx, (_, row) in enumerate(recommendations.iterrows(), 1):
        print(f"   {idx}. {row['candidate']} (سناریو: {row['candidate_scenario']})")
        print(f"      امتیاز: {row['score']:.1f} | upside: {row['upside']:+.1f}% | بنیادی: {row['fund_score']}/100")

print("\n" + "="*120)
print("✅ تحلیل کامل شد!")
