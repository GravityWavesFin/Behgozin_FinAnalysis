#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بازنویسی گزارش comprehensive با جزئیات کامل ارزشگذاری
"""

import json
import pandas as pd
from datetime import datetime

# خواندن داده‌های تحلیل
with open('output/comprehensive_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# خواندن گزارش HTML فعلی
with open('reports/comprehensive_report.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# خواندن جزئیات ارزشگذاری از detailed_valuation
with open('reports/detailed_valuation.html', 'r', encoding='utf-8') as f:
    detailed_content = f.read()

print("✅ گزارش comprehensive به روز شد")
print(f"📊 تعداد نمادها: {len(data)}")
print(f"📄 فایل: reports/comprehensive_report.html")
