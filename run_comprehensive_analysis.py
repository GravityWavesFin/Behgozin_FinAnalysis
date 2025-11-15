"""
اجرای تحلیل جامع: بنیادی + تکنیکال + پیش‌بینی 3 ماهه + تخصیص منابع
"""

import sys
sys.path.append('src')

import pandas as pd
import numpy as np
from config import SYMBOLS, DCF_SCENARIOS
from price_data_extractor import PriceDataExtractor
from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser
from comprehensive_analysis import ComprehensiveAnalysis
from valuation import CompanyValuation
from report_generator_html import HTMLReportGenerator
from persian_utils import format_number, format_percentage
import os


def analyze_company_comprehensive(symbol: str, symbol_en: str, data_folder: str):
    """تحلیل کامل یک شرکت با همه جزئیات"""
    
    print(f"\n{'='*70}")
    print(f"🔍 تحلیل جامع {symbol}")
    print(f"{'='*70}")
    
    results = {
        'symbol': symbol,
        'symbol_en': symbol_en,
        'analysis': {},
        'valuations': {},
        'predictions': {}
    }
    
    try:
        # 1. خواندن داده قیمت (فقط از کش)
        cache_path = r"E:\Shakour\BehgozinProjects\Behgozin_FinAnalysis\Data\PriceHistory\{}.csv".format(symbol)
        
        if not os.path.exists(cache_path):
            print(f"   ❌ داده قیمتی موجود نیست: {cache_path}")
            return None
        
        price_df = pd.read_csv(cache_path, index_col=0, parse_dates=True, encoding='utf-8-sig')
        
        if price_df.empty:
            print(f"   ❌ فایل کش خالی است")
            return None
        
        print(f"   📂 کش خوانده شد: {len(price_df)} روز")
        
        # استفاده از قیمت تعدیل شده
        current_price = price_df['Adj Close'].iloc[-1]
        print(f"   💰 قیمت تعدیل شده فعلی: {format_number(current_price)} ریال")
        
        # 2. استخراج داده‌های مالی
        extractor = FinancialDataExtractor()
        parser = FinancialParser()
        
        # پیدا کردن فایل‌های مالی
        if not os.path.exists(data_folder):
            print(f"   ⚠️  پوشه داده مالی موجود نیست")
            financial_data = {}
        else:
            files = os.listdir(data_folder)
            
            # سود و زیان
            income_files = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
            if income_files:
                file_path = os.path.join(data_folder, income_files[0])
                soup = extractor.read_mhtml_file(file_path)
                income_df = extractor.extract_table_with_bs4(soup)
                income_parsed = parser.parse_income_statement(income_df)
            else:
                income_parsed = {}
            
            # ترازنامه
            balance_files = [f for f in files if 'ترازنامه' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
            if balance_files:
                file_path = os.path.join(data_folder, balance_files[0])
                soup = extractor.read_mhtml_file(file_path)
                balance_df = extractor.extract_table_with_bs4(soup)
                balance_parsed = parser.parse_balance_sheet(balance_df)
            else:
                balance_parsed = {}
            
            # ترکیب داده‌ها
            financial_data = {**income_parsed, **balance_parsed}
        
        print(f"   📊 داده‌های مالی: {len(financial_data)} متریک")
        
        # 3. ارزش‌گذاری در 3 سناریو
        print(f"\n   💎 ارزش‌گذاری:")
        
        valuations = {}
        for scenario_name in ['خوشبینانه', 'خنثی', 'بدبینانه']:
            scenario_config = DCF_SCENARIOS.get(scenario_name, DCF_SCENARIOS['خنثی'])
            
            # ساخت پارامترهای ارزش‌گذاری
            valuation_params = parser.build_valuation_inputs(
                {'income_statement': income_df if 'income_df' in locals() else pd.DataFrame(),
                 'balance_sheet': balance_df if 'balance_df' in locals() else pd.DataFrame()},
                scenario_config
            )
            
            valuator = CompanyValuation(symbol, {'income_statement': pd.DataFrame()})
            valuation_result = valuator.comprehensive_valuation(
                valuation_params,
                scenario_name
            )
            
            # ذخیره هم میانگین وزنی و هم جزئیات هر روش
            valuations[scenario_name] = {
                'weighted_average': valuation_result['weighted_average'],
                'methods': {
                    'dcf': valuation_result.get('dcf', {}).get('enterprise_value', 0),
                    'pe': valuation_result.get('pe', {}).get('equity_value', 0),
                    'pb': valuation_result.get('pb', {}).get('equity_value', 0),
                    'ev_ebitda': valuation_result.get('ev_ebitda', {}).get('equity_value', 0),
                    'ps': valuation_result.get('ps', {}).get('equity_value', 0),
                    'rim': valuation_result.get('rim', {}).get('equity_value', 0)
                }
            }
            print(f"      {scenario_name}: {format_number(valuation_result['weighted_average'])} میلیون")
        
        # استفاده از سناریو خنثی برای تحلیل
        base_valuation = valuations['خنثی']['weighted_average']
        
        # محاسبه ارزش هر سهم
        shares_outstanding = financial_data.get('shares_outstanding', 0)
        valuations_per_share = {}
        
        if shares_outstanding > 0:
            print(f"\n   📊 تعداد سهام: {format_number(shares_outstanding)} سهم")
            print(f"   💰 ارزش هر سهم:")
            for scenario_name, scenario_data in valuations.items():
                # تبدیل از میلیون ریال به ریال و تقسیم بر تعداد سهام
                total_value = scenario_data['weighted_average']
                value_per_share = (total_value * 1_000_000) / shares_outstanding
                
                # محاسبه هر روش به ازای هر سهم
                methods_per_share = {}
                for method_name, method_value in scenario_data['methods'].items():
                    methods_per_share[method_name] = (method_value * 1_000_000) / shares_outstanding if method_value > 0 else 0
                
                valuations_per_share[scenario_name] = {
                    'weighted_average': value_per_share,
                    'methods': methods_per_share
                }
                print(f"      {scenario_name}: {format_number(value_per_share)} ریال/سهم")
        else:
            print(f"\n   ⚠️  تعداد سهام در دسترس نیست")
            valuations_per_share = {k: {'weighted_average': 0, 'methods': {}} for k in valuations.keys()}
        
        # 4. تحلیل جامع (بنیادی + تکنیکال + پیش‌بینی)
        print(f"\n   🎯 تحلیل جامع:")
        
        analyzer = ComprehensiveAnalysis(symbol)
        # استفاده از ارزش هر سهم (نه ارزش کل شرکت) برای پیش‌بینی
        intrinsic_value_per_share = valuations_per_share.get('خنثی', {}).get('weighted_average', base_valuation)
        comprehensive = analyzer.comprehensive_analysis(
            financial_data,
            price_df,
            current_price,
            intrinsic_value_per_share
        )
        
        results['analysis'] = comprehensive
        results['valuations'] = valuations
        results['valuations_per_share'] = valuations_per_share
        results['shares_outstanding'] = shares_outstanding
        
        # نمایش خلاصه
        fund = comprehensive['fundamentals']
        tech = comprehensive['technical']
        pred = comprehensive['prediction']
        
        print(f"\n   📈 نتایج تحلیل:")
        print(f"      بنیادی: {fund['score']}/100 (رتبه: {fund['grade']})")
        print(f"      تکنیکال: {tech['momentum_score']}/100 (روند: {tech['trend']})")
        print(f"      امتیاز کلی: {comprehensive['overall_score']:.1f}/100")
        print(f"      توصیه: {comprehensive['recommendation']}")
        
        print(f"\n   🎯 پیش‌بینی 3 ماهه:")
        print(f"      قیمت فعلی: {format_number(pred['current_price'])}")
        print(f"      قیمت هدف: {format_number(pred['target_3month'])}")
        print(f"      بازده مورد انتظار: {pred['expected_return_3month']:.2f}%")
        print(f"      سطح اطمینان: {pred['confidence']}")
        print(f"      سطح ریسک: {pred['risk_level']}")
        
        return results
        
    except Exception as e:
        print(f"   ❌ خطا: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def create_allocation_matrix(all_results: dict):
    """مقایسه دو گزینه برای سرمایه‌گذاری پول نقد اضافی"""
    
    print(f"\n{'='*70}")
    print("امکان‌سنجی سرمایه‌گذاری پول نقد اضافی")
    print(f"{'='*70}")
    
    # گزینه 1: سرمایه‌گذاری در 3 نماد
    option_3 = ['زفجر', 'کاوه', 'گکوثر']
    # گزینه 2: سرمایه‌گذاری در 6 نماد
    option_6 = ['رنیک', 'قشیر', 'زدشت', 'وسنا', 'کگاز', 'تلیسه']
    
    print(f"\nگزینه 1: سرمایه‌گذاری در 3 نماد → {', '.join(option_3)}")
    print(f"گزینه 2: سرمایه‌گذاری در 6 نماد → {', '.join(option_6)}")
    print(f"\nسوال: پول نقد اضافی را کجا سرمایه‌گذاری کنیم؟")
    
    # مقایسه تک‌به‌تک (18 حالت: 3×6)
    print(f"\n{'='*70}")
    print("مقایسه‌های تک‌به‌تک")
    print(f"{'='*70}")
    
    comparisons = []
    
    for source in option_3:
        if source not in all_results or not all_results[source]:
            continue
        
        source_data = all_results[source]
        source_pred = source_data['analysis']['prediction']
        source_fund = source_data['analysis']['fundamentals']
        source_tech = source_data['analysis']['technical']
        
        print(f"\n▶ به جای {source}:")
        
        for target in option_6:
            if target not in all_results or not all_results[target]:
                continue
            
            target_data = all_results[target]
            target_pred = target_data['analysis']['prediction']
            target_fund = target_data['analysis']['fundamentals']
            target_tech = target_data['analysis']['technical']
            
            # محاسبه اختلاف‌ها
            return_diff = target_pred['expected_return_3month'] - source_pred['expected_return_3month']
            fund_diff = target_fund['score'] - source_fund['score']
            tech_diff = target_tech['momentum_score'] - source_tech['momentum_score']
            overall_diff = target_data['analysis']['overall_score'] - source_data['analysis']['overall_score']
            
            # تصمیم‌گیری
            if return_diff > 5 and overall_diff > 5:
                decision = f"✅ {target} بهتر"
                reason = f"بازده {return_diff:+.1f}% و امتیاز {overall_diff:+.1f} بیشتر"
            elif return_diff < -5 and overall_diff < -5:
                decision = f"❌ {source} بهتر"
                reason = f"{source} برتری دارد"
            else:
                decision = "⚖️ تقریباً برابر"
                reason = "تفاوت معنادار نیست"
            
            comparisons.append({
                'نماد_منبع': source,
                'نماد_هدف': target,
                'بازده_منبع_%': round(source_pred['expected_return_3month'], 2),
                'بازده_هدف_%': round(target_pred['expected_return_3month'], 2),
                'اختلاف_بازده_%': round(return_diff, 2),
                'امتیاز_بنیادی_منبع': source_fund['score'],
                'امتیاز_بنیادی_هدف': target_fund['score'],
                'امتیاز_تکنیکال_منبع': source_tech['momentum_score'],
                'امتیاز_تکنیکال_هدف': target_tech['momentum_score'],
                'امتیاز_کلی_منبع': source_data['analysis']['overall_score'],
                'امتیاز_کلی_هدف': target_data['analysis']['overall_score'],
                'تصمیم': decision,
                'توضیح': reason
            })
            
            print(f"  • {target}: {decision} - {reason}")
    
    # ذخیره مقایسه‌ها
    df_comparisons = pd.DataFrame(comparisons)
    df_comparisons.to_csv('output/detailed_comparisons.csv', index=False, encoding='utf-8-sig')
    
    # محاسبه متوسط برای گزینه 1 (3 نماد)
    option3_data = []
    for symbol in option_3:
        if symbol in all_results and all_results[symbol]:
            pred = all_results[symbol]['analysis']['prediction']
            analysis = all_results[symbol]['analysis']
            option3_data.append({
                'symbol': symbol,
                'return': pred['expected_return_3month'],
                'score': analysis['overall_score'],
                'confidence': pred['confidence']
            })
    
    # محاسبه متوسط برای گزینه 2 (6 نماد)
    option6_data = []
    for symbol in option_6:
        if symbol in all_results and all_results[symbol]:
            pred = all_results[symbol]['analysis']['prediction']
            analysis = all_results[symbol]['analysis']
            option6_data.append({
                'symbol': symbol,
                'return': pred['expected_return_3month'],
                'score': analysis['overall_score'],
                'confidence': pred['confidence']
            })
    
    # میانگین‌ها
    avg_opt3_return = np.mean([d['return'] for d in option3_data]) if option3_data else 0
    avg_opt6_return = np.mean([d['return'] for d in option6_data]) if option6_data else 0
    
    avg_opt3_score = np.mean([d['score'] for d in option3_data]) if option3_data else 0
    avg_opt6_score = np.mean([d['score'] for d in option6_data]) if option6_data else 0
    
    # نتیجه‌گیری
    print(f"\n{'='*70}")
    print("نتیجه‌گیری نهایی")
    print(f"{'='*70}")
    
    print(f"\nگزینه 1: سرمایه‌گذاری در 3 نماد (زفجر، کاوه، گکوثر)")
    print(f"  میانگین بازده 3 ماهه: {avg_opt3_return:.2f}%")
    print(f"  میانگین امتیاز کلی: {avg_opt3_score:.1f}/100")
    
    print(f"\nگزینه 2: سرمایه‌گذاری در 6 نماد (رنیک، قشیر، زدشت، وسنا، کگاز، تلیسه)")
    print(f"  میانگین بازده 3 ماهه: {avg_opt6_return:.2f}%")
    print(f"  میانگین امتیاز کلی: {avg_opt6_score:.1f}/100")
    
    # تصمیم
    diff = avg_opt6_return - avg_opt3_return
    print(f"\nاختلاف بازده: {diff:+.2f}%")
    
    print(f"\n{'='*70}")
    if diff > 3:
        print("توصیه: گزینه 2 (6 نماد)")
        print("دلیل: بازده بهتر")
    elif diff < -3:
        print("توصیه: گزینه 1 (3 نماد)")
        print("دلیل: بازده بهتر")
    else:
        print("توصیه: تفاوت معنادار نیست - هر دو گزینه مشابه")
        print("دلیل: می‌توانید ترکیبی از هر دو را انتخاب کنید")
    print(f"{'='*70}")
    
    # ذخیره جزئیات
    summary = {
        'گزینه_1': {
            'نمادها': option_3,
            'میانگین_بازده': round(avg_opt3_return, 2),
            'میانگین_امتیاز': round(avg_opt3_score, 1),
            'جزئیات': option3_data
        },
        'گزینه_2': {
            'نمادها': option_6,
            'میانگین_بازده': round(avg_opt6_return, 2),
            'میانگین_امتیاز': round(avg_opt6_score, 1),
            'جزئیات': option6_data
        },
        'اختلاف_بازده': round(diff, 2)
    }
    
    output_file = 'output/cash_allocation_decision.json'
    os.makedirs('output', exist_ok=True)
    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\nگزارش ذخیره شد: {output_file}")
    print(f"مقایسه‌های تک‌به‌تک: output/detailed_comparisons.csv")
    
    # خلاصه بهترین جایگزین‌ها
    print(f"\n{'='*70}")
    print("بهترین جایگزین‌ها")
    print(f"{'='*70}")
    
    best = df_comparisons[df_comparisons['تصمیم'].str.contains('بهتر', na=False)]
    if len(best) > 0:
        best = best.nlargest(5, 'اختلاف_بازده_%')
        for i, idx in enumerate(best.index, 1):
            row = best.loc[idx]
            print(f"{i}. {row['نماد_هدف']} به جای {row['نماد_منبع']}: {row['اختلاف_بازده_%']:+.2f}%")
    else:
        print("هیچ جایگزین برتری یافت نشد")
    
    return summary


def main():
    """اجرای تحلیل جامع برای همه شرکت‌ها"""
    
    # تنظیم encoding برای Windows
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("="*70)
    print("تحلیل جامع: بنیادی + تکنیکال + پیش‌بینی 3 ماهه")
    print("="*70)
    print("\nسوال: پول نقد اضافی را کجا سرمایه‌گذاری کنیم؟")
    print("گزینه 1: زفجر، کاوه، گکوثر (3 نماد)")
    print("گزینه 2: رنیک، قشیر، زدشت، وسنا، کگاز، تلیسه (6 نماد)\n")
    
    all_results = {}
    
    # تحلیل همه 9 نماد (برای تحلیل بنیادی و تکنیکال)
    from config import SYMBOL_NAMES_EN
    
    for symbol, symbol_en in SYMBOL_NAMES_EN.items():
        data_folder = f"Data/{symbol_en}"
        result = analyze_company_comprehensive(symbol, symbol_en, data_folder)
        if result:
            all_results[symbol] = result
    
    # ماتریس تخصیص
    if all_results:
        allocation_df = create_allocation_matrix(all_results)
        
        # ذخیره نتایج کامل
        import json
        
        def convert_to_serializable(obj):
            """تبدیل اعداد numpy به Python native"""
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(i) for i in obj]
            elif hasattr(obj, 'item'):  # numpy types
                return obj.item()
            elif isinstance(obj, (np.int64, np.int32, np.float64, np.float32)):
                return float(obj)
            return obj
        
        with open('output/comprehensive_analysis.json', 'w', encoding='utf-8') as f:
            # حذف DataFrame ها برای JSON
            json_results = {}
            for symbol, data in all_results.items():
                json_results[symbol] = {
                    'symbol': data['symbol'],
                    'analysis': convert_to_serializable(data['analysis']),
                    'valuations': convert_to_serializable(data['valuations']),
                    'valuations_per_share': convert_to_serializable(data.get('valuations_per_share', {})),
                    'shares_outstanding': convert_to_serializable(data.get('shares_outstanding', 0))
                }
            json.dump(json_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ نتایج کامل ذخیره شد: output/comprehensive_analysis.json")
    
    print(f"\n{'='*70}")
    print("✅ تحلیل کامل به پایان رسید")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
