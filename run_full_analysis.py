"""
اجرای کامل تحلیل بنیادی برای همه 9 شرکت
با گزارش‌های HTML حرفه‌ای
"""

import sys
sys.path.append('src')

import pandas as pd
import numpy as np
import jdatetime
from config import SYMBOLS
from report_generator_html import HTMLReportGenerator
from persian_utils import format_number, format_percentage, to_persian_digits
import os


def analyze_company(symbol: str, price_data: pd.DataFrame, generator: HTMLReportGenerator):
    """تحلیل کامل یک شرکت"""
    
    print(f"\n{'='*70}")
    print(f"تحلیل {symbol}")
    print(f"{'='*70}")
    
    # محاسبات پایه
    first_price = price_data['Adj Close'].iloc[0]
    last_price = price_data['Adj Close'].iloc[-1]
    total_return = ((last_price / first_price) - 1) * 100
    
    max_price = price_data['Adj Close'].max()
    min_price = price_data['Adj Close'].min()
    avg_price = price_data['Adj Close'].mean()
    
    total_volume = price_data['Volume'].sum()
    avg_volume = price_data['Volume'].mean()
    
    # محاسبه نوسان (انحراف معیار)
    volatility = price_data['Adj Close'].pct_change().std() * 100
    
    # محاسبه شارپ (ساده)
    daily_returns = price_data['Adj Close'].pct_change()
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() > 0 else 0
    
    # تشخیص روند
    trend = "صعودی" if total_return > 10 else "خنثی" if total_return > -10 else "نزولی"
    trend_class = "value-positive" if total_return > 0 else "value-negative"
    
    # امتیاز سلامت (ساده بر اساس بازده و نوسان)
    health_score = min(100, max(0, (total_return + 50) - (volatility * 2)))
    
    # توصیه
    if health_score >= 70:
        recommendation = "خرید قوی"
        rec_class = "alert-success"
        rec_badge = "badge-excellent"
    elif health_score >= 50:
        recommendation = "خرید"
        rec_class = "alert-success"
        rec_badge = "badge-good"
    elif health_score >= 30:
        recommendation = "نگهداری"
        rec_class = "alert-info"
        rec_badge = "badge-moderate"
    else:
        recommendation = "فروش"
        rec_class = "alert-warning"
        rec_badge = "badge-weak"
    
    print(f"✓ بازده: {total_return:.2f}%")
    print(f"✓ نوسان: {volatility:.2f}%")
    print(f"✓ امتیاز سلامت: {health_score:.1f}")
    print(f"✓ توصیه: {recommendation}")
    
    # ایجاد داده نمودار
    chart_data = generator.create_price_chart_js(price_data, symbol)
    
    # ایجاد HTML
    today_jalali = jdatetime.date.today()
    today_str = f"{today_jalali.year}/{today_jalali.month}/{today_jalali.day}"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش تحلیل بنیادی {symbol}</title>
    <style>
        {generator.executive_css}
    </style>
</head>
<body>
    <div class="page">
        <div class="executive-header">
            <h1>گزارش تحلیل بنیادی و ارزش‌گذاری</h1>
            <div class="subtitle">نماد: {symbol}</div>
            <div class="meta">
                <span>تاریخ گزارش: {to_persian_digits(today_str)}</span>
                <span>سیستم تحلیل بازارگردانی بهگزین</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                📊 خلاصه اجرایی
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-icon">💯</div>
                    <div class="metric-label">امتیاز سلامت مالی</div>
                    <div class="metric-value">{to_persian_digits(f'{health_score:.1f}')}</div>
                    <div class="metric-change">{trend}</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon">📈</div>
                    <div class="metric-label">بازده دوره</div>
                    <div class="metric-value {trend_class}">{to_persian_digits(format_percentage(total_return))}</div>
                    <div class="metric-change">از ابتدای سال ۱۴۰۳</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-label">نوسان‌پذیری</div>
                    <div class="metric-value">{to_persian_digits(f'{volatility:.1f}%')}</div>
                    <div class="metric-change">انحراف معیار روزانه</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon">⚖️</div>
                    <div class="metric-label">نسبت شارپ</div>
                    <div class="metric-value">{to_persian_digits(f'{sharpe:.2f}')}</div>
                    <div class="metric-change">بازده تعدیل شده</div>
                </div>
            </div>
            
            <div class="alert-box {rec_class}">
                <div class="alert-title">🎯 توصیه سرمایه‌گذاری</div>
                <p><strong><span class="badge {rec_badge}">{recommendation}</span></strong></p>
                <p>بر اساس تحلیل {to_persian_digits(str(len(price_data)))} روز معاملاتی اخیر</p>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                📈 تحلیل تکنیکال و روند قیمتی
            </div>
            <div class="chart-container">
                <div class="chart-wrapper">
                    <canvas id="priceChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="executive-summary">
            <div class="summary-title">آمار کلیدی</div>
            <div class="summary-item">
                <span class="summary-label">دوره تحلیل:</span>
                <span class="summary-value">{price_data['J-Date'].iloc[0]} تا {price_data['J-Date'].iloc[-1]}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">تعداد روزهای معاملاتی:</span>
                <span class="summary-value">{to_persian_digits(str(len(price_data)))} روز</span>
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
                <span class="summary-label">بالاترین قیمت:</span>
                <span class="summary-value">{to_persian_digits(format_number(max_price))} ریال</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">پایین‌ترین قیمت:</span>
                <span class="summary-value">{to_persian_digits(format_number(min_price))} ریال</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">میانگین قیمت:</span>
                <span class="summary-value">{to_persian_digits(format_number(avg_price))} ریال</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">میانگین حجم روزانه:</span>
                <span class="summary-value">{to_persian_digits(format_number(avg_volume))}</span>
            </div>
        </div>
    </div>
    
    <div class="page">
        <div class="section">
            <div class="section-header">
                💰 تحلیل نسبت‌های مالی (برآوردی)
            </div>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>نسبت مالی</th>
                        <th>مقدار</th>
                        <th>وضعیت</th>
                        <th>توضیحات</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>بازده کل سرمایه‌گذاری</td>
                        <td class="{trend_class}">{to_persian_digits(format_percentage(total_return))}</td>
                        <td><span class="badge {rec_badge}">{recommendation}</span></td>
                        <td>بازده تجمعی از ابتدای دوره</td>
                    </tr>
                    <tr>
                        <td>نوسان‌پذیری (ریسک)</td>
                        <td>{to_persian_digits(f'{volatility:.2f}%')}</td>
                        <td><span class="badge {'badge-good' if volatility < 5 else 'badge-moderate' if volatility < 10 else 'badge-weak'}">
                            {'کم' if volatility < 5 else 'متوسط' if volatility < 10 else 'زیاد'}
                        </span></td>
                        <td>انحراف معیار بازده روزانه</td>
                    </tr>
                    <tr>
                        <td>نسبت شارپ</td>
                        <td>{to_persian_digits(f'{sharpe:.2f}')}</td>
                        <td><span class="badge {'badge-excellent' if sharpe > 2 else 'badge-good' if sharpe > 1 else 'badge-moderate' if sharpe > 0 else 'badge-weak'}">
                            {'عالی' if sharpe > 2 else 'خوب' if sharpe > 1 else 'متوسط' if sharpe > 0 else 'ضعیف'}
                        </span></td>
                        <td>بازده تعدیل شده به ازای ریسک</td>
                    </tr>
                    <tr>
                        <td>محدوده نوسان قیمت</td>
                        <td>{to_persian_digits(format_number(max_price - min_price))} ریال</td>
                        <td><span class="badge badge-good">{'%.1f' % ((max_price/min_price - 1) * 100)}%</span></td>
                        <td>اختلاف بالاترین و پایین‌ترین قیمت</td>
                    </tr>
                    <tr>
                        <td>امتیاز سلامت مالی کلی</td>
                        <td class="value-positive">{to_persian_digits(f'{health_score:.1f}')}</td>
                        <td><span class="badge {rec_badge}">{recommendation}</span></td>
                        <td>ترکیبی از بازده، نوسان و روند</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="alert-box alert-info">
            <div class="alert-title">📝 نکات مهم</div>
            <ul style="margin-right: 20px; line-height: 2;">
                <li>قیمت‌های تعدیل شده شامل تاثیر افزایش سرمایه و تقسیم سود می‌باشد</li>
                <li>تحلیل بر اساس داده‌های واقعی از سایت tsetmc انجام شده است</li>
                <li>نسبت شارپ بالاتر از ۱ نشان‌دهنده بازده مناسب به ازای ریسک است</li>
                <li>امتیاز سلامت مالی ترکیبی از عملکرد قیمتی و ریسک است</li>
            </ul>
        </div>
        
        <div class="page-footer">
            <div class="footer-logo">🔷 سیستم بازارگردانی بهگزین</div>
            <p>گزارش تحلیل بنیادی - نماد: {symbol}</p>
            <p>تاریخ: {to_persian_digits(today_str)} | محرمانه - ویژه مدیران ارشد</p>
        </div>
    </div>
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script>
        const chartData = {chart_data};
        
        const ctx = document.getElementById('priceChart').getContext('2d');
        const priceChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: chartData.dates,
                datasets: [
                    {{
                        label: 'قیمت پایانی (تعدیل شده)',
                        data: chartData.closes,
                        borderColor: '#2C3E50',
                        backgroundColor: 'rgba(44, 62, 80, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 2,
                        pointHoverRadius: 5
                    }},
                    {{
                        label: 'میانگین ۲۰ روزه',
                        data: chartData.sma20,
                        borderColor: '#F39C12',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4,
                        pointRadius: 0
                    }},
                    {{
                        label: 'میانگین ۵۰ روزه',
                        data: chartData.sma50,
                        borderColor: '#E74C3C',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4,
                        pointRadius: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    mode: 'index',
                    intersect: false
                }},
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top',
                        rtl: true,
                        labels: {{
                            font: {{
                                family: 'Tahoma',
                                size: 13
                            }},
                            padding: 15,
                            usePointStyle: true
                        }}
                    }},
                    title: {{
                        display: true,
                        text: 'روند قیمت {symbol} - آخرین 100 روز معاملاتی',
                        font: {{
                            family: 'Tahoma',
                            size: 16,
                            weight: 'bold'
                        }},
                        padding: 20
                    }},
                    tooltip: {{
                        rtl: true,
                        titleFont: {{
                            family: 'Tahoma',
                            size: 13
                        }},
                        bodyFont: {{
                            family: 'Tahoma',
                            size: 12
                        }},
                        callbacks: {{
                            label: function(context) {{
                                let label = context.dataset.label || '';
                                if (label) {{
                                    label += ': ';
                                }}
                                label += new Intl.NumberFormat('fa-IR').format(context.parsed.y) + ' ریال';
                                return label;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        ticks: {{
                            font: {{
                                family: 'Tahoma',
                                size: 11
                            }},
                            callback: function(value) {{
                                return new Intl.NumberFormat('fa-IR').format(value);
                            }}
                        }},
                        grid: {{
                            color: 'rgba(0, 0, 0, 0.05)'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            font: {{
                                family: 'Tahoma',
                                size: 10
                            }},
                            maxRotation: 45,
                            minRotation: 45,
                            maxTicksLimit: 15
                        }},
                        grid: {{
                            display: false
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
    generator.save_report(html_content, f'{symbol}_analysis', generate_pdf=False)
    
    return {
        'symbol': symbol,
        'total_return': total_return,
        'volatility': volatility,
        'sharpe': sharpe,
        'health_score': health_score,
        'recommendation': recommendation
    }


def create_summary_report(all_results: list, generator: HTMLReportGenerator):
    """ایجاد گزارش خلاصه برای همه شرکت‌ها"""
    
    print(f"\n{'='*70}")
    print("ایجاد گزارش خلاصه")
    print(f"{'='*70}")
    
    # مرتب‌سازی بر اساس امتیاز سلامت
    sorted_results = sorted(all_results, key=lambda x: x['health_score'], reverse=True)
    
    # جداسازی شرکت‌ها
    surplus_symbols = SYMBOLS['با_مازاد_منابع']
    deficit_symbols = SYMBOLS['با_کمبود_منابع']
    
    surplus_companies = [r for r in all_results if r['symbol'] in surplus_symbols]
    deficit_companies = [r for r in all_results if r['symbol'] in deficit_symbols]
    
    today_jalali = jdatetime.date.today()
    today_str = f"{today_jalali.year}/{today_jalali.month}/{today_jalali.day}"
    
    # ساخت جداول
    ranking_rows = ""
    for i, result in enumerate(sorted_results, 1):
        trend_class = "value-positive" if result['total_return'] > 0 else "value-negative"
        badge_class = "badge-excellent" if result['health_score'] >= 70 else "badge-good" if result['health_score'] >= 50 else "badge-moderate" if result['health_score'] >= 30 else "badge-weak"
        
        ranking_rows += f"""
        <tr>
            <td>{to_persian_digits(str(i))}</td>
            <td><strong>{result['symbol']}</strong></td>
            <td class="value-positive">{to_persian_digits(f"{result['health_score']:.1f}")}</td>
            <td class="{trend_class}">{to_persian_digits(format_percentage(result['total_return']))}</td>
            <td>{to_persian_digits(f"{result['volatility']:.2f}%")}</td>
            <td>{to_persian_digits(f"{result['sharpe']:.2f}")}</td>
            <td><span class="badge {badge_class}">{result['recommendation']}</span></td>
        </tr>
        """
    
    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش خلاصه تحلیل بازارگردانی</title>
    <style>
        {generator.executive_css}
    </style>
</head>
<body>
    <div class="page">
        <div class="executive-header">
            <h1>گزارش جامع تحلیل بازارگردانی</h1>
            <div class="subtitle">تحلیل ۹ نماد برای تخصیص منابع</div>
            <div class="meta">
                <span>تاریخ گزارش: {to_persian_digits(today_str)}</span>
                <span>سیستم تحلیل بازارگردانی بهگزین</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                📊 خلاصه اجرایی
            </div>
            
            <div class="executive-summary">
                <div class="summary-title">نتایج کلی</div>
                <div class="summary-item">
                    <span class="summary-label">تعداد کل نمادها:</span>
                    <span class="summary-value">{to_persian_digits(str(len(all_results)))} نماد</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">شرکت‌های با مازاد منابع:</span>
                    <span class="summary-value">{', '.join(surplus_symbols)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">شرکت‌های با کمبود منابع:</span>
                    <span class="summary-value">{', '.join(deficit_symbols)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">بهترین عملکرد:</span>
                    <span class="summary-value value-positive">{sorted_results[0]['symbol']} 
                    ({to_persian_digits(format_percentage(sorted_results[0]['total_return']))})</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">میانگین بازده:</span>
                    <span class="summary-value">{to_persian_digits(format_percentage(sum(r['total_return'] for r in all_results) / len(all_results)))}</span>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                🏆 رتبه‌بندی کلی نمادها
            </div>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>رتبه</th>
                        <th>نماد</th>
                        <th>امتیاز سلامت</th>
                        <th>بازده کل</th>
                        <th>نوسان</th>
                        <th>شارپ</th>
                        <th>توصیه</th>
                    </tr>
                </thead>
                <tbody>
                    {ranking_rows}
                </tbody>
            </table>
        </div>
        
        <div class="alert-box alert-success">
            <div class="alert-title">✅ توصیه تخصیص منابع</div>
            <p><strong>بر اساس تحلیل‌های انجام شده، بهترین نمادها برای تخصیص منابع:</strong></p>
            <ul style="margin-right: 20px; line-height: 2; margin-top: 10px;">
                <li><strong>{sorted_results[0]['symbol']}</strong> - امتیاز: {to_persian_digits(f"{sorted_results[0]['health_score']:.1f}")}</li>
                <li><strong>{sorted_results[1]['symbol']}</strong> - امتیاز: {to_persian_digits(f"{sorted_results[1]['health_score']:.1f}")}</li>
                <li><strong>{sorted_results[2]['symbol']}</strong> - امتیاز: {to_persian_digits(f"{sorted_results[2]['health_score']:.1f}")}</li>
            </ul>
        </div>
        
        <div class="page-footer">
            <div class="footer-logo">🔷 سیستم بازارگردانی بهگزین</div>
            <p>گزارش جامع تحلیل ۹ نماد</p>
            <p>تاریخ: {to_persian_digits(today_str)} | محرمانه - ویژه مدیران ارشد</p>
        </div>
    </div>
</body>
</html>
    """
    
    generator.save_report(html_content, 'summary_all_companies', generate_pdf=False)
    print("[OK] گزارش خلاصه ذخیره شد")


def main():
    """اجرای تحلیل کامل"""
    
    print("\n" + "="*70)
    print("سیستم تحلیل جامع بازارگردانی بهگزین")
    print("="*70)
    
    # همه نمادها
    all_symbols = SYMBOLS['با_مازاد_منابع'] + SYMBOLS['با_کمبود_منابع']
    
    print(f"\nتعداد نمادها: {len(all_symbols)}")
    print(f"نمادها: {', '.join(all_symbols)}")
    
    generator = HTMLReportGenerator(output_dir='reports')
    all_results = []
    
    # تحلیل هر نماد
    for i, symbol in enumerate(all_symbols, 1):
        print(f"\n[{i}/{len(all_symbols)}] پردازش {symbol}...")
        
        try:
            # خواندن داده
            cache_file = f'Data/PriceHistory/{symbol}.csv'
            if not os.path.exists(cache_file):
                print(f"[خطا] فایل داده برای {symbol} یافت نشد")
                continue
            
            df = pd.read_csv(cache_file)
            
            # تحلیل و ایجاد گزارش
            result = analyze_company(symbol, df, generator)
            all_results.append(result)
            
            print(f"[OK] گزارش {symbol} ذخیره شد")
            
        except Exception as e:
            print(f"[خطا] {symbol}: {e}")
            continue
    
    # گزارش خلاصه
    if all_results:
        create_summary_report(all_results, generator)
    
    print("\n" + "="*70)
    print("✅ تحلیل کامل انجام شد!")
    print(f"📁 گزارش‌ها در پوشه 'reports' ذخیره شدند")
    print(f"📊 تعداد گزارش‌های ایجاد شده: {len(all_results) + 1}")
    print("="*70)


if __name__ == "__main__":
    main()
