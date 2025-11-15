"""یافتن ردیف سود خالص در فایل‌های MHTML"""
import sys
import os
sys.path.append('src')

from data_extractor import FinancialDataExtractor
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)

extractor = FinancialDataExtractor()

# بررسی گکوثر
symbol = 'گکوثر'
folder = 'Data/Gkowthar'
files = os.listdir(folder)
income_files = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')]

if income_files:
    print(f"بررسی {symbol}:")
    print("="*80)
    file_path = os.path.join(folder, income_files[0])
    soup = extractor.read_mhtml_file(file_path)
    income_df = extractor.extract_table_with_bs4(soup)
    
    # چاپ ستون اول (نام ردیف‌ها)
    print("\nنام ردیف‌ها (ستون 0):")
    for i, val in enumerate(income_df.iloc[:, 0]):
        print(f"{i:2d}: {val}")
    
    print("\n" + "="*80)
    print(f"بررسی ردیف‌هایی که حاوی 'سود' یا 'خالص' یا 'سرمایه' هستند:")
    for i, val in enumerate(income_df.iloc[:, 0]):
        if 'سود' in str(val) or 'خالص' in str(val) or 'زیان' in str(val) or 'سرمایه' in str(val):
            row_values = income_df.iloc[i, 1:6].tolist()
            print(f"\nردیف {i}: {val}")
            print(f"   مقادیر: {row_values}")
