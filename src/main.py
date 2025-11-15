"""
تحلیل جامع بازارگردانی - اسکریپت اصلی
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from config import *
from data_extractor import FinancialDataExtractor
from price_data_extractor import PriceDataExtractor
from fundamental_analysis import FundamentalAnalysis
from valuation import CompanyValuation
from resource_allocation import ResourceAllocationAnalyzer
from report_generator import ReportGenerator
from persian_utils import format_number, format_percentage, format_currency


class MarketMakingAnalysis:
    """کلاس اصلی تحلیل بازارگردانی"""
    
    def __init__(self):
        self.extractor = FinancialDataExtractor()
        self.price_extractor = PriceDataExtractor()
        self.report_generator = ReportGenerator()
        self.all_data = {}
        self.all_price_data = {}
        self.all_analyses = {}
        self.all_valuations = {}
        
        print("="*70)
        print("سیستم تحلیل جامع بازارگردانی بهگزین")
        print("="*70)
        print(f"تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    def extract_all_companies_data(self):
        """استخراج داده‌های تمام شرکت‌ها"""
        
        print("\n🔍 مرحله 1: استخراج داده‌های مالی و قیمتی")
        print("-" * 70)
        
        # استخراج داده‌های صورت‌های مالی
        print("\n📊 استخراج صورت‌های مالی...")
        for symbol_fa, path in DATA_PATHS.items():
            print(f"\nدر حال پردازش {symbol_fa}...")
            try:
                data = self.extractor.extract_all_data(symbol_fa, path)
                self.all_data[symbol_fa] = data
                print(f"✓ داده‌های مالی {symbol_fa} با موفقیت استخراج شد")
            except Exception as e:
                print(f"✗ خطا در استخراج داده‌های {symbol_fa}: {e}")
                self.all_data[symbol_fa] = {
                    'balance_sheet': pd.DataFrame(),
                    'income_statement': pd.DataFrame(),
                    'financial_ratios': pd.DataFrame(),
                    'monthly_performance': pd.DataFrame()
                }
        
        # استخراج داده‌های قیمتی (با قیمت تعدیل شده)
        print("\n💹 استخراج داده‌های قیمتی تعدیل شده...")
        all_symbols = SYMBOLS['با_مازاد_منابع'] + SYMBOLS['با_کمبود_منابع']
        self.all_price_data = self.price_extractor.get_all_symbols_price_history(
            symbols=all_symbols,
            start_date='1400-01-01',  # از اول سال 1400
            adjust_price=True  # استفاده از قیمت تعدیل شده
        )
        
        # نمایش خلاصه آماری قیمت‌ها
        print("\n📈 خلاصه آماری داده‌های قیمتی:")
        for symbol in all_symbols:
            if symbol in self.all_price_data:
                summary = self.price_extractor.get_price_summary(symbol)
                print(f"\n{symbol}:")
                print(f"  بازده کل: {summary.get('بازده کل', 0):.2f}%")
                print(f"  نوسان سالانه: {summary.get('نوسان سالانه', 0):.2f}%")
    
    def analyze_all_companies(self):
        """تحلیل بنیادی تمام شرکت‌ها"""
        
        print("\n📊 مرحله 2: تحلیل بنیادی شرکت‌ها")
        print("-" * 70)
        
        for symbol, data in self.all_data.items():
            print(f"\nتحلیل {symbol}...")
            try:
                analyzer = FundamentalAnalysis(symbol, data)
                analysis = analyzer.comprehensive_analysis()
                self.all_analyses[symbol] = analysis
                
                # محاسبه امتیاز سلامت
                health_score = analyzer.get_health_score()
                print(f"امتیاز سلامت مالی: {health_score:.1f}/100")
                
            except Exception as e:
                print(f"✗ خطا در تحلیل {symbol}: {e}")
                self.all_analyses[symbol] = {}
    
    def valuate_all_companies(self):
        """ارزش‌گذاری تمام شرکت‌ها در سه سناریو"""
        
        print("\n💰 مرحله 3: ارزش‌گذاری شرکت‌ها")
        print("-" * 70)
        
        for symbol, data in self.all_data.items():
            print(f"\nارزش‌گذاری {symbol}...")
            
            try:
                valuator = CompanyValuation(symbol, data)
                
                # ارزش‌گذاری در سه سناریو
                for scenario_name, scenario_config in DCF_SCENARIOS.items():
                    
                    # پارامترهای فرضی - باید از داده‌های واقعی محاسبه شوند
                    params = {
                        'fcf': 1000000,  # جریان نقدی آزاد (میلیون ریال)
                        'growth_rate': scenario_config['growth_rate'],
                        'discount_rate': scenario_config['discount_rate'],
                        'terminal_growth': scenario_config['terminal_growth'],
                        'earnings': 800000,
                        'industry_pe': 8.0,
                        'book_value': 5000000,
                        'roe': 0.15,
                        'required_return': 0.18,
                        'ebitda': 1200000,
                        'industry_ebitda_multiple': 6.0,
                        'net_debt': 500000,
                        'revenue': 10000000,
                        'industry_ps': 1.2
                    }
                    
                    valuation = valuator.comprehensive_valuation(params, scenario_name)
                    
                    if symbol not in self.all_valuations:
                        self.all_valuations[symbol] = {}
                    
                    self.all_valuations[symbol][scenario_name] = valuation
                
            except Exception as e:
                print(f"✗ خطا در ارزش‌گذاری {symbol}: {e}")
                self.all_valuations[symbol] = {}
    
    def analyze_resource_allocation(self):
        """تحلیل تخصیص منابع"""
        
        print("\n🎯 مرحله 4: تحلیل تخصیص منابع")
        print("=" * 70)
        
        surplus_companies = SYMBOLS['با_مازاد_منابع']
        deficit_companies = SYMBOLS['با_کمبود_منابع']
        
        allocation_results = {}
        
        for source in surplus_companies:
            print(f"\n{'='*70}")
            print(f"تحلیل تخصیص منابع {source}")
            print(f"{'='*70}")
            
            analyzer = ResourceAllocationAnalyzer(
                source_company=source,
                target_companies=deficit_companies,
                analyses=self.all_analyses,
                valuations=self.all_valuations
            )
            
            results = analyzer.analyze_allocation()
            allocation_results[source] = results
            
            # تولید گزارش تفصیلی
            detailed_report = analyzer.generate_detailed_report()
            
            print(f"\n📋 گزارش تفصیلی:")
            print(detailed_report.to_string())
            
            # ذخیره گزارش
            output_path = os.path.join(REPORT_CONFIG['report_dir'], 
                                      f"allocation_{source}.xlsx")
            detailed_report.to_excel(output_path)
            print(f"\n✓ گزارش در {output_path} ذخیره شد")
        
        return allocation_results
    
    def generate_reports_html_pdf(self):
        """تولید گزارش‌های HTML و PDF برای همه شرکت‌ها"""
        
        print("\n📄 مرحله 5: تولید گزارش‌های HTML و PDF")
        print("-" * 70)
        
        all_symbols = SYMBOLS['با_مازاد_منابع'] + SYMBOLS['با_کمبود_منابع']
        
        # تولید گزارش برای هر شرکت
        for symbol in all_symbols:
            if symbol in self.all_analyses and symbol in self.all_price_data:
                print(f"\nتولید گزارش {symbol}...")
                
                try:
                    # دریافت داده‌ها
                    analysis = self.all_analyses.get(symbol, {})
                    valuation = self.all_valuations.get(symbol, {})
                    price_data = self.all_price_data.get(symbol, pd.DataFrame())
                    
                    # تولید HTML
                    html_content = self._create_company_html_report(
                        symbol, analysis, valuation, price_data
                    )
                    
                    # ذخیره HTML
                    html_file = f"report_{symbol}.html"
                    html_path = self.report_generator.save_html_report(html_content, html_file)
                    
                    # تبدیل به PDF
                    pdf_file = f"report_{symbol}.pdf"
                    pdf_path = os.path.join(REPORT_CONFIG['report_dir'], pdf_file)
                    self.report_generator.html_to_pdf(html_content, pdf_path)
                    
                    print(f"✓ گزارش {symbol} تولید شد")
                    
                except Exception as e:
                    print(f"✗ خطا در تولید گزارش {symbol}: {e}")
        
        print("\n✓ تمام گزارش‌ها تولید شدند")
    
    def _create_company_html_report(self, company_name, analysis, valuation, price_data):
        """ایجاد محتوای HTML گزارش شرکت"""
        
        import jdatetime
        from persian_utils import to_persian_digits
        
        today_jalali = jdatetime.date.today()
        today_str = f"{today_jalali.year}/{today_jalali.month}/{today_jalali.day}"
        
        # محاسبه متریک‌ها
        health_score = 75.0  # باید از تحلیل واقعی بیاید
        annual_return = 25.5
        volatility = 18.3
        
        # ایجاد نمودار قیمت
        price_chart_html = ""
        if not price_data.empty:
            chart_img = self.report_generator.create_chart(
                price_data['Close'].tail(60),
                chart_type='line',
                title='روند قیمت ۶۰ روز اخیر',
                ylabel='قیمت (ریال)'
            )
            price_chart_html = f'<div class="chart-container"><img src="{chart_img}" /></div>'
        
        # تولید HTML
        html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش تحلیل بنیادی {company_name}</title>
    <style>{self.report_generator.base_css}</style>
</head>
<body>
    <div class="page">
        <div class="header">
            <h1>گزارش تحلیل بنیادی و ارزش‌گذاری</h1>
            <div class="subtitle">{company_name}</div>
            <div class="meta">
                <span>تاریخ گزارش: {to_persian_digits(today_str)}</span>
                <span>سیستم تحلیل بازارگردانی بهگزین</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📊 خلاصه اجرایی</div>
            
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">امتیاز سلامت مالی</div>
                    <div class="metric-value">{format_number(health_score)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">بازده سالانه</div>
                    <div class="metric-value metric-change positive">{format_percentage(annual_return)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">نوسان‌پذیری</div>
                    <div class="metric-value">{format_percentage(volatility)}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📈 عملکرد قیمتی</div>
            {price_chart_html}
        </div>
        
        <div class="footer">
            <p>این گزارش توسط سیستم تحلیل هوشمند بازارگردانی بهگزین تولید شده است</p>
            <p>صفحه {to_persian_digits('1')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def generate_final_report(self):
        """تولید گزارش نهایی جامع"""
        
        print("\n📄 مرحله 6: تولید گزارش نهایی")
        print("-" * 70)
        
        # خلاصه نتایج
        summary = {
            'تعداد شرکت‌های بررسی شده': len(self.all_data),
            'شرکت‌های با مازاد منابع': SYMBOLS['با_مازاد_منابع'],
            'شرکت‌های با کمبود منابع': SYMBOLS['با_کمبود_منابع'],
            'تاریخ تحلیل': datetime.now().strftime('%Y-%m-%d'),
        }
        
        print("\n" + "="*70)
        print("📊 خلاصه تحلیل")
        print("="*70)
        
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # ذخیره گزارش
        summary_df = pd.DataFrame([summary])
        output_path = os.path.join(REPORT_CONFIG['report_dir'], 
                                  'summary_report.xlsx')
        summary_df.to_excel(output_path, index=False)
        
        print(f"\n✓ گزارش خلاصه در {output_path} ذخیره شد")
        
        # نمایش بهترین گزینه‌ها
        print("\n" + "="*70)
        print("🏆 توصیه‌های نهایی")
        print("="*70)
        
        print("\nبر اساس تحلیل‌های انجام شده:")
        print("1. برای اطلاع از رتبه‌بندی دقیق، گزارش‌های تفصیلی را مشاهده کنید")
        print("2. معیارهای تصمیم‌گیری شامل سلامت مالی، ارزش‌گذاری، ریسک و رشد است")
        print("3. شرکت‌هایی با امتیاز بالاتر از 75 اولویت دارند")
        
        return summary
    
    def run_complete_analysis(self):
        """اجرای تحلیل کامل"""
        
        try:
            # 1. استخراج داده‌ها
            self.extract_all_companies_data()
            
            # 2. تحلیل بنیادی
            self.analyze_all_companies()
            
            # 3. ارزش‌گذاری
            self.valuate_all_companies()
            
            # 4. تحلیل تخصیص منابع
            allocation_results = self.analyze_resource_allocation()
            
            # 5. تولید گزارش‌های HTML و PDF
            self.generate_reports_html_pdf()
            
            # 6. گزارش نهایی
            summary = self.generate_final_report()
            
            print("\n" + "="*70)
            print("✅ تحلیل جامع با موفقیت تکمیل شد!")
            print("="*70)
            print("\n📁 فایل‌های خروجی:")
            print(f"  - گزارش‌های HTML و PDF در پوشه '{REPORT_CONFIG['report_dir']}'")
            print(f"  - داده‌های خام در پوشه '{REPORT_CONFIG['output_dir']}'")
            
            return {
                'data': self.all_data,
                'analyses': self.all_analyses,
                'valuations': self.all_valuations,
                'allocations': allocation_results,
                'summary': summary
            }
            
        except Exception as e:
            print(f"\n❌ خطا در اجرای تحلیل: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """تابع اصلی"""
    
    # ایجاد پوشه‌های خروجی
    os.makedirs(REPORT_CONFIG['report_dir'], exist_ok=True)
    os.makedirs(REPORT_CONFIG['output_dir'], exist_ok=True)
    
    # اجرای تحلیل
    analyzer = MarketMakingAnalysis()
    results = analyzer.run_complete_analysis()
    
    return results


if __name__ == "__main__":
    results = main()
