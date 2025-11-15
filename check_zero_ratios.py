import json

with open('output/comprehensive_analysis.json', encoding='utf-8') as f:
    data = json.load(f)

print("بررسی نسبت‌های مالی:\n")
print("="*100)

for sym, d in data.items():
    fund = d['analysis']['fundamentals']['profitability']
    print(f"\n{sym}:")
    print(f"  ROE: {fund['roe']:.6f} = {fund['roe']*100:.2f}%")
    print(f"  ROA: {fund['roa']:.6f} = {fund['roa']*100:.2f}%")
    print(f"  Net Margin: {fund['net_margin']:.6f} = {fund['net_margin']*100:.2f}%")
    print(f"  Operating Margin: {fund['operating_margin']:.6f} = {fund['operating_margin']*100:.2f}%")
