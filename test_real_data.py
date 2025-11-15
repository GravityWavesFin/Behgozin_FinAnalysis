"""
تست سیستم با داده‌های واقعی ذخیره شده
"""

import sys
sys.path.append('src')

import pandas as pd
from report_generator_html import HTMLReportGenerator
from persian_utils import format_number, format_percentage, to_persian_digits
import jdatetime
import json

def test_with_real_data():
    """تست با داده‌های واقعی"""
    
    print("\n" + "="*70)
    print("تست با داده‌های واقعی")
    print("="*70)
    
    # خواندن داده زفجر
    symbol = 'زفجر'
    cache_file = f'Data/PriceHistory/{symbol}.csv'
    
    print(f"\nخواندن داده {symbol}...")
    df = pd.read_csv(cache_file)
    
    print(f"[OK] {len(df)} رکورد خوانده شد")
    print(f"\nستون‌ها: {list(df.columns)}")
    print(f"\nنمونه داده:")
    print(df.head(3))
    
    # محاسبات ساده
    if 'Adj Close' in df.columns:
        first_price = df['Adj Close'].iloc[0]
        last_price = df['Adj Close'].iloc[-1]
        total_return = ((last_price / first_price) - 1) * 100
        
        print(f"\n📊 تحلیل:")
        print(f"   قیمت اول: {format_number(first_price)} ریال")
        print(f"   قیمت آخر: {format_number(last_price)} ریال")
        print(f"   بازده کل: {format_percentage(total_return)}")
    
    # ایجاد گزارش ساده
    print(f"\nایجاد گزارش...")
    generator = HTMLReportGenerator(output_dir='reports')
    
    # ایجاد داده نمودار
    print(f"   آماده‌سازی داده نمودار...")
    chart_data = generator.create_price_chart_js(df, symbol)
    
    # ایجاد HTML ساده
    today_jalali = jdatetime.date.today()
    today_str = f"{today_jalali.year}/{today_jalali.month}/{today_jalali.day}"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>گزارش {symbol}</title>
    <style>
        {generator.executive_css}
    </style>
</head>
<body>
    <div class="page">
        <div class="executive-header">
            <h1>گزارش تحلیل تکنیکال</h1>
            <div class="subtitle">{symbol}</div>
            <div class="meta">
                <span>تاریخ: {to_persian_digits(today_str)}</span>
                <span>سیستم بازارگردانی بهگزین</span>
            </div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-icon">📅</div>
                <div class="metric-label">تعداد روزها</div>
                <div class="metric-value">{to_persian_digits(str(len(df)))}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-label">قیمت فعلی</div>
                <div class="metric-value">{to_persian_digits(format_number(last_price))}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-label">بازده کل</div>
                <div class="metric-value value-positive">{to_persian_digits(format_percentage(total_return))}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-label">حجم معاملات</div>
                <div class="metric-value">{to_persian_digits(format_number(df['Volume'].iloc[-1]))}</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                <span>📈 روند قیمتی و شاخص‌های تکنیکال</span>
            </div>
            <div class="chart-container">
                <div class="chart-wrapper">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="executive-summary">
            <div class="summary-title">خلاصه اجرایی</div>
            <div class="summary-item">
                <span class="summary-label">نماد:</span>
                <span class="summary-value">{symbol}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">دوره تحلیل:</span>
                <span class="summary-value">{df['J-Date'].iloc[0]} تا {df['J-Date'].iloc[-1]}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">تعداد روزهای معاملاتی:</span>
                <span class="summary-value">{to_persian_digits(str(len(df)))} روز</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">قیمت اولیه (تعدیل شده):</span>
                <span class="summary-value">{to_persian_digits(format_number(first_price))} ریال</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">قیمت فعلی (تعدیل شده):</span>
                <span class="summary-value">{to_persian_digits(format_number(last_price))} ریال</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">بازده کل:</span>
                <span class="summary-value value-positive">{to_persian_digits(format_percentage(total_return))}</span>
            </div>
        </div>
        
        <div class="alert-box alert-info">
            <div class="alert-title">نکته</div>
            <p>قیمت‌های تعدیل شده (Adjusted) شامل تاثیر افزایش سرمایه و تقسیم سود می‌باشد.</p>
            <p>داده‌ها از سایت tsetmc دریافت و به صورت خودکار کش می‌شوند.</p>
        </div>
        
        <div class="page-footer">
            <div class="footer-logo">سیستم بازارگردانی بهگزین</div>
            <p>گزارش تحلیل تکنیکال - تاریخ: {to_persian_digits(today_str)}</p>
        </div>
    </div>
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script>
        // داده نمودار
        const chartData = {chart_data};
        
        // نمودار قیمت
        const ctx = document.getElementById('priceChart').getContext('2d');
        const priceChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: chartData.dates,
                datasets: [
                    {{
                        label: 'قیمت پایانی',
                        data: chartData.closes,
                        borderColor: '#2C3E50',
                        backgroundColor: 'rgba(44, 62, 80, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }},
                    {{
                        label: 'میانگین ۲۰ روزه',
                        data: chartData.sma20,
                        borderColor: '#F39C12',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4
                    }},
                    {{
                        label: 'میانگین ۵۰ روزه',
                        data: chartData.sma50,
                        borderColor: '#E74C3C',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top',
                        rtl: true,
                        labels: {{
                            font: {{
                                family: 'Tahoma',
                                size: 12
                            }}
                        }}
                    }},
                    title: {{
                        display: true,
                        text: 'روند قیمت {symbol}',
                        font: {{
                            family: 'Tahoma',
                            size: 16,
                            weight: 'bold'
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        ticks: {{
                            font: {{
                                family: 'Tahoma'
                            }},
                            callback: function(value) {{
                                return value.toLocaleString('fa-IR');
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            font: {{
                                family: 'Tahoma'
                            }},
                            maxRotation: 45,
                            minRotation: 45
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
    """
    
    # ذخیره
    generator.save_report(html_content, f'test_real_data_{symbol}', generate_pdf=True)
    
    print(f"\n[OK] گزارش ذخیره شد:")
    print(f"   HTML: reports/test_real_data_{symbol}.html")
    print(f"   PDF: reports/test_real_data_{symbol}.pdf")


if __name__ == "__main__":
    test_with_real_data()
