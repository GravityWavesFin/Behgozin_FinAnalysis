"""
اجرای تحلیل کامل با ارزش‌گذاری و تخصیص منابع
شامل: تحلیل بنیادی + ارزش‌گذاری چندگانه + تخصیص منابع در 9 سناریو
"""

import sys
sys.path.append('src')

import pandas as pd
import numpy as np
from config import SYMBOLS, DCF_SCENARIOS
from price_data_extractor import PriceDataExtractor
from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser
from fundamental_analysis import FundamentalAnalysis
from valuation import CompanyValuation
from report_generator_html import HTMLReportGenerator
from persian_utils import format_number, format_percentage, to_persian_digits
import jdatetime
import json
import os


def analyze_company(symbol: str, price_df: pd.DataFrame, financial_data: dict = None):
    """
    تحلیل کامل یک شرکت
    """
    print(f"\n{'='*70}")
    print(f"Analyzing {symbol}")
    print(f"{'='*70}")
    
    results = {
        'symbol': symbol,
        'price_data': {},
        'fundamental': {},
        'valuation': {}
    }
    
    # 1. تحلیل قیمتی
    if not price_df.empty:
        print(f"[OK] تحلیل قیمتی...")
        first_price = price_df['Adj Close'].iloc[0]
        last_price = price_df['Adj Close'].iloc[-1]
        total_return = ((last_price / first_price) - 1) * 100
        
        # محاسبه نوسان (استاندارد دیویشن بازده روزانه)
        daily_returns = price_df['Adj Close'].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252) * 100  # سالانه
        
        results['price_data'] = {
            'days': len(price_df),
            'first_price': first_price,
            'last_price': last_price,
            'total_return': total_return,
            'volatility': volatility,
            'avg_volume': price_df['Volume'].mean()
        }
        
        print(f"   قیمت: {format_number(first_price)} -> {format_number(last_price)}")
        print(f"   بازده: {format_percentage(total_return)}")
        print(f"   نوسان: {format_percentage(volatility)}")
    
    # 2. تحلیل بنیادی (اگر داده مالی داشتیم)
    if financial_data:
        try:
            print(f"[OK] تحلیل بنیادی...")
            analyzer = FundamentalAnalysis(financial_data)
            ratios = analyzer.calculate_all_ratios()
            
            results['fundamental'] = {
                'profitability': ratios.get('profitability', {}),
                'liquidity': ratios.get('liquidity', {}),
                'leverage': ratios.get('leverage', {}),
                'efficiency': ratios.get('efficiency', {})
            }
            
            print(f"   نسبت‌های محاسبه شد")
        except Exception as e:
            print(f"   [!] خطا در تحلیل بنیادی: {str(e)[:50]}")
    
    # 3. ارزش‌گذاری در 3 سناریو
    print(f"[OK] ارزش‌گذاری...")
    # اگر داده مالی نداریم، از داده ساده استفاده می‌کنیم
    if not financial_data:
        financial_data = {
            'balance_sheet': pd.DataFrame(),
            'income_statement': pd.DataFrame(),
            'cash_flow': pd.DataFrame()
        }
    
    try:
        # پارس داده‌های مالی
        parser = FinancialParser()
        
        valuator = CompanyValuation(symbol, financial_data)
        
        for scenario_name in ['خوشبینانه', 'خنثی', 'بدبینانه']:
            scenario_config = DCF_SCENARIOS.get(scenario_name, DCF_SCENARIOS['خنثی'])
            
            # ساخت پارامترهای کامل برای ارزش‌گذاری
            valuation_params = parser.build_valuation_inputs(financial_data, scenario_config)
            
            print(f"   سناریوی {scenario_name}...")
            try:
                valuation_result = valuator.comprehensive_valuation(
                    scenario_params=valuation_params,
                    scenario_name=scenario_name
                )
                results['valuation'][scenario_name] = valuation_result
            except Exception as e:
                print(f"   [!] خطا در سناریوی {scenario_name}: {str(e)[:50]}")
                results['valuation'][scenario_name] = {'weighted_average': 0}
    except Exception as e:
        print(f"   [!] خطا در ایجاد ارزش‌گذار: {str(e)[:50]}")
        for scenario_name in ['خوشبینانه', 'خنثی', 'بدبینانه']:
            results['valuation'][scenario_name] = {'weighted_average': 0}
    
    return results


def create_allocation_matrix(source_results: dict, target_results: dict):
    """
    ایجاد ماتریس تصمیم‌گیری 9 سناریو (3×3)
    """
    print(f"\n{'='*70}")
    print(f"Creating Allocation Matrix")
    print(f"{'='*70}")
    
    scenarios = ['خوشبینانه', 'خنثی', 'بدبینانه']
    matrix = []
    
    for source_symbol, source_data in source_results.items():
        for target_symbol, target_data in target_results.items():
            
            for source_scenario in scenarios:
                for target_scenario in scenarios:
                    
                    # ارزش‌گذاری منبع و هدف
                    source_val = source_data['valuation'].get(source_scenario, {})
                    target_val = target_data['valuation'].get(target_scenario, {})
                    
                    source_avg = source_val.get('weighted_average', 0)
                    target_avg = target_val.get('weighted_average', 0)
                    
                    # قیمت فعلی
                    source_price = source_data['price_data'].get('last_price', 1)
                    target_price = target_data['price_data'].get('last_price', 1)
                    
                    # محاسبه upside potential
                    source_upside = ((source_avg / source_price) - 1) * 100 if source_price > 0 else 0
                    target_upside = ((target_avg / target_price) - 1) * 100 if target_price > 0 else 0
                    
                    # تصمیم: اگر upside هدف بیشتر از منبع باشد -> تخصیص
                    decision = "تخصیص" if target_upside > source_upside else "نگهداری"
                    
                    # امتیاز (اختلاف upside)
                    score = target_upside - source_upside
                    
                    matrix.append({
                        'source': source_symbol,
                        'target': target_symbol,
                        'source_scenario': source_scenario,
                        'target_scenario': target_scenario,
                        'source_valuation': source_avg,
                        'source_price': source_price,
                        'source_upside': source_upside,
                        'target_valuation': target_avg,
                        'target_price': target_price,
                        'target_upside': target_upside,
                        'decision': decision,
                        'score': score
                    })
    
    return pd.DataFrame(matrix)


def generate_comprehensive_report(source_results: dict, target_results: dict, allocation_matrix: pd.DataFrame):
    """
    تولید گزارش جامع
    """
    print(f"\n{'='*70}")
    print(f"Generating Comprehensive Report")
    print(f"{'='*70}")
    
    generator = HTMLReportGenerator(output_dir='reports')
    
    # تاریخ
    today = jdatetime.date.today()
    today_str = f"{today.year}/{today.month}/{today.day}"
    
    # ایجاد HTML با همه صفحات...
    # (کد HTML طولانی است - در ادامه)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>گزارش تخصیص منابع</title>
    <style>{generator.executive_css}</style>
</head>
<body>
    <div class="page">
        <div class="executive-header">
            <h1>گزارش تحلیل تخصیص منابع</h1>
            <div class="subtitle">تحلیل بنیادی و ارزش‌گذاری ۹ نماد</div>
            <div class="meta">
                <span>تاریخ: {to_persian_digits(today_str)}</span>
                <span>سیستم بازارگردانی بهگزین</span>
            </div>
        </div>
        
        <div class="executive-summary">
            <div class="summary-title">🎯 هدف تحلیل</div>
            <p style="line-height: 2; margin-top: 15px;">
                بررسی امکان تخصیص منابع مالی از <strong>۳ نماد دارای مازاد نقدینگی</strong> 
                (زفجر، گکوثر، کاوه) به <strong>۶ نماد با فرصت سرمایه‌گذاری</strong>
                (رنیک، قشیر، زدشت، وسنا، کگاز، تلیسه) در <strong>۹ سناریوی مختلف</strong>.
            </p>
        </div>
"""
    
    # اضافه کردن جداول برای هر جفت
    page_num = 1
    for source_symbol in source_results.keys():
        for target_symbol in target_results.keys():
            pair_matrix = allocation_matrix[
                (allocation_matrix['source'] == source_symbol) & 
                (allocation_matrix['target'] == target_symbol)
            ]
            
            total_positive = len(pair_matrix[pair_matrix['decision'] == 'تخصیص'])
            confidence = (total_positive / 9 * 100) if len(pair_matrix) > 0 else 0
            
            html_content += f"""
        <div class="section">
            <h2>{source_symbol} ← {target_symbol}</h2>
            <p>اطمینان: {to_persian_digits(f'{confidence:.0f}%')} ({to_persian_digits(str(total_positive))}/۹)</p>
            <table class="data-table">
                <tr>
                    <th>سناریوی منبع</th>
                    <th>سناریوی هدف</th>
                    <th>پتانسیل منبع</th>
                    <th>پتانسیل هدف</th>
                    <th>تصمیم</th>
                </tr>
"""
            
            for _, row in pair_matrix.iterrows():
                html_content += f"""
                <tr>
                    <td>{row['source_scenario']}</td>
                    <td>{row['target_scenario']}</td>
                    <td>{to_persian_digits(format_percentage(row['source_upside']))}</td>
                    <td>{to_persian_digits(format_percentage(row['target_upside']))}</td>
                    <td>{'✅' if row['decision']=='تخصیص' else '❌'}</td>
                </tr>
"""
            
            html_content += """
            </table>
        </div>
"""
            page_num += 1
    
    html_content += """
    </div>
</body>
</html>
"""
    
    generator.save_report(html_content, 'summary_all_companies', generate_pdf=False)
    print(f"\n[OK] گزارش: reports/summary_all_companies.html")


def main():
    """اجرای تحلیل کامل"""
    print("\n" + "="*70)
    print("Complete Analysis with Valuation")
    print("="*70)
    
    # خواندن داده‌ها
    cache_dir = 'Data/PriceHistory'
    source_symbols = SYMBOLS['با_مازاد_منابع']
    target_symbols = SYMBOLS['با_کمبود_منابع']
    
    # نگاشت نمادهای فارسی به نام فولدر انگلیسی
    symbol_to_folder = {
        'زفجر': 'Zfajr',
        'کاوه': 'Kaveh',
        'گکوثر': 'Gkowthar',
        'رنیک': 'Renik',
        'قشیر': 'Qshir',
        'زدشت': 'Zdasht',
        'وسنا': 'Vsana',
        'کگاز': 'Kgaz',
        'تلیسه': 'Tliseh'
    }
    
    # استخراج داده‌های مالی
    print("\n[*] استخراج داده‌های مالی...")
    extractor = FinancialDataExtractor()
    financial_data_all = {}
    
    for symbol in source_symbols + target_symbols:
        try:
            folder_name = symbol_to_folder.get(symbol, symbol)
            folder_path = f'Data/{folder_name}'
            if os.path.exists(folder_path):
                data = extractor.extract_all_data(symbol, folder_path)
                financial_data_all[symbol] = data
                print(f"   ✓ {symbol}: OK")
            else:
                print(f"   ✗ {symbol}: No data folder ({folder_path})")
        except Exception as e:
            print(f"   ✗ {symbol}: {str(e)[:50]}")
            financial_data_all[symbol] = None
    
    price_data = {}
    for symbol in source_symbols + target_symbols:
        cache_file = os.path.join(cache_dir, f"{symbol}.csv")
        if os.path.exists(cache_file):
            price_data[symbol] = pd.read_csv(cache_file)
    
    # تحلیل
    source_results = {}
    for symbol in source_symbols:
        if symbol in price_data:
            fin_data = financial_data_all.get(symbol)
            source_results[symbol] = analyze_company(symbol, price_data[symbol], fin_data)
    
    target_results = {}
    for symbol in target_symbols:
        if symbol in price_data:
            fin_data = financial_data_all.get(symbol)
            target_results[symbol] = analyze_company(symbol, price_data[symbol], fin_data)
    
    # ماتریس
    allocation_matrix = create_allocation_matrix(source_results, target_results)
    allocation_matrix.to_csv('output/allocation_matrix.csv', index=False, encoding='utf-8-sig')
    
    # گزارش
    generate_comprehensive_report(source_results, target_results, allocation_matrix)
    
    print(f"\n{'='*70}")
    print(f"[OK] Analysis Complete!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
