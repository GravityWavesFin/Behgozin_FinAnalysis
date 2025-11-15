"""
پارسر داده‌های مالی - استخراج اطلاعات کلیدی از DataFrame‌های خام
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
import re


class FinancialParser:
    """پارس و استخراج متریک‌های کلیدی از داده‌های مالی"""
    
    def __init__(self):
        # کلمات کلیدی برای جستجو در صورت‌های مالی
        self.keywords = {
            'revenue': ['خالص فروش', 'درآمد عملیاتی', 'خالص درآمد عملیاتی', 'درآمدهای عملیاتی'],
            'net_income': ['سود(زیان) خالص عملیات', 'سود(زیان) خالص', 'سود (زیان) خالص', 'سود خالص', 'سود یا زیان خالص'],
            'ebitda': ['EBITDA', 'سود عملیاتی', 'سود(زیان) عملیاتی', 'سود (زیان) عملیاتی'],
            'total_assets': ['جمع دارایی', 'کل دارایی', 'جمع کل دارایی'],
            'total_equity': ['جمع حقوق صاحبان سهام', 'حقوق صاحبان سهام', 'جمع حقوق'],
            'total_debt': ['جمع بدهی', 'بدهی های بلند', 'تسهیلات'],
            'cash': ['موجودی نقد', 'وجه نقد', 'نقد و بانک'],
            'operating_profit': ['سود(زیان) عملیاتی', 'سود (زیان) عملیاتی', 'سود عملیاتی'],
            'capital': ['سرمایه'],
            'eps': ['سود(زیان) خالص هر سهم', 'سود (زیان) خالص هر سهم', 'سود خالص هر سهم'],
        }
    
    def clean_value(self, value) -> float:
        """تمیز کردن و تبدیل مقادیر به عدد"""
        if pd.isna(value) or value == '-' or value == '':
            return 0.0
        
        try:
            # حذف کاما و تبدیل به float
            if isinstance(value, str):
                value = value.replace(',', '').replace('،', '').strip()
                # حذف کاراکترهای غیرعددی
                value = re.sub(r'[^\d.-]', '', value)
            return float(value) if value else 0.0
        except:
            return 0.0
    
    def find_row_by_keywords(self, df: pd.DataFrame, keywords: list) -> Optional[int]:
        """پیدا کردن ردیف بر اساس کلمات کلیدی"""
        if df.empty:
            return None
        
        # جستجو در ستون اول (معمولاً نام ردیف‌ها اینجاست)
        first_col = df.iloc[:, 0].astype(str)
        
        # Pass 1: Try exact match first (برای کلماتی مثل 'سرمایه' که ممکنه جزئی از کلمه دیگه باشن)
        for keyword in keywords:
            for idx, cell in enumerate(first_col):
                cell_clean = cell.strip()
                if cell_clean == keyword:
                    return idx
        
        # Pass 2: Try contains match (برای کلمات ترکیبی)
        for keyword in keywords:
            for idx, cell in enumerate(first_col):
                if keyword in cell:
                    return idx
        return None
    
    def extract_latest_value(self, df: pd.DataFrame, row_idx: int) -> float:
        """استخراج آخرین مقدار (جدیدترین دوره) از یک ردیف"""
        if row_idx is None or df.empty:
            return 0.0
        
        try:
            # آخرین ستون با مقدار معتبر (معمولا ستون 1 یا 2 جدیدترین است)
            row = df.iloc[row_idx]
            
            # اول ستون‌های اول رو چک کن (معمولا جدیدترین دوره)
            for col in df.columns[1:6]:  # ستون‌های 1 تا 5
                val = self.clean_value(row[col])
                if val != 0:
                    return val
            
            # اگر نبود، از آخر شروع کن
            for col in reversed(df.columns[1:]):
                val = self.clean_value(row[col])
                if val != 0:
                    return val
            return 0.0
        except:
            return 0.0
    
    def parse_income_statement(self, df: pd.DataFrame) -> Dict[str, float]:
        """استخراج اطلاعات از صورت سود و زیان"""
        result = {}
        
        # درآمد
        revenue_row = self.find_row_by_keywords(df, self.keywords['revenue'])
        result['revenue'] = self.extract_latest_value(df, revenue_row)
        
        # سود ناخالص
        gross_profit_keywords = ['سود ناخالص', 'سودناخالص', 'Gross Profit', 'سود خالص عملیات']
        gross_profit_row = self.find_row_by_keywords(df, gross_profit_keywords)
        result['gross_profit'] = self.extract_latest_value(df, gross_profit_row)
        
        # سود خالص
        net_income_row = self.find_row_by_keywords(df, self.keywords['net_income'])
        result['net_income'] = self.extract_latest_value(df, net_income_row)
        
        # سود عملیاتی (برای محاسبه EBITDA)
        operating_profit_row = self.find_row_by_keywords(df, self.keywords['operating_profit'])
        result['operating_profit'] = self.extract_latest_value(df, operating_profit_row)
        
        # سرمایه (برای محاسبه تعداد سهام)
        capital_row = self.find_row_by_keywords(df, self.keywords['capital'])
        capital_millions = self.extract_latest_value(df, capital_row)
        result['capital'] = capital_millions
        
        # محاسبه تعداد سهام (فرض: ارزش اسمی هر سهم = 1000 ریال)
        if capital_millions > 0:
            # سرمایه به میلیون ریال است، تبدیل به ریال و تقسیم بر 1000
            result['shares_outstanding'] = (capital_millions * 1_000_000) / 1000
        else:
            result['shares_outstanding'] = 0
        
        # EPS (سود هر سهم) - برای تأیید محاسبات
        eps_row = self.find_row_by_keywords(df, self.keywords['eps'])
        result['eps'] = self.extract_latest_value(df, eps_row)
        
        # اگر سود ناخالص پیدا نشد، تخمین بزن
        if result['gross_profit'] == 0 and result['revenue'] > 0:
            # تخمین بر اساس سود عملیاتی یا سود خالص
            if result['operating_profit'] > 0:
                result['gross_profit'] = result['operating_profit'] * 1.25  # فرض 20% هزینه عملیاتی
            elif result['net_income'] > 0:
                result['gross_profit'] = result['net_income'] * 1.5  # تخمین محافظه‌کارانه
        
        # اگر سود عملیاتی پیدا نشد، از سود خالص استفاده کن
        if result['operating_profit'] == 0 and result['net_income'] != 0:
            result['operating_profit'] = result['net_income'] * 1.3  # تخمین
        
        # Sanity check: سود خالص نباید بیشتر از درآمد باشه
        if result['net_income'] > result['revenue'] and result['revenue'] > 0:
            # احتمالا سود خالص اشتباه پیدا شده - تخمین بزن
            result['net_income'] = result['revenue'] * 0.10  # فرض 10% profit margin
            result['operating_profit'] = result['net_income'] * 1.3
        
        # اگر درآمد خیلی کوچیک و سود خیلی بزرگه، جابجا شدن
        if result['revenue'] < result['net_income'] * 0.1:
            # احتمالا revenue و net_income جابجا شدن
            result['revenue'], result['net_income'] = result['net_income'], result['revenue']
        
        return result
    
    def parse_balance_sheet(self, df: pd.DataFrame) -> Dict[str, float]:
        """استخراج اطلاعات از ترازنامه"""
        result = {}
        
        # کل دارایی
        assets_row = self.find_row_by_keywords(df, self.keywords['total_assets'])
        result['total_assets'] = self.extract_latest_value(df, assets_row)
        
        # حقوق صاحبان سهام
        equity_row = self.find_row_by_keywords(df, self.keywords['total_equity'])
        result['total_equity'] = self.extract_latest_value(df, equity_row)
        
        # بدهی
        debt_row = self.find_row_by_keywords(df, self.keywords['total_debt'])
        result['total_debt'] = self.extract_latest_value(df, debt_row)
        
        # نقد
        cash_row = self.find_row_by_keywords(df, self.keywords['cash'])
        result['cash'] = self.extract_latest_value(df, cash_row)
        
        # اگر حقوق صاحبان سهام نیست، از دارایی منهای بدهی استفاده کن
        if result['total_equity'] == 0 and result['total_assets'] > 0:
            result['total_equity'] = result['total_assets'] - result['total_debt']
        
        # Sanity check: اگه دارایی < حقوق صاحبان، مشکل داره
        if result['total_assets'] > 0 and result['total_equity'] > result['total_assets']:
            # احتمالا یکی از اعداد اشتباهه - از منطقی‌تر استفاده کن
            result['total_equity'] = result['total_assets'] * 0.6  # فرض 60% equity ratio
        
        return result
    
    def parse_financial_ratios(self, df: pd.DataFrame) -> Dict[str, float]:
        """استخراج نسبت‌های مالی"""
        result = {}
        
        if df.empty:
            return result
        
        try:
            # P/E
            pe_row = df[df.iloc[:, 0].astype(str).str.contains('P/E', na=False)]
            if not pe_row.empty:
                result['pe_ratio'] = self.clean_value(pe_row.iloc[0, 1])
            
            # P/B
            pb_row = df[df.iloc[:, 0].astype(str).str.contains('P/B', na=False)]
            if not pb_row.empty:
                result['pb_ratio'] = self.clean_value(pb_row.iloc[0, 1])
            
            # P/S
            ps_row = df[df.iloc[:, 0].astype(str).str.contains('P/S', na=False)]
            if not ps_row.empty:
                result['ps_ratio'] = self.clean_value(ps_row.iloc[0, 1])
        except:
            pass
        
        return result
    
    def normalize_units(self, income_data: Dict, balance_data: Dict) -> tuple:
        """تشخیص و نرمال‌سازی واحد (میلیون/میلیارد)"""
        # معمولا اگر درآمد < 1000 میلیون باشه، احتمالا میلیارد است
        # یا اگر دارایی < 10000 میلیون باشه
        
        revenue = income_data.get('revenue', 0)
        assets = balance_data.get('total_assets', 0)
        equity = balance_data.get('total_equity', 0)
        
        # اگر اعداد خیلی کوچیکن، احتمالا واحد میلیارد است
        multiplier = 1.0
        
        if revenue > 0 and revenue < 100000:  # کمتر از 100 میلیارد ریال
            # احتمالا واحد میلیارد است، تبدیل به میلیون
            multiplier = 1000.0
        elif assets > 0 and assets < 500000:  # کمتر از 500 میلیارد
            multiplier = 1000.0
        elif equity > 0 and equity < 500000:
            multiplier = 1000.0
        
        # اعمال ضریب
        income_normalized = {k: v * multiplier for k, v in income_data.items()}
        balance_normalized = {k: v * multiplier for k, v in balance_data.items()}
        
        return income_normalized, balance_normalized
    
    def build_valuation_inputs(self, financial_data: Dict[str, pd.DataFrame], 
                               scenario_config: Dict) -> Dict:
        """ساخت ورودی‌های لازم برای ارزش‌گذاری"""
        
        # پارس صورت‌های مالی
        income_data = self.parse_income_statement(financial_data.get('income_statement', pd.DataFrame()))
        balance_data = self.parse_balance_sheet(financial_data.get('balance_sheet', pd.DataFrame()))
        ratio_data = self.parse_financial_ratios(financial_data.get('financial_ratios', pd.DataFrame()))
        
        # نرمال‌سازی واحدها
        income_data, balance_data = self.normalize_units(income_data, balance_data)
        
        # ترکیب با scenario_config
        valuation_params = scenario_config.copy()
        
        # اضافه کردن داده‌های واقعی
        valuation_params['revenue'] = income_data.get('revenue', 0)
        valuation_params['earnings'] = income_data.get('net_income', 0)
        valuation_params['ebitda'] = income_data.get('operating_profit', 0)
        valuation_params['book_value'] = balance_data.get('total_equity', 0)
        valuation_params['total_assets'] = balance_data.get('total_assets', 0)
        valuation_params['total_debt'] = balance_data.get('total_debt', 0)
        valuation_params['cash'] = balance_data.get('cash', 0)
        
        # اگر سود خالص صفر یا اشتباهه، از P/E و market cap تخمین بزن
        if valuation_params['earnings'] <= 0 and ratio_data.get('pe_ratio', 0) > 0:
            # تخمین از روی P/E: اگر P/E و قیمت رو داریم
            # این رو بعدا با قیمت واقعی محاسبه می‌کنیم
            # فعلا از میانگین حاشیه سود استفاده می‌کنیم
            valuation_params['earnings'] = valuation_params['revenue'] * 0.08  # فرض 8% profit margin
        
        # محاسبه متریک‌های اضافی
        if valuation_params['earnings'] > 0:
            # FCF تخمینی: 70% سود خالص
            valuation_params['fcf'] = valuation_params['earnings'] * 0.7
        else:
            valuation_params['fcf'] = valuation_params['revenue'] * 0.05  # فرض 5% FCF margin
        
        # Net Debt
        valuation_params['net_debt'] = valuation_params['total_debt'] - valuation_params['cash']
        
        # ROE
        if valuation_params['book_value'] > 0:
            valuation_params['roe'] = valuation_params['earnings'] / valuation_params['book_value']
        else:
            valuation_params['roe'] = 0.15  # مقدار پیش‌فرض
        
        # Required Return (از discount_rate)
        valuation_params['required_return'] = valuation_params.get('discount_rate', 0.20)
        
        # Industry multiples (مقادیر متوسط بازار ایران)
        valuation_params['industry_pe'] = ratio_data.get('pe_ratio', 8.0)  # P/E متوسط بورس
        valuation_params['industry_pb'] = ratio_data.get('pb_ratio', 3.0)
        valuation_params['industry_ebitda_multiple'] = 6.0  # EV/EBITDA متوسط
        valuation_params['industry_ps'] = ratio_data.get('ps_ratio', 1.5)
        
        # Cost of equity & debt (برای WACC)
        valuation_params['cost_of_equity'] = valuation_params['discount_rate']
        valuation_params['cost_of_debt'] = 0.18  # نرخ متوسط تسهیلات
        
        # Equity & Debt values
        valuation_params['equity_value'] = valuation_params['book_value']
        valuation_params['debt_value'] = valuation_params['total_debt']
        
        return valuation_params


if __name__ == "__main__":
    # تست
    pass
