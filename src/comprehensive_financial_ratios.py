#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ماژول محاسبه کامل نسبت‌های مالی
"""

import pandas as pd
from typing import Dict

class ComprehensiveFinancialRatios:
    """محاسبه تمام نسبت‌های مالی برای تحلیل بنیادی کامل"""
    
    def __init__(self, financial_data: Dict):
        """
        financial_data شامل:
        - revenue: درآمد
        - net_income: سود خالص
        - operating_profit: سود عملیاتی
        - ebitda: EBITDA
        - total_assets: کل دارایی‌ها
        - total_equity: حقوق صاحبان سهام
        - total_debt: کل بدهی‌ها
        - cash: وجه نقد
        - shares_outstanding: تعداد سهام
        - capital: سرمایه
        """
        self.data = financial_data
        self.ratios = {}
    
    def calculate_all_ratios(self) -> Dict:
        """محاسبه تمام نسبت‌های مالی"""
        
        # 1. نسبت‌های سودآوری (Profitability Ratios)
        self.ratios['profitability'] = self._calculate_profitability()
        
        # 2. نسبت‌های نقدینگی (Liquidity Ratios)
        self.ratios['liquidity'] = self._calculate_liquidity()
        
        # 3. نسبت‌های اهرمی (Leverage Ratios)
        self.ratios['leverage'] = self._calculate_leverage()
        
        # 4. نسبت‌های کارایی (Efficiency Ratios)
        self.ratios['efficiency'] = self._calculate_efficiency()
        
        # 5. نسبت‌های بازار (Market Ratios)
        self.ratios['market'] = self._calculate_market_ratios()
        
        # 6. نسبت‌های رشد (Growth Ratios)
        self.ratios['growth'] = self._calculate_growth()
        
        # 7. نسبت‌های پوشش (Coverage Ratios)
        self.ratios['coverage'] = self._calculate_coverage()
        
        return self.ratios
    
    def _calculate_profitability(self) -> Dict:
        """نسبت‌های سودآوری"""
        revenue = self.data.get('revenue', 0)
        net_income = self.data.get('net_income', 0)
        operating_profit = self.data.get('operating_profit', 0)
        ebitda = self.data.get('ebitda', 0)
        total_assets = self.data.get('total_assets', 0)
        total_equity = self.data.get('total_equity', 0)
        
        ratios = {}
        
        # 1. حاشیه سود خالص (Net Profit Margin)
        if revenue > 0:
            ratios['net_profit_margin'] = (net_income / revenue)
            ratios['net_profit_margin_pct'] = ratios['net_profit_margin'] * 100
        else:
            ratios['net_profit_margin'] = 0
            ratios['net_profit_margin_pct'] = 0
        
        # 2. حاشیه سود عملیاتی (Operating Profit Margin)
        if revenue > 0:
            ratios['operating_profit_margin'] = (operating_profit / revenue)
            ratios['operating_profit_margin_pct'] = ratios['operating_profit_margin'] * 100
        else:
            ratios['operating_profit_margin'] = 0
            ratios['operating_profit_margin_pct'] = 0
        
        # 3. حاشیه EBITDA
        if revenue > 0:
            ratios['ebitda_margin'] = (ebitda / revenue)
            ratios['ebitda_margin_pct'] = ratios['ebitda_margin'] * 100
        else:
            ratios['ebitda_margin'] = 0
            ratios['ebitda_margin_pct'] = 0
        
        # 4. بازده دارایی‌ها (ROA)
        if total_assets > 0:
            ratios['roa'] = (net_income / total_assets)
            ratios['roa_pct'] = ratios['roa'] * 100
        else:
            ratios['roa'] = 0
            ratios['roa_pct'] = 0
        
        # 5. بازده حقوق صاحبان سهام (ROE)
        if total_equity > 0:
            ratios['roe'] = (net_income / total_equity)
            ratios['roe_pct'] = ratios['roe'] * 100
        else:
            ratios['roe'] = 0
            ratios['roe_pct'] = 0
        
        # 6. بازده سرمایه به‌کار گرفته شده (ROIC)
        total_debt = self.data.get('total_debt', 0)
        invested_capital = total_equity + total_debt
        if invested_capital > 0:
            nopat = operating_profit * 0.75  # فرض: نرخ مالیات 25%
            ratios['roic'] = (nopat / invested_capital)
            ratios['roic_pct'] = ratios['roic'] * 100
        else:
            ratios['roic'] = 0
            ratios['roic_pct'] = 0
        
        # 7. بازده دارایی‌های عملیاتی (ROOA)
        if total_assets > 0:
            ratios['rooa'] = (operating_profit / total_assets)
            ratios['rooa_pct'] = ratios['rooa'] * 100
        else:
            ratios['rooa'] = 0
            ratios['rooa_pct'] = 0
        
        return ratios
    
    def _calculate_liquidity(self) -> Dict:
        """نسبت‌های نقدینگی"""
        cash = self.data.get('cash', 0)
        total_assets = self.data.get('total_assets', 0)
        total_debt = self.data.get('total_debt', 0)
        
        ratios = {}
        
        # 1. نسبت نقدی (Cash Ratio)
        # فرض: بدهی جاری = 70% از کل بدهی
        current_liabilities = total_debt * 0.7 if total_debt > 0 else 1
        ratios['cash_ratio'] = (cash / current_liabilities) if current_liabilities > 0 else 0
        
        # 2. نسبت جاری (Current Ratio)
        # فرض: دارایی جاری = 60% از کل دارایی
        current_assets = total_assets * 0.6
        ratios['current_ratio'] = (current_assets / current_liabilities) if current_liabilities > 0 else 0
        
        # 3. نسبت آنی (Quick Ratio)
        # فرض: موجودی کالا = 20% از دارایی جاری
        inventory = current_assets * 0.2
        ratios['quick_ratio'] = ((current_assets - inventory) / current_liabilities) if current_liabilities > 0 else 0
        
        # 4. سرمایه در گردش (Working Capital)
        ratios['working_capital'] = current_assets - current_liabilities
        ratios['working_capital_ratio'] = (ratios['working_capital'] / total_assets) if total_assets > 0 else 0
        
        # 5. نسبت وجه نقد به کل دارایی
        ratios['cash_to_assets'] = (cash / total_assets) if total_assets > 0 else 0
        
        return ratios
    
    def _calculate_leverage(self) -> Dict:
        """نسبت‌های اهرمی"""
        total_assets = self.data.get('total_assets', 0)
        total_equity = self.data.get('total_equity', 0)
        total_debt = self.data.get('total_debt', 0)
        ebitda = self.data.get('ebitda', 0)
        
        ratios = {}
        
        # 1. نسبت بدهی به حقوق صاحبان سهام (D/E)
        if total_equity > 0:
            ratios['debt_to_equity'] = (total_debt / total_equity)
        else:
            ratios['debt_to_equity'] = 0
        
        # 2. نسبت بدهی به دارایی (Debt Ratio)
        if total_assets > 0:
            ratios['debt_ratio'] = (total_debt / total_assets)
            ratios['debt_ratio_pct'] = ratios['debt_ratio'] * 100
        else:
            ratios['debt_ratio'] = 0
            ratios['debt_ratio_pct'] = 0
        
        # 3. نسبت حقوق صاحبان سهام به دارایی (Equity Ratio)
        if total_assets > 0:
            ratios['equity_ratio'] = (total_equity / total_assets)
            ratios['equity_ratio_pct'] = ratios['equity_ratio'] * 100
        else:
            ratios['equity_ratio'] = 0
            ratios['equity_ratio_pct'] = 0
        
        # 4. ضریب اهرمی (Leverage Multiplier)
        if total_equity > 0:
            ratios['leverage_multiplier'] = (total_assets / total_equity)
        else:
            ratios['leverage_multiplier'] = 0
        
        # 5. نسبت بدهی به EBITDA
        if ebitda > 0:
            ratios['debt_to_ebitda'] = (total_debt / ebitda)
        else:
            ratios['debt_to_ebitda'] = 0
        
        # 6. نسبت پوشش بهره
        interest_expense = total_debt * 0.15  # فرض: نرخ بهره 15%
        if interest_expense > 0:
            ratios['interest_coverage'] = (ebitda / interest_expense)
        else:
            ratios['interest_coverage'] = 0
        
        return ratios
    
    def _calculate_efficiency(self) -> Dict:
        """نسبت‌های کارایی"""
        revenue = self.data.get('revenue', 0)
        total_assets = self.data.get('total_assets', 0)
        total_equity = self.data.get('total_equity', 0)
        
        ratios = {}
        
        # 1. گردش دارایی‌ها (Asset Turnover)
        if total_assets > 0:
            ratios['asset_turnover'] = (revenue / total_assets)
        else:
            ratios['asset_turnover'] = 0
        
        # 2. گردش حقوق صاحبان سهام (Equity Turnover)
        if total_equity > 0:
            ratios['equity_turnover'] = (revenue / total_equity)
        else:
            ratios['equity_turnover'] = 0
        
        # 3. گردش دارایی‌های ثابت (Fixed Asset Turnover)
        # فرض: دارایی ثابت = 40% از کل دارایی
        fixed_assets = total_assets * 0.4
        if fixed_assets > 0:
            ratios['fixed_asset_turnover'] = (revenue / fixed_assets)
        else:
            ratios['fixed_asset_turnover'] = 0
        
        # 4. گردش سرمایه در گردش
        working_capital = self.ratios.get('liquidity', {}).get('working_capital', 0)
        if working_capital > 0:
            ratios['working_capital_turnover'] = (revenue / working_capital)
        else:
            ratios['working_capital_turnover'] = 0
        
        return ratios
    
    def _calculate_market_ratios(self) -> Dict:
        """نسبت‌های بازار"""
        net_income = self.data.get('net_income', 0)
        revenue = self.data.get('revenue', 0)
        total_equity = self.data.get('total_equity', 0)
        shares_outstanding = self.data.get('shares_outstanding', 0)
        ebitda = self.data.get('ebitda', 0)
        
        ratios = {}
        
        # 1. سود هر سهم (EPS)
        if shares_outstanding > 0:
            ratios['eps'] = (net_income * 1_000_000) / shares_outstanding  # تبدیل به ریال
        else:
            ratios['eps'] = 0
        
        # 2. ارزش دفتری هر سهم (Book Value per Share)
        if shares_outstanding > 0:
            ratios['book_value_per_share'] = (total_equity * 1_000_000) / shares_outstanding
        else:
            ratios['book_value_per_share'] = 0
        
        # 3. فروش هر سهم (Sales per Share)
        if shares_outstanding > 0:
            ratios['sales_per_share'] = (revenue * 1_000_000) / shares_outstanding
        else:
            ratios['sales_per_share'] = 0
        
        # 4. EBITDA per Share
        if shares_outstanding > 0:
            ratios['ebitda_per_share'] = (ebitda * 1_000_000) / shares_outstanding
        else:
            ratios['ebitda_per_share'] = 0
        
        # 5. نسبت سود به ارزش دفتری (P/B potential)
        if total_equity > 0:
            ratios['pb_potential'] = (net_income / total_equity)
        else:
            ratios['pb_potential'] = 0
        
        return ratios
    
    def _calculate_growth(self) -> Dict:
        """نسبت‌های رشد (در صورت وجود داده تاریخی)"""
        ratios = {}
        
        # این نسبت‌ها نیاز به داده‌های چند دوره دارند
        # فعلاً مقادیر پیش‌فرض
        ratios['revenue_growth'] = 0
        ratios['net_income_growth'] = 0
        ratios['eps_growth'] = 0
        ratios['asset_growth'] = 0
        ratios['equity_growth'] = 0
        
        return ratios
    
    def _calculate_coverage(self) -> Dict:
        """نسبت‌های پوشش"""
        ebitda = self.data.get('ebitda', 0)
        operating_profit = self.data.get('operating_profit', 0)
        total_debt = self.data.get('total_debt', 0)
        
        ratios = {}
        
        # 1. نسبت پوشش سود عملیاتی
        interest_expense = total_debt * 0.15
        if interest_expense > 0:
            ratios['operating_income_coverage'] = (operating_profit / interest_expense)
        else:
            ratios['operating_income_coverage'] = 0
        
        # 2. نسبت پوشش خدمات بدهی
        # فرض: اصل و فرع بدهی = 20% از بدهی سالانه
        debt_service = total_debt * 0.2
        if debt_service > 0:
            ratios['debt_service_coverage'] = (ebitda / debt_service)
        else:
            ratios['debt_service_coverage'] = 0
        
        # 3. نسبت پوشش جریان نقدی
        cash_flow = ebitda * 0.8  # تخمین جریان نقدی عملیاتی
        if debt_service > 0:
            ratios['cash_flow_coverage'] = (cash_flow / debt_service)
        else:
            ratios['cash_flow_coverage'] = 0
        
        return ratios
    
    def get_ratio_analysis(self) -> Dict:
        """تحلیل و امتیازدهی نسبت‌ها"""
        analysis = {}
        
        profitability = self.ratios.get('profitability', {})
        liquidity = self.ratios.get('liquidity', {})
        leverage = self.ratios.get('leverage', {})
        efficiency = self.ratios.get('efficiency', {})
        
        # تحلیل سودآوری
        roe = profitability.get('roe', 0)
        roa = profitability.get('roa', 0)
        npm = profitability.get('net_profit_margin', 0)
        
        if roe > 0.25:
            analysis['profitability_status'] = 'عالی'
            analysis['profitability_score'] = 90
        elif roe > 0.15:
            analysis['profitability_status'] = 'خوب'
            analysis['profitability_score'] = 70
        elif roe > 0.10:
            analysis['profitability_status'] = 'متوسط'
            analysis['profitability_score'] = 50
        else:
            analysis['profitability_status'] = 'ضعیف'
            analysis['profitability_score'] = 30
        
        # تحلیل نقدینگی
        current_ratio = liquidity.get('current_ratio', 0)
        if current_ratio > 2:
            analysis['liquidity_status'] = 'عالی'
            analysis['liquidity_score'] = 90
        elif current_ratio > 1.5:
            analysis['liquidity_status'] = 'خوب'
            analysis['liquidity_score'] = 70
        elif current_ratio > 1:
            analysis['liquidity_status'] = 'متوسط'
            analysis['liquidity_score'] = 50
        else:
            analysis['liquidity_status'] = 'ضعیف'
            analysis['liquidity_score'] = 30
        
        # تحلیل اهرم
        de_ratio = leverage.get('debt_to_equity', 0)
        if de_ratio < 0.3:
            analysis['leverage_status'] = 'عالی (بدهی کم)'
            analysis['leverage_score'] = 90
        elif de_ratio < 0.6:
            analysis['leverage_status'] = 'خوب'
            analysis['leverage_score'] = 70
        elif de_ratio < 1.0:
            analysis['leverage_status'] = 'متوسط'
            analysis['leverage_score'] = 50
        else:
            analysis['leverage_status'] = 'ضعیف (بدهی زیاد)'
            analysis['leverage_score'] = 30
        
        # تحلیل کارایی
        asset_turnover = efficiency.get('asset_turnover', 0)
        if asset_turnover > 1.5:
            analysis['efficiency_status'] = 'عالی'
            analysis['efficiency_score'] = 90
        elif asset_turnover > 1.0:
            analysis['efficiency_status'] = 'خوب'
            analysis['efficiency_score'] = 70
        elif asset_turnover > 0.5:
            analysis['efficiency_status'] = 'متوسط'
            analysis['efficiency_score'] = 50
        else:
            analysis['efficiency_status'] = 'ضعیف'
            analysis['efficiency_score'] = 30
        
        # امتیاز کلی
        analysis['overall_score'] = (
            analysis['profitability_score'] * 0.35 +
            analysis['liquidity_score'] * 0.20 +
            analysis['leverage_score'] * 0.25 +
            analysis['efficiency_score'] * 0.20
        )
        
        if analysis['overall_score'] >= 80:
            analysis['overall_status'] = 'عالی'
            analysis['grade'] = 'A'
        elif analysis['overall_score'] >= 65:
            analysis['overall_status'] = 'خوب'
            analysis['grade'] = 'B'
        elif analysis['overall_score'] >= 50:
            analysis['overall_status'] = 'متوسط'
            analysis['grade'] = 'C'
        else:
            analysis['overall_status'] = 'ضعیف'
            analysis['grade'] = 'D'
        
        return analysis
