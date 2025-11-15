import sys
sys.path.append('src')
from data_extractor import FinancialDataExtractor

extractor = FinancialDataExtractor()

income_file = "Data/Zfajr/زفجر - سود و زیان - گزارش_های مالی _ انیگما.mhtml"

soup = extractor.read_mhtml_file(income_file)
df = extractor.extract_table_with_bs4(soup)

print(f"ردیف 34 (capital row):")
print(f"  متن دقیق: '{df.iloc[34, 0]}'")
print(f"  طول: {len(df.iloc[34, 0])}")
print(f"  repr: {repr(df.iloc[34, 0])}")
print()

print(f"ردیف 14 (investment income):")
print(f"  متن دقیق: '{df.iloc[14, 0]}'")
print(f"  طول: {len(df.iloc[14, 0])}")
print(f"  repr: {repr(df.iloc[14, 0])}")
