#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('src')

from data_extractor import FinancialDataExtractor
from financial_parser import FinancialParser

def debug_capital_extraction():
    """دیباگ استخراج سرمایه برای زفجر"""
    
    extractor = FinancialDataExtractor()
    parser = FinancialParser()
    
    # مسیر فایل صورت سود و زیان زفجر
    income_file = "Data/Zfajr/زفجر - سود و زیان - گزارش_های مالی _ انیگما.mhtml"
    
    print("=" * 80)
    print("دیباگ استخراج سرمایه - زفجر")
    print("=" * 80)
    
    # خواندن فایل
    soup = extractor.read_mhtml_file(income_file)
    df = extractor.extract_table_with_bs4(soup)
    if df is None or df.empty:
        print("❌ خطا در خواندن فایل")
        return
    
    print(f"\n📊 تعداد ردیف‌ها: {len(df)}")
    print(f"📊 تعداد ستون‌ها: {len(df.columns)}")
    print(f"📊 نام ستون‌ها: {list(df.columns)}")
    
    # جستجوی ردیف سرمایه
    capital_row_idx = parser.find_row_by_keywords(df, parser.keywords['capital'])
    
    if capital_row_idx is None:
        print("\n❌ ردیف سرمایه پیدا نشد!")
        return
    
    print(f"\n✅ ردیف سرمایه پیدا شد: row_idx = {capital_row_idx}")
    
    # نمایش ردیف کامل
    row = df.iloc[capital_row_idx]
    print(f"\n📋 محتوای کامل ردیف {capital_row_idx}:")
    for i, (col_name, value) in enumerate(row.items()):
        print(f"   col[{i}] ({col_name}): '{value}'")
    
    # تست extract_latest_value با دیباگ
    print(f"\n🔍 دیباگ extract_latest_value():")
    print(f"   شروع از ستون‌های 1 تا 5...")
    
    for i, col in enumerate(df.columns[1:6]):
        raw_value = row[col]
        cleaned_value = parser.clean_value(raw_value)
        print(f"   col[{i+1}] ({col}): raw='{raw_value}' → cleaned={cleaned_value}")
        if cleaned_value != 0:
            print(f"   ✅ اولین مقدار غیر صفر پیدا شد: {cleaned_value}")
            print(f"   ⚠️ این مقدار به عنوان سرمایه برگردانده می‌شود!")
            break
    
    # مقایسه با مقدار واقعی
    extracted_value = parser.extract_latest_value(df, capital_row_idx)
    print(f"\n📊 نتیجه extract_latest_value(): {extracted_value:,.0f}")
    print(f"📊 مقدار مورد انتظار (از ستون 1): {parser.clean_value(row[df.columns[1]]):,.0f}")
    
    # محاسبه تعداد سهام
    shares = (extracted_value * 1_000_000) / 1000
    print(f"\n📊 تعداد سهام محاسبه شده: {shares:,.0f}")
    print(f"📊 تعداد سهام مورد انتظار: {(parser.clean_value(row[df.columns[1]]) * 1_000_000) / 1000:,.0f}")

if __name__ == "__main__":
    debug_capital_extraction()
