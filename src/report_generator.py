"""
تولید گزارش‌های HTML و PDF حرفه‌ای با فونت فارسی
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime
import jdatetime
from jinja2 import Template
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Import matplotlib برای نمودارها
import matplotlib
matplotlib.use('Agg')  # برای ذخیره بدون نمایش
import matplotlib.pyplot as plt
import seaborn as sns

# تنظیم فونت فارسی
plt.rcParams['font.family'] = 'Tahoma'
plt.rcParams['axes.unicode_minus'] = False

from persian_utils import format_number, format_percentage, format_currency, to_persian_digits


class ReportGenerator:
    """کلاس تولید گزارش‌های HTML و PDF"""
    
    def __init__(self, output_dir: str = 'reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # قالب CSS برای A4
        self.base_css = """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Tahoma', 'Arial', sans-serif;
            direction: rtl;
            text-align: right;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }
        
        .page {
            width: 21cm;
            min-height: 29.7cm;
            padding: 2cm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            page-break-after: always;
        }
        
        .page:last-child {
            page-break-after: avoid;
        }
        
        .header {
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 28px;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .header .subtitle {
            color: #7f8c8d;
            font-size: 16px;
            text-align: center;
        }
        
        .header .meta {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 14px;
            color: #95a5a6;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 20px;
            font-weight: bold;
        }
        
        .card {
            background: #f8f9fa;
            border-right: 4px solid #3498db;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        
        .card-title {
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        table th {
            padding: 12px;
            text-align: right;
            font-weight: bold;
        }
        
        table td {
            padding: 10px 12px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        table tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        table tbody tr:hover {
            background-color: #e8f4f8;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: white;
            border: 2px solid #ecf0f1;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .metric-value {
            color: #2c3e50;
            font-size: 28px;
            font-weight: bold;
        }
        
        .metric-change {
            font-size: 14px;
            margin-top: 5px;
        }
        
        .metric-change.positive {
            color: #27ae60;
        }
        
        .metric-change.negative {
            color: #e74c3c;
        }
        
        .chart-container {
            margin: 30px 0;
            text-align: center;
        }
        
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background-color: #d4edda;
            border-right: 4px solid #28a745;
            color: #155724;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            border-right: 4px solid #ffc107;
            color: #856404;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            border-right: 4px solid #dc3545;
            color: #721c24;
        }
        
        .alert-info {
            background-color: #d1ecf1;
            border-right: 4px solid #17a2b8;
            color: #0c5460;
        }
        
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            text-align: center;
            color: #95a5a6;
            font-size: 12px;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin: 0 5px;
        }
        
        .badge-success {
            background-color: #28a745;
            color: white;
        }
        
        .badge-warning {
            background-color: #ffc107;
            color: #333;
        }
        
        .badge-danger {
            background-color: #dc3545;
            color: white;
        }
        
        .score-bar {
            height: 30px;
            background: #ecf0f1;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }
        
        .score-fill {
            height: 100%;
            background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #27ae60 100%);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        @media print {
            body {
                background: white;
            }
            .page {
                box-shadow: none;
                margin: 0;
                padding: 1cm;
            }
            .metric-card:hover {
                transform: none;
            }
        }
        """
    
    def create_chart(self, data, chart_type='line', title='', xlabel='', ylabel='', figsize=(12, 6)):
        """ایجاد نمودار و تبدیل به base64"""
        fig, ax = plt.subplots(figsize=figsize)
        
        if chart_type == 'line':
            ax.plot(data.index, data.values, linewidth=2, marker='o')
        elif chart_type == 'bar':
            ax.bar(range(len(data)), data.values)
            ax.set_xticks(range(len(data)))
            ax.set_xticklabels(data.index, rotation=45, ha='right')
        elif chart_type == 'pie':
            ax.pie(data.values, labels=data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # تبدیل به base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def generate_company_report(self, company_name, analysis_data, valuation_data, price_data):
        """تولید گزارش کامل یک شرکت"""
        
        today_jalali = jdatetime.date.today()
        today_str = f"{today_jalali.year}/{today_jalali.month}/{today_jalali.day}"
        
        html_template = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش تحلیل بنیادی {{{{ company_name }}}}</title>
    <style>
        {self.base_css}
    </style>
</head>
<body>
    <!-- صفحه اول: خلاصه اجرایی -->
    <div class="page">
        <div class="header">
            <h1>گزارش تحلیل بنیادی و ارزش‌گذاری</h1>
            <div class="subtitle">{{{{ company_name }}}}</div>
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
                    <div class="metric-value">{{{{ health_score }}}}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">بازده سالانه</div>
                    <div class="metric-value {{{{ return_class }}}}">{{{{ annual_return }}}}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">نوسان‌پذیری</div>
                    <div class="metric-value">{{{{ volatility }}}}</div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">🎯 توصیه سرمایه‌گذاری</div>
                <div class="alert {{{{ recommendation_class }}}}">
                    <strong>{{{{ recommendation }}}}</strong>
                    <p>{{{{ recommendation_text }}}}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📈 عملکرد قیمتی</div>
            {{{{ price_chart }}}}
        </div>
        
        <div class="footer">
            <p>این گزارش توسط سیستم تحلیل هوشمند بازارگردانی بهگزین تولید شده است</p>
            <p>صفحه ۱</p>
        </div>
    </div>
    
    <!-- صفحه دوم: نسبت‌های مالی -->
    <div class="page">
        <div class="header">
            <h1>تحلیل نسبت‌های مالی</h1>
            <div class="subtitle">{{{{ company_name }}}}</div>
        </div>
        
        <div class="section">
            <div class="section-title">💰 نسبت‌های سودآوری</div>
            <table>
                <thead>
                    <tr>
                        <th>نسبت مالی</th>
                        <th>مقدار</th>
                        <th>وضعیت</th>
                        <th>توضیحات</th>
                    </tr>
                </thead>
                <tbody>
                    {{{{ profitability_rows }}}}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">🌊 نسبت‌های نقدینگی</div>
            <table>
                <thead>
                    <tr>
                        <th>نسبت مالی</th>
                        <th>مقدار</th>
                        <th>وضعیت</th>
                        <th>توضیحات</th>
                    </tr>
                </thead>
                <tbody>
                    {{{{ liquidity_rows }}}}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>صفحه ۲</p>
        </div>
    </div>
    
    <!-- صفحه سوم: ارزش‌گذاری -->
    <div class="page">
        <div class="header">
            <h1>ارزش‌گذاری در سناریوهای مختلف</h1>
            <div class="subtitle">{{{{ company_name }}}}</div>
        </div>
        
        <div class="section">
            <div class="section-title">💎 نتایج ارزش‌گذاری</div>
            {{{{ valuation_chart }}}}
            
            <table>
                <thead>
                    <tr>
                        <th>روش ارزش‌گذاری</th>
                        <th>سناریوی خوشبینانه</th>
                        <th>سناریوی خنثی</th>
                        <th>سناریوی بدبینانه</th>
                    </tr>
                </thead>
                <tbody>
                    {{{{ valuation_rows }}}}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>صفحه ۳</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template
    
    def generate_allocation_report(self, source_company, target_companies, allocation_results):
        """تولید گزارش تخصیص منابع"""
        
        today_jalali = jdatetime.date.today()
        today_str = f"{today_jalali.year}/{today_jalali.month}/{today_jalali.day}"
        
        html_template = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش تحلیل تخصیص منابع - {{{{ source_company }}}}</title>
    <style>
        {self.base_css}
    </style>
</head>
<body>
    <div class="page">
        <div class="header">
            <h1>گزارش تحلیل تخصیص منابع</h1>
            <div class="subtitle">از {{{{ source_company }}}} به نمادهای هدف</div>
            <div class="meta">
                <span>تاریخ گزارش: {to_persian_digits(today_str)}</span>
                <span>سیستم تحلیل بازارگردانی بهگزین</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">🎯 رتبه‌بندی نمادهای هدف</div>
            {{{{ ranking_chart }}}}
            
            <table>
                <thead>
                    <tr>
                        <th>رتبه</th>
                        <th>نماد</th>
                        <th>امتیاز کل</th>
                        <th>سلامت مالی</th>
                        <th>ارزش‌گذاری</th>
                        <th>ریسک</th>
                        <th>رشد</th>
                        <th>توصیه</th>
                    </tr>
                </thead>
                <tbody>
                    {{{{ ranking_rows }}}}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>صفحه ۱</p>
        </div>
    </div>
    
    <!-- صفحات بعدی: تحلیل تک به تک -->
    {{{{ detailed_pages }}}}
</body>
</html>
        """
        
        return html_template
    
    def html_to_pdf(self, html_content, output_path):
        """تبدیل HTML به PDF با استفاده از xhtml2pdf"""
        try:
            from xhtml2pdf import pisa
            from io import BytesIO
            
            # تبدیل HTML به PDF
            result_file = open(output_path, "w+b")
            
            # تبدیل
            pisa_status = pisa.CreatePDF(
                html_content.encode('utf-8'),
                dest=result_file,
                encoding='utf-8'
            )
            
            result_file.close()
            
            if not pisa_status.err:
                print(f"✓ PDF ذخیره شد: {output_path}")
                return True
            else:
                print(f"⚠️ PDF با خطاهای جزئی ذخیره شد: {output_path}")
                return True
                
        except ImportError:
            print("⚠️ xhtml2pdf نصب نیست - فقط HTML ذخیره می‌شود")
            return False
        except Exception as e:
            print(f"✗ خطا در تبدیل به PDF: {e}")
            print("💡 HTML به صورت کامل ذخیره شده و قابل استفاده است")
            return False
    
    def save_html_report(self, html_content, filename):
        """ذخیره گزارش HTML"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML ذخیره شد: {filepath}")
        return filepath


if __name__ == "__main__":
    # تست
    generator = ReportGenerator()
    print("Generator آماده است")
