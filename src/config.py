"""
تنظیمات اصلی پروژه تحلیل مالی بهگزین
"""

# نمادهای بازارگردانی
SYMBOLS = {
    'با_مازاد_منابع': ['زفجر', 'کاوه', 'گکوثر'],
    'با_کمبود_منابع': ['رنیک', 'قشیر', 'زدشت', 'وسنا', 'کگاز', 'تلیسه']
}

# نام انگلیسی نمادها برای استفاده با finpy-tse
SYMBOL_NAMES_EN = {
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

# مسیرهای داده
DATA_PATHS = {
    'زفجر': r'Data\Zfajr',
    'کاوه': r'Data\Kaveh',
    'گکوثر': r'Data\Gkowthar',
    'رنیک': r'Data\Renik',
    'قشیر': r'Data\Qshir',
    'زدشت': r'Data\Zdasht',
    'وسنا': r'Data\Vsana',
    'کگاز': r'Data\Kgaz',
    'تلیسه': r'Data\Tliseh'
}

# تنظیمات تحلیل
ANALYSIS_CONFIG = {
    'scenarios': ['خوشبینانه', 'خنثی', 'بدبینانه'],
    'valuation_methods': ['DCF', 'P/E', 'P/B', 'EV/EBITDA', 'P/S'],
    'financial_ratios': {
        'نقدینگی': ['نسبت جاری', 'نسبت آنی', 'نسبت نقدی'],
        'سودآوری': ['حاشیه سود خالص', 'ROE', 'ROA', 'ROIC'],
        'اهرمی': ['نسبت بدهی به حقوق صاحبان سهام', 'نسبت بدهی به دارایی'],
        'فعالیت': ['گردش دارایی', 'گردش موجودی', 'دوره وصول مطالبات'],
        'بازار': ['P/E', 'P/B', 'EPS', 'DPS']
    }
}

# تنظیمات سناریوها برای DCF
DCF_SCENARIOS = {
    'خوشبینانه': {
        'growth_rate': 0.20,  # 20% رشد
        'discount_rate': 0.18,  # نرخ تنزیل
        'terminal_growth': 0.10
    },
    'خنثی': {
        'growth_rate': 0.15,  # 15% رشد
        'discount_rate': 0.20,
        'terminal_growth': 0.08
    },
    'بدبینانه': {
        'growth_rate': 0.08,  # 8% رشد
        'discount_rate': 0.22,
        'terminal_growth': 0.05
    }
}

# پارامترهای تصمیم‌گیری برای تخصیص منابع
ALLOCATION_CRITERIA = {
    'حداقل_ROE': 0.15,  # حداقل بازده حقوق صاحبان سهام
    'حداقل_نسبت_جاری': 1.5,
    'حداکثر_نسبت_بدهی': 0.65,
    'حداقل_رشد_فروش': 0.10,
    'وزن_سودآوری': 0.35,
    'وزن_نقدینگی': 0.25,
    'وزن_رشد': 0.25,
    'وزن_ریسک': 0.15
}

# تنظیمات گزارش‌گیری
REPORT_CONFIG = {
    'output_dir': 'output',
    'report_dir': 'reports',
    'chart_style': 'seaborn-v0_8-darkgrid',
    'persian_font': 'Tahoma',
    'figure_size': (12, 8),
    'dpi': 300
}
