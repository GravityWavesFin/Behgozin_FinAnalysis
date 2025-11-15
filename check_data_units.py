"""بررسی واحدهای داده‌های مالی خام"""
import sys
sys.path.append('src')

from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser

extractor = FinancialDataExtractor()
parser = FinancialParser()

symbol = 'زفجر'
folder = 'Data/Zfajr'

print(f"بررسی واحدهای داده {symbol}:\n")
print("="*80)

import os
files = os.listdir(folder)

# سود و زیان
income_files = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
if income_files:
    file_path = os.path.join(folder, income_files[0])
    soup = extractor.read_mhtml_file(file_path)
    income_df = extractor.extract_table_with_bs4(soup)
    income_parsed = parser.parse_income_statement(income_df)
    
    print("صورت سود و زیان:")
    for key, value in income_parsed.items():
        print(f"  {key}: {value:,.0f}")

# ترازنامه
balance_files = [f for f in files if 'ترازنامه' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
if balance_files:
    file_path = os.path.join(folder, balance_files[0])
    soup = extractor.read_mhtml_file(file_path)
    balance_df = extractor.extract_table_with_bs4(soup)
    balance_parsed = parser.parse_balance_sheet(balance_df)
    
    print("\nترازنامه:")
    for key, value in balance_parsed.items():
        print(f"  {key}: {value:,.0f}")

print("\n" + "="*80)
print("بررسی منطقی بودن:")
print(f"  حقوق صاحبان / دارایی = {balance_parsed['total_equity']/balance_parsed['total_assets']:.1%}")
print(f"  سود خالص / درآمد = {income_parsed['net_income']/income_parsed['revenue']:.1%}")
print(f"  سود خالص / حقوق صاحبان (ROE) = {income_parsed['net_income']/balance_parsed['total_equity']:.1%}")

# قیمت سهم فعلی
current_price = 21550  # ریال
print(f"\nقیمت سهم فعلی: {current_price:,.0f} ریال")
print(f"\nاگر واحد میلیون ریال باشد:")
print(f"  P/E = قیمت / (سود خالص × 1,000,000 / تعداد سهام)")
print(f"  P/B = قیمت / (حقوق × 1,000,000 / تعداد سهام)")
