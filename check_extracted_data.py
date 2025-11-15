import sys
sys.path.append('src')
from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser

symbols = ['زفجر', 'کاوه', 'رنیک', 'گکوثر']
ext = FinancialDataExtractor()
parser = FinancialParser()

for sym in symbols:
    folder_map = {
        'زفجر': 'Zfajr', 
        'کاوه': 'Kaveh', 
        'رنیک': 'Renik',
        'گکوثر': 'Gkowthar'
    }
    
    try:
        data = ext.extract_all_data(sym, f'Data/{folder_map[sym]}')
        
        income = parser.parse_income_statement(data['income_statement'])
        balance = parser.parse_balance_sheet(data['balance_sheet'])
        
        print(f'\n{sym}:')
        print(f'  Revenue: {income.get("revenue", 0):,.0f} million')
        print(f'  Net Income: {income.get("net_income", 0):,.0f} million')
        print(f'  Total Assets: {balance.get("total_assets", 0):,.0f} million')
        print(f'  Total Equity: {balance.get("total_equity", 0):,.0f} million')
        
        # Show first few income statement rows
        print(f'  Income Statement rows (first 5):')
        for i in range(min(5, len(data['income_statement']))):
            print(f'    {i}: {data["income_statement"].iloc[i, 0][:50]}')
            
    except Exception as e:
        print(f'\n{sym}: ERROR - {str(e)[:80]}')
