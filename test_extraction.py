import sys
sys.path.append('src')
from data_extractor import FinancialDataExtractor
import pandas as pd

ext = FinancialDataExtractor()
data = ext.extract_all_data('زفجر', 'Data/Zfajr')

print('Balance Sheet:')
if not data['balance_sheet'].empty:
    print(data['balance_sheet'].head())
    print(f'\nColumns: {list(data["balance_sheet"].columns)}')
    print(f'Rows: {len(data["balance_sheet"])}')
else:
    print('Empty!')
    
print('\n\n' + '='*70)
print('Income Statement:')
if not data['income_statement'].empty:
    print(data['income_statement'].head())
    print(f'\nColumns: {list(data["income_statement"].columns)}')
    print(f'Rows: {len(data["income_statement"])}')
else:
    print('Empty!')

print('\n\n' + '='*70)
print('Financial Ratios:')
if not data['financial_ratios'].empty:
    print(data['financial_ratios'])
else:
    print('Empty!')
