"""
تست سیستم استخراج داده‌های قیمتی
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from price_data_extractor import PriceDataExtractor
from config import SYMBOLS

def test_single_symbol():
    """تست استخراج یک نماد"""
    print("="*70)
    print("تست استخراج داده‌های قیمتی - نماد واحد")
    print("="*70)
    
    extractor = PriceDataExtractor()
    
    # تست زفجر
    symbol = 'زفجر'
    df = extractor.get_symbol_price_history(
        symbol=symbol,
        start_date='1402-01-01',
        adjust_price=True
    )
    
    if not df.empty:
        print(f"\n✓ داده‌های {symbol} دریافت شد")
        print(f"\nستون‌های موجود: {list(df.columns)}")
        print(f"\n5 رکورد اول:")
        print(df.head())
        print(f"\n5 رکورد آخر:")
        print(df.tail())
        
        # بررسی قیمت‌های تعدیل شده
        if 'Adj Close' in df.columns:
            print(f"\n✓ قیمت‌های تعدیل شده موجود است")
            print(f"\nمقایسه قیمت معمولی و تعدیل شده:")
            comparison = df[['Close', 'Adj Close', 'Final', 'Adj Final']].tail(10)
            print(comparison)
        
        # خلاصه آماری
        summary = extractor.get_price_summary(symbol)
        print(f"\n📊 خلاصه آماری {symbol}:")
        print("-" * 70)
        for key, value in summary.items():
            if isinstance(value, (int, float)):
                print(f"{key:.<35} {value:>20,.2f}")
            else:
                print(f"{key:.<35} {value:>20}")
        
        return True
    else:
        print(f"\n✗ داده‌ای برای {symbol} دریافت نشد")
        return False


def test_multiple_symbols():
    """تست استخراج چند نماد"""
    print("\n\n" + "="*70)
    print("تست استخراج داده‌های قیمتی - چند نماد")
    print("="*70)
    
    extractor = PriceDataExtractor()
    
    # تست نمادهای با مازاد منابع
    symbols = SYMBOLS['با_مازاد_منابع']
    
    all_data = extractor.get_all_symbols_price_history(
        symbols=symbols,
        start_date='1402-01-01',
        adjust_price=True
    )
    
    print(f"\n✓ داده‌های {len(all_data)} نماد از {len(symbols)} نماد درخواستی دریافت شد")
    
    # نمایش خلاصه برای هر نماد
    print("\n📊 خلاصه نتایج:")
    print("-" * 70)
    
    for symbol in symbols:
        if symbol in all_data:
            summary = extractor.get_price_summary(symbol)
            print(f"\n{symbol}:")
            print(f"  تعداد روز: {summary.get('تعداد روزهای معاملاتی', 0)}")
            print(f"  بازده کل: {summary.get('بازده کل', 0):,.2f}%")
            print(f"  نوسان سالانه: {summary.get('نوسان سالانه', 0):.2f}%")
            print(f"  آخرین قیمت: {summary.get('آخرین قیمت', 0):,.0f} ریال")
        else:
            print(f"\n{symbol}: ✗ داده‌ای دریافت نشد")
    
    return len(all_data) > 0


def test_technical_indicators():
    """تست محاسبه اندیکاتورهای تکنیکال"""
    print("\n\n" + "="*70)
    print("تست محاسبه اندیکاتورهای تکنیکال")
    print("="*70)
    
    extractor = PriceDataExtractor()
    
    symbol = 'زفجر'
    df = extractor.get_symbol_price_history(
        symbol=symbol,
        start_date='1401-01-01',
        adjust_price=True
    )
    
    if not df.empty:
        # محاسبه اندیکاتورها
        df_indicators = extractor.calculate_technical_indicators(symbol)
        
        print(f"\n✓ اندیکاتورها برای {symbol} محاسبه شد")
        print(f"\nستون‌های جدید: {[col for col in df_indicators.columns if col not in df.columns]}")
        
        # نمایش 10 رکورد آخر
        indicators_cols = ['Close', 'Adj Close', 'SMA_20', 'SMA_50', 'RSI', 'MACD']
        available_cols = [col for col in indicators_cols if col in df_indicators.columns]
        
        print(f"\n10 رکورد آخر اندیکاتورها:")
        print(df_indicators[available_cols].tail(10))
        
        return True
    else:
        print(f"\n✗ داده‌ای برای {symbol} دریافت نشد")
        return False


def main():
    """اجرای تست‌ها"""
    results = {}
    
    try:
        # تست 1: نماد واحد
        results['single'] = test_single_symbol()
        
        # تست 2: چند نماد
        results['multiple'] = test_multiple_symbols()
        
        # تست 3: اندیکاتورهای تکنیکال
        results['indicators'] = test_technical_indicators()
        
        # نتیجه کلی
        print("\n\n" + "="*70)
        print("خلاصه نتایج تست")
        print("="*70)
        
        for test_name, result in results.items():
            status = "✓ موفق" if result else "✗ ناموفق"
            print(f"{test_name:.<50} {status:>20}")
        
        all_passed = all(results.values())
        
        if all_passed:
            print("\n✅ تمام تست‌ها با موفقیت اجرا شدند!")
        else:
            print("\n⚠️ برخی از تست‌ها با خطا مواجه شدند")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ خطای کلی: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    print("\n" + "="*70)
    if success:
        print("✅ سیستم استخراج داده‌های قیمتی آماده است")
    else:
        print("❌ سیستم نیاز به بررسی بیشتر دارد")
    print("="*70)
