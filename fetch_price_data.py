"""
دریافت و ذخیره داده‌های قیمتی تاریخی برای همه نمادها
"""

import sys
sys.path.append('src')

from finpy_tse import get_price_history
import pandas as pd
import os
import jdatetime
from config import SYMBOLS

def fetch_and_save_all_symbols():
    """دریافت و ذخیره داده‌های قیمتی همه نمادها"""
    
    cache_dir = 'Data/PriceHistory'
    os.makedirs(cache_dir, exist_ok=True)
    
    # همه نمادها
    all_symbols = SYMBOLS['با_مازاد_منابع'] + SYMBOLS['با_کمبود_منابع']
    
    # تاریخ امروز به شمسی
    today = jdatetime.date.today()
    end_date_str = f'{today.year:04d}-{today.month:02d}-{today.day:02d}'
    start_date_str = '1403-01-01'
    
    print("\n" + "="*70)
    print(f"دریافت داده‌های قیمتی {len(all_symbols)} نماد")
    print(f"از {start_date_str} تا {end_date_str}")
    print("="*70)
    
    success_count = 0
    failed_symbols = []
    
    for i, symbol in enumerate(all_symbols, 1):
        print(f"\n[{i}/{len(all_symbols)}] {symbol}")
        print("-" * 50)
        
        try:
            # دریافت داده
            print(f"در حال دریافت از finpy-tse...")
            print(f"   پارامترها: symbol={symbol}, از {start_date_str} تا {end_date_str}")
            
            try:
                df = get_price_history(
                    stock=symbol,
                    start_date=start_date_str,
                    end_date=end_date_str,
                    ignore_date=False,
                    adjust_price=True,
                    show_weekday=True,
                    double_date=True
                )
            except Exception as api_error:
                print(f"[خطا] خطا در فراخوانی get_price_history: {api_error}")
                print(f"   نوع خطا: {type(api_error).__name__}")
                import traceback
                traceback.print_exc()
                failed_symbols.append(symbol)
                continue
            
            print(f"   نوع بازگشتی: {type(df)}")
            
            if df is None:
                print(f"[خطا] تابع None برگرداند - احتمالاً نماد در سیستم یافت نشد")
                print(f"   نکته: نماد باید دقیقاً مطابق با نام در سایت tsetmc باشد")
                failed_symbols.append(symbol)
                continue
            
            if df.empty:
                print(f"[خطا] DataFrame خالی است")
                failed_symbols.append(symbol)
                continue
            
            print(f"[OK] {len(df)} روز داده دریافت شد")
            
            # نمایش ستون‌ها
            print(f"ستون‌ها: {list(df.columns)}")
            print(f"نوع index: {type(df.index[0]) if len(df) > 0 else 'خالی'}")
            
            # ذخیره به CSV
            cache_file = os.path.join(cache_dir, f"{symbol}.csv")
            df.to_csv(cache_file, encoding='utf-8-sig')
            print(f"[ذخیره] ذخیره شد: {cache_file}")
            
            # نمایش نمونه
            print(f"\nنمونه داده:")
            print(df.head(3))
            
            success_count += 1
            
        except Exception as e:
            print(f"[خطا] خطا: {e}")
            failed_symbols.append(symbol)
    
    # خلاصه
    print("\n" + "="*70)
    print("خلاصه")
    print("="*70)
    print(f"[OK] موفق: {success_count}/{len(all_symbols)}")
    
    if failed_symbols:
        print(f"[خطا] ناموفق: {len(failed_symbols)}")
        print(f"   نمادها: {', '.join(failed_symbols)}")
    
    print("="*70)
    
    return success_count, failed_symbols


if __name__ == "__main__":
    fetch_and_save_all_symbols()
