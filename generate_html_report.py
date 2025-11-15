"""
تولید گزارش HTML جامع با نمودارها و جداول
"""

import json
import pandas as pd
from datetime import datetime

def generate_html_report():
    """تولید گزارش HTML کامل"""
    
    # خواندن نتایج
    with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    with open('output/cash_allocation_decision.json', 'r', encoding='utf-8') as f:
        decision_data = json.load(f)
    
    comparisons_df = pd.read_csv('output/detailed_comparisons.csv', encoding='utf-8-sig')
    
    # HTML Template
    html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش تحلیل جامع - امکان‌سنجی تخصیص منابع</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @media print {
            .page-break { page-break-before: always; }
            @page { size: A4; margin: 2cm; }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Tahoma, Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 210mm;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            color: #7f8c8d;
            font-size: 16px;
        }
        
        .header .date {
            color: #95a5a6;
            font-size: 14px;
            margin-top: 10px;
        }
        
        .section {
            margin: 30px 0;
        }
        
        .section-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            font-size: 20px;
            margin-bottom: 20px;
        }
        
        .subsection-title {
            background: #ecf0f1;
            padding: 10px 15px;
            border-right: 4px solid #3498db;
            font-size: 18px;
            margin: 20px 0 15px 0;
            color: #2c3e50;
        }
        
        .info-box {
            background: #e8f4f8;
            border-right: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .warning-box {
            background: #fff3cd;
            border-right: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .success-box {
            background: #d4edda;
            border-right: 4px solid #28a745;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }
        
        td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ecf0f1;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tr:hover {
            background-color: #e9ecef;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: white;
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
            margin: 10px 0;
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .assumptions {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .assumptions h4 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .assumptions ul {
            list-style-position: inside;
            color: #555;
        }
        
        .assumptions li {
            margin: 8px 0;
        }
        
        .comparison-item {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .comparison-header {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 16px;
        }
        
        .comparison-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }
        
        .detail-item {
            padding: 8px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        
        .positive { color: #28a745; font-weight: bold; }
        .negative { color: #dc3545; font-weight: bold; }
        .neutral { color: #6c757d; font-weight: bold; }
        
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>گزارش تحلیل جامع سرمایه‌گذاری</h1>
            <div class="subtitle">امکان‌سنجی تخصیص منابع نقد - تحلیل بنیادی و تکنیکال</div>
            <div class="date">تاریخ: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """</div>
        </div>
"""

    # خلاصه اجرایی
    html_content += """
        <div class="section page-break">
            <div class="section-title">📊 خلاصه اجرایی</div>
            
            <div class="info-box">
                <h3>سوال اصلی:</h3>
                <p>با پول نقد اضافی که برای سرمایه‌گذاری داریم، کدام گزینه بهتر است؟</p>
            </div>
            
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">گزینه 1: سرمایه‌گذاری در</div>
                    <div class="metric-value">3 نماد</div>
                    <div class="metric-label">زفجر، کاوه، گکوثر</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">گزینه 2: سرمایه‌گذاری در</div>
                    <div class="metric-value">6 نماد</div>
                    <div class="metric-label">رنیک، قشیر، زدشت، وسنا، کگاز، تلیسه</div>
                </div>
            </div>
"""

    # نتایج کلی
    opt1_return = decision_data['گزینه_1']['میانگین_بازده']
    opt2_return = decision_data['گزینه_2']['میانگین_بازده']
    diff = decision_data['اختلاف_بازده']
    
    html_content += f"""
            <div class="subsection-title">نتیجه مقایسه</div>
            <table>
                <thead>
                    <tr>
                        <th>گزینه</th>
                        <th>نمادها</th>
                        <th>میانگین بازده 3 ماهه</th>
                        <th>میانگین امتیاز</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>گزینه 1</td>
                        <td>زفجر، کاوه، گکوثر</td>
                        <td class="{'positive' if opt1_return > opt2_return else 'neutral'}">{opt1_return:.2f}%</td>
                        <td>{decision_data['گزینه_1']['میانگین_امتیاز']:.1f}/100</td>
                    </tr>
                    <tr>
                        <td>گزینه 2</td>
                        <td>رنیک، قشیر، زدشت، وسنا، کگاز، تلیسه</td>
                        <td class="{'positive' if opt2_return > opt1_return else 'neutral'}">{opt2_return:.2f}%</td>
                        <td>{decision_data['گزینه_2']['میانگین_امتیاز']:.1f}/100</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="{'success-box' if abs(diff) < 3 else 'warning-box'}">
                <h3>{'✅ توصیه نهایی' if abs(diff) < 3 else '⚠️ توصیه نهایی'}</h3>
                <p><strong>اختلاف بازده: {diff:+.2f}%</strong></p>
"""
    
    if abs(diff) < 3:
        html_content += """
                <p>تفاوت معناداری بین دو گزینه وجود ندارد. می‌توانید ترکیبی از هر دو را انتخاب کنید تا ریسک را کاهش دهید.</p>
"""
    elif diff > 3:
        html_content += """
                <p>گزینه 2 (6 نماد) بازده بهتری دارد. توصیه می‌شود منابع را به این گزینه تخصیص دهید.</p>
"""
    else:
        html_content += """
                <p>گزینه 1 (3 نماد) بازده بهتری دارد. توصیه می‌شود منابع را به این گزینه تخصیص دهید.</p>
"""
    
    html_content += """
            </div>
        </div>
"""

    # تحلیل هر نماد
    html_content += """
        <div class="section page-break">
            <div class="section-title">📈 تحلیل تفصیلی هر نماد</div>
"""
    
    for symbol, data in analysis_data.items():
        pred = data['analysis']['prediction']
        fund = data['analysis']['fundamentals']
        tech = data['analysis']['technical']
        overall = data['analysis']
        
        html_content += f"""
            <div class="subsection-title">{symbol}</div>
            
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">قیمت فعلی</div>
                    <div class="metric-value">{pred['current_price']:,.0f}</div>
                    <div class="metric-label">ریال</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">قیمت هدف 3 ماهه</div>
                    <div class="metric-value">{pred['target_3month']:,.0f}</div>
                    <div class="metric-label">ریال</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">بازده پیش‌بینی</div>
                    <div class="metric-value {'positive' if pred['expected_return_3month'] > 0 else 'negative'}">{pred['expected_return_3month']:+.2f}%</div>
                    <div class="metric-label">3 ماهه</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">امتیاز کلی</div>
                    <div class="metric-value">{overall['overall_score']:.1f}/100</div>
                    <div class="metric-label">{overall['recommendation']}</div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th colspan="2">تحلیل بنیادی</th>
                        <th colspan="2">تحلیل تکنیکال</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>امتیاز بنیادی</td>
                        <td><strong>{fund['score']}/100</strong> (رتبه: {fund['grade']})</td>
                        <td>امتیاز تکنیکال</td>
                        <td><strong>{tech['momentum_score']}/100</strong></td>
                    </tr>
                    <tr>
                        <td>ROE</td>
                        <td>{fund.get('profitability', {}).get('roe', 0)*100:.2f}%</td>
                        <td>روند</td>
                        <td>{tech['trend']}</td>
                    </tr>
                    <tr>
                        <td>ROA</td>
                        <td>{fund.get('profitability', {}).get('roa', 0)*100:.2f}%</td>
                        <td>RSI</td>
                        <td>{tech.get('rsi', 0):.1f}</td>
                    </tr>
                    <tr>
                        <td>حاشیه سود خالص</td>
                        <td>{fund.get('profitability', {}).get('net_margin', 0)*100:.2f}%</td>
                        <td>نسبت به MA20</td>
                        <td>{tech['moving_averages'].get('ma_20', 0):,.0f}</td>
                    </tr>
                    <tr>
                        <td>نسبت بدهی</td>
                        <td>{fund.get('leverage', {}).get('debt_ratio', 0)*100:.2f}%</td>
                        <td>نوسان (20 روزه)</td>
                        <td>{tech.get('volatility', 0):.1f}%</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="info-box">
                <p><strong>اطمینان:</strong> {pred['confidence']} | <strong>سطح ریسک:</strong> {pred['risk_level']}</p>
            </div>
            
            <div class="subsection-title">ارزش‌گذاری</div>
            <table>
                <thead>
                    <tr>
                        <th>سناریو</th>
                        <th>ارزش کل شرکت (میلیارد ریال)</th>
                        <th>ارزش هر سهم (ریال)</th>
                        <th>قیمت فعلی (ریال)</th>
                        <th>اختلاف</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        valuations = data.get('valuations', {})
        valuations_per_share = data.get('valuations_per_share', {})
        current_price = pred['current_price']
        
        for scenario_name in ['خوشبینانه', 'خنثی', 'بدبینانه']:
            scenario_value = valuations.get(scenario_name, 0)
            scenario_value_billion = scenario_value / 1000
            
            value_per_share = valuations_per_share.get(scenario_name, 0)
            
            if value_per_share > 0:
                diff_pct = ((value_per_share - current_price) / current_price) * 100
                diff_class = 'positive' if diff_pct > 0 else 'negative' if diff_pct < 0 else 'neutral'
                
                html_content += f"""
                    <tr>
                        <td><strong>{scenario_name}</strong></td>
                        <td>{scenario_value_billion:,.1f}</td>
                        <td>{value_per_share:,.0f}</td>
                        <td>{current_price:,.0f}</td>
                        <td class="{diff_class}">{diff_pct:+.1f}%</td>
                    </tr>
"""
            else:
                html_content += f"""
                    <tr>
                        <td><strong>{scenario_name}</strong></td>
                        <td>{scenario_value_billion:,.1f}</td>
                        <td colspan="3">داده تعداد سهام موجود نیست</td>
                    </tr>
"""
        
        html_content += """
                </tbody>
            </table>
            
            <div class="warning-box">
                <p><strong>نحوه محاسبه:</strong> ارزش هر سهم = (ارزش کل شرکت) ÷ (تعداد سهام منتشر شده). ارزش کل شرکت بر اساس 6 روش مختلف (DCF, P/E, P/B, EV/EBITDA, P/S, RIM) و میانگین وزنی آنها محاسبه شده است.</p>
            </div>
"""
    
    html_content += """
        </div>
"""

    # مقایسه‌های تک‌به‌تک
    html_content += """
        <div class="section page-break">
            <div class="section-title">🔄 مقایسه‌های تک‌به‌تک (18 حالت)</div>
            <p style="margin-bottom: 20px;">در این بخش، هر یک از 3 نماد اصلی با 6 نماد جایگزین مقایسه می‌شود.</p>
"""
    
    # گروه‌بندی بر اساس منبع
    for source in ['زفجر', 'کاوه', 'گکوثر']:
        source_comps = comparisons_df[comparisons_df['نماد_منبع'] == source]
        if len(source_comps) == 0:
            continue
            
        html_content += f"""
            <div class="subsection-title">به جای {source} کدام نماد را بخریم؟</div>
"""
        
        html_content += """
            <table>
                <thead>
                    <tr>
                        <th>نماد جایگزین</th>
                        <th>بازده منبع</th>
                        <th>بازده هدف</th>
                        <th>اختلاف</th>
                        <th>امتیاز بنیادی</th>
                        <th>امتیاز تکنیکال</th>
                        <th>تصمیم</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for _, row in source_comps.iterrows():
            diff_class = 'positive' if row['اختلاف_بازده_%'] > 0 else 'negative' if row['اختلاف_بازده_%'] < 0 else 'neutral'
            html_content += f"""
                    <tr>
                        <td><strong>{row['نماد_هدف']}</strong></td>
                        <td>{row['بازده_منبع_%']:.2f}%</td>
                        <td>{row['بازده_هدف_%']:.2f}%</td>
                        <td class="{diff_class}">{row['اختلاف_بازده_%']:+.2f}%</td>
                        <td>{row['امتیاز_بنیادی_منبع']} → {row['امتیاز_بنیادی_هدف']}</td>
                        <td>{row['امتیاز_تکنیکال_منبع']} → {row['امتیاز_تکنیکال_هدف']}</td>
                        <td>{row['تصمیم']}</td>
                    </tr>
"""
        
        html_content += """
                </tbody>
            </table>
"""
    
    html_content += """
        </div>
"""

    # نمودارها
    html_content += """
        <div class="section page-break">
            <div class="section-title">📊 نمودارها</div>
            
            <div class="chart-container">
                <canvas id="returnsChart"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="scoresChart"></canvas>
            </div>
            
            <div class="chart-container">
                <canvas id="comparisonChart"></canvas>
            </div>
        </div>
"""

    # مفروضات
    html_content += """
        <div class="section page-break">
            <div class="section-title">📋 مفروضات و روش‌شناسی</div>
            
            <div class="assumptions">
                <h4>مفروضات ارزش‌گذاری:</h4>
                <ul>
                    <li>نرخ بهره بدون ریسک: 22%</li>
                    <li>صرف ریسک بازار: 10%</li>
                    <li>نرخ تورم: 40%</li>
                    <li>نرخ مالیات شرکتی: 25%</li>
                    <li>افق زمانی پیش‌بینی: 3 ماه</li>
                </ul>
                
                <h4>روش‌های ارزش‌گذاری استفاده شده:</h4>
                <ul>
                    <li><strong>DCF:</strong> جریان نقدی آزاد تنزیل شده</li>
                    <li><strong>P/E:</strong> نسبت قیمت به سود (ضریب صنعت: 8x)</li>
                    <li><strong>P/B:</strong> نسبت قیمت به ارزش دفتری</li>
                    <li><strong>EV/EBITDA:</strong> ارزش شرکت به سود عملیاتی (ضریب: 6x)</li>
                    <li><strong>P/S:</strong> نسبت قیمت به فروش (ضریب: 1.5x)</li>
                    <li><strong>RIM:</strong> مدل درآمد باقیمانده</li>
                </ul>
                
                <h4>تحلیل بنیادی:</h4>
                <ul>
                    <li>سودآوری: ROE, ROA, حاشیه سود خالص و عملیاتی (40% از امتیاز)</li>
                    <li>اهرم مالی: نسبت بدهی، نسبت بدهی به حقوق صاحبان سهام (20%)</li>
                    <li>کارایی: گردش دارایی‌ها (20%)</li>
                    <li>نقدینگی: نسبت نقدی (20%)</li>
                </ul>
                
                <h4>تحلیل تکنیکال:</h4>
                <ul>
                    <li>میانگین‌های متحرک: MA10, MA20, MA50</li>
                    <li>شاخص قدرت نسبی (RSI): دوره 14 روزه</li>
                    <li>تشخیص روند: بر اساس موقعیت نسبی قیمت و MA</li>
                    <li>نوسان: انحراف معیار 20 روزه</li>
                    <li>سطوح حمایت و مقاومت</li>
                </ul>
                
                <h4>محاسبه بازده پیش‌بینی 3 ماهه:</h4>
                <ul>
                    <li>بازده ذاتی محدود شده به بازه -30% تا +50%</li>
                    <li>ضریب اطمینان: 0.3 تا 0.8 بر اساس امتیاز کلی</li>
                    <li>بازده مورد انتظار = بازده محدود شده × ضریب اطمینان</li>
                    <li>امتیاز کلی = 60% بنیادی + 40% تکنیکال</li>
                </ul>
            </div>
        </div>
"""

    # Footer
    html_content += """
        <div class="footer">
            <p>این گزارش با استفاده از تحلیل‌های بنیادی و تکنیکال تهیه شده است.</p>
            <p>تمامی اعداد و ارقام بر اساس داده‌های مالی منتشر شده شرکت‌ها و قیمت‌های تعدیل شده بازار محاسبه شده‌اند.</p>
        </div>
    </div>
    
    <script>
        // داده‌ها برای نمودارها
"""

    # داده‌های نمودار
    symbols = []
    returns = []
    scores = []
    
    for symbol, data in analysis_data.items():
        symbols.append(symbol)
        returns.append(data['analysis']['prediction']['expected_return_3month'])
        scores.append(data['analysis']['overall_score'])
    
    html_content += f"""
        const symbols = {json.dumps(symbols, ensure_ascii=False)};
        const returns = {json.dumps(returns)};
        const scores = {json.dumps(scores)};
        
        // نمودار بازده‌ها
        new Chart(document.getElementById('returnsChart'), {{
            type: 'bar',
            data: {{
                labels: symbols,
                datasets: [{{
                    label: 'بازده پیش‌بینی 3 ماهه (%)',
                    data: returns,
                    backgroundColor: returns.map(r => r > 0 ? 'rgba(75, 192, 192, 0.6)' : 'rgba(255, 99, 132, 0.6)'),
                    borderColor: returns.map(r => r > 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)'),
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'بازده پیش‌بینی 3 ماهه (درصد)',
                        font: {{ size: 16 }}
                    }},
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'بازده (%)'
                        }}
                    }}
                }}
            }}
        }});
        
        // نمودار امتیازها
        new Chart(document.getElementById('scoresChart'), {{
            type: 'radar',
            data: {{
                labels: symbols,
                datasets: [{{
                    label: 'امتیاز کلی',
                    data: scores,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgb(153, 102, 255)',
                    pointBackgroundColor: 'rgb(153, 102, 255)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(153, 102, 255)'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'امتیاز کلی نمادها',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
        
        // نمودار مقایسه گروهی
        new Chart(document.getElementById('comparisonChart'), {{
            type: 'bar',
            data: {{
                labels: ['گزینه 1 (3 نماد)', 'گزینه 2 (6 نماد)'],
                datasets: [{{
                    label: 'میانگین بازده 3 ماهه (%)',
                    data: [{opt1_return:.2f}, {opt2_return:.2f}],
                    backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(255, 159, 64, 0.6)'],
                    borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 159, 64, 1)'],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'مقایسه دو گزینه سرمایه‌گذاری',
                        font: {{ size: 16 }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'بازده (%)'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    # ذخیره فایل
    output_file = 'reports/comprehensive_report.html'
    import os
    os.makedirs('reports', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ گزارش HTML ذخیره شد: {output_file}")
    return output_file


if __name__ == '__main__':
    generate_html_report()
