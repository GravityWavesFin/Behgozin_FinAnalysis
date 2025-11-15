"""بررسی داده‌های خام استخراج شده از فایل‌های MHTML"""
import sys
import os
sys.path.append('src')
os.system('chcp 65001 > nul')

from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser
import pandas as pd

# نمادهای مشکل‌دار
problem_symbols = [
    ('گکوثر', 'Data/Gkowthar'),
    ('رنیک', 'Data/Renik'),
    ('وسنا', 'Data/Vsana')
]

extractor = FinancialDataExtractor()
parser = FinancialParser()

for symbol, folder in problem_symbols:
    print(f"\n{'='*70}")
    print(f"بررسی {symbol} از {folder}")
    print(f"{'='*70}")
    
    import os
    if not os.path.exists(folder):
        print(f"❌ پوشه موجود نیست!")
        continue
    
    files = os.listdir(folder)
    
    # فایل سود و زیان
    income_files = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
    if income_files:
        print(f"\n📄 فایل سود و زیان: {income_files[0]}")
        file_path = os.path.join(folder, income_files[0])
        soup = extractor.read_mhtml_file(file_path)
        income_df = extractor.extract_table_with_bs4(soup)
        
        print(f"\n🔍 ابعاد DataFrame: {income_df.shape}")
        print(f"\n📊 همه ردیف‌ها:")
        pd.set_option('display.max_columns', 5)
        pd.set_option('display.width', 150)
        pd.set_option('display.max_rows', 50)
        print(income_df.to_string())
        
        # پارس داده
        income_parsed = parser.parse_income_statement(income_df)
        print(f"\n📈 داده‌های پارس شده:")
        for key, value in income_parsed.items():
            print(f"   {key}: {value:,.0f}")
    
    # فایل ترازنامه
    balance_files = [f for f in files if 'ترازنامه' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
    if balance_files:
        print(f"\n📄 فایل ترازنامه: {balance_files[0]}")
        file_path = os.path.join(folder, balance_files[0])
        soup = extractor.read_mhtml_file(file_path)
        balance_df = extractor.extract_table_with_bs4(soup)
        
        print(f"\n🔍 ابعاد DataFrame: {balance_df.shape}")
        print(f"\n📊 5 ردیف اول:")
        print(balance_df.head(10))
        
        # پارس داده
        balance_parsed = parser.parse_balance_sheet(balance_df)
        print(f"\n📈 داده‌های پارس شده:")
        for key, value in balance_parsed.items():
            print(f"   {key}: {value:,.0f}")
