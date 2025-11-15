import sys
sys.path.append('src')
from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser

extractor = FinancialDataExtractor()
parser = FinancialParser()

income_file = "Data/Zfajr/زفجر - سود و زیان - گزارش_های مالی _ انیگما.mhtml"

soup = extractor.read_mhtml_file(income_file)
df = extractor.extract_table_with_bs4(soup)

print("جستجوی همه ردیف‌هایی که حاوی 'سرمایه' هستند:\n")
print("="*80)

for idx, row in df.iterrows():
    cell_text = str(row[0])
    if 'سرمایه' in cell_text:
        print(f"ردیف {idx}: {cell_text}")
        print(f"   مقادیر: {list(row[1:6])}")
        print()
