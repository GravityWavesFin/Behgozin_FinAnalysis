#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ارتقای سیستم ارزشگذاری - نمایش جزئیات هر روش
"""

import json
import pandas as pd

def generate_detailed_valuation_report():
    """تولید گزارش HTML با جزئیات کامل هر روش ارزشگذاری"""
    
    # خواندن نتایج تحلیل
    with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    html = """
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تحلیل تفصیلی ارزشگذاری</title>
    <style>
        body { font-family: Tahoma, Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { text-align: center; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #e74c3c; margin-top: 30px; }
        h3 { color: #27ae60; margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: right; border: 1px solid #ddd; }
        th { background: #34495e; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        .positive { color: green; font-weight: bold; }
        .negative { color: red; font-weight: bold; }
        .warning { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; border-right: 5px solid #ffc107; }
        .info { background: #d1ecf1; padding: 15px; border-radius: 5px; margin: 15px 0; border-right: 5px solid #17a2b8; }
        .method-box { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-right: 4px solid #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 تحلیل تفصیلی ارزشگذاری</h1>
        
        <div class="warning">
            <strong>⚠️ توجه مهم:</strong> ارزشگذاری بنیادی با قیمت بازار متفاوت است.
            بازار تحت تأثیر عوامل روانی، سیاسی، و انتظارات آینده قرار دارد.
            این ارزشگذاری‌ها بر اساس داده‌های مالی تاریخی و مفروضات محافظه‌کارانه محاسبه شده‌اند.
        </div>
"""
    
    for symbol, stock_data in data.items():
        shares = stock_data.get('shares_outstanding', 0)
        valuations = stock_data.get('valuations', {})
        val_per_share = stock_data.get('valuations_per_share', {})
        
        # قیمت فعلی
        try:
            price_df = pd.read_csv(f'Data/PriceHistory/{symbol}.csv')
            current_price = price_df['Adj Close'].iloc[-1]
        except:
            current_price = 0
        
        if shares == 0 or not valuations:
            continue
            
        # محاسبه ارزش بازار
        market_cap = (current_price * shares) / 1_000_000 if current_price > 0 else 0
        
        html += f"""
        <h2>🏢 {symbol}</h2>
        
        <div class="info">
            <strong>اطلاعات پایه:</strong><br>
            تعداد سهام: {shares:,.0f}<br>
            قیمت فعلی: {current_price:,.0f} ریال<br>
            ارزش بازار: {market_cap:,.0f} میلیون ریال ({market_cap/1000:,.1f} میلیارد)
        </div>
        
        <h3>📈 مقایسه سناریوها</h3>
        <table>
            <tr>
                <th>سناریو</th>
                <th>ارزش کل (میلیارد)</th>
                <th>ارزش/سهم (ریال)</th>
                <th>اختلاف با بازار</th>
                <th>نتیجه</th>
            </tr>
"""
        
        for scenario in ['خوشبینانه', 'خنثی', 'بدبینانه']:
            total = valuations.get(scenario, 0)
            per_share = val_per_share.get(scenario, 0)
            
            if current_price > 0 and per_share > 0:
                diff_pct = ((per_share - current_price) / current_price) * 100
                diff_class = 'positive' if diff_pct > 0 else 'negative'
                
                if diff_pct > 20:
                    verdict = "سهم زیرارزش - فرصت خرید"
                elif diff_pct > 0:
                    verdict = "سهم نزدیک به ارزش ذاتی"
                elif diff_pct > -20:
                    verdict = "سهم کمی گران - محتاط باشید"
                elif diff_pct > -50:
                    verdict = "سهم گران - ریسک بالا"
                else:
                    verdict = "سهم بسیار گران - احتمال حباب"
                    
                html += f"""
            <tr>
                <td><strong>{scenario}</strong></td>
                <td>{total/1000:,.1f}</td>
                <td>{per_share:,.0f}</td>
                <td class="{diff_class}">{diff_pct:+.1f}%</td>
                <td>{verdict}</td>
            </tr>
"""
        
        html += """
        </table>
        
        <h3>🎯 روش‌های ارزشگذاری استفاده شده</h3>
        
        <div class="method-box">
            <strong>1. DCF (Discounted Cash Flow):</strong> جریان نقدی آزاد تنزیل شده<br>
            وزن: 30% | مناسب برای: شرکت‌های با جریان نقدی پایدار
        </div>
        
        <div class="method-box">
            <strong>2. P/E Multiple:</strong> ضریب قیمت به سود<br>
            وزن: 15% | مناسب برای: مقایسه با شرکت‌های مشابه
        </div>
        
        <div class="method-box">
            <strong>3. P/B Multiple:</strong> ضریب قیمت به ارزش دفتری<br>
            وزن: 15% | مناسب برای: شرکت‌های با دارایی‌های محسوس
        </div>
        
        <div class="method-box">
            <strong>4. EV/EBITDA:</strong> ارزش شرکت به سود عملیاتی<br>
            وزن: 10% | مناسب برای: مقایسه شرکت‌های با ساختار سرمایه متفاوت
        </div>
        
        <div class="method-box">
            <strong>5. P/S Multiple:</strong> ضریب قیمت به فروش<br>
            وزن: 5% | مناسب برای: شرکت‌های کم‌سود یا زیان‌ده
        </div>
        
        <div class="method-box">
            <strong>6. RIM (Residual Income Model):</strong> مدل درآمد باقیمانده<br>
            وزن: 20% | مناسب برای: ارزشگذاری مبتنی بر ROE و ارزش افزوده اقتصادی
        </div>
        
        <div class="method-box">
            <strong>7. APV (Adjusted Present Value):</strong> ارزش فعلی تعدیل شده<br>
            وزن: 5% | مناسب برای: شرکت‌های با اهرم مالی بالا
        </div>
"""
    
    html += """
        <hr>
        
        <h2>💡 نکات کلیدی</h2>
        <div class="info">
            <ul>
                <li><strong>تفاوت با بازار طبیعی است:</strong> قیمت بازار شامل انتظارات آینده، ریسک‌های سیاسی، و عوامل روانی است</li>
                <li><strong>محافظه‌کاری مدل:</strong> ارزشگذاری بنیادی معمولاً محافظه‌کارانه است و حاشیه امنیت دارد</li>
                <li><strong>نقش کیفی:</strong> کیفیت مدیریت، برند، موقعیت رقابتی در مدل لحاظ نمی‌شود</li>
                <li><strong>تورم و رشد:</strong> مدل فرض می‌کند رشد محدود است (طبق GDP)</li>
                <li><strong>چند روش بهتر از یک روش:</strong> استفاده از 7 روش مختلف اعتماد بیشتری ایجاد می‌کند</li>
            </ul>
        </div>
        
        <h2>📋 نتیجه‌گیری</h2>
        <div class="warning">
"""
    
    # خلاصه عمومی
    overvalued_count = 0
    undervalued_count = 0
    
    for symbol, stock_data in data.items():
        shares = stock_data.get('shares_outstanding', 0)
        val_per_share = stock_data.get('valuations_per_share', {})
        
        try:
            price_df = pd.read_csv(f'Data/PriceHistory/{symbol}.csv')
            current_price = price_df['Adj Close'].iloc[-1]
        except:
            continue
        
        neutral = val_per_share.get('خنثی', 0)
        if neutral > 0 and current_price > 0:
            diff_pct = ((neutral - current_price) / current_price) * 100
            if diff_pct < 0:
                overvalued_count += 1
            else:
                undervalued_count += 1
    
    html += f"""
            <strong>خلاصه تحلیل {len(data)} نماد:</strong><br>
            • سهام بیش‌ارزش (گران): {overvalued_count} نماد<br>
            • سهام کم‌ارزش (ارزان): {undervalued_count} نماد<br>
            <br>
            <strong>توصیه کلی:</strong> بازار ایران در حال حاضر تمایل به بیش‌ارزشی دارد.
            برای سرمایه‌گذاری محتاطانه، به سهامی با اختلاف کمتر از 20% توجه کنید.
        </div>
    </div>
</body>
</html>
"""
    
    # ذخیره فایل
    with open('reports/detailed_valuation.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ گزارش تفصیلی ارزشگذاری ذخیره شد: reports/detailed_valuation.html")

if __name__ == "__main__":
    generate_detailed_valuation_report()
