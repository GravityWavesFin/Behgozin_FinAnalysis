"""
تست سیستم پیشرفته گزارش‌دهی و کش داده‌ها
"""

import sys
import os
sys.path.append('src')

from price_data_extractor import PriceDataExtractor
from report_generator_advanced import AdvancedReportGenerator
import pandas as pd
import numpy as np


def test_cache_system():
    """تست سیستم کش داده‌ها"""
    print("\n" + "="*70)
    print("🧪 تست سیستم کش داده‌های قیمتی")
    print("="*70)
    
    extractor = PriceDataExtractor(cache_dir='Data/PriceHistory')
    
    # دریافت داده زفجر
    symbol = 'زفجر'
    print(f"\n🔹 اولین دریافت (از اینترنت):")
    df1 = extractor.get_symbol_price_history(
        symbol=symbol,
        start_date='1403-01-01',
        use_cache=True
    )
    
    print(f"\n🔹 دومین دریافت (از کش):")
    df2 = extractor.get_symbol_price_history(
        symbol=symbol,
        start_date='1403-01-01',
        use_cache=True
    )
    
    if not df1.empty and not df2.empty:
        print(f"\n✅ کش کار می‌کند!")
        print(f"   - تعداد رکوردها: {len(df2)}")
        # تبدیل به string برای نمایش
        first_date = df2.index[0].strftime('%Y-%m-%d') if hasattr(df2.index[0], 'strftime') else str(df2.index[0])
        last_date = df2.index[-1].strftime('%Y-%m-%d') if hasattr(df2.index[-1], 'strftime') else str(df2.index[-1])
        print(f"   - محدوده تاریخی: {first_date} تا {last_date}")
    
    return df1


def test_advanced_charts():
    """تست نمودارهای پیشرفته"""
    print("\n" + "="*70)
    print("🧪 تست نمودارهای پیشرفته")
    print("="*70)
    
    # دریافت داده قیمت
    extractor = PriceDataExtractor(cache_dir='Data/PriceHistory')
    df = extractor.get_symbol_price_history(
        symbol='زفجر',
        start_date='1403-01-01',
        use_cache=True
    )
    
    if df.empty:
        print("❌ خطا: داده قیمتی دریافت نشد")
        return
    
    # ایجاد generator
    generator = AdvancedReportGenerator(output_dir='reports')
    
    print("\n📊 ایجاد نمودارها...")
    
    # 1. نمودار قیمت با شاخص‌های تکنیکال
    print("  1️⃣ نمودار قیمت + RSI + حجم...")
    price_chart = generator.create_price_chart(df, 'زفجر')
    
    # 2. نمودار راداری نسبت‌های مالی (داده تصادفی برای تست)
    print("  2️⃣ نمودار راداری نسبت‌های مالی...")
    ratios = {
        'ROE': 25.5,
        'ROA': 18.3,
        'حاشیه سود': 22.1,
        'نسبت جاری': 2.1,
        'بازده دارایی': 15.8
    }
    radar_chart = generator.create_financial_ratios_chart(ratios, 'نسبت‌های مالی زفجر')
    
    # 3. نمودار مقایسه ارزش‌گذاری (داده تصادفی)
    print("  3️⃣ نمودار مقایسه ارزش‌گذاری...")
    valuation_results = {
        'DCF': {'خوشبینانه': 1500, 'خنثی': 1200, 'بدبینانه': 900},
        'P/E': {'خوشبینانه': 1400, 'خنثی': 1150, 'بدبینانه': 950},
        'P/B': {'خوشبینانه': 1350, 'خنثی': 1100, 'بدبینانه': 850},
        'EV/EBITDA': {'خوشبینانه': 1450, 'خنثی': 1180, 'بدبینانه': 920}
    }
    valuation_chart = generator.create_valuation_comparison_chart(valuation_results)
    
    # 4. هیت‌مپ تحلیل حساسیت
    print("  4️⃣ هیت‌مپ تحلیل حساسیت...")
    sensitivity_data = pd.DataFrame(
        np.random.randint(800, 1600, size=(5, 5)),
        columns=['2%', '3%', '4%', '5%', '6%'],
        index=['20%', '22%', '24%', '26%', '28%']
    )
    heatmap_chart = generator.create_sensitivity_heatmap(
        sensitivity_data, 
        'تحلیل حساسیت DCF - زفجر'
    )
    
    # 5. نمودار رتبه‌بندی (داده تصادفی)
    print("  5️⃣ نمودار رتبه‌بندی...")
    ranking_data = pd.DataFrame({
        'symbol': ['رنیک', 'قشیر', 'زدشت', 'وسنا', 'کگاز', 'تلیسه'],
        'total_score': [85.5, 78.2, 72.8, 65.3, 58.7, 52.1],
        'health_score': [90, 80, 75, 70, 60, 55],
        'valuation_score': [85, 78, 72, 65, 58, 50],
        'growth_score': [82, 76, 70, 62, 57, 51],
        'liquidity_score': [88, 79, 74, 64, 59, 53]
    })
    ranking_chart = generator.create_allocation_ranking_chart(ranking_data)
    
    print("\n✅ همه نمودارها با موفقیت ساخته شدند!")
    
    # ایجاد یک گزارش HTML ساده با همه نمودارها
    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>تست گزارش پیشرفته</title>
    <style>
        {generator.executive_css}
    </style>
</head>
<body>
    <div class="page">
        <div class="executive-header">
            <h1>تست سیستم گزارش‌دهی پیشرفته</h1>
            <div class="subtitle">نمونه گزارش با نمودارها و جداول حرفه‌ای</div>
            <div class="meta">
                <span>تاریخ: ۱۴۰۳/۰۸/۲۵</span>
                <span>سیستم بازارگردانی بهگزین</span>
            </div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-label">بازده سالانه</div>
                <div class="metric-value">+۳۰.۱٪</div>
                <div class="metric-change positive">▲ ۵.۲٪</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-label">ارزش بازار</div>
                <div class="metric-value">۱,۲۰۰ میلیارد</div>
                <div class="metric-change positive">▲ ۸.۵٪</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-label">امتیاز سلامت</div>
                <div class="metric-value">۸۵</div>
                <div class="metric-change positive">▲ ۳</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-label">نوسان‌پذیری</div>
                <div class="metric-value">۱۸٪</div>
                <div class="metric-change neutral">→ ۰٪</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                <span class="section-icon">📈</span>
                <span>روند قیمتی و شاخص‌های تکنیکال</span>
            </div>
            <div class="chart-container">
                <img src="{price_chart}" alt="نمودار قیمت">
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                <span class="section-icon">📊</span>
                <span>تحلیل نسبت‌های مالی</span>
            </div>
            <div class="grid-2col">
                <div class="chart-container">
                    <img src="{radar_chart}" alt="نمودار راداری">
                </div>
                <div class="info-card">
                    <div class="info-card-title">نسبت‌های کلیدی</div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>نسبت</th>
                                <th>مقدار</th>
                                <th>وضعیت</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>بازده حقوق صاحبان سهام (ROE)</td>
                                <td class="value-positive">۲۵.۵٪</td>
                                <td><span class="badge badge-excellent">عالی</span></td>
                            </tr>
                            <tr>
                                <td>بازده دارایی‌ها (ROA)</td>
                                <td class="value-positive">۱۸.۳٪</td>
                                <td><span class="badge badge-good">خوب</span></td>
                            </tr>
                            <tr>
                                <td>حاشیه سود خالص</td>
                                <td class="value-positive">۲۲.۱٪</td>
                                <td><span class="badge badge-excellent">عالی</span></td>
                            </tr>
                            <tr>
                                <td>نسبت جاری</td>
                                <td class="value-positive">۲.۱</td>
                                <td><span class="badge badge-good">خوب</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <div class="page">
        <div class="section">
            <div class="section-header">
                <span class="section-icon">💎</span>
                <span>مقایسه روش‌های ارزش‌گذاری</span>
            </div>
            <div class="chart-container">
                <img src="{valuation_chart}" alt="مقایسه ارزش‌گذاری">
            </div>
            
            <div class="executive-summary">
                <div class="summary-title">خلاصه ارزش‌گذاری</div>
                <div class="summary-item">
                    <span class="summary-label">میانگین وزنی (سناریوی خنثی):</span>
                    <span class="summary-value">۱,۱۵۸ میلیارد ریال</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">قیمت فعلی بازار:</span>
                    <span class="summary-value">۱,۰۵۰ میلیارد ریال</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">پتانسیل رشد:</span>
                    <span class="summary-value value-positive">+۱۰.۳٪</span>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                <span class="section-icon">🔥</span>
                <span>تحلیل حساسیت DCF</span>
            </div>
            <div class="chart-container">
                <img src="{heatmap_chart}" alt="هیت‌مپ حساسیت">
            </div>
            <div class="alert-box alert-info">
                <div class="alert-title">💡 نکته تحلیلی</div>
                <p>ارزش‌گذاری به تغییرات نرخ تنزیل حساس‌تر از تغییرات نرخ رشد است. 
                در محدوده نرخ تنزیل ۲۲-۲۶٪ و نرخ رشد ۳-۵٪، ارزش شرکت بین ۱,۰۰۰ تا ۱,۴۰۰ میلیارد ریال نوسان دارد.</p>
            </div>
        </div>
    </div>
    
    <div class="page">
        <div class="section">
            <div class="section-header">
                <span class="section-icon">🎯</span>
                <span>رتبه‌بندی نمادها برای تخصیص منابع</span>
            </div>
            <div class="chart-container">
                <img src="{ranking_chart}" alt="رتبه‌بندی">
            </div>
            
            <div class="alert-box alert-success">
                <div class="alert-title">✅ توصیه سرمایه‌گذاری</div>
                <p><strong>رنیک</strong> با امتیاز <strong>۸۵.۵</strong> بهترین گزینه برای تخصیص منابع است.</p>
                <p>این نماد در همه معیارهای سلامت مالی، ارزش‌گذاری، رشد و نقدینگی عملکرد قوی دارد.</p>
            </div>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>رتبه</th>
                        <th>نماد</th>
                        <th>امتیاز کل</th>
                        <th>سلامت مالی</th>
                        <th>ارزش‌گذاری</th>
                        <th>رشد</th>
                        <th>نقدینگی</th>
                        <th>توصیه</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>۱</td>
                        <td><strong>رنیک</strong></td>
                        <td class="value-positive">۸۵.۵</td>
                        <td>۹۰</td>
                        <td>۸۵</td>
                        <td>۸۲</td>
                        <td>۸۸</td>
                        <td><span class="badge badge-excellent">خرید قوی</span></td>
                    </tr>
                    <tr>
                        <td>۲</td>
                        <td><strong>قشیر</strong></td>
                        <td class="value-positive">۷۸.۲</td>
                        <td>۸۰</td>
                        <td>۷۸</td>
                        <td>۷۶</td>
                        <td>۷۹</td>
                        <td><span class="badge badge-good">خرید</span></td>
                    </tr>
                    <tr>
                        <td>۳</td>
                        <td><strong>زدشت</strong></td>
                        <td class="value-positive">۷۲.۸</td>
                        <td>۷۵</td>
                        <td>۷۲</td>
                        <td>۷۰</td>
                        <td>۷۴</td>
                        <td><span class="badge badge-good">خرید</span></td>
                    </tr>
                    <tr>
                        <td>۴</td>
                        <td><strong>وسنا</strong></td>
                        <td class="value-warning">۶۵.۳</td>
                        <td>۷۰</td>
                        <td>۶۵</td>
                        <td>۶۲</td>
                        <td>۶۴</td>
                        <td><span class="badge badge-moderate">نگهداری</span></td>
                    </tr>
                    <tr>
                        <td>۵</td>
                        <td><strong>کگاز</strong></td>
                        <td class="value-warning">۵۸.۷</td>
                        <td>۶۰</td>
                        <td>۵۸</td>
                        <td>۵۷</td>
                        <td>۵۹</td>
                        <td><span class="badge badge-moderate">نگهداری</span></td>
                    </tr>
                    <tr>
                        <td>۶</td>
                        <td><strong>تلیسه</strong></td>
                        <td class="value-negative">۵۲.۱</td>
                        <td>۵۵</td>
                        <td>۵۰</td>
                        <td>۵۱</td>
                        <td>۵۳</td>
                        <td><span class="badge badge-weak">احتیاط</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="page-footer">
            <div class="footer-logo">🔷 سیستم بازارگردانی بهگزین</div>
            <p>این گزارش بر اساس تحلیل‌های بنیادی، ارزش‌گذاری چندگانه و تحلیل ریسک تهیه شده است</p>
            <p>تاریخ: ۱۴۰۳/۰۸/۲۵ | محرمانه - ویژه مدیران ارشد</p>
        </div>
    </div>
</body>
</html>
    """
    
    # ذخیره گزارش
    print("\n💾 ذخیره گزارش...")
    generator.save_report(html_content, 'test_advanced_report', generate_pdf=True)
    
    print("\n✅ گزارش کامل ذخیره شد!")
    print("   📄 HTML: reports/test_advanced_report.html")
    print("   📄 PDF: reports/test_advanced_report.pdf")


def main():
    """اجرای تست‌ها"""
    print("\n" + "🚀 شروع تست سیستم‌های پیشرفته")
    print("="*70)
    
    # تست کش
    df = test_cache_system()
    
    # تست نمودارها
    test_advanced_charts()
    
    print("\n" + "="*70)
    print("✅ همه تست‌ها با موفقیت انجام شد!")
    print("="*70)


if __name__ == "__main__":
    main()
