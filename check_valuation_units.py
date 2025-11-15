import json

with open('output/comprehensive_analysis.json', encoding='utf-8') as f:
    data = json.load(f)

print("بررسی واحدهای ارزش‌گذاری:\n")
print("="*100)

for sym, d in data.items():
    val_opt = d['valuations']['خوشبینانه']
    val_neu = d['valuations']['خنثی']
    current_price = d['analysis']['prediction']['current_price']
    equity = d['analysis']['fundamentals'].get('leverage', {}).get('total_equity', 0)
    
    # اگر equity نداریم، خودش را از ترازنامه می‌گیریم
    if equity == 0:
        # ارزش‌گذاری به حقوق صاحبان سهام
        print(f"\n{sym}:")
        print(f"  قیمت سهم: {current_price:,.0f} ریال")
        print(f"  ارزش‌گذاری خوشبینانه: {val_opt:,.0f} میلیون ریال = {val_opt/1000:,.0f} میلیارد")
        print(f"  ارزش‌گذاری خنثی: {val_neu:,.0f} میلیون ریال = {val_neu/1000:,.0f} میلیارد")
        print(f"  ⚠️ نیاز به حقوق صاحبان سهام برای محاسبه P/B")
    else:
        print(f"\n{sym}:")
        print(f"  قیمت سهم: {current_price:,.0f} ریال")
        print(f"  ارزش‌گذاری (میلیون ریال): {val_neu:,.0f}")
        print(f"  حقوق صاحبان سهام (میلیون ریال): {equity:,.0f}")
        print(f"  P/B implied از ارزش‌گذاری: {val_neu/equity:.2f}x")
