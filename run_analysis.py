"""
اسکریپت اجرای کامل سیستم تحلیل بازارگردانی
این اسکریپت تمام تحلیل‌ها را انجام داده و گزارش‌های HTML و PDF تولید می‌کند
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🚀 سیستم تحلیل جامع بازارگردانی بهگزین")
print("="*80)
print(f"⏰ زمان شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# بررسی اتصال اینترنت
print("\n🌐 بررسی اتصال اینترنت...")
try:
    import requests
    response = requests.get('https://www.google.com', timeout=5)
    print("✓ اتصال اینترنت برقرار است")
except:
    print("⚠️ اتصال اینترنت وجود ندارد - ممکن است در دریافت داده‌های قیمتی مشکل پیش بیاید")
    response = input("آیا می‌خواهید ادامه دهید؟ (y/n): ")
    if response.lower() != 'y':
        print("خروج از برنامه")
        sys.exit(0)

# بررسی نصب کتابخانه‌ها
print("\n📦 بررسی کتابخانه‌های مورد نیاز...")
required_packages = [
    'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
    'beautifulsoup4', 'lxml', 'openpyxl',
    'finpy_tse', 'jdatetime',
    'xhtml2pdf', 'jinja2', 'reportlab'
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} - نصب نشده")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️ کتابخانه‌های زیر نصب نشده‌اند:")
    for pkg in missing_packages:
        print(f"  - {pkg}")
    print("\nبرای نصب:")
    print(f"pip install {' '.join(missing_packages)}")
    sys.exit(1)

print("\n✓ تمام کتابخانه‌ها نصب شده‌اند")

# اجرای تحلیل
print("\n" + "="*80)
print("شروع تحلیل...")
print("="*80)

try:
    from main import main
    
    # اجرای تابع اصلی
    results = main()
    
    if results:
        print("\n" + "="*80)
        print("✅ تحلیل با موفقیت تکمیل شد!")
        print("="*80)
        
        print("\n📊 خلاصه نتایج:")
        print(f"  - تعداد شرکت‌های تحلیل شده: {len(results.get('data', {}))}")
        print(f"  - تعداد تحلیل‌های بنیادی: {len(results.get('analyses', {}))}")
        print(f"  - تعداد ارزش‌گذاری: {len(results.get('valuations', {}))}")
        
        print("\n📁 مسیر فایل‌های خروجی:")
        print(f"  - گزارش‌های HTML و PDF: ./reports/")
        print(f"  - داده‌های خام: ./output/")
        
        print("\n💡 نکات:")
        print("  1. گزارش‌های HTML را می‌توانید با مرورگر باز کنید")
        print("  2. گزارش‌های PDF برای پرینت آماده هستند")
        print("  3. تمام اعداد و متن‌ها به فارسی هستند")
        print("  4. گزارش‌ها در سایز A4 طراحی شده‌اند")
        
    else:
        print("\n❌ تحلیل با خطا مواجه شد")
        sys.exit(1)
        
except KeyboardInterrupt:
    print("\n\n⚠️ برنامه توسط کاربر متوقف شد")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ خطای غیرمنتظره: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    print(f"\n⏰ زمان پایان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
input("\n\nEnter را برای خروج فشار دهید...")
