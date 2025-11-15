"""
ماژول تلفیق تحلیل بنیادی و تکنیکال
Visualization Module for Combined Fundamental & Technical Analysis

این ماژول 18 سطح قیمتی حاصل از ارزشگذاری بنیادی را 
روی نمودار تکنیکال نمایش می‌دهد.

18 سطح = 6 روش ارزشگذاری × 3 سناریو:
- DCF (Discounted Cash Flow)
- P/E (Price to Earnings)
- P/B (Price to Book)
- EV/EBITDA
- P/S (Price to Sales)
- RIM (Residual Income Model)

× 3 سناریو:
- خوشبینانه (Optimistic)
- خنثی (Neutral)
- بدبینانه (Pessimistic)

نویسنده: شکور علیشاهی
تاریخ: 1403/08/25 (15 نوامبر 2025)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import json
import jdatetime


class FundamentalTechnicalChart:
    """کلاس تلفیق تحلیل بنیادی و تکنیکال"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.price_levels = {}
        self.current_price = 0
        self.support_levels = []
        self.resistance_levels = []
        
    def load_valuation_data(self, comprehensive_data: Dict) -> bool:
        """بارگذاری داده‌های ارزشگذاری از فایل JSON"""
        
        try:
            stock_data = comprehensive_data.get(self.symbol)
            if not stock_data:
                print(f"❌ داده برای {self.symbol} یافت نشد")
                return False
            
            # استخراج 18 سطح قیمتی
            valuations_per_share = stock_data.get('valuations_per_share', {})
            
            self.price_levels = {
                'optimistic': {},
                'neutral': {},
                'pessimistic': {}
            }
            
            scenario_mapping = {
                'خوشبینانه': 'optimistic',
                'خنثی': 'neutral',
                'بدبینانه': 'pessimistic'
            }
            
            for persian_name, english_name in scenario_mapping.items():
                scenario_data = valuations_per_share.get(persian_name, {})
                
                if isinstance(scenario_data, dict) and 'methods' in scenario_data:
                    methods = scenario_data['methods']
                    self.price_levels[english_name] = {
                        'dcf': methods.get('dcf', 0),
                        'pe': methods.get('pe', 0),
                        'pb': methods.get('pb', 0),
                        'ev_ebitda': methods.get('ev_ebitda', 0),
                        'ps': methods.get('ps', 0),
                        'rim': methods.get('rim', 0),
                        'weighted_avg': scenario_data.get('weighted_average', 0)
                    }
            
            print(f"✅ 18 سطح قیمتی برای {self.symbol} بارگذاری شد")
            return True
            
        except Exception as e:
            print(f"❌ خطا در بارگذاری داده: {str(e)}")
            return False
    
    def set_current_price(self, price: float):
        """تنظیم قیمت فعلی سهم"""
        self.current_price = price
    
    def classify_price_levels(self):
        """طبقه‌بندی سطوح قیمتی به Support و Resistance"""
        
        all_levels = []
        
        # جمع‌آوری تمام سطوح
        for scenario, methods in self.price_levels.items():
            for method, price in methods.items():
                if price > 0 and method != 'weighted_avg':
                    all_levels.append({
                        'price': price,
                        'scenario': scenario,
                        'method': method,
                        'label': f"{method.upper()} ({scenario})"
                    })
        
        # مرتب‌سازی بر اساس قیمت
        all_levels.sort(key=lambda x: x['price'])
        
        # تفکیک Support و Resistance
        self.support_levels = [l for l in all_levels if l['price'] < self.current_price]
        self.resistance_levels = [l for l in all_levels if l['price'] >= self.current_price]
        
        return {
            'support': self.support_levels,
            'resistance': self.resistance_levels,
            'total_levels': len(all_levels)
        }
    
    def get_key_levels(self, top_n: int = 5) -> Dict:
        """دریافت مهم‌ترین سطوح Support و Resistance"""
        
        # نزدیک‌ترین سطوح Support
        closest_supports = self.support_levels[-top_n:] if len(self.support_levels) >= top_n else self.support_levels
        
        # نزدیک‌ترین سطوح Resistance
        closest_resistances = self.resistance_levels[:top_n] if len(self.resistance_levels) >= top_n else self.resistance_levels
        
        return {
            'closest_supports': closest_supports,
            'closest_resistances': closest_resistances,
            'strongest_support': closest_supports[-1] if closest_supports else None,
            'strongest_resistance': closest_resistances[0] if closest_resistances else None
        }
    
    def calculate_zones(self) -> Dict:
        """محاسبه نواحی خرید، فروش و خنثی"""
        
        # میانگین‌های وزنی هر سناریو
        optimistic_avg = self.price_levels['optimistic'].get('weighted_avg', 0)
        neutral_avg = self.price_levels['neutral'].get('weighted_avg', 0)
        pessimistic_avg = self.price_levels['pessimistic'].get('weighted_avg', 0)
        
        # محاسبه نواحی
        zones = {
            'strong_buy': {
                'min': 0,
                'max': pessimistic_avg * 0.85,
                'color': '#27ae60',
                'label': 'ناحیه خرید قوی',
                'description': 'قیمت زیر 85% سناریو بدبینانه'
            },
            'buy': {
                'min': pessimistic_avg * 0.85,
                'max': pessimistic_avg * 1.1,
                'color': '#2ecc71',
                'label': 'ناحیه خرید',
                'description': 'قیمت نزدیک سناریو بدبینانه'
            },
            'neutral': {
                'min': pessimistic_avg * 1.1,
                'max': neutral_avg * 1.1,
                'color': '#f39c12',
                'label': 'ناحیه خنثی',
                'description': 'قیمت بین سناریو بدبینانه و خنثی'
            },
            'sell': {
                'min': neutral_avg * 1.1,
                'max': optimistic_avg * 1.15,
                'color': '#e74c3c',
                'label': 'ناحیه فروش',
                'description': 'قیمت بالاتر از سناریو خنثی'
            },
            'strong_sell': {
                'min': optimistic_avg * 1.15,
                'max': float('inf'),
                'color': '#c0392b',
                'label': 'ناحیه فروش قوی',
                'description': 'قیمت بالاتر از 115% سناریو خوشبینانه'
            }
        }
        
        # تشخیص ناحیه فعلی
        current_zone = None
        for zone_name, zone_data in zones.items():
            if zone_data['min'] <= self.current_price < zone_data['max']:
                current_zone = zone_name
                break
        
        return {
            'zones': zones,
            'current_zone': current_zone,
            'optimistic_avg': optimistic_avg,
            'neutral_avg': neutral_avg,
            'pessimistic_avg': pessimistic_avg
        }
    
    def generate_chart_html(self, price_df: pd.DataFrame, days: int = 90) -> str:
        """تولید HTML نمودار تلفیقی با Canvas و Chart.js"""
        
        # آماده‌سازی داده‌های قیمتی
        recent_prices = price_df.tail(days).copy()
        
        # تبدیل تاریخ‌ها به شمسی
        dates = []
        for date in recent_prices.index:
            jdate = jdatetime.date.fromgregorian(date=date.date())
            dates.append(jdate.strftime('%Y/%m/%d'))
        
        # داده‌های قیمت بسته شدن
        prices = recent_prices['Close'].tolist()
        
        # طبقه‌بندی سطوح
        classification = self.classify_price_levels()
        zones = self.calculate_zones()
        
        # آماده‌سازی سطوح برای نمودار
        levels_data = []
        for level in classification['support'] + classification['resistance']:
            levels_data.append({
                'price': float(level['price']),
                'label': str(level['label']),
                'scenario': str(level['scenario']),
                'is_support': 'true' if level['price'] < self.current_price else 'false'
            })
        
        # رنگ‌بندی سطوح
        level_colors = {
            'optimistic': 'rgba(39, 174, 96, 0.6)',   # سبز
            'neutral': 'rgba(243, 156, 18, 0.6)',      # نارنجی
            'pessimistic': 'rgba(231, 76, 60, 0.6)'   # قرمز
        }
        
        html = f"""
        <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #2c3e50; margin-bottom: 20px;">
                📊 نمودار تلفیقی - تحلیل بنیادی + تکنیکال
            </h3>
            
            <div style="position: relative; height: 500px;">
                <canvas id="combinedChart"></canvas>
            </div>
            
            <!-- وضعیت فعلی -->
            <div style="margin-top: 15px; padding: 15px; background: {zones['zones'][zones['current_zone']]['color']}22; 
                        border-right: 4px solid {zones['zones'][zones['current_zone']]['color']}; border-radius: 8px;">
                <strong>وضعیت فعلی:</strong> {zones['zones'][zones['current_zone']]['label']}<br>
                <small>{zones['zones'][zones['current_zone']]['description']}</small><br>
                <strong>قیمت فعلی:</strong> {self.current_price:,.0f} ریال
            </div>
        </div>
        
        <script>
        (function() {{
            const ctx = document.getElementById('combinedChart').getContext('2d');
            
            // داده‌های قیمت
            const dates = {json.dumps(dates)};
            const prices = {json.dumps(prices)};
            
            // سطوح قیمتی (18 سطح از ارزشگذاری)
            const levels = {json.dumps(levels_data)};
            
            // ایجاد annotations برای سطوح قیمتی
            const annotations = {{}};
            
            levels.forEach((level, index) => {{
                const scenario = level.scenario;
                const color = scenario === 'optimistic' ? 'rgba(39, 174, 96, 0.6)' : 
                             (scenario === 'neutral' ? 'rgba(52, 152, 219, 0.6)' : 'rgba(231, 76, 60, 0.6)');
                
                annotations[`level${{index}}`] = {{
                    type: 'line',
                    yMin: level.price,
                    yMax: level.price,
                    borderColor: color,
                    borderWidth: (level.is_support === 'true') ? 2 : 1,
                    borderDash: (level.is_support === 'true') ? [] : [5, 5],
                    label: {{
                        content: level.label.split(' ')[0],
                        enabled: true,
                        position: 'end',
                        backgroundColor: color,
                        color: 'white',
                        font: {{ size: 9 }}
                    }}
                }};
            }});
            
            // خطوط میانگین وزنی
            annotations['avg_optimistic'] = {{
                type: 'line',
                yMin: {zones['optimistic_avg']},
                yMax: {zones['optimistic_avg']},
                borderColor: 'rgba(39, 174, 96, 1)',
                borderWidth: 3,
                label: {{
                    content: 'میانگین خوشبینانه: {zones['optimistic_avg']:,.0f}',
                    enabled: true,
                    position: 'start',
                    backgroundColor: 'rgba(39, 174, 96, 1)',
                    color: 'white'
                }}
            }};
            
            annotations['avg_neutral'] = {{
                type: 'line',
                yMin: {zones['neutral_avg']},
                yMax: {zones['neutral_avg']},
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 3,
                label: {{
                    content: 'میانگین خنثی: {zones['neutral_avg']:,.0f}',
                    enabled: true,
                    position: 'start',
                    backgroundColor: 'rgba(52, 152, 219, 1)',
                    color: 'white'
                }}
            }};
            
            annotations['avg_pessimistic'] = {{
                type: 'line',
                yMin: {zones['pessimistic_avg']},
                yMax: {zones['pessimistic_avg']},
                borderColor: 'rgba(231, 76, 60, 1)',
                borderWidth: 3,
                label: {{
                    content: 'میانگین بدبینانه: {zones['pessimistic_avg']:,.0f}',
                    enabled: true,
                    position: 'start',
                    backgroundColor: 'rgba(231, 76, 60, 1)',
                    color: 'white'
                }}
            }};
            
            const chart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: dates,
                    datasets: [
                        {{
                            label: 'قیمت ({self.symbol})',
                            data: prices,
                            borderColor: 'rgba(0, 0, 0, 1)',
                            backgroundColor: 'rgba(0, 0, 0, 0.05)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 0,
                            pointHoverRadius: 5
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{
                        mode: 'index',
                        intersect: false,
                    }},
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'نمودار قیمت با 18 سطح ارزشگذاری بنیادی',
                            font: {{ size: 16, family: 'Tahoma' }}
                        }},
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    let label = context.dataset.label || '';
                                    if (label) {{
                                        label += ': ';
                                    }}
                                    if (context.parsed.y !== null) {{
                                        label += context.parsed.y.toLocaleString('fa-IR') + ' ریال';
                                    }}
                                    return label;
                                }},
                                afterBody: function(context) {{
                                    // نمایش اطلاعات سطوح قیمتی در tooltip
                                    const yValue = context[0].parsed.y;
                                    const closestLevels = levels.filter(l => Math.abs(l.price - yValue) < yValue * 0.05);
                                    if (closestLevels.length > 0) {{
                                        return closestLevels.map(l => l.label).join('\\n');
                                    }}
                                    return '';
                                }}
                            }}
                        }},
                        annotation: {{
                            annotations: annotations
                        }}
                    }},
                    scales: {{
                        y: {{
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: {{
                                display: true,
                                text: 'قیمت (ریال)',
                                font: {{ size: 14, family: 'Tahoma', weight: 'bold' }}
                            }},
                            grid: {{
                                color: 'rgba(200, 200, 200, 0.3)',
                                lineWidth: 1
                            }},
                            ticks: {{
                                callback: function(value) {{
                                    return value.toLocaleString('fa-IR');
                                }},
                                font: {{ size: 12 }}
                            }}
                        }},
                        x: {{
                            display: true,
                            grid: {{
                                display: false
                            }},
                            ticks: {{
                                maxRotation: 45,
                                minRotation: 45,
                                font: {{ size: 11 }}
                            }}
                        }}
                    }}
                }}
            }});
        }})();
        </script>
"""
        
        return html
    
    def get_trading_signals(self) -> Dict:
        """تولید سیگنال‌های معاملاتی بر اساس موقعیت قیمت"""
        
        zones = self.calculate_zones()
        key_levels = self.get_key_levels(top_n=3)
        
        current_zone = zones['current_zone']
        
        # تعیین سیگنال
        if current_zone == 'strong_buy':
            signal = 'خرید قوی'
            confidence = 95
        elif current_zone == 'buy':
            signal = 'خرید'
            confidence = 75
        elif current_zone == 'neutral':
            signal = 'نگهداری'
            confidence = 50
        elif current_zone == 'sell':
            signal = 'فروش'
            confidence = 75
        else:  # strong_sell
            signal = 'فروش قوی'
            confidence = 95
        
        # محاسبه پتانسیل رشد
        avg_intrinsic = zones['neutral_avg']
        upside_potential = ((avg_intrinsic - self.current_price) / self.current_price * 100) if self.current_price > 0 else 0
        
        return {
            'signal': signal,
            'confidence': confidence,
            'current_zone': zones['zones'][current_zone]['label'],
            'upside_potential': upside_potential,
            'target_price': avg_intrinsic,
            'stop_loss': key_levels['strongest_support']['price'] if key_levels['strongest_support'] else self.current_price * 0.90,
            'take_profit': key_levels['strongest_resistance']['price'] if key_levels['strongest_resistance'] else self.current_price * 1.15
        }


def generate_combined_analysis_html(symbol: str, comprehensive_data: Dict, price_df: pd.DataFrame) -> str:
    """
    تولید گزارش HTML کامل تلفیق تحلیل بنیادی و تکنیکال
    
    Parameters:
    -----------
    symbol: نماد سهم
    comprehensive_data: داده‌های تحلیل جامع از JSON
    price_df: دیتافریم قیمت‌ها
    
    Returns:
    --------
    str: کد HTML کامل
    """
    
    chart = FundamentalTechnicalChart(symbol)
    
    # بارگذاری داده‌های ارزشگذاری
    if not chart.load_valuation_data(comprehensive_data):
        return "<p>خطا در بارگذاری داده‌ها</p>"
    
    # تنظیم قیمت فعلی
    current_price = price_df['Adj Close'].iloc[-1]
    chart.set_current_price(current_price)
    
    # طبقه‌بندی سطوح
    chart.classify_price_levels()
    
    # تولید نمودار
    chart_html = chart.generate_chart_html(price_df, days=90)
    
    # دریافت سیگنال‌های معاملاتی
    signals = chart.get_trading_signals()
    
    # تولید HTML نهایی
    html = f"""
    <div style="margin: 30px 0;">
        <h2>🔗 تلفیق تحلیل بنیادی و تکنیکال</h2>
        
        {chart_html}
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
            <h3 style="color: white; margin: 0 0 20px 0;">🎯 سیگنال معاملاتی</h3>
            <div style="font-size: 48px; font-weight: bold; margin: 20px 0;">
                {signals['signal']}
            </div>
            <div style="font-size: 18px; opacity: 0.9;">
                سطح اطمینان: {signals['confidence']}% | پتانسیل رشد: {signals['upside_potential']:+.1f}%
            </div>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.3);">
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; text-align: center;">
                    <div>
                        <div style="font-size: 14px; opacity: 0.8;">قیمت هدف</div>
                        <div style="font-size: 24px; font-weight: bold;">{signals['target_price']:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size: 14px; opacity: 0.8;">حد ضرر</div>
                        <div style="font-size: 24px; font-weight: bold;">{signals['stop_loss']:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size: 14px; opacity: 0.8;">حد سود</div>
                        <div style="font-size: 24px; font-weight: bold;">{signals['take_profit']:,.0f}</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="info-box">
            <strong>💡 توضیح:</strong> این نمودار 18 سطح قیمتی حاصل از 6 روش ارزشگذاری بنیادی (DCF, P/E, P/B, EV/EBITDA, P/S, RIM) 
            در 3 سناریو (خوشبینانه، خنثی، بدبینانه) را روی نمودار تکنیکال نمایش می‌دهد. 
            خطوط سبز (خوشبینانه)، نارنجی (خنثی) و قرمز (بدبینانه) به عنوان سطوح Support/Resistance بنیادی عمل می‌کنند.
        </div>
    </div>
    """
    
    return html


if __name__ == "__main__":
    # تست ماژول
    print("📊 ماژول تلفیق تحلیل بنیادی و تکنیکال")
    print("=" * 70)
    print("این ماژول 18 سطح قیمتی را روی نمودار تکنیکال نمایش می‌دهد:")
    print("  • 6 روش ارزشگذاری × 3 سناریو = 18 سطح")
    print("  • طبقه‌بندی Support/Resistance")
    print("  • تولید سیگنال معاملاتی")
    print("  • نمودار تعاملی با Chart.js")
    print("=" * 70)
