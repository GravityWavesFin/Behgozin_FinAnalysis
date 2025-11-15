"""
سیستم گزارش‌دهی پیشرفته با نمودارها و جداول حرفه‌ای
برای ارائه به مدیران ارشد
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime
import jdatetime
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Import matplotlib برای نمودارها
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.gridspec import GridSpec

# تنظیم فونت فارسی
plt.rcParams['font.family'] = 'Tahoma'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'

from persian_utils import format_number, format_percentage, format_currency, to_persian_digits


class AdvancedReportGenerator:
    """کلاس تولید گزارش‌های حرفه‌ای با نمودارها و جداول پیشرفته"""
    
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
        
        # CSS حرفه‌ای با طراحی مدرن
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
            background: #ffffff;
        }
        
        .page {
            width: 21cm;
            min-height: 29.7cm;
            padding: 1.5cm;
            margin: 0 auto;
            background: white;
            page-break-after: always;
        }
        
        .page:last-child {
            page-break-after: avoid;
        }
        
        /* هدر اجرایی با طراحی مدرن */
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
        
        /* کارت‌های متریک با افکت هاور */
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
        
        .metric-change.positive {
            background: #D4EDDA;
            color: #27AE60;
        }
        
        .metric-change.negative {
            background: #F8D7DA;
            color: #E74C3C;
        }
        
        .metric-change.neutral {
            background: #FFF3CD;
            color: #F39C12;
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
        
        .section-icon {
            font-size: 28px;
            margin-left: 15px;
        }
        
        /* جداول حرفه‌ای */
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
            letter-spacing: 0.3px;
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
        
        /* ستون اول (نام) */
        .data-table td:first-child,
        .data-table th:first-child {
            text-align: right;
            font-weight: 600;
        }
        
        /* رنگ‌بندی شرطی */
        .value-positive {
            color: #27AE60;
            font-weight: bold;
        }
        
        .value-negative {
            color: #E74C3C;
            font-weight: bold;
        }
        
        .value-warning {
            color: #F39C12;
            font-weight: bold;
        }
        
        /* نشان‌ها */
        .badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
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
        
        /* نمودارها */
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
            page-break-inside: avoid;
        }
        
        .chart-title {
            font-size: 18px;
            font-weight: bold;
            color: #2C3E50;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .chart-container img {
            width: 100%;
            height: auto;
            border-radius: 8px;
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
        
        .alert-warning {
            background: linear-gradient(135deg, #FFF3CD, #FFE69C);
            border-color: #F39C12;
            color: #856404;
        }
        
        .alert-danger {
            background: linear-gradient(135deg, #F8D7DA, #F5C6CB);
            border-color: #E74C3C;
            color: #721C24;
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
        
        /* نوار پیشرفت */
        .progress-container {
            background: #ECF0F1;
            border-radius: 20px;
            height: 35px;
            overflow: hidden;
            margin: 15px 0;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
            transition: width 0.6s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .progress-excellent {
            background: linear-gradient(90deg, #27AE60, #2ECC71);
        }
        
        .progress-good {
            background: linear-gradient(90deg, #3498DB, #5DADE2);
        }
        
        .progress-moderate {
            background: linear-gradient(90deg, #F39C12, #F8C471);
        }
        
        .progress-weak {
            background: linear-gradient(90deg, #E74C3C, #EC7063);
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
        
        .summary-item:last-child {
            border-bottom: none;
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
                box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            }
            .data-table tbody tr:hover {
                background-color: inherit;
            }
        }
        
        /* نمودارهای کوچک داخل متن */
        .sparkline {
            display: inline-block;
            vertical-align: middle;
            margin: 0 5px;
        }
        
        /* گرید لی‌آوت */
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        
        .grid-3col {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        
        /* کارت‌های اطلاعاتی */
        .info-card {
            background: white;
            border: 2px solid #E8E8E8;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        }
        
        .info-card-title {
            font-weight: bold;
            color: #2C3E50;
            font-size: 16px;
            margin-bottom: 15px;
            border-bottom: 2px solid #667EEA;
            padding-bottom: 8px;
        }
        
        /* جداول مقایسه‌ای */
        .comparison-table {
            width: 100%;
            margin: 20px 0;
        }
        
        .comparison-table td {
            padding: 10px;
            text-align: center;
        }
        
        .comparison-table .company-col {
            background: #F8F9FA;
            font-weight: bold;
        }
        
        .comparison-table .winner {
            background: #D4EDDA;
            color: #27AE60;
            font-weight: bold;
        }
        """
    
    def create_price_chart(self, price_data: pd.DataFrame, symbol: str) -> str:
        """
        نمودار قیمت حرفه‌ای با شاخص‌های تکنیکال
        """
        fig = plt.figure(figsize=(14, 8))
        gs = GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.3)
        
        # محاسبه میانگین‌های متحرک
        price_data['SMA20'] = price_data['close'].rolling(window=20).mean()
        price_data['SMA50'] = price_data['close'].rolling(window=50).mean()
        
        # نمودار اصلی قیمت
        ax1 = fig.add_subplot(gs[0])
        ax1.plot(price_data.index, price_data['close'], 
                linewidth=2, color=self.colors['primary'], label='قیمت پایانی', alpha=0.8)
        ax1.plot(price_data.index, price_data['SMA20'], 
                linewidth=1.5, color=self.colors['warning'], label='میانگین ۲۰ روزه', linestyle='--', alpha=0.7)
        ax1.plot(price_data.index, price_data['SMA50'], 
                linewidth=1.5, color=self.colors['danger'], label='میانگین ۵۰ روزه', linestyle='--', alpha=0.7)
        
        ax1.fill_between(price_data.index, price_data['close'].min(), price_data['close'],
                         alpha=0.1, color=self.colors['secondary'])
        
        ax1.set_title(f'روند قیمتی {symbol}', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('قیمت (ریال)', fontsize=12, fontweight='bold')
        ax1.legend(loc='upper right', framealpha=0.9)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_facecolor('#F8F9FA')
        
        # نمودار حجم
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        colors_volume = [self.colors['success'] if price_data['close'].iloc[i] >= price_data['close'].iloc[i-1] 
                        else self.colors['danger'] for i in range(1, len(price_data))]
        colors_volume.insert(0, self.colors['secondary'])
        
        ax2.bar(price_data.index, price_data['volume'], color=colors_volume, alpha=0.6, width=0.8)
        ax2.set_ylabel('حجم معاملات', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax2.set_facecolor('#F8F9FA')
        
        # محاسبه RSI
        delta = price_data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # نمودار RSI
        ax3 = fig.add_subplot(gs[2], sharex=ax1)
        ax3.plot(price_data.index, rsi, linewidth=2, color=self.colors['purple'], label='RSI')
        ax3.axhline(y=70, color=self.colors['danger'], linestyle='--', alpha=0.7, linewidth=1)
        ax3.axhline(y=30, color=self.colors['success'], linestyle='--', alpha=0.7, linewidth=1)
        ax3.fill_between(price_data.index, 30, 70, alpha=0.1, color=self.colors['secondary'])
        
        ax3.set_ylabel('RSI', fontsize=11, fontweight='bold')
        ax3.set_xlabel('تاریخ', fontsize=11, fontweight='bold')
        ax3.set_ylim(0, 100)
        ax3.legend(loc='upper right', framealpha=0.9)
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.set_facecolor('#F8F9FA')
        
        plt.tight_layout()
        
        # تبدیل به base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def create_financial_ratios_chart(self, ratios_data: dict, title: str) -> str:
        """
        نمودار راداری برای نسبت‌های مالی
        """
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        categories = list(ratios_data.keys())
        values = list(ratios_data.values())
        
        # نرمال‌سازی مقادیر به بازه 0-10
        normalized_values = []
        for v in values:
            if v > 0:
                norm = min(10, (v / max(values)) * 10)
            else:
                norm = 0
            normalized_values.append(norm)
        
        # تعداد متغیرها
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        normalized_values += normalized_values[:1]
        angles += angles[:1]
        
        # رسم
        ax.plot(angles, normalized_values, 'o-', linewidth=2, color=self.colors['secondary'], label=title)
        ax.fill(angles, normalized_values, alpha=0.25, color=self.colors['secondary'])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=10)
        ax.set_ylim(0, 10)
        ax.set_title(title, size=16, fontweight='bold', pad=20)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def create_valuation_comparison_chart(self, valuation_results: dict) -> str:
        """
        نمودار مقایسه روش‌های ارزش‌گذاری در سناریوهای مختلف
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # نمودار میله‌ای مقایسه روش‌ها
        methods = list(valuation_results.keys())
        scenarios = ['خوشبینانه', 'خنثی', 'بدبینانه']
        
        x = np.arange(len(methods))
        width = 0.25
        
        for i, scenario in enumerate(scenarios):
            values = [valuation_results[m].get(scenario, 0) for m in methods]
            offset = width * (i - 1)
            ax1.bar(x + offset, values, width, label=scenario, alpha=0.8)
        
        ax1.set_xlabel('روش ارزش‌گذاری', fontweight='bold', fontsize=12)
        ax1.set_ylabel('ارزش (میلیارد ریال)', fontweight='bold', fontsize=12)
        ax1.set_title('مقایسه روش‌های ارزش‌گذاری', fontweight='bold', fontsize=14)
        ax1.set_xticks(x)
        ax1.set_xticklabels(methods, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_facecolor('#F8F9FA')
        
        # نمودار باکس‌پلات برای توزیع
        all_values = []
        labels = []
        for scenario in scenarios:
            scenario_values = [valuation_results[m].get(scenario, 0) for m in methods]
            all_values.append(scenario_values)
            labels.append(scenario)
        
        bp = ax2.boxplot(all_values, labels=labels, patch_artist=True,
                        boxprops=dict(facecolor=self.colors['secondary'], alpha=0.7),
                        medianprops=dict(color=self.colors['danger'], linewidth=2),
                        whiskerprops=dict(color=self.colors['dark'], linewidth=1.5),
                        capprops=dict(color=self.colors['dark'], linewidth=1.5))
        
        ax2.set_ylabel('ارزش (میلیارد ریال)', fontweight='bold', fontsize=12)
        ax2.set_title('توزیع ارزش‌گذاری در سناریوها', fontweight='bold', fontsize=14)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_facecolor('#F8F9FA')
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def create_sensitivity_heatmap(self, sensitivity_data: pd.DataFrame, title: str) -> str:
        """
        هیت‌مپ تحلیل حساسیت
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        sns.heatmap(sensitivity_data, annot=True, fmt='.0f', cmap='RdYlGn',
                   center=sensitivity_data.mean().mean(),
                   linewidths=1, linecolor='white',
                   cbar_kws={'label': 'ارزش (میلیارد ریال)'},
                   ax=ax)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('نرخ رشد پایانی (%)', fontweight='bold', fontsize=12)
        ax.set_ylabel('نرخ تنزیل (%)', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def create_allocation_ranking_chart(self, ranking_data: pd.DataFrame) -> str:
        """
        نمودار رتبه‌بندی نمادها برای تخصیص منابع
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # نمودار میله‌ای افقی امتیازات
        symbols = ranking_data['symbol'].tolist()
        scores = ranking_data['total_score'].tolist()
        
        colors_list = [self.colors['success'] if s >= 80 
                      else self.colors['secondary'] if s >= 60 
                      else self.colors['warning'] if s >= 40 
                      else self.colors['danger'] 
                      for s in scores]
        
        y_pos = np.arange(len(symbols))
        ax1.barh(y_pos, scores, color=colors_list, alpha=0.8, height=0.7)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(symbols, fontsize=11, fontweight='bold')
        ax1.set_xlabel('امتیاز کل', fontweight='bold', fontsize=12)
        ax1.set_title('رتبه‌بندی نمادها', fontweight='bold', fontsize=14)
        ax1.grid(True, alpha=0.3, axis='x')
        ax1.set_facecolor('#F8F9FA')
        
        # اضافه کردن مقادیر روی میله‌ها
        for i, v in enumerate(scores):
            ax1.text(v + 1, i, f'{v:.1f}', va='center', fontweight='bold')
        
        # نمودار رادار مقایسه معیارها برای بهترین نماد
        if not ranking_data.empty:
            top_symbol = ranking_data.iloc[0]
            categories = ['سلامت مالی', 'ارزش‌گذاری', 'رشد', 'نقدینگی']
            values = [
                top_symbol.get('health_score', 0),
                top_symbol.get('valuation_score', 0),
                top_symbol.get('growth_score', 0),
                top_symbol.get('liquidity_score', 0)
            ]
            
            N = len(categories)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            values += values[:1]
            angles += angles[:1]
            
            ax2 = plt.subplot(122, projection='polar')
            ax2.plot(angles, values, 'o-', linewidth=2, color=self.colors['success'])
            ax2.fill(angles, values, alpha=0.25, color=self.colors['success'])
            ax2.set_xticks(angles[:-1])
            ax2.set_xticklabels(categories, size=11)
            ax2.set_ylim(0, 100)
            ax2.set_title(f'تحلیل جامع: {top_symbol["symbol"]}', 
                         fontweight='bold', fontsize=14, pad=20)
            ax2.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def get_rating_badge(self, score: float) -> tuple:
        """
        تعیین رتبه و کلاس CSS بر اساس امتیاز
        
        Returns:
        --------
        tuple: (نام رتبه، کلاس CSS)
        """
        if score >= 80:
            return ('عالی', 'badge-excellent')
        elif score >= 60:
            return ('خوب', 'badge-good')
        elif score >= 40:
            return ('متوسط', 'badge-moderate')
        else:
            return ('ضعیف', 'badge-weak')
    
    def get_progress_class(self, score: float) -> str:
        """کلاس CSS برای نوار پیشرفت"""
        if score >= 80:
            return 'progress-excellent'
        elif score >= 60:
            return 'progress-good'
        elif score >= 40:
            return 'progress-moderate'
        else:
            return 'progress-weak'
    
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
            return False
    
    def save_report(self, html_content: str, filename: str, generate_pdf: bool = True):
        """ذخیره گزارش HTML و PDF"""
        # ذخیره HTML
        html_path = os.path.join(self.output_dir, filename + '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML ذخیره شد: {html_path}")
        
        # تبدیل به PDF
        if generate_pdf:
            pdf_path = os.path.join(self.output_dir, filename + '.pdf')
            self.html_to_pdf(html_content, pdf_path)
        
        return html_path


if __name__ == "__main__":
    print("Advanced Report Generator آماده است")
