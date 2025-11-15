"""
تحلیل تخصیص منابع بین نمادها
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class ResourceAllocationAnalyzer:
    """تحلیلگر تخصیص منابع مالی"""
    
    def __init__(self, 
                 source_company: str,
                 target_companies: List[str],
                 analyses: Dict[str, Dict],
                 valuations: Dict[str, Dict]):
        """
        Parameters:
        -----------
        source_company: شرکت منبع (دارای مازاد منابع)
        target_companies: لیست شرکت‌های هدف (نیازمند منابع)
        analyses: دیکشنری تحلیل‌های بنیادی
        valuations: دیکشنری ارزش‌گذاری‌ها
        """
        self.source = source_company
        self.targets = target_companies
        self.analyses = analyses
        self.valuations = valuations
        self.allocation_scores = {}
    
    def calculate_financial_health_score(self, company: str) -> float:
        """محاسبه امتیاز سلامت مالی"""
        
        try:
            analysis = self.analyses.get(company, {})
            
            # وزن‌ها
            weights = {
                'profitability': 0.35,
                'liquidity': 0.25,
                'leverage': 0.20,
                'growth': 0.20
            }
            
            score = 0.0
            
            # امتیاز سودآوری
            profitability = analysis.get('profitability', {})
            roe = profitability.get('roe', 0)
            roa = profitability.get('roa', 0)
            profit_margin = profitability.get('net_profit_margin', 0)
            
            prof_score = (
                (min(roe / 0.20, 1.0) * 40) +  # ROE حداکثر 20%
                (min(roa / 0.15, 1.0) * 30) +  # ROA حداکثر 15%
                (min(profit_margin / 0.15, 1.0) * 30)  # Margin حداکثر 15%
            )
            score += prof_score * weights['profitability']
            
            # امتیاز نقدینگی
            liquidity = analysis.get('liquidity', {})
            current_ratio = liquidity.get('current_ratio', 0)
            quick_ratio = liquidity.get('quick_ratio', 0)
            
            liq_score = (
                (min(current_ratio / 2.0, 1.0) * 60) +  # Current Ratio حداکثر 2
                (min(quick_ratio / 1.5, 1.0) * 40)  # Quick Ratio حداکثر 1.5
            )
            score += liq_score * weights['liquidity']
            
            # امتیاز اهرمی (کمتر بهتر)
            leverage = analysis.get('leverage', {})
            debt_to_equity = leverage.get('debt_to_equity', 1.0)
            debt_to_assets = leverage.get('debt_to_assets', 0.5)
            
            lev_score = (
                (max(1.0 - debt_to_equity / 1.0, 0.0) * 60) +  # D/E کمتر از 1
                (max(1.0 - debt_to_assets / 0.6, 0.0) * 40)  # D/A کمتر از 0.6
            )
            score += lev_score * weights['leverage']
            
            # امتیاز رشد
            trends = analysis.get('trends', {})
            cagr_revenue = trends.get('cagr_revenue', 0)
            cagr_profit = trends.get('cagr_profit', 0)
            
            growth_score = (
                (min(cagr_revenue / 0.20, 1.0) * 50) +  # رشد درآمد حداکثر 20%
                (min(cagr_profit / 0.25, 1.0) * 50)  # رشد سود حداکثر 25%
            )
            score += growth_score * weights['growth']
            
            return min(100, max(0, score))
            
        except Exception as e:
            print(f"خطا در محاسبه امتیاز سلامت مالی {company}: {e}")
            return 50.0
    
    def calculate_valuation_attractiveness(self, company: str) -> float:
        """محاسبه جذابیت ارزش‌گذاری"""
        
        try:
            valuation = self.valuations.get(company, {})
            
            # مقایسه ارزش ذاتی با قیمت بازار
            # اگر ارزش ذاتی > قیمت بازار: جذاب
            
            # فرض: ارزش‌گذاری خنثی را به عنوان مبنا می‌گیریم
            neutral_val = valuation.get('خنثی', {})
            optimistic_val = valuation.get('خوشبینانه', {})
            pessimistic_val = valuation.get('بدبینانه', {})
            
            if not neutral_val:
                return 50.0
            
            avg_val_neutral = neutral_val.get('average_valuation', 0)
            avg_val_optimistic = optimistic_val.get('average_valuation', 0) if optimistic_val else 0
            avg_val_pessimistic = pessimistic_val.get('average_valuation', 0) if pessimistic_val else 0
            
            # امتیاز بر اساس پتانسیل رشد
            if avg_val_optimistic > 0 and avg_val_neutral > 0:
                upside_potential = (avg_val_optimistic - avg_val_neutral) / avg_val_neutral
                downside_risk = (avg_val_neutral - avg_val_pessimistic) / avg_val_neutral if avg_val_pessimistic > 0 else 0
                
                # نسبت ریسک به بازده
                risk_reward = upside_potential / (downside_risk + 0.01)
                
                # امتیاز از 0 تا 100
                score = min(100, max(0, 50 + (risk_reward - 1) * 25))
                return score
            
            return 50.0
            
        except Exception as e:
            print(f"خطا در محاسبه جذابیت ارزش‌گذاری {company}: {e}")
            return 50.0
    
    def calculate_risk_score(self, company: str) -> float:
        """محاسبه امتیاز ریسک (0-100، کمتر = ریسک بیشتر)"""
        
        try:
            analysis = self.analyses.get(company, {})
            
            risk_score = 100.0
            
            # ریسک نقدینگی
            liquidity = analysis.get('liquidity', {})
            current_ratio = liquidity.get('current_ratio', 0)
            if current_ratio < 1.0:
                risk_score -= 20
            elif current_ratio < 1.5:
                risk_score -= 10
            
            # ریسک اهرمی
            leverage = analysis.get('leverage', {})
            debt_to_equity = leverage.get('debt_to_equity', 0)
            if debt_to_equity > 1.5:
                risk_score -= 25
            elif debt_to_equity > 1.0:
                risk_score -= 15
            
            # ریسک سودآوری
            profitability = analysis.get('profitability', {})
            roe = profitability.get('roe', 0)
            if roe < 0:
                risk_score -= 30
            elif roe < 0.10:
                risk_score -= 15
            
            # ریسک رشد منفی
            trends = analysis.get('trends', {})
            cagr_revenue = trends.get('cagr_revenue', 0)
            if cagr_revenue < 0:
                risk_score -= 20
            
            return max(0, min(100, risk_score))
            
        except Exception as e:
            print(f"خطا در محاسبه امتیاز ریسک {company}: {e}")
            return 50.0
    
    def calculate_allocation_score(self, target_company: str) -> Dict[str, any]:
        """محاسبه امتیاز کلی تخصیص منابع"""
        
        # وزن‌های معیارها
        weights = {
            'financial_health': 0.35,
            'valuation': 0.25,
            'risk': 0.15,
            'growth': 0.25
        }
        
        # محاسبه امتیازها
        health_score = self.calculate_financial_health_score(target_company)
        valuation_score = self.calculate_valuation_attractiveness(target_company)
        risk_score = self.calculate_risk_score(target_company)
        
        # امتیاز رشد از تحلیل بنیادی
        analysis = self.analyses.get(target_company, {})
        trends = analysis.get('trends', {})
        cagr_revenue = trends.get('cagr_revenue', 0)
        growth_score = min(100, max(0, 50 + (cagr_revenue - 0.10) * 200))
        
        # امتیاز کلی
        total_score = (
            health_score * weights['financial_health'] +
            valuation_score * weights['valuation'] +
            risk_score * weights['risk'] +
            growth_score * weights['growth']
        )
        
        return {
            'company': target_company,
            'total_score': total_score,
            'health_score': health_score,
            'valuation_score': valuation_score,
            'risk_score': risk_score,
            'growth_score': growth_score,
            'weights': weights
        }
    
    def analyze_allocation(self) -> Dict[str, any]:
        """تحلیل جامع تخصیص منابع"""
        
        print(f"\n{'='*70}")
        print(f"تحلیل تخصیص منابع از {self.source} به شرکت‌های هدف")
        print(f"{'='*70}")
        
        results = {
            'source': self.source,
            'targets': {},
            'ranking': []
        }
        
        # محاسبه امتیاز برای هر شرکت هدف
        for target in self.targets:
            score_data = self.calculate_allocation_score(target)
            results['targets'][target] = score_data
            results['ranking'].append((target, score_data['total_score']))
            
            print(f"\n📊 {target}:")
            print(f"  امتیاز کل: {score_data['total_score']:.1f}/100")
            print(f"  ├─ سلامت مالی: {score_data['health_score']:.1f}/100")
            print(f"  ├─ جذابیت ارزش‌گذاری: {score_data['valuation_score']:.1f}/100")
            print(f"  ├─ امتیاز ریسک: {score_data['risk_score']:.1f}/100")
            print(f"  └─ پتانسیل رشد: {score_data['growth_score']:.1f}/100")
        
        # رتبه‌بندی
        results['ranking'].sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n{'='*70}")
        print("🏆 رتبه‌بندی اولویت تخصیص منابع:")
        print(f"{'='*70}")
        
        for rank, (company, score) in enumerate(results['ranking'], 1):
            recommendation = self._get_recommendation(score)
            print(f"{rank}. {company}: {score:.1f}/100 - {recommendation}")
        
        return results
    
    def _get_recommendation(self, score: float) -> str:
        """توصیه بر اساس امتیاز"""
        if score >= 75:
            return "✅ توصیه می‌شود (اولویت بالا)"
        elif score >= 60:
            return "⚠️ قابل توجه (با احتیاط)"
        elif score >= 50:
            return "⚡ نیاز به بررسی بیشتر"
        else:
            return "❌ توصیه نمی‌شود"
    
    def generate_detailed_report(self) -> pd.DataFrame:
        """تولید گزارش تفصیلی به صورت DataFrame"""
        
        data = []
        for target in self.targets:
            score_data = self.allocation_scores.get(target, 
                         self.calculate_allocation_score(target))
            
            data.append({
                'شرکت': target,
                'امتیاز کل': score_data['total_score'],
                'سلامت مالی': score_data['health_score'],
                'ارزش‌گذاری': score_data['valuation_score'],
                'ریسک': score_data['risk_score'],
                'رشد': score_data['growth_score'],
                'توصیه': self._get_recommendation(score_data['total_score'])
            })
        
        df = pd.DataFrame(data)
        df = df.sort_values('امتیاز کل', ascending=False).reset_index(drop=True)
        df.index = df.index + 1
        df.index.name = 'رتبه'
        
        return df


if __name__ == "__main__":
    # تست تحلیلگر تخصیص منابع
    pass
