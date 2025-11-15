import sys
sys.path.append('src')
from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser
from config import DCF_SCENARIOS
import pandas as pd

ext = FinancialDataExtractor()
data = ext.extract_all_data('زفجر', 'Data/Zfajr')

print('='*70)
print('Balance Sheet - First 10 rows, column 0:')
print('='*70)
if not data['balance_sheet'].empty:
    for i in range(min(10, len(data['balance_sheet']))):
        print(f"{i}: {data['balance_sheet'].iloc[i, 0]}")

print('\n' + '='*70)
print('Income Statement - First 10 rows, column 0:')
print('='*70)
if not data['income_statement'].empty:
    for i in range(min(10, len(data['income_statement']))):
        print(f"{i}: {data['income_statement'].iloc[i, 0]}")

print('\n' + '='*70)
print('Testing Parser:')
print('='*70)
parser = FinancialParser()

income_data = parser.parse_income_statement(data['income_statement'])
balance_data = parser.parse_balance_sheet(data['balance_sheet'])

print(f"\nIncome Statement Data:")
for key, val in income_data.items():
    print(f"  {key}: {val:,.0f}")

print(f"\nBalance Sheet Data:")
for key, val in balance_data.items():
    print(f"  {key}: {val:,.0f}")

print('\n' + '='*70)
print('Building Valuation Inputs:')
print('='*70)
scenario_config = DCF_SCENARIOS['خنثی']
valuation_params = parser.build_valuation_inputs(data, scenario_config)

print(f"\nKey Valuation Parameters:")
print(f"  Revenue: {valuation_params.get('revenue', 0):,.0f}")
print(f"  Earnings: {valuation_params.get('earnings', 0):,.0f}")
print(f"  EBITDA: {valuation_params.get('ebitda', 0):,.0f}")
print(f"  FCF: {valuation_params.get('fcf', 0):,.0f}")
print(f"  Book Value: {valuation_params.get('book_value', 0):,.0f}")
print(f"  Total Assets: {valuation_params.get('total_assets', 0):,.0f}")
print(f"  ROE: {valuation_params.get('roe', 0):.2%}")
