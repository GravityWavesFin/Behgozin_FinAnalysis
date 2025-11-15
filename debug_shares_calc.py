import sys
sys.path.append('src')
from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser

extractor = FinancialDataExtractor()
parser = FinancialParser()

symbol = 'زفجر'
folder = 'Data/Zfajr'

print(f"بررسی محاسبه تعداد سهام برای {symbol}:\n")
print("="*80)

import os
files = os.listdir(folder)

income_files = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
if income_files:
    file_path = os.path.join(folder, income_files[0])
    soup = extractor.read_mhtml_file(file_path)
    income_df = extractor.extract_table_with_bs4(soup)
    income_parsed = parser.parse_income_statement(income_df)
    
    print("داده‌های استخراج شده:")
    print(f"  سرمایه (capital): {income_parsed.get('capital', 0):,.0f} میلیون ریال")
    print(f"  تعداد سهام محاسبه شده: {income_parsed.get('shares_outstanding', 0):,.0f}")
    
    print("\nمنطق محاسبه در کد:")
    capital_millions = income_parsed.get('capital', 0)
    print(f"  capital_millions = {capital_millions:,.0f}")
    print(f"  shares = (capital × 1,000,000) / 1000")
    print(f"  shares = ({capital_millions:,.0f} × 1,000,000) / 1000")
    print(f"  shares = {capital_millions * 1_000_000 / 1000:,.0f}")
    
    print("\n⚠️ مشکل: سرمایه اشتباه است!")
    print(f"  سرمایه از فایل: {capital_millions:,.0f} (باید 3,829,327 باشد)")
