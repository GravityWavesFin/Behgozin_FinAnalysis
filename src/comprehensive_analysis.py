"""
تحلیل جامع: بنیادی + تکنیکال + پیش‌بینی 3 ماهه
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from datetime import datetime, timedelta


class ComprehensiveAnalysis:
    """تحلیل جامع شرکت با پیش‌بینی 3 ماهه"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.analysis_result = {}
    
    def analyze_fundamentals(self, financial_data: Dict) -> Dict:
        """تحلیل بنیادی با نسبت‌های واقعی"""
        
        fundamentals = {
            'profitability': {},
            'liquidity': {},
            'leverage': {},
            'efficiency': {},
            'market_ratios': {},
            'score': 0,
            'grade': 'N/A'
        }
        
        try:
            revenue = financial_data.get('revenue', 0)
            net_income = financial_data.get('net_income', 0)
            operating_profit = financial_data.get('operating_profit', 0)
            total_assets = financial_data.get('total_assets', 0)
            total_equity = financial_data.get('total_equity', 0)
            total_debt = financial_data.get('total_debt', 0)
            cash = financial_data.get('cash', 0)
            
            # نسبت‌های سودآوری (به صورت decimal: 0.05 = 5%)
            if revenue > 0:
                fundamentals['profitability']['net_margin'] = net_income / revenue
                fundamentals['profitability']['operating_margin'] = operating_profit / revenue
            
            if total_assets > 0:
                fundamentals['profitability']['roa'] = net_income / total_assets
            
            if total_equity > 0:
                fundamentals['profitability']['roe'] = net_income / total_equity
            
            # نسبت‌های نقدینگی و اهرمی
            if total_equity > 0:
                fundamentals['leverage']['debt_to_equity'] = total_debt / total_equity
            
            if total_assets > 0:
                fundamentals['leverage']['debt_ratio'] = total_debt / total_assets
                fundamentals['liquidity']['cash_ratio'] = cash / total_assets
            
            # کارایی
            if total_assets > 0:
                fundamentals['efficiency']['asset_turnover'] = revenue / total_assets
            
            # امتیازدهی (0-100)
            score = 0
            
            # سودآوری (40 امتیاز) - نسبت‌ها decimal هستند (0.2 = 20%)
            roe = fundamentals['profitability'].get('roe', 0)
            if roe > 0.20: score += 20
            elif roe > 0.15: score += 15
            elif roe > 0.10: score += 10
            elif roe > 0.05: score += 5
            
            net_margin = fundamentals['profitability'].get('net_margin', 0)
            if net_margin > 0.20: score += 20
            elif net_margin > 0.15: score += 15
            elif net_margin > 0.10: score += 10
            elif net_margin > 0.05: score += 5
            
            # اهرم مالی (20 امتیاز) - کمتر بهتر
            d_to_e = fundamentals['leverage'].get('debt_to_equity', 0)
            if d_to_e < 0.5: score += 20
            elif d_to_e < 1.0: score += 15
            elif d_to_e < 1.5: score += 10
            elif d_to_e < 2.0: score += 5
            
            # کارایی (20 امتیاز)
            asset_turn = fundamentals['efficiency'].get('asset_turnover', 0)
            if asset_turn > 2: score += 20
            elif asset_turn > 1.5: score += 15
            elif asset_turn > 1: score += 10
            elif asset_turn > 0.5: score += 5
            
            # نقدینگی (20 امتیاز)
            cash_ratio = fundamentals['liquidity'].get('cash_ratio', 0)
            if cash_ratio > 0.3: score += 20
            elif cash_ratio > 0.2: score += 15
            elif cash_ratio > 0.1: score += 10
            elif cash_ratio > 0.05: score += 5
            
            fundamentals['score'] = score
            
            # رتبه‌بندی
            if score >= 80:
                fundamentals['grade'] = 'A'
            elif score >= 60:
                fundamentals['grade'] = 'B'
            elif score >= 40:
                fundamentals['grade'] = 'C'
            elif score >= 20:
                fundamentals['grade'] = 'D'
            else:
                fundamentals['grade'] = 'F'
                
        except Exception as e:
            print(f"خطا در تحلیل بنیادی {self.symbol}: {e}")
        
        return fundamentals
    
    def analyze_technical(self, price_data: pd.DataFrame) -> Dict:
        """تحلیل تکنیکال"""
        
        technical = {
            'trend': 'خنثی',
            'support': 0,
            'resistance': 0,
            'rsi': 50,
            'macd_signal': 'خنثی',
            'moving_averages': {},
            'volatility': 0,
            'momentum_score': 0
        }
        
        try:
            if price_data.empty or len(price_data) < 20:
                return technical
            
            # استفاده از قیمت‌های تعدیل شده
            closes = price_data['Adj Close'].values if 'Adj Close' in price_data.columns else price_data['Close'].values
            volumes = price_data['Volume'].values if 'Volume' in price_data.columns else price_data['volume'].values
            
            # میانگین‌های متحرک
            if len(closes) >= 50:
                technical['moving_averages']['ma_10'] = closes[-10:].mean()
                technical['moving_averages']['ma_20'] = closes[-20:].mean()
                technical['moving_averages']['ma_50'] = closes[-50:].mean()
                
                # تشخیص روند
                current_price = closes[-1]
                ma_10 = technical['moving_averages']['ma_10']
                ma_20 = technical['moving_averages']['ma_20']
                ma_50 = technical['moving_averages']['ma_50']
                
                if current_price > ma_10 > ma_20 > ma_50:
                    technical['trend'] = 'صعودی قوی'
                elif current_price > ma_10 > ma_20:
                    technical['trend'] = 'صعودی'
                elif current_price < ma_10 < ma_20 < ma_50:
                    technical['trend'] = 'نزولی قوی'
                elif current_price < ma_10 < ma_20:
                    technical['trend'] = 'نزولی'
            
            # RSI
            if len(closes) >= 14:
                deltas = np.diff(closes[-15:])
                gains = np.where(deltas > 0, deltas, 0)
                losses = np.where(deltas < 0, -deltas, 0)
                
                avg_gain = gains.mean()
                avg_loss = losses.mean()
                
                if avg_loss != 0:
                    rs = avg_gain / avg_loss
                    technical['rsi'] = 100 - (100 / (1 + rs))
                else:
                    technical['rsi'] = 100
            
            # حمایت و مقاومت (بر اساس 60 روز اخیر)
            recent_prices = closes[-60:] if len(closes) >= 60 else closes
            technical['support'] = recent_prices.min()
            technical['resistance'] = recent_prices.max()
            
            # نوسان (انحراف معیار 20 روز)
            if len(closes) >= 20:
                technical['volatility'] = (closes[-20:].std() / closes[-20:].mean()) * 100
            
            # امتیاز مومنتوم (0-100)
            momentum = 0
            
            # روند (40 امتیاز)
            if technical['trend'] == 'صعودی قوی':
                momentum += 40
            elif technical['trend'] == 'صعودی':
                momentum += 30
            elif technical['trend'] == 'خنثی':
                momentum += 20
            elif technical['trend'] == 'نزولی':
                momentum += 10
            
            # RSI (30 امتیاز)
            rsi = technical['rsi']
            if 40 <= rsi <= 60:  # محدوده خنثی
                momentum += 20
            elif 60 < rsi <= 70:  # قدری گرم
                momentum += 25
            elif 30 <= rsi < 40:  # قدری سرد
                momentum += 15
            elif rsi > 70:  # خرید بیش از حد
                momentum += 10
            elif rsi < 30:  # فروش بیش از حد - فرصت خرید
                momentum += 30
            
            # نوسان (30 امتیاز) - کمتر بهتر
            vol = technical['volatility']
            if vol < 20:
                momentum += 30
            elif vol < 30:
                momentum += 20
            elif vol < 40:
                momentum += 10
            elif vol < 50:
                momentum += 5
            
            technical['momentum_score'] = momentum
            
        except Exception as e:
            print(f"خطا در تحلیل تکنیکال {self.symbol}: {e}")
        
        return technical
    
    def predict_3month_target(self, current_price: float, valuation: float, 
                             fundamental_score: int, technical_score: int) -> Dict:
        """پیش‌بینی قیمت هدف 3 ماهه با رویکرد محافظه‌کارانه"""
        
        prediction = {
            'current_price': current_price,
            'intrinsic_value': valuation,
            'target_3month': current_price,
            'upside_pct': 0,
            'expected_return_3month': 0,
            'confidence': 'پایین',
            'risk_level': 'متوسط'
        }
        
        try:
            # محاسبه اختلاف قیمت فعلی با ارزش ذاتی
            if current_price > 0:
                intrinsic_upside = ((valuation - current_price) / current_price) * 100
                
                # محدود کردن upside به محدوده منطقی (حداکثر 50% در 3 ماه)
                capped_upside = max(-30, min(50, intrinsic_upside))
                
                # تعدیل بر اساس امتیازات بنیادی و تکنیکال
                combined_score = (fundamental_score * 0.6 + technical_score * 0.4)
                
                # ضریب اطمینان (0.3 تا 0.8)
                confidence_factor = 0.3 + (combined_score / 100) * 0.5
                
                # بازده مورد انتظار 3 ماهه (با ضریب اطمینان)
                expected_3month = capped_upside * confidence_factor
                
                # قیمت هدف
                target_price = current_price * (1 + expected_3month / 100)
                
                prediction['target_3month'] = target_price
                prediction['upside_pct'] = ((target_price - current_price) / current_price) * 100
                prediction['expected_return_3month'] = expected_3month
                
                # سطح اطمینان
                if combined_score >= 70:
                    prediction['confidence'] = 'بالا'
                elif combined_score >= 50:
                    prediction['confidence'] = 'متوسط'
                else:
                    prediction['confidence'] = 'پایین'
                
                # سطح ریسک
                if abs(expected_3month) > 30:
                    prediction['risk_level'] = 'بالا'
                elif abs(expected_3month) > 15:
                    prediction['risk_level'] = 'متوسط'
                else:
                    prediction['risk_level'] = 'پایین'
                
        except Exception as e:
            print(f"خطا در پیش‌بینی 3 ماهه {self.symbol}: {e}")
        
        return prediction
    
    def comprehensive_analysis(self, financial_data: Dict, price_data: pd.DataFrame,
                              current_price: float, valuation: float) -> Dict:
        """تحلیل جامع کامل"""
        
        # تحلیل بنیادی
        fundamentals = self.analyze_fundamentals(financial_data)
        
        # تحلیل تکنیکال
        technical = self.analyze_technical(price_data)
        
        # پیش‌بینی 3 ماهه
        prediction = self.predict_3month_target(
            current_price, 
            valuation,
            fundamentals['score'],
            technical['momentum_score']
        )
        
        # امتیاز کلی (0-100)
        overall_score = (fundamentals['score'] * 0.6 + technical['momentum_score'] * 0.4)
        
        # توصیه نهایی
        if overall_score >= 70 and prediction['upside_pct'] > 10:
            recommendation = 'خرید قوی'
        elif overall_score >= 60 and prediction['upside_pct'] > 5:
            recommendation = 'خرید'
        elif overall_score >= 40 and prediction['upside_pct'] > -5:
            recommendation = 'نگهداری'
        elif overall_score >= 30 or prediction['upside_pct'] > -10:
            recommendation = 'فروش'
        else:
            recommendation = 'فروش قوی'
        
        return {
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'fundamentals': fundamentals,
            'technical': technical,
            'prediction': prediction,
            'overall_score': overall_score,
            'recommendation': recommendation
        }
