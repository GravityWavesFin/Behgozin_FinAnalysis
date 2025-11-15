"""
سیستم گزارش‌دهی پیشرفته با HTML/CSS/JavaScript
بدون وابستگی به matplotlib و seaborn
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime
import jdatetime
import json
import warnings
warnings.filterwarnings('ignore')

from persian_utils import format_number, format_percentage, format_currency, to_persian_digits


class HTMLReportGenerator:
    """کلاس تولید گزارش‌های HTML خالص با JavaScript Charts"""
    
    def __init__(self, output_dir: str = 'reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # پالت رنگی حرفه‌ای
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'info': '#17A2B8',
            'purple': '#9B59B6',
            'dark': '#34495E',
            'light': '#ECF0F1',
            'gradient_start': '#667EEA',
            'gradient_end': '#764BA2'
        }
        
        # CSS حرفه‌ای
        self.executive_css = """
        @page {
            size: A4;
            margin: 1.5cm;
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
            line-height: 1.8;
            color: #2C3E50;
            background: #f5f6fa;
        }
        
        .page {
            width: 21cm;
            min-height: 29.7cm;
            padding: 1.5cm;
            margin: 1cm auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            page-break-after: always;
        }
        
        .page:last-child {
            page-break-after: avoid;
        }
        
        /* هدر اجرایی */
        .executive-header {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            color: white;
            padding: 30px;
            margin: -1.5cm -1.5cm 30px -1.5cm;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .executive-header h1 {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .executive-header .subtitle {
            font-size: 20px;
            text-align: center;
            opacity: 0.95;
            margin-bottom: 20px;
        }
        
        .executive-header .meta {
            display: flex;
            justify-content: space-between;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.3);
            font-size: 14px;
        }
        
        /* کارت‌های متریک */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 30px 0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 2px solid #E8E8E8;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            border-color: #667EEA;
        }
        
        .metric-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .metric-label {
            color: #7F8C8D;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            color: #2C3E50;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 5px;
            font-family: 'Tahoma', monospace;
        }
        
        .metric-change {
            font-size: 13px;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 12px;
            display: inline-block;
        }
        
        .value-positive {
            color: #27AE60;
        }
        
        .value-negative {
            color: #E74C3C;
        }
        
        /* بخش‌ها */
        .section {
            margin: 40px 0;
            page-break-inside: avoid;
        }
        
        .section-header {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            margin-bottom: 25px;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
            display: flex;
            align-items: center;
        }
        
        /* نمودارها */
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
            page-break-inside: avoid;
        }
        
        .chart-wrapper {
            position: relative;
            height: 400px;
            margin: 20px 0;
        }
        
        /* جداول */
        .data-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0;
            font-size: 13px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-radius: 10px;
            overflow: hidden;
        }
        
        .data-table thead {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            color: white;
        }
        
        .data-table th {
            padding: 15px 12px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
        }
        
        .data-table td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #ECF0F1;
        }
        
        .data-table tbody tr {
            background: white;
            transition: background 0.2s;
        }
        
        .data-table tbody tr:nth-child(even) {
            background-color: #F8F9FA;
        }
        
        .data-table tbody tr:hover {
            background-color: #E8F4F8;
        }
        
        .data-table td:first-child,
        .data-table th:first-child {
            text-align: right;
            font-weight: 600;
        }
        
        /* نشان‌ها */
        .badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .badge-excellent {
            background: linear-gradient(135deg, #27AE60, #2ECC71);
            color: white;
        }
        
        .badge-good {
            background: linear-gradient(135deg, #3498DB, #5DADE2);
            color: white;
        }
        
        .badge-moderate {
            background: linear-gradient(135deg, #F39C12, #F8C471);
            color: white;
        }
        
        .badge-weak {
            background: linear-gradient(135deg, #E74C3C, #EC7063);
            color: white;
        }
        
        /* اعلان‌ها */
        .alert-box {
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-right: 5px solid;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .alert-success {
            background: linear-gradient(135deg, #D4EDDA, #C3E6CB);
            border-color: #27AE60;
            color: #155724;
        }
        
        .alert-info {
            background: linear-gradient(135deg, #D1ECF1, #BEE5EB);
            border-color: #17A2B8;
            color: #0C5460;
        }
        
        .alert-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        /* خلاصه اجرایی */
        .executive-summary {
            background: linear-gradient(135deg, #F8F9FA, #FFFFFF);
            border: 2px solid #E8E8E8;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }
        
        .summary-title {
            font-size: 22px;
            font-weight: bold;
            color: #2C3E50;
            margin-bottom: 20px;
            border-bottom: 3px solid #667EEA;
            padding-bottom: 10px;
        }
        
        .summary-item {
            padding: 12px 0;
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #ECF0F1;
        }
        
        .summary-label {
            font-weight: 600;
            color: #7F8C8D;
        }
        
        .summary-value {
            font-weight: bold;
            color: #2C3E50;
        }
        
        /* فوتر */
        .page-footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #ECF0F1;
            text-align: center;
            color: #95A5A6;
            font-size: 11px;
        }
        
        .footer-logo {
            font-size: 16px;
            font-weight: bold;
            color: #667EEA;
            margin-bottom: 5px;
        }
        
        /* گرید */
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        
        /* پرینت */
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
    
    def create_price_chart_js(self, price_data: pd.DataFrame, symbol: str) -> str:
        """
        ایجاد نمودار قیمت با Chart.js
        """
        # آماده‌سازی داده
        dates = price_data['J-Date'].tolist()[-100:]  # آخرین 100 روز
        closes = price_data['Adj Close'].tolist()[-100:]
        volumes = price_data['Volume'].tolist()[-100:]
        
        # محاسبه SMA
        sma20 = pd.Series(closes).rolling(window=20).mean().tolist()
        sma50 = pd.Series(closes).rolling(window=50).mean().tolist()
        
        chart_data = {
            'dates': dates,
            'closes': closes,
            'sma20': sma20,
            'sma50': sma50,
            'volumes': volumes
        }
        
        return json.dumps(chart_data, ensure_ascii=False)
    
    def create_comparison_chart_js(self, data: dict) -> str:
        """ایجاد نمودار مقایسه‌ای"""
        return json.dumps(data, ensure_ascii=False)
    
    def html_to_pdf(self, html_content: str, output_path: str) -> bool:
        """تبدیل HTML به PDF"""
        try:
            from xhtml2pdf import pisa
            
            result_file = open(output_path, "w+b")
            pisa_status = pisa.CreatePDF(
                html_content.encode('utf-8'),
                dest=result_file,
                encoding='utf-8'
            )
            result_file.close()
            
            if not pisa_status.err:
                print(f"[OK] PDF: {output_path}")
                return True
            else:
                print(f"[هشدار] PDF با خطا: {output_path}")
                return True
                
        except ImportError:
            print("[هشدار] xhtml2pdf نصب نیست - فقط HTML")
            return False
        except Exception as e:
            print(f"[خطا] PDF: {e}")
            return False
    
    def save_report(self, html_content: str, filename: str, generate_pdf: bool = True):
        """ذخیره گزارش"""
        # HTML
        html_path = os.path.join(self.output_dir, filename + '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[OK] HTML: {html_path}")
        
        # PDF
        if generate_pdf:
            pdf_path = os.path.join(self.output_dir, filename + '.pdf')
            self.html_to_pdf(html_content, pdf_path)
        
        return html_path


if __name__ == "__main__":
    print("HTML Report Generator آماده است")
