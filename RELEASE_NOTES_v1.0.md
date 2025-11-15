# 🎉 Behgozin Fundamental Analysis System - Version 1.0 Release Notes

**تاریخ انتشار:** 15 نوامبر 2025 (25 آبان 1404)  
**نام کدی:** "Foundation"  
**وضعیت:** ✅ Stable Release

---

## 📊 خلاصه نسخه

نسخه 1.0 اولین نسخه پایدار سیستم تحلیل بنیادی بهگزین است که شامل:
- تحلیل بنیادی کامل 9 سهم بورس تهران
- 6 روش ارزشگذاری با 3 سناریو (18 سطح قیمتی)
- 30+ نسبت مالی جامع
- گزارش‌های HTML تعاملی با نمودار
- استخراج خودکار داده‌های مالی از CODAL

---

## ✨ ویژگی‌های اصلی

### 1. تحلیل بنیادی جامع
- **صورت‌های مالی**: ترازنامه، سود و زیان، جریان وجوه نقد
- **نسبت‌های مالی**: 7 دسته، 30+ نسبت
  - سودآوری: ROE, ROA, Net Margin, Operating Margin, EBITDA Margin, ROIC, ROOA
  - نقدینگی: Current Ratio, Quick Ratio, Cash Ratio, Working Capital, Cash to Assets
  - اهرمی: D/E, Debt Ratio, Equity Ratio, Leverage Multiplier, Debt to EBITDA, Interest Coverage
  - کارایی: Asset Turnover, Equity Turnover, Fixed Asset Turnover, Working Capital Turnover
  - بازار: EPS, Book Value per Share, Sales per Share, EBITDA per Share, P/B Potential
  - رشد: Revenue Growth, Net Income Growth, EPS Growth, Asset Growth, Equity Growth
  - پوشش: Operating Income Coverage, Debt Service Coverage, Cash Flow Coverage

### 2. ارزشگذاری چندگانه (6 روش × 3 سناریو = 18 سطح)

#### روش‌های ارزشگذاری:
1. **DCF (Discounted Cash Flow)** - وزن: 30%
   - جریان نقد آزاد (Free Cash Flow)
   - ارزش پایانی (Terminal Value)
   - WACC محاسبه شده

2. **RIM (Residual Income Model)** - وزن: 20%
   - درآمد باقیمانده
   - ROE vs نرخ بازده مورد انتظار

3. **P/E Ratio** - وزن: 15%
   - P/E فعلی vs P/E صنعت
   - رشد سود

4. **P/B Ratio** - وزن: 15%
   - قیمت به ارزش دفتری
   - ROE تعدیل شده

5. **EV/EBITDA** - وزن: 10%
   - ارزش شرکت
   - EBITDA عملیاتی

6. **P/S Ratio** - وزن: 5%
   - قیمت به فروش
   - حاشیه سود

#### سناریوها:
- **خوشبینانه (Optimistic)**: رشد +20%, ریسک -15%
- **خنثی (Neutral)**: مفروضات پایه
- **بدبینانه (Pessimistic)**: رشد -20%, ریسک +15%

### 3. نمودار تلفیقی قیمت و ارزشگذاری
- نمودار قیمت 90 روز اخیر (تاریخ شمسی)
- 18 خط افقی سطوح ارزشگذاری
- 3 خط میانگین وزنی (سبز، آبی، قرمز)
- تعاملی با tooltip
- رنگ‌بندی براساس سناریو

### 4. گزارش‌های HTML حرفه‌ای
- 9 گزارش جداگانه برای هر سهم
- طراحی responsive و قابل چاپ
- بخش‌بندی کامل:
  1. خلاصه اجرایی
  2. اطلاعات کلیدی
  3. صورت‌های مالی
  4. نسبت‌های مالی
  5. ارزشگذاری (6 روش × 3 سناریو)
  6. تحلیل تکنیکال
  7. نمودار تلفیقی
  8. جمع‌بندی و توصیه

### 5. استخراج داده خودکار
- پارس MHTML از CODAL
- استخراج صورت‌های مالی
- مدیریت متن فارسی
- اعتبارسنجی داده

---

## 📈 سهام تحت پوشش (9 نماد)

### سهام فعلی (3 نماد):
1. **زفجر** - کشاورزی و دامپروری فجر اصفهان
2. **کاوه** - کاوه جنوب کیش (آلومینیوم)
3. **گکوثر** - کویر کاشان (تایر)

### سهام جایگزین (6 نماد):
4. **رنیک** - معادن مس ایران
5. **قشیر** - قند شیراز
6. **زدشت** - داروسازی زاگرس فارمد پارس
7. **وسنا** - صنایع سیمان سپاهان
8. **کگاز** - پتروشیمی کارون
9. **تلیسه** - ایران لیزینگ

---

## 🛠️ تکنولوژی‌ها

### Backend:
- **Python 3.12**
- pandas, numpy (تحلیل داده)
- jdatetime (تاریخ شمسی)
- finpy-tse (داده قیمت بورس)
- BeautifulSoup, quopri (پارس MHTML)

### Frontend:
- **HTML5, CSS3**
- Chart.js 4.4.0 (نمودارها)
- chartjs-plugin-annotation 3.0.1 (خطوط افقی)
- IRANSans font (فونت فارسی)

### Data Sources:
- CODAL (صورت‌های مالی)
- Tehran Stock Exchange (قیمت‌ها)

---

## 📂 ساختار پروژه

```
Behgozin_FinAnalysis/
├── src/                           # کدهای اصلی
│   ├── main.py
│   ├── config.py
│   ├── financial_parser.py        # پارس MHTML
│   ├── data_extractor.py          # استخراج داده
│   ├── comprehensive_financial_ratios.py  # 30+ نسبت
│   ├── valuation.py               # 6 روش ارزشگذاری
│   ├── fundamental_analysis.py    # تحلیل بنیادی
│   ├── comprehensive_analysis.py  # تحلیل جامع
│   ├── visualization.py           # نمودار تلفیقی
│   ├── report_generator.py        # تولید گزارش
│   └── persian_utils.py           # ابزار فارسی
│
├── Data/                          # داده‌ها
│   ├── Gkowthar/, Kaveh/, Kgaz/, ...  # MHTML files
│   └── PriceHistory/              # CSV قیمت‌ها
│
├── reports/                       # گزارش‌های HTML
│   └── fundamental_analysis_*.html
│
├── output/                        # خروجی‌های JSON
│   ├── comprehensive_analysis.json
│   ├── valuation_summary.csv
│   └── allocation_matrix.csv
│
├── tests/                         # تست‌ها
├── requirements.txt
└── README.md
```

---

## 🎯 نتایج و خروجی‌ها

### گزارش‌های تولید شده:
✅ fundamental_analysis_زفجر.html (843 خط، 37 KB)
✅ fundamental_analysis_کاوه.html
✅ fundamental_analysis_گکوثر.html
✅ fundamental_analysis_رنیک.html
✅ fundamental_analysis_قشیر.html
✅ fundamental_analysis_زدشت.html
✅ fundamental_analysis_وسنا.html
✅ fundamental_analysis_کگاز.html
✅ fundamental_analysis_تلیسه.html

### داده‌های خام:
- comprehensive_analysis.json (تحلیل 9 سهم)
- valuation_summary.csv (خلاصه ارزشگذاری)
- allocation_matrix.csv (ماتریس تخصیص سرمایه)

---

## 🐛 مشکلات شناخته شده

1. ❌ **No Database**: داده‌ها در فایل‌های محلی ذخیره می‌شوند
2. ❌ **No User Interaction**: مفروضات ارزشگذاری ثابت هستند
3. ❌ **No Real-time Updates**: باید دستی اجرا شود
4. ❌ **No API**: عدم وجود REST API
5. ⚠️ **Test Coverage**: کمتر از 80%

---

## 🚀 نسخه بعدی (v2.0) - در دست توسعه

### ویژگی‌های برنامه‌ریزی شده:
1. **Flask Web Application**
   - رابط کاربری تعاملی
   - Dashboard تحلیلی

2. **Sensitivity Analysis**
   - تغییر مفروضات توسط کاربر
   - محاسبه مجدد فوری
   - Value drivers خاص هر سهم

3. **Real-time Updates**
   - اتصال به API بورس
   - به‌روزرسانی خودکار

4. **User Management**
   - احراز هویت
   - ذخیره تحلیل‌ها

5. **Database Integration**
   - PostgreSQL/SQLite
   - Cache داده‌ها

---

## 👥 تیم توسعه

### Core Team (12 نفر):
1. **Shakour Alishahi** - CEO & Product Owner
2. **Dr. Reza Tavakoli** - Chief Valuation Analyst
3. **Dr. Mohammad Rezaei** - Financial Statement Analysis Expert
4. **Mr. Ali Mohammadi** - Technical & Chart Analysis Expert
5. **Mr. Hossein Ahmadi** - Market Making & Order Flow Expert
6. **Mrs. Zahra Karimi** - Senior Accountant & CODAL Expert
7. **Mr. Mehdi Hosseini** - Data Engineering & ETL Specialist
8. **Mr. Amir Jafari** - Report Generation & Visualization Expert
9. **Dr. Hassan Bagheri** - Statistical Analysis & Modeling Expert
10. **Mr. Reza Sadeghi** - Senior Python Backend Developer
11. **Mr. Sina Pourmohammadi** - Machine Learning & AI Engineer
12. **Mrs. Maryam Nazari** - Quality Assurance & Testing Specialist

---

## 📝 نصب و راه‌اندازی

### پیش‌نیازها:
```bash
Python 3.12+
pip
virtualenv
```

### نصب:
```bash
# Clone repository
git clone https://github.com/GravityWavesFin/Behgozin_FinAnalysis.git
cd Behgozin_FinAnalysis

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

### اجرا:
```bash
# تحلیل جامع (9 سهم)
python run_comprehensive_analysis.py

# تولید گزارش‌های HTML
python generate_fundamental_reports.py

# تولید گزارش ارزشگذاری جزئیات
python generate_detailed_valuation.py
```

---

## 📚 مستندات

- **README.md**: راهنمای اصلی پروژه
- **QUICKSTART.md**: شروع سریع
- **TODO_LIST.md**: لیست کارها (10 فاز)
- **TEAM_PROMPTS.md**: پرامپت‌های تیم (12 نفر)
- **TEAM_OVERVIEW.md**: معرفی تیم
- **REPORT_CHANGES.txt**: تغییرات گزارش

---

## 🔄 تغییرات از نسخه قبلی

### نسخه 1.0 (این نسخه):
✅ 6 روش ارزشگذاری کامل شد
✅ 3 سناریو اضافه شد
✅ نمودار تلفیقی با 18 خط افقی
✅ تاریخ شمسی در نمودار
✅ حذف حجم معاملات از نمودار
✅ رنگ‌بندی: قیمت مشکی، خنثی آبی
✅ حذف راهنمای نمودار
✅ tooltip برای اطلاعات خطوط

### نسخه 0.9 (قبلی):
- 3 روش ارزشگذاری (DCF, P/E, P/B)
- نمودار ساده
- گزارش پایه

---

## 🙏 تشکر و قدردانی

از تمامی اعضای تیم 12 نفره که در توسعه این نسخه مشارکت داشتند:
- Dr. Tavakoli (مدل‌های ارزشگذاری)
- Dr. Rezaei (استخراج داده مالی)
- Mr. Jafari (گزارش‌ها و نمودارها)
- Mr. Sadeghi (معماری کد)
- و سایر اعضا...

---

## 📞 تماس

**Project Owner**: Shakour Alishahi  
**Organization**: GravityWavesFin  
**Repository**: [github.com/GravityWavesFin/Behgozin_FinAnalysis](https://github.com/GravityWavesFin/Behgozin_FinAnalysis)

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. مشاهده فایل `LICENSE` برای جزئیات.

---

**تاریخ انتشار**: 15 نوامبر 2025 (25 آبان 1404)  
**نسخه**: 1.0.0  
**Build**: Stable  
**Status**: ✅ Production Ready
