#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
به‌روزرسانی گزارش comprehensive با توضیحات کامل
"""

# خواندن فایل
with open('reports/comprehensive_report.html', 'r', encoding='utf-8') as f:
    content = f.read()

# متن قدیمی که باید جایگزین شود
old_text = '''            <div class="warning-box">
                <p><strong>نحوه محاسبه:</strong> ارزش هر سهم = (ارزش کل شرکت) ÷ (تعداد سهام منتشر شده). ارزش کل شرکت بر اساس 6 روش مختلف (DCF, P/E, P/B, EV/EBITDA, P/S, RIM) و میانگین وزنی آنها محاسبه شده است.</p>
            </div>'''

# متن جدید با توضیحات کامل
new_text = '''            <div class="warning-box">
                <p><strong>💡 چرا اختلاف با قیمت بازار وجود دارد؟</strong></p>
                <ul style="margin: 10px 0 0 20px; line-height: 2;">
                    <li><strong>ارزشگذاری بنیادی محافظه‌کارانه است:</strong> فقط از داده‌های تاریخی مالی استفاده می‌شود</li>
                    <li><strong>قیمت بازار انتظارات آینده را لحاظ می‌کند:</strong> رشد، پروژه‌های جدید، تغییرات مدیریت</li>
                    <li><strong>عوامل کیفی:</strong> برند، موقعیت رقابتی، کیفیت مدیریت در مدل ریاضی لحاظ نمی‌شود</li>
                    <li><strong>نقدینگی بازار:</strong> عرضه و تقاضا، معاملات هیجانی، اخبار و شایعات</li>
                    <li><strong>تورم و رشد:</strong> ارزشگذاری فرض می‌کند رشد محدود به GDP است (4-5% سالانه)</li>
                    <li><strong>ریسک سیاسی و اقتصادی:</strong> تحریم‌ها، نرخ ارز، تورم بالا در مدل کاملاً منعکس نمی‌شود</li>
                </ul>
                <p style="margin-top: 15px;"><strong>🎯 روش‌های ارزشگذاری استفاده شده:</strong></p>
                <ul style="margin: 5px 0 0 20px;">
                    <li><strong>DCF (30%):</strong> جریان نقدی آزاد تنزیل شده - مناسب شرکت‌های با CF پایدار</li>
                    <li><strong>P/E (15%):</strong> ضریب قیمت به سود - مقایسه با شرکت‌های مشابه</li>
                    <li><strong>P/B (15%):</strong> ضریب قیمت به ارزش دفتری - مناسب دارایی‌های محسوس</li>
                    <li><strong>EV/EBITDA (10%):</strong> ارزش شرکت به سود عملیاتی - بدون تأثیر ساختار سرمایه</li>
                    <li><strong>P/S (5%):</strong> ضریب قیمت به فروش - مناسب شرکت‌های کم‌سود</li>
                    <li><strong>RIM (20%):</strong> مدل درآمد باقیمانده - ارزش افزوده بر حقوق صاحبان سهام</li>
                    <li><strong>APV (5%):</strong> ارزش فعلی تعدیل شده - لحاظ کردن مزایای مالیاتی بدهی</li>
                </ul>
                <p style="margin-top: 10px; font-size: 13px; color: #666;">
                    <strong>📌 نکته:</strong> ارزش نهایی = میانگین وزنی هفت روش فوق. ارزش هر سهم = ارزش کل ÷ تعداد سهام منتشر شده
                </p>
            </div>'''

# جایگزینی تمام موارد
content = content.replace(old_text, new_text)

# اضافه کردن بخش توضیحات در ابتدای گزارش
explanation_section = '''
        <div class="section">
            <div class="section-title">🔍 درباره اختلاف با قیمت بازار</div>
            
            <div class="info-box">
                <h3 style="color: #2c3e50; margin-bottom: 10px;">چرا ارزشگذاری بنیادی با قیمت بازار متفاوت است؟</h3>
                <p style="line-height: 2;">
                    ارزشگذاری بنیادی یک <strong>تخمین علمی و محافظه‌کارانه</strong> از ارزش ذاتی شرکت است که 
                    فقط بر اساس <strong>داده‌های مالی تاریخی</strong> و <strong>مفروضات منطقی</strong> محاسبه می‌شود.
                    در مقابل، قیمت بازار تحت تأثیر عوامل متعددی است:
                </p>
            </div>
            
            <div class="metric-grid" style="grid-template-columns: repeat(2, 1fr); margin-top: 20px;">
                <div class="metric-card">
                    <div class="metric-label">🧮 ارزشگذاری بنیادی</div>
                    <ul style="text-align: right; margin: 15px 20px; line-height: 2; font-size: 14px;">
                        <li>محاسبات ریاضی دقیق</li>
                        <li>داده‌های مالی تاریخی</li>
                        <li>مفروضات محافظه‌کارانه</li>
                        <li>بدون تأثیر احساسات</li>
                        <li>رشد محدود به GDP</li>
                    </ul>
                </div>
                <div class="metric-card">
                    <div class="metric-label">📈 قیمت بازار</div>
                    <ul style="text-align: right; margin: 15px 20px; line-height: 2; font-size: 14px;">
                        <li>انتظارات آینده</li>
                        <li>پروژه‌های جدید</li>
                        <li>اخبار و شایعات</li>
                        <li>عرضه و تقاضا</li>
                        <li>احساسات سرمایه‌گذاران</li>
                    </ul>
                </div>
            </div>
            
            <div class="warning-box" style="margin-top: 20px;">
                <h4 style="color: #856404; margin-bottom: 10px;">⚠️ دلایل اصلی اختلاف قیمت:</h4>
                <table style="width: 100%; border: none; box-shadow: none;">
                    <tr style="background: transparent;">
                        <td style="border: none; padding: 10px; width: 50%; vertical-align: top;">
                            <strong>1️⃣ عوامل کیفی (غیرقابل اندازه‌گیری):</strong><br>
                            • کیفیت مدیریت<br>
                            • قدرت برند<br>
                            • موقعیت رقابتی<br>
                            • نوآوری و تحقیق<br>
                        </td>
                        <td style="border: none; padding: 10px; width: 50%; vertical-align: top;">
                            <strong>2️⃣ انتظارات آینده:</strong><br>
                            • رشد فروش پیش‌بینی شده<br>
                            • پروژه‌های در دست اجرا<br>
                            • تغییرات استراتژیک<br>
                            • فرصت‌های جدید بازار<br>
                        </td>
                    </tr>
                    <tr style="background: transparent;">
                        <td style="border: none; padding: 10px; vertical-align: top;">
                            <strong>3️⃣ عوامل بازار:</strong><br>
                            • نقدینگی بازار<br>
                            • معاملات هیجانی<br>
                            • عرضه و تقاضا<br>
                            • شایعات و اخبار<br>
                        </td>
                        <td style="border: none; padding: 10px; vertical-align: top;">
                            <strong>4️⃣ محیط اقتصادی:</strong><br>
                            • تورم بالا (40%)<br>
                            • تحریم‌ها<br>
                            • نوسانات ارز<br>
                            • سیاست‌های دولت<br>
                        </td>
                    </tr>
                </table>
            </div>
            
            <div class="success-box" style="margin-top: 20px;">
                <h4 style="color: #155724; margin-bottom: 10px;">✅ چگونه از این اطلاعات استفاده کنیم؟</h4>
                <ul style="margin: 10px 20px; line-height: 2;">
                    <li><strong>اختلاف کمتر از 10%:</strong> قیمت بازار نزدیک به ارزش ذاتی است - سهم منطقی</li>
                    <li><strong>اختلاف 10% تا 30%:</strong> قابل قبول - بازار ممکن است انتظارات خوبی داشته باشد</li>
                    <li><strong>اختلاف 30% تا 50%:</strong> سهم گران است - فقط اگر به آینده شرکت اطمینان دارید</li>
                    <li><strong>اختلاف بیش از 50%:</strong> احتمال حباب قیمتی - خرید بسیار پرریسک</li>
                    <li><strong>قیمت زیر ارزش ذاتی:</strong> فرصت خرید عالی - اما دلیل را بررسی کنید</li>
                </ul>
            </div>
        </div>
'''

# پیدا کردن محل درج (بعد از بخش خلاصه اجرایی)
insert_position = content.find('<div class="section page-break">\n            <div class="section-title">📈 تحلیل تفصیلی هر نماد</div>')
if insert_position > 0:
    content = content[:insert_position] + explanation_section + '\n        ' + content[insert_position:]

# ذخیره فایل
with open('reports/comprehensive_report.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ گزارش comprehensive به‌روز شد!")
print("📄 فایل: reports/comprehensive_report.html")
print("\n🔍 تغییرات اعمال شده:")
print("  ✓ توضیحات کامل درباره اختلاف قیمت")
print("  ✓ تشریح 7 روش ارزشگذاری")
print("  ✓ راهنمای تصمیم‌گیری بر اساس اختلاف قیمت")
print("  ✓ بخش جدید قبل از تحلیل نمادها")
