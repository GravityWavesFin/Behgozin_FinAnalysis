import json

with open('output/comprehensive_analysis.json', encoding='utf-8') as f:
    data = json.load(f)

sym = 'زفجر'
print(f"بررسی محاسبات برای {sym}:\n")
print("="*80)

shares = data[sym]['shares_outstanding']
val_neutral_million = data[sym]['valuations']['خنثی']
val_per_share = data[sym]['valuations_per_share']['خنثی']
current_price = data[sym]['analysis']['prediction']['current_price']

print(f"تعداد سهام: {shares:,.0f} سهم")
print(f"ارزش کل (خنثی): {val_neutral_million:,.0f} میلیون ریال")
print(f"ارزش کل (میلیارد): {val_neutral_million/1000:,.1f} میلیارد ریال")
print(f"\nمحاسبه ارزش هر سهم:")
print(f"  فرمول: (ارزش کل میلیون × 1,000,000) ÷ تعداد سهام")
print(f"  محاسبه: ({val_neutral_million:,.0f} × 1,000,000) ÷ {shares:,.0f}")
print(f"  نتیجه: {val_per_share:,.0f} ریال")
print(f"\nقیمت فعلی بازار: {current_price:,.0f} ریال")
print(f"اختلاف: {((val_per_share - current_price)/current_price*100):+.1f}%")

print("\n" + "="*80)
print("⚠️ مشکل: ارزش هر سهم خیلی بالاست!")
print(f"   ارزش محاسبه شده ({val_per_share:,.0f}) بیش از {val_per_share/current_price:.0f} برابر قیمت بازار است")
