"""
تست سریع سیستم با یک نماد
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🧪 تست سریع سیستم")
print("="*80)

try:
    print("\n1️⃣ تست استخراج قیمت...")
    from price_data_extractor import PriceDataExtractor
    
    extractor = PriceDataExtractor()
    df = extractor.get_symbol_price_history(
        symbol='زفجر',
        start_date='1403-01-01',
        adjust_price=True
    )
    
    if not df.empty:
        print(f"✓ {len(df)} روز داده قیمتی دریافت شد")
        summary = extractor.get_price_summary('زفجر')
        print(f"✓ بازده کل: {summary.get('بازده کل', 0):.2f}%")
    else:
        print("✗ داده قیمتی دریافت نشد")
    
    print("\n2️⃣ تست تولید گزارش HTML...")
    from report_generator import ReportGenerator
    from persian_utils import format_number, format_percentage
    
    generator = ReportGenerator()
    
    # ایجاد HTML ساده
    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>تست گزارش زفجر</title>
    <style>{generator.base_css}</style>
</head>
<body>
    <div class="page">
        <div class="header">
            <h1>گزارش تست زفجر</h1>
        </div>
        <div class="section">
            <div class="section-title">📊 خلاصه</div>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">تعداد روزها</div>
                    <div class="metric-value">{format_number(len(df))}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">بازده</div>
                    <div class="metric-value">{format_percentage(summary.get('بازده کل', 0))}</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    # ذخیره HTML
    html_path = generator.save_html_report(html_content, "test_report.html")
    print(f"✓ HTML ذخیره شد: {html_path}")
    
    # تبدیل به PDF
    print("\n3️⃣ تست تولید PDF...")
    pdf_path = os.path.join(generator.output_dir, "test_report.pdf")
    success = generator.html_to_pdf(html_content, pdf_path)
    
    if success:
        print(f"✓ PDF ذخیره شد: {pdf_path}")
    else:
        print("⚠️ PDF تولید نشد اما HTML موجود است")
    
    print("\n" + "="*80)
    print("✅ تست با موفقیت تکمیل شد!")
    print("="*80)
    print(f"\n📁 فایل‌ها در پوشه '{generator.output_dir}' ذخیره شدند")
    
except Exception as e:
    print(f"\n❌ خطا: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ سیستم آماده اجرای کامل است!")
