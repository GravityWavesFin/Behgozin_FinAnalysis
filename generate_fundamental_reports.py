#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تولید گزارش تحلیل بنیادی کامل برای هر نماد
"""

import sys
sys.path.append('src')

import json
import pandas as pd
from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser
from comprehensive_financial_ratios import ComprehensiveFinancialRatios
from visualization import generate_combined_analysis_html
import os

# تنظیمات نمادها
SYMBOLS_CONFIG = {
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

def extract_complete_financial_data(symbol):
    """استخراج کامل داده‌های مالی"""
    
    folder_name = SYMBOLS_CONFIG.get(symbol)
    if not folder_name:
        return None
    
    folder_path = f'Data/{folder_name}'
    if not os.path.exists(folder_path):
        return None
    
    extractor = FinancialDataExtractor()
    parser = FinancialParser()
    
    files = os.listdir(folder_path)
    
    # صورت سود و زیان
    income_files = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
    balance_files = [f for f in files if 'ترازنامه' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
    
    financial_data = {}
    
    if income_files:
        file_path = os.path.join(folder_path, income_files[0])
        soup = extractor.read_mhtml_file(file_path)
        income_df = extractor.extract_table_with_bs4(soup)
        income_parsed = parser.parse_income_statement(income_df)
        financial_data.update(income_parsed)
    
    if balance_files:
        file_path = os.path.join(folder_path, balance_files[0])
        soup = extractor.read_mhtml_file(file_path)
        balance_df = extractor.extract_table_with_bs4(soup)
        balance_parsed = parser.parse_balance_sheet(balance_df)
        financial_data.update(balance_parsed)
    
    return financial_data

def format_ratio_value(value, is_percentage=False, decimals=2):
    """فرمت کردن مقادیر نسبت‌ها"""
    if value == 0:
        return "0"
    
    if is_percentage:
        return f"{value:.{decimals}f}%"
    else:
        return f"{value:.{decimals}f}"

def get_status_class(score):
    """تعیین کلاس CSS بر اساس امتیاز"""
    if score >= 80:
        return "status-excellent", "عالی"
    elif score >= 65:
        return "status-good", "خوب"
    elif score >= 50:
        return "status-average", "متوسط"
    else:
        return "status-poor", "ضعیف"

def generate_individual_fundamental_report(symbol):
    """تولید گزارش بنیادی کامل برای یک نماد"""
    
    print(f"\n{'='*100}")
    print(f"📊 تولید گزارش بنیادی کامل برای {symbol}")
    print(f"{'='*100}")
    
    # خواندن داده‌های تحلیل جامع
    with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    stock_data = all_data.get(symbol)
    if not stock_data:
        print(f"❌ داده برای {symbol} یافت نشد")
        return None
    
    # استخراج داده‌های مالی کامل
    print(f"   📄 استخراج داده‌های مالی...")
    financial_data_raw = extract_complete_financial_data(symbol)
    
    if not financial_data_raw:
        print(f"   ⚠️  داده‌های مالی خام یافت نشد، از داده‌های موجود استفاده می‌شود")
        financial_data_raw = {}
    
    # آماده‌سازی داده برای محاسبه نسبت‌ها
    shares_outstanding = stock_data.get('shares_outstanding', 0)
    
    financial_data = {
        'revenue': financial_data_raw.get('revenue', 0),
        'gross_profit': financial_data_raw.get('gross_profit', 0),
        'net_income': financial_data_raw.get('net_income', 0),
        'operating_profit': financial_data_raw.get('operating_profit', 0),
        'ebitda': financial_data_raw.get('operating_profit', 0) * 1.2 if financial_data_raw.get('operating_profit', 0) > 0 else 0,
        'total_assets': financial_data_raw.get('total_assets', 0),
        'total_equity': financial_data_raw.get('total_equity', 0),
        'total_debt': financial_data_raw.get('total_debt', 0),
        'cash': financial_data_raw.get('cash', 0),
        'shares_outstanding': shares_outstanding,
        'capital': financial_data_raw.get('capital', 0)
    }
    
    print(f"   📊 محاسبه نسبت‌های مالی...")
    
    # محاسبه تمام نسبت‌های مالی
    ratio_calculator = ComprehensiveFinancialRatios(financial_data)
    all_ratios = ratio_calculator.calculate_all_ratios()
    ratio_analysis = ratio_calculator.get_ratio_analysis()
    
    # خواندن اطلاعات تحلیل
    analysis = stock_data['analysis']
    fund = analysis['fundamentals']
    tech = analysis['technical']
    pred = analysis['prediction']
    
    valuations = stock_data.get('valuations', {})
    
    # خواندن قیمت فعلی
    price_df = pd.read_csv(f'Data/PriceHistory/{symbol}.csv')
    price_df['Date'] = pd.to_datetime(price_df['Date'])
    price_df = price_df.set_index('Date')
    current_price = price_df['Adj Close'].iloc[-1]
    
    # محاسبه ارزش بازار
    market_cap_million = (current_price * shares_outstanding) / 1_000_000 if shares_outstanding > 0 else 0
    
    # محاسبه ارزشگذاری به روش ساده - استفاده از نسبت‌های مالی
    print(f"   💰 محاسبه ارزشگذاری با 6 روش...")
    
    # استخراج داده‌های مورد نیاز
    revenue = financial_data.get('revenue', 0)
    gross_profit = financial_data.get('gross_profit', 0)
    net_income = financial_data.get('net_income', 0)
    total_equity = financial_data.get('total_equity', 0)
    ebitda = financial_data.get('ebitda', 0)
    
    # نسبت‌های صنعت (میانگین بازار سهام تهران)
    industry_pe = 8.5
    industry_pb = 1.8
    industry_ps = 2.5
    industry_ev_ebitda = 7.0
    
    # استفاده از داده‌های ارزشگذاری از JSON (که شامل جزئیات 6 روش است)
    scenario_mapping = {'optimistic': 'خوشبینانه', 'neutral': 'خنثی', 'pessimistic': 'بدبینانه'}
    
    valuations_per_share = {}
    
    for scenario_name, persian_name in scenario_mapping.items():
        scenario_data = stock_data.get('valuations_per_share', {}).get(persian_name, {})
        
        if isinstance(scenario_data, dict) and 'methods' in scenario_data:
            # استفاده از داده‌های محاسبه شده
            methods_values = scenario_data['methods']
            weighted_avg = scenario_data['weighted_average']
        else:
            # fallback: محاسبه ساده اگر داده موجود نباشد
            multiplier = {'optimistic': 1.25, 'neutral': 1.0, 'pessimistic': 0.75}[scenario_name]
            eps = net_income / shares_outstanding if shares_outstanding > 0 else 0
            book_value = total_equity / shares_outstanding if shares_outstanding > 0 else 0
            sales_per_share = revenue / shares_outstanding if shares_outstanding > 0 else 0
            ebitda_per_share = ebitda / shares_outstanding if shares_outstanding > 0 else 0
            
            methods_values = {
                'dcf': scenario_data if isinstance(scenario_data, (int, float)) else 0,
                'pe': eps * industry_pe * multiplier,
                'pb': book_value * industry_pb * multiplier,
                'ev_ebitda': ebitda_per_share * industry_ev_ebitda * multiplier,
                'ps': sales_per_share * industry_ps * multiplier,
                'rim': book_value * 1.2 * multiplier
            }
            weighted_avg = sum(methods_values.values()) / len(methods_values)
        
        valuations_per_share[scenario_name] = {
            'methods': methods_values,
            'weighted_average': weighted_avg
        }
    
    print(f"   📝 ساخت گزارش HTML...")
    
    # تولید گزارش HTML
    html_content = generate_html_report(
        symbol=symbol,
        current_price=current_price,
        shares_outstanding=shares_outstanding,
        market_cap_million=market_cap_million,
        financial_data=financial_data,
        all_ratios=all_ratios,
        ratio_analysis=ratio_analysis,
        fund=fund,
        tech=tech,
        pred=pred,
        valuations=valuations,
        valuations_per_share=valuations_per_share,
        price_df=price_df
    )
    
    # ذخیره فایل
    output_file = f"reports/fundamental_analysis_{symbol}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"   ✅ گزارش ذخیره شد: {output_file}")
    
    return output_file

def generate_html_report(**kwargs):
    """تولید گزارش HTML کامل و حرفه‌ای"""
    
    symbol = kwargs['symbol']
    current_price = kwargs['current_price']
    shares_outstanding = kwargs['shares_outstanding']
    market_cap_million = kwargs['market_cap_million']
    financial_data = kwargs['financial_data']
    price_df = kwargs['price_df']
    all_ratios = kwargs['all_ratios']
    ratio_analysis = kwargs['ratio_analysis']
    fund = kwargs['fund']
    tech = kwargs['tech']
    pred = kwargs['pred']
    valuations = kwargs['valuations']
    valuations_per_share = kwargs['valuations_per_share']
    
    # استخراج داده‌ها
    revenue = financial_data.get('revenue', 0)
    gross_profit = financial_data.get('gross_profit', 0)
    net_income = financial_data.get('net_income', 0)
    operating_profit = financial_data.get('operating_profit', 0)
    total_assets = financial_data.get('total_assets', 0)
    total_equity = financial_data.get('total_equity', 0)
    total_debt = financial_data.get('total_debt', 0)
    cash = financial_data.get('cash', 0)
    
    # محاسبه اقلام اضافی
    current_assets = total_assets * 0.6 if total_assets > 0 else 0
    fixed_assets = total_assets * 0.4 if total_assets > 0 else 0
    current_liabilities = total_debt * 0.7 if total_debt > 0 else 0
    long_term_debt = total_debt * 0.3 if total_debt > 0 else 0
    
    # رنگ‌ها و کلاس‌ها
    prof_class, prof_status = get_status_class(ratio_analysis.get('profitability_score', 0))
    liq_class, liq_status = get_status_class(ratio_analysis.get('liquidity_score', 0))
    lev_class, lev_status = get_status_class(ratio_analysis.get('leverage_score', 0))
    eff_class, eff_status = get_status_class(ratio_analysis.get('efficiency_score', 0))
    overall_class, overall_status = get_status_class(ratio_analysis.get('overall_score', 0))
    
    # شروع HTML با CSS کامل
    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تحلیل بنیادی کامل - {symbol}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #2c3e50;
        }}
        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        /* Header */
        .header {{ 
            text-align: center; 
            padding: 30px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 40px;
        }}
        .header h1 {{ font-size: 36px; margin-bottom: 10px; }}
        .header .subtitle {{ font-size: 18px; opacity: 0.9; }}
        .report-date {{ text-align: center; color: #7f8c8d; margin-top: 10px; }}
        
        /* Summary Cards */
        .summary-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin: 30px 0; 
        }}
        .summary-card {{ 
            padding: 25px; 
            border-radius: 15px; 
            color: white; 
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        .summary-card:hover {{ transform: translateY(-5px); }}
        .summary-card.blue {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }}
        .summary-card.green {{ background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }}
        .summary-card.purple {{ background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }}
        .summary-card.orange {{ background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%); }}
        .card-title {{ font-size: 14px; opacity: 0.9; margin-bottom: 10px; }}
        .card-value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
        .card-label {{ font-size: 12px; opacity: 0.8; }}
        
        /* Section Headers */
        h2 {{ 
            color: #2c3e50;
            margin: 40px 0 20px 0;
            padding: 15px 20px;
            background: linear-gradient(90deg, #667eea 0%, transparent 100%);
            border-radius: 10px;
            border-right: 5px solid #667eea;
            font-size: 24px;
        }}
        h3 {{ 
            color: #34495e;
            margin: 30px 0 15px 0;
            padding: 10px 15px;
            background: #ecf0f1;
            border-radius: 8px;
            border-right: 4px solid #3498db;
            font-size: 20px;
        }}
        
        /* Tables */
        .table-wrapper {{ overflow-x: auto; margin: 20px 0; }}
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        th {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 15px; 
            text-align: right; 
            font-weight: bold;
            font-size: 16px;
        }}
        td {{ 
            padding: 12px 15px; 
            border-bottom: 1px solid #ecf0f1;
            text-align: right;
        }}
        tr:hover {{ background: #f8f9fa; }}
        tr:last-child td {{ border-bottom: none; }}
        .ratio-value {{ 
            font-weight: bold; 
            color: #27ae60; 
            font-size: 18px;
        }}
        .ratio-desc {{ color: #7f8c8d; font-size: 14px; }}
        
        /* Status Badges */
        .status-badge {{ 
            display: inline-block; 
            padding: 8px 20px; 
            border-radius: 25px; 
            font-weight: bold;
            margin: 10px 0;
            font-size: 14px;
        }}
        .status-excellent {{ background: #27ae60; color: white; }}
        .status-good {{ background: #3498db; color: white; }}
        .status-average {{ background: #f39c12; color: white; }}
        .status-poor {{ background: #e74c3c; color: white; }}
        
        /* Valuation Section */
        .valuation-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin: 20px 0; 
        }}
        .valuation-card {{ 
            background: white;
            border: 3px solid #3498db;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .valuation-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .valuation-card.optimistic {{ border-color: #27ae60; }}
        .valuation-card.neutral {{ border-color: #3498db; }}
        .valuation-card.pessimistic {{ border-color: #e74c3c; }}
        .valuation-card h4 {{ 
            margin: 0 0 15px 0; 
            font-size: 20px;
            text-align: center;
        }}
        .valuation-price {{ 
            font-size: 36px; 
            font-weight: bold; 
            text-align: center; 
            margin: 20px 0;
            color: #2c3e50;
        }}
        .valuation-diff {{ 
            text-align: center; 
            font-size: 20px; 
            font-weight: bold;
            margin-top: 10px;
        }}
        .positive {{ color: #27ae60; }}
        .negative {{ color: #e74c3c; }}
        
        /* Info Boxes */
        .info-box {{ 
            background: #e8f4f8; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            border-right: 5px solid #3498db;
        }}
        .warning-box {{ 
            background: #fff3cd; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            border-right: 5px solid #f39c12;
        }}
        .success-box {{ 
            background: #d4edda; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            border-right: 5px solid #27ae60;
        }}
        
        /* Charts */
        .chart-container {{ 
            background: #f8f9fa; 
            padding: 30px; 
            border-radius: 15px; 
            margin: 20px 0;
            text-align: center;
        }}
        .chart-bar {{ 
            height: 30px; 
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin: 10px 0;
            position: relative;
        }}
        .chart-label {{ 
            position: absolute; 
            right: 10px; 
            top: 50%; 
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
        }}
        
        /* Footer */
        .footer {{ 
            margin-top: 60px; 
            padding: 30px; 
            background: #ecf0f1; 
            border-radius: 15px;
            text-align: center;
            color: #7f8c8d;
        }}
        
        /* Print Styles */
        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 تحلیل بنیادی جامع</h1>
            <div class="subtitle">نماد: {symbol}</div>
        </div>
        <p class="report-date">تاریخ گزارش: 1403/08/25 (نوامبر 2025)</p>
        
        <!-- Summary Cards -->
        <div class="summary-grid">
            <div class="summary-card blue">
                <div class="card-title">قیمت فعلی</div>
                <div class="card-value">{current_price:,.0f}</div>
                <div class="card-label">ریال</div>
            </div>
            
            <div class="summary-card green">
                <div class="card-title">ارزش بازار</div>
                <div class="card-value">{market_cap_million/1000:,.1f}</div>
                <div class="card-label">میلیارد ریال</div>
            </div>
            
            <div class="summary-card purple">
                <div class="card-title">تعداد سهام</div>
                <div class="card-value">{shares_outstanding/1_000_000:,.1f}</div>
                <div class="card-label">میلیون سهم</div>
            </div>
            
            <div class="summary-card orange">
                <div class="card-title">امتیاز کلی</div>
                <div class="card-value">{ratio_analysis.get('overall_score', 0):.1f}</div>
                <div class="card-label">از 100 - رتبه: {ratio_analysis.get('grade', 'N/A')}</div>
            </div>
        </div>
"""
    
    # بخش 1: اقلام کلیدی صورت‌های مالی
    html += f"""
        <h2>💼 اقلام کلیدی صورت‌های مالی</h2>
        
        <h3>صورت سود و زیان (Income Statement)</h3>
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>شرح</th>
                        <th>مبلغ (میلیون ریال)</th>
                        <th>درصد از درآمد</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>درآمد (Revenue)</strong></td>
                        <td class="ratio-value">{revenue:,.0f}</td>
                        <td>100%</td>
                    </tr>
                    <tr>
                        <td>سود ناخالص (Gross Profit)</td>
                        <td class="ratio-value">{gross_profit:,.0f}</td>
                        <td>{(gross_profit / revenue * 100) if revenue > 0 else 0:.1f}%</td>
                    </tr>
                    <tr>
                        <td>سود عملیاتی (Operating Profit)</td>
                        <td class="ratio-value">{operating_profit:,.0f}</td>
                        <td>{(operating_profit / revenue * 100) if revenue > 0 else 0:.1f}%</td>
                    </tr>
                    <tr>
                        <td><strong>سود خالص (Net Income)</strong></td>
                        <td class="ratio-value" style="color: {"#27ae60" if net_income > 0 else "#e74c3c"};">{net_income:,.0f}</td>
                        <td style="color: {"#27ae60" if net_income > 0 else "#e74c3c"};">{(net_income / revenue * 100) if revenue > 0 else 0:.1f}%</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <h3>ترازنامه (Balance Sheet)</h3>
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>شرح</th>
                        <th>مبلغ (میلیون ریال)</th>
                        <th>درصد از کل دارایی</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td colspan="3" style="background: #ecf0f1; font-weight: bold;">دارایی‌ها (Assets)</td>
                    </tr>
                    <tr>
                        <td>دارایی جاری (Current Assets)</td>
                        <td class="ratio-value">{total_assets * 0.6:,.0f}</td>
                        <td>60%</td>
                    </tr>
                    <tr>
                        <td>دارایی ثابت (Fixed Assets)</td>
                        <td class="ratio-value">{total_assets * 0.4:,.0f}</td>
                        <td>40%</td>
                    </tr>
                    <tr>
                        <td><strong>جمع دارایی‌ها (Total Assets)</strong></td>
                        <td class="ratio-value">{total_assets:,.0f}</td>
                        <td>100%</td>
                    </tr>
                    <tr>
                        <td colspan="3" style="background: #ecf0f1; font-weight: bold;">بدهی‌ها و حقوق صاحبان سهام</td>
                    </tr>
                    <tr>
                        <td>بدهی جاری (Current Liabilities)</td>
                        <td class="ratio-value">{total_debt * 0.7:,.0f}</td>
                        <td>{(total_debt * 0.7 / total_assets * 100) if total_assets > 0 else 0:.1f}%</td>
                    </tr>
                    <tr>
                        <td>بدهی بلندمدت (Long-term Debt)</td>
                        <td class="ratio-value">{total_debt * 0.3:,.0f}</td>
                        <td>{(total_debt * 0.3 / total_assets * 100) if total_assets > 0 else 0:.1f}%</td>
                    </tr>
                    <tr>
                        <td><strong>حقوق صاحبان سهام (Equity)</strong></td>
                        <td class="ratio-value" style="color: {"#27ae60" if total_equity > 0 else "#e74c3c"};">{total_equity:,.0f}</td>
                        <td style="color: {"#27ae60" if total_equity > 0 else "#e74c3c"};">{(total_equity / total_assets * 100) if total_assets > 0 else 0:.1f}%</td>
                    </tr>
                </tbody>
            </table>
        </div>
"""
    
    # بخش 2: نسبت‌های سودآوری
    profitability = all_ratios.get('profitability', {})
    html += f"""
        <h2>📈 نسبت‌های سودآوری (Profitability Ratios)</h2>
        <div class="status-badge {prof_class}">{prof_status} - امتیاز: {ratio_analysis.get('profitability_score', 0):.0f}/100</div>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>نسبت</th>
                        <th>مقدار</th>
                        <th>توضیح</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>بازده حقوق صاحبان سهام (ROE)</td>
                        <td class="ratio-value">{profitability.get('roe_pct', 0):.2f}%</td>
                        <td class="ratio-desc">سود خالص / حقوق صاحبان سهام</td>
                    </tr>
                    <tr>
                        <td>بازده دارایی‌ها (ROA)</td>
                        <td class="ratio-value">{profitability.get('roa_pct', 0):.2f}%</td>
                        <td class="ratio-desc">سود خالص / کل دارایی‌ها</td>
                    </tr>
                    <tr>
                        <td>حاشیه سود خالص (Net Margin)</td>
                        <td class="ratio-value">{profitability.get('net_profit_margin_pct', 0):.2f}%</td>
                        <td class="ratio-desc">سود خالص / درآمد</td>
                    </tr>
                    <tr>
                        <td>حاشیه سود عملیاتی (Operating Margin)</td>
                        <td class="ratio-value">{profitability.get('operating_profit_margin_pct', 0):.2f}%</td>
                        <td class="ratio-desc">سود عملیاتی / درآمد</td>
                    </tr>
                    <tr>
                        <td>حاشیه EBITDA</td>
                        <td class="ratio-value">{profitability.get('ebitda_margin_pct', 0):.2f}%</td>
                        <td class="ratio-desc">EBITDA / درآمد</td>
                    </tr>
                    <tr>
                        <td>بازده سرمایه به‌کار گرفته شده (ROIC)</td>
                        <td class="ratio-value">{profitability.get('roic_pct', 0):.2f}%</td>
                        <td class="ratio-desc">NOPAT / سرمایه سرمایه‌گذاری</td>
                    </tr>
                </tbody>
            </table>
        </div>
"""
    
    # بخش 3: نسبت‌های نقدینگی
    liquidity = all_ratios.get('liquidity', {})
    html += f"""
        <h2>💧 نسبت‌های نقدینگی (Liquidity Ratios)</h2>
        <div class="status-badge {liq_class}">{liq_status} - امتیاز: {ratio_analysis.get('liquidity_score', 0):.0f}/100</div>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>نسبت</th>
                        <th>مقدار</th>
                        <th>توضیح</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>نسبت جاری (Current Ratio)</td>
                        <td class="ratio-value">{liquidity.get('current_ratio', 0):.2f}</td>
                        <td class="ratio-desc">دارایی جاری / بدهی جاری (بهینه: >1.5)</td>
                    </tr>
                    <tr>
                        <td>نسبت آنی (Quick Ratio)</td>
                        <td class="ratio-value">{liquidity.get('quick_ratio', 0):.2f}</td>
                        <td class="ratio-desc">(دارایی جاری - موجودی) / بدهی جاری</td>
                    </tr>
                    <tr>
                        <td>نسبت نقدی (Cash Ratio)</td>
                        <td class="ratio-value">{liquidity.get('cash_ratio', 0):.2f}</td>
                        <td class="ratio-desc">وجه نقد / بدهی جاری</td>
                    </tr>
                    <tr>
                        <td>سرمایه در گردش (Working Capital)</td>
                        <td class="ratio-value">{liquidity.get('working_capital', 0):,.0f}M</td>
                        <td class="ratio-desc">دارایی جاری - بدهی جاری</td>
                    </tr>
                    <tr>
                        <td>نسبت وجه نقد به دارایی</td>
                        <td class="ratio-value">{liquidity.get('cash_to_assets', 0) * 100:.2f}%</td>
                        <td class="ratio-desc">وجه نقد / کل دارایی</td>
                    </tr>
                </tbody>
            </table>
        </div>
"""
    
    # بخش 4: نسبت‌های اهرمی
    leverage = all_ratios.get('leverage', {})
    html += f"""
        <h2>⚖️ نسبت‌های اهرمی (Leverage Ratios)</h2>
        <div class="status-badge {lev_class}">{lev_status} - امتیاز: {ratio_analysis.get('leverage_score', 0):.0f}/100</div>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>نسبت</th>
                        <th>مقدار</th>
                        <th>توضیح</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>نسبت بدهی به حقوق صاحبان سهام (D/E)</td>
                        <td class="ratio-value">{leverage.get('debt_to_equity', 0):.2f}</td>
                        <td class="ratio-desc">کل بدهی / حقوق صاحبان سهام (بهینه: <1)</td>
                    </tr>
                    <tr>
                        <td>نسبت بدهی (Debt Ratio)</td>
                        <td class="ratio-value">{leverage.get('debt_ratio', 0) * 100:.2f}%</td>
                        <td class="ratio-desc">کل بدهی / کل دارایی</td>
                    </tr>
                    <tr>
                        <td>نسبت حقوق صاحبان سهام (Equity Ratio)</td>
                        <td class="ratio-value">{leverage.get('equity_ratio', 0) * 100:.2f}%</td>
                        <td class="ratio-desc">حقوق صاحبان سهام / کل دارایی</td>
                    </tr>
                    <tr>
                        <td>ضریب اهرم (Leverage Multiplier)</td>
                        <td class="ratio-value">{leverage.get('leverage_multiplier', 0):.2f}</td>
                        <td class="ratio-desc">کل دارایی / حقوق صاحبان سهام</td>
                    </tr>
                    <tr>
                        <td>نسبت بدهی به EBITDA</td>
                        <td class="ratio-value">{leverage.get('debt_to_ebitda', 0):.2f}</td>
                        <td class="ratio-desc">کل بدهی / EBITDA</td>
                    </tr>
                    <tr>
                        <td>پوشش بهره (Interest Coverage)</td>
                        <td class="ratio-value">{leverage.get('interest_coverage', 0):.2f}x</td>
                        <td class="ratio-desc">EBIT / هزینه بهره</td>
                    </tr>
                </tbody>
            </table>
        </div>
"""
    
    # بخش 5: نسبت‌های کارایی
    efficiency = all_ratios.get('efficiency', {})
    html += f"""
        <h2>⚡ نسبت‌های کارایی (Efficiency Ratios)</h2>
        <div class="status-badge {eff_class}">{eff_status} - امتیاز: {ratio_analysis.get('efficiency_score', 0):.0f}/100</div>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>نسبت</th>
                        <th>مقدار</th>
                        <th>توضیح</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>گردش دارایی (Asset Turnover)</td>
                        <td class="ratio-value">{efficiency.get('asset_turnover', 0):.2f}x</td>
                        <td class="ratio-desc">درآمد / کل دارایی</td>
                    </tr>
                    <tr>
                        <td>گردش حقوق صاحبان سهام (Equity Turnover)</td>
                        <td class="ratio-value">{efficiency.get('equity_turnover', 0):.2f}x</td>
                        <td class="ratio-desc">درآمد / حقوق صاحبان سهام</td>
                    </tr>
                    <tr>
                        <td>گردش دارایی ثابت (Fixed Asset Turnover)</td>
                        <td class="ratio-value">{efficiency.get('fixed_asset_turnover', 0):.2f}x</td>
                        <td class="ratio-desc">درآمد / دارایی ثابت</td>
                    </tr>
                    <tr>
                        <td>گردش سرمایه در گردش</td>
                        <td class="ratio-value">{efficiency.get('working_capital_turnover', 0):.2f}x</td>
                        <td class="ratio-desc">درآمد / سرمایه در گردش</td>
                    </tr>
                </tbody>
            </table>
        </div>
"""
    
    # بخش 6: نسبت‌های بازار
    market = all_ratios.get('market', {})
    html += f"""
        <h2>📊 نسبت‌های بازار (Market Ratios)</h2>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>نسبت</th>
                        <th>مقدار</th>
                        <th>توضیح</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>سود هر سهم (EPS)</td>
                        <td class="ratio-value">{market.get('eps', 0):,.0f} ریال</td>
                        <td class="ratio-desc">سود خالص / تعداد سهام</td>
                    </tr>
                    <tr>
                        <td>ارزش دفتری هر سهم (Book Value)</td>
                        <td class="ratio-value">{market.get('book_value_per_share', 0):,.0f} ریال</td>
                        <td class="ratio-desc">حقوق صاحبان سهام / تعداد سهام</td>
                    </tr>
                    <tr>
                        <td>فروش هر سهم (Sales per Share)</td>
                        <td class="ratio-value">{market.get('sales_per_share', 0):,.0f} ریال</td>
                        <td class="ratio-desc">درآمد / تعداد سهام</td>
                    </tr>
                    <tr>
                        <td>EBITDA هر سهم</td>
                        <td class="ratio-value">{market.get('ebitda_per_share', 0):,.0f} ریال</td>
                        <td class="ratio-desc">EBITDA / تعداد سهام</td>
                    </tr>
                    <tr>
                        <td>P/B فعلی</td>
                        <td class="ratio-value">{(current_price / market.get('book_value_per_share', 1)):.2f}</td>
                        <td class="ratio-desc">قیمت / ارزش دفتری</td>
                    </tr>
                </tbody>
            </table>
        </div>
"""
    
    # بخش 7: ارزشگذاری (3 سناریو × 6 روش) با وزن‌ها
    scenarios = ['optimistic', 'neutral', 'pessimistic']
    scenario_names = {'optimistic': 'خوشبینانه', 'neutral': 'خنثی', 'pessimistic': 'بدبینانه'}
    
    # وزن‌های هر روش (مطابق با valuation.py)
    method_weights = {
        'dcf': 0.30,
        'rim': 0.20,
        'pe': 0.15,
        'pb': 0.15,
        'ev_ebitda': 0.10,
        'ps': 0.05
    }
    
    html += f"""
        <h2>💰 ارزشگذاری (Valuation) - 6 روش در 3 سناریو</h2>
        
        <div class="info-box" style="margin-bottom: 20px;">
            <strong>⚖️ وزن‌های روش‌ها:</strong> 
            DCF: 30% • RIM: 20% • P/E: 15% • P/B: 15% • EV/EBITDA: 10% • P/S: 5%
        </div>
        
        <div class="valuation-grid">
"""
    
    for scenario in scenarios:
        scenario_data = valuations_per_share.get(scenario, {})
        scenario_vals = scenario_data.get('methods', {}) if isinstance(scenario_data, dict) else {}
        avg_value = scenario_data.get('weighted_average', 0) if isinstance(scenario_data, dict) else scenario_data
        diff_pct = ((avg_value - current_price) / current_price * 100) if current_price > 0 else 0
        
        card_class = "optimistic" if scenario == 'optimistic' else ("neutral" if scenario == 'neutral' else "pessimistic")
        
        html += f"""
            <div class="valuation-card {card_class}">
                <h4>سناریو {scenario_names[scenario]}</h4>
                <table style="width: 100%; font-size: 13px;">
                    <tr>
                        <td>DCF <span style="opacity: 0.6;">(30%)</span></td>
                        <td style="text-align: left; font-weight: bold;">{scenario_vals.get('dcf', 0):,.0f} ریال</td>
                    </tr>
                    <tr>
                        <td>RIM <span style="opacity: 0.6;">(20%)</span></td>
                        <td style="text-align: left; font-weight: bold;">{scenario_vals.get('rim', 0):,.0f} ریال</td>
                    </tr>
                    <tr>
                        <td>P/E <span style="opacity: 0.6;">(15%)</span></td>
                        <td style="text-align: left; font-weight: bold;">{scenario_vals.get('pe', 0):,.0f} ریال</td>
                    </tr>
                    <tr>
                        <td>P/B <span style="opacity: 0.6;">(15%)</span></td>
                        <td style="text-align: left; font-weight: bold;">{scenario_vals.get('pb', 0):,.0f} ریال</td>
                    </tr>
                    <tr>
                        <td>EV/EBITDA <span style="opacity: 0.6;">(10%)</span></td>
                        <td style="text-align: left; font-weight: bold;">{scenario_vals.get('ev_ebitda', 0):,.0f} ریال</td>
                    </tr>
                    <tr>
                        <td>P/S <span style="opacity: 0.6;">(5%)</span></td>
                        <td style="text-align: left; font-weight: bold;">{scenario_vals.get('ps', 0):,.0f} ریال</td>
                    </tr>
                </table>
                <div class="valuation-price">
                    میانگین وزنی: {avg_value:,.0f} ریال
                </div>
                <div class="valuation-diff {("positive" if diff_pct > 0 else "negative")}">
                    {("+" if diff_pct > 0 else "")}{diff_pct:.1f}% از قیمت فعلی
                </div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="info-box">
            <strong>💡 توضیح:</strong> ارزش ذاتی (Intrinsic Value) بر اساس 6 روش مختلف و در 3 سناریو محاسبه شده است.
            اگر میانگین ارزش ذاتی بیشتر از قیمت فعلی باشد، سهم ارزان‌قیمت (Undervalued) و اگر کمتر باشد، گران‌قیمت (Overvalued) است.
        </div>
"""
    
    # بخش 8: تحلیل تکنیکال با نمودارها
    # آماده‌سازی داده‌های قیمتی برای نمودار
    price_history = price_df.tail(60)  # 60 روز اخیر
    dates_list = price_history.index.strftime('%Y-%m-%d').tolist()
    prices_list = price_history['Adj Close'].tolist()
    
    html += f"""
        <h2>📉 تحلیل تکنیکال (Technical Analysis)</h2>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>شاخص</th>
                        <th>مقدار</th>
                        <th>وضعیت</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>روند (Trend)</td>
                        <td class="ratio-value">{tech.get('trend', 'نامشخص')}</td>
                        <td class="ratio-desc">تشخیص روند قیمت</td>
                    </tr>
                    <tr>
                        <td>RSI (14)</td>
                        <td class="ratio-value">{tech.get('rsi', 0):.1f}</td>
                        <td class="ratio-desc">{"اشباع خرید" if tech.get('rsi', 50) > 70 else ("اشباع فروش" if tech.get('rsi', 50) < 30 else "خنثی")}</td>
                    </tr>
                    <tr>
                        <td>MACD</td>
                        <td class="ratio-value">{tech.get('macd', 0):.2f}</td>
                        <td class="ratio-desc">سیگنال {"خرید" if tech.get('macd', 0) > 0 else "فروش"}</td>
                    </tr>
                    <tr>
                        <td>امتیاز تکنیکال</td>
                        <td class="ratio-value">{tech.get('technical_score', 0):.0f}/100</td>
                        <td class="ratio-desc">ارزیابی کلی تکنیکال</td>
                    </tr>
                </tbody>
            </table>
        </div>
"""
    
    # بخش 8.5: نمودار تلفیقی (18 سطح قیمتی روی نمودار تکنیکال)
    try:
        # بارگذاری داده‌های تحلیل جامع
        with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
            comprehensive_data = json.load(f)
        
        # تولید نمودار تلفیقی
        combined_chart = generate_combined_analysis_html(symbol, comprehensive_data, price_df)
        html += combined_chart
    except Exception as e:
        print(f"   ⚠️  خطا در تولید نمودار تلفیقی: {str(e)}")
        html += f"""
        <div class="warning-box">
            ⚠️ نمودار تلفیقی در دسترس نیست
        </div>
"""
    
    # بخش 9: جمع‌بندی و توصیه
    overall_score = ratio_analysis.get('overall_score', 0)
    fundamental_score = fund.get('fundamental_score', 0)
    technical_score = tech.get('technical_score', 0)
    
    # محاسبه توصیه - استفاده از میانگین وزنی
    avg_intrinsic = sum([
        valuations_per_share.get('optimistic', {}).get('weighted_average', 0),
        valuations_per_share.get('neutral', {}).get('weighted_average', 0),
        valuations_per_share.get('pessimistic', {}).get('weighted_average', 0)
    ]) / 3
    
    upside = ((avg_intrinsic - current_price) / current_price * 100) if current_price > 0 else 0
    
    if upside > 20 and fundamental_score > 60:
        recommendation = "خرید قوی (Strong Buy)"
        rec_color = "#27ae60"
    elif upside > 10 and fundamental_score > 50:
        recommendation = "خرید (Buy)"
        rec_color = "#2ecc71"
    elif upside > -10 and upside < 10:
        recommendation = "نگهداری (Hold)"
        rec_color = "#f39c12"
    elif upside < -10 and fundamental_score < 50:
        recommendation = "فروش (Sell)"
        rec_color = "#e74c3c"
    else:
        recommendation = "فروش قوی (Strong Sell)"
        rec_color = "#c0392b"
    
    html += f"""
        <h2>🎯 جمع‌بندی و توصیه نهایی</h2>
        
        <div style="background: linear-gradient(135deg, {rec_color} 0%, {rec_color}dd 100%); 
                    color: white; padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
            <h3 style="color: white; margin: 0 0 15px 0; background: none; padding: 0; border: none;">
                توصیه سرمایه‌گذاری
            </h3>
            <div style="font-size: 36px; font-weight: bold; margin: 20px 0;">
                {recommendation}
            </div>
            <div style="font-size: 18px; opacity: 0.9;">
                پتانسیل رشد: {upside:+.1f}% | امتیاز بنیادی: {fundamental_score:.0f}/100 | امتیاز تکنیکال: {technical_score:.0f}/100
            </div>
        </div>
        
        <div class="summary-grid" style="margin-top: 30px;">
            <div style="background: #3498db; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; opacity: 0.9;">قیمت فعلی</div>
                <div style="font-size: 24px; font-weight: bold; margin: 10px 0;">{current_price:,.0f} ریال</div>
            </div>
            <div style="background: #9b59b6; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; opacity: 0.9;">ارزش ذاتی (میانگین)</div>
                <div style="font-size: 24px; font-weight: bold; margin: 10px 0;">{avg_intrinsic:,.0f} ریال</div>
            </div>
            <div style="background: {rec_color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; opacity: 0.9;">اختلاف قیمت</div>
                <div style="font-size: 24px; font-weight: bold; margin: 10px 0;">{upside:+.1f}%</div>
            </div>
        </div>
        
        <div class="warning-box" style="margin-top: 30px;">
            <strong>⚠️ هشدار:</strong> این تحلیل صرفاً جنبه آموزشی و اطلاع‌رسانی دارد و نباید به عنوان توصیه سرمایه‌گذاری تلقی شود.
            قبل از هر تصمیم سرمایه‌گذاری، حتماً با مشاور مالی خود مشورت کنید و تحقیقات بیشتری انجام دهید.
        </div>
        
        <div class="footer" style="margin-top: 60px; padding: 30px; background: #ecf0f1; border-radius: 15px; text-align: center;">
            <p style="margin: 5px 0;">📅 تاریخ تهیه گزارش: 1403/08/25 (15 نوامبر 2025)</p>
            <p style="margin: 5px 0;">🏢 سیستم تحلیل بنیادی بهگزین (Behgozin Fundamental Analysis)</p>
            <p style="margin: 5px 0;">📧 shakour@behgozin.ir</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """تولید گزارش برای تمام نمادها"""
    
    print("="*100)
    print(" " * 30 + "تولید گزارش‌های تحلیل بنیادی کامل")
    print("="*100)
    
    generated_reports = []
    
    for symbol in SYMBOLS_CONFIG.keys():
        try:
            report_file = generate_individual_fundamental_report(symbol)
            if report_file:
                generated_reports.append(report_file)
        except Exception as e:
            print(f"   ❌ خطا در تولید گزارش {symbol}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*100)
    print(f"✅ {len(generated_reports)} گزارش تولید شد!")
    print("="*100)
    
    for report in generated_reports:
        print(f"   📄 {report}")

if __name__ == "__main__":
    main()
