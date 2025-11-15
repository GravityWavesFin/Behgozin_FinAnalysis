"""
Test improved MHTML extraction
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser

print("="*70)
print("Testing Improved MHTML Extraction")
print("="*70)

# Test کاوه
symbol = "کاوه"
folder = "Data/Kaveh"

print(f"\n🔍 Testing: {symbol}")
print("-"*70)

extractor = FinancialDataExtractor()

# پیدا کردن فایل سود و زیان
files = os.listdir(folder)
income_file = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')][0]
file_path = os.path.join(folder, income_file)

print(f"📄 File: {income_file}")

# خواندن فایل
soup = extractor.read_mhtml_file(file_path)

if soup:
    print("✓ File read successfully")
    
    # استخراج جدول
    df = extractor.extract_table_with_bs4(soup)
    
    if not df.empty:
        print(f"\n✓ Table extracted: {df.shape[0]} rows × {df.shape[1]} columns")
        print("\n📊 First 5 rows:")
        print(df.head())
        
        # تست parser
        parser = FinancialParser()
        parsed = parser.parse_income_statement(df)
        
        print(f"\n💰 Parsed Income Statement:")
        for key, value in parsed.items():
            if isinstance(value, (int, float)) and value != 0:
                print(f"   {key}: {value:,}")
    else:
        print("❌ No table extracted")
else:
    print("❌ Failed to read file")

print("\n" + "="*70)
