"""
Test data extraction from decoded MHTML files
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser

# Test one company that should have data now
test_symbol = "کاوه"
data_folder = "Data/Kaveh"

print("="*70)
print(f"Testing Extraction for {test_symbol}")
print("="*70)

extractor = FinancialDataExtractor(data_folder)
parser = FinancialParser()

# Extract income statement
print("\n[1] Extracting Income Statement...")
income_df = extractor.extract_income_statement()
if income_df is not None and not income_df.empty:
    print(f"   Rows: {len(income_df)}, Columns: {len(income_df.columns)}")
    print("\n   Preview:")
    print(income_df.head())
    
    # Parse it
    print("\n[2] Parsing Income Statement...")
    parsed_income = parser.parse_income_statement(income_df)
    print(f"   Parsed data: {parsed_income}")
else:
    print("   ❌ No data extracted")

# Extract balance sheet
print("\n[3] Extracting Balance Sheet...")
balance_df = extractor.extract_balance_sheet()
if balance_df is not None and not balance_df.empty:
    print(f"   Rows: {len(balance_df)}, Columns: {len(balance_df.columns)}")
    print("\n   Preview:")
    print(balance_df.head())
    
    # Parse it
    print("\n[4] Parsing Balance Sheet...")
    parsed_balance = parser.parse_balance_sheet(balance_df)
    print(f"   Parsed data: {parsed_balance}")
else:
    print("   ❌ No data extracted")

# Check final valuation inputs
if income_df is not None and balance_df is not None:
    print("\n[5] Building Valuation Inputs...")
    data = {
        'income_statement': income_df,
        'balance_sheet': balance_df
    }
    scenario_config = {
        'growth_rate': 0.15,
        'perpetual_growth': 0.08
    }
    
    valuation_inputs = parser.build_valuation_inputs(data, scenario_config)
    
    print("\n   📊 Final Valuation Inputs:")
    for key, value in valuation_inputs.items():
        if isinstance(value, (int, float)):
            print(f"   {key}: {value:,}")
        else:
            print(f"   {key}: {value}")

print("\n" + "="*70)
print("Test Complete!")
print("="*70)
