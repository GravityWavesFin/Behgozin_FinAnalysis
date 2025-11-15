"""
استخراج داده از فایل‌های MHTML
"""

import os
import pandas as pd
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Tuple
import warnings
import quopri
warnings.filterwarnings('ignore')


class FinancialDataExtractor:
    """کلاس استخراج داده‌های مالی از فایل‌های MHTML"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        
    def read_mhtml_file(self, file_path: str) -> BeautifulSoup:
        """خواندن و پارس فایل MHTML - فقط جداول HTML"""
        try:
            # خواندن فایل با encoding مناسب
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            # استخراج بخش HTML از MHTML
            html_match = re.search(r'Content-Type: text/html.*?charset[=:][\s"]*([\w-]+)', 
                                  content, re.IGNORECASE | re.DOTALL)
            
            if html_match:
                start_pos = html_match.end()
                next_boundary = re.search(r'\n------', content[start_pos:])
                if next_boundary:
                    html_content = content[start_pos:start_pos + next_boundary.start()]
                else:
                    html_content = content[start_pos:]
            else:
                html_content = content
            
            # Decode quoted-printable اگر لازمه
            if '=D8=A7' in html_content or '=3D' in html_content:
                try:
                    decoded = quopri.decodestring(html_content.encode('latin-1'))
                    html_content = decoded.decode('utf-8', errors='ignore')
                except:
                    pass
            
            return BeautifulSoup(html_content, 'lxml')
            
        except Exception as e:
            print(f"خطا در خواندن فایل {file_path}: {e}")
            return None
    
    def decode_quoted_printable(self, text: str) -> str:
        """Decode quoted-printable encoding"""
        try:
            if '=D' in text or '=d' in text:  # احتمالا quoted-printable است
                decoded_bytes = quopri.decodestring(text.encode('ascii'))
                return decoded_bytes.decode('utf-8')
            return text
        except:
            return text
    
    def extract_table_with_bs4(self, soup: BeautifulSoup) -> pd.DataFrame:
        """استخراج جدول با BeautifulSoup - متن خام فارسی"""
        if soup is None:
            return pd.DataFrame()
        
        try:
            tables = soup.find_all('table')
            if not tables:
                return pd.DataFrame()
            
            # پیدا کردن بزرگترین جدول
            largest_table = max(tables, key=lambda t: len(t.find_all('tr')))
            
            # استخراج تمام ردیف‌ها
            rows = []
            for tr in largest_table.find_all('tr'):
                cells = []
                for cell in tr.find_all(['td', 'th']):
                    # استخراج متن خام (بدون encoding)
                    text = cell.get_text(strip=True)
                    # حذف کاراکترهای اضافی
                    text = text.replace('\n', ' ').replace('\r', '').strip()
                    cells.append(text)
                if cells:  # فقط ردیف‌های غیرخالی
                    rows.append(cells)
            
            if not rows:
                return pd.DataFrame()
            
            # ساخت DataFrame
            # اگر طول ردیف‌ها متفاوت باشه، به طول ماکزیمم برسون
            max_cols = max(len(row) for row in rows)
            for row in rows:
                while len(row) < max_cols:
                    row.append('')
            
            df = pd.DataFrame(rows)
            return df
            
        except Exception as e:
            print(f"خطا در استخراج با BS4: {e}")
            return pd.DataFrame()
    
    def extract_table_data(self, soup: BeautifulSoup) -> pd.DataFrame:
        """استخراج داده‌های جدولی از HTML"""
        if soup is None:
            return pd.DataFrame()
        
        # اول سعی کن با BeautifulSoup
        df = self.extract_table_with_bs4(soup)
        if not df.empty:
            return df
        
        # اگر نشد، از pandas استفاده کن
        try:
            tables = soup.find_all('table')
            if not tables:
                return pd.DataFrame()
            
            for table in tables:
                df = pd.read_html(str(table))[0]
                if len(df) > 3 and len(df.columns) > 2:
                    return df
            
            return pd.DataFrame()
        except Exception as e:
            print(f"خطا در استخراج جدول: {e}")
            return pd.DataFrame()
            return pd.DataFrame()
    
    def clean_numeric_value(self, value) -> float:
        """تمیز کردن و تبدیل مقادیر عددی"""
        if pd.isna(value):
            return 0.0
        
        if isinstance(value, (int, float)):
            return float(value)
        
        # حذف کاراکترهای غیرعددی
        value_str = str(value).replace(',', '').replace('٬', '').replace('%', '')
        value_str = re.sub(r'[^\d.\-+]', '', value_str)
        
        try:
            return float(value_str) if value_str else 0.0
        except:
            return 0.0
    
    def decode_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Decode entire dataframe from quoted-printable - اعمال به همه سلول‌ها"""
        if df.empty:
            return df
        
        df_copy = df.copy()
        # Decode all cells, not just object dtype
        for col in df_copy.columns:
            df_copy[col] = df_copy[col].apply(
                lambda x: self.decode_quoted_printable(str(x)) if pd.notna(x) and x != '' else x
            )
        return df_copy
    
    def extract_balance_sheet(self, symbol: str, folder_path: str) -> pd.DataFrame:
        """استخراج ترازنامه"""
        file_pattern = f"{symbol} - ترازنامه"
        df = self._extract_financial_statement(folder_path, file_pattern)
        return self.decode_dataframe(df)
    
    def extract_income_statement(self, symbol: str, folder_path: str) -> pd.DataFrame:
        """استخراج صورت سود و زیان"""
        file_pattern = f"{symbol} - سود و زیان"
        df = self._extract_financial_statement(folder_path, file_pattern)
        return self.decode_dataframe(df)
    
    def extract_financial_ratios(self, symbol: str, folder_path: str) -> pd.DataFrame:
        """استخراج نسبت‌های مالی"""
        file_pattern = f"{symbol} - نسبت های مالی"
        df = self._extract_financial_statement(folder_path, file_pattern)
        return self.decode_dataframe(df)
    
    def extract_monthly_performance(self, symbol: str, folder_path: str) -> pd.DataFrame:
        """استخراج عملکرد ماهانه"""
        file_pattern = f"{symbol} - عملکرد ماهانه"
        df = self._extract_financial_statement(folder_path, file_pattern)
        return self.decode_dataframe(df)
    
    def _extract_financial_statement(self, folder_path: str, file_pattern: str) -> pd.DataFrame:
        """متد عمومی برای استخراج صورت‌های مالی"""
        full_path = os.path.join(self.base_path, folder_path)
        
        if not os.path.exists(full_path):
            print(f"مسیر {full_path} وجود ندارد")
            return pd.DataFrame()
        
        # جستجوی فایل
        matching_files = [f for f in os.listdir(full_path) if file_pattern in f and f.endswith('.mhtml')]
        
        if not matching_files:
            print(f"فایل با الگوی {file_pattern} یافت نشد")
            return pd.DataFrame()
        
        file_path = os.path.join(full_path, matching_files[0])
        soup = self.read_mhtml_file(file_path)
        df = self.extract_table_data(soup)
        
        return df
    
    def extract_all_data(self, symbol: str, folder_path: str) -> Dict[str, pd.DataFrame]:
        """استخراج تمام داده‌های مالی یک شرکت"""
        print(f"\n{'='*60}")
        print(f"استخراج داده‌های مالی {symbol}")
        print(f"{'='*60}")
        
        data = {
            'balance_sheet': self.extract_balance_sheet(symbol, folder_path),
            'income_statement': self.extract_income_statement(symbol, folder_path),
            'financial_ratios': self.extract_financial_ratios(symbol, folder_path),
            'monthly_performance': self.extract_monthly_performance(symbol, folder_path)
        }
        
        # گزارش وضعیت
        for key, df in data.items():
            status = f"✓ {len(df)} سطر" if not df.empty else "✗ داده موجود نیست"
            print(f"{key:25s}: {status}")
        
        return data


def test_extractor():
    """تست عملکرد استخراج‌کننده"""
    extractor = FinancialDataExtractor()
    
    # تست برای زفجر
    symbol = 'زفجر'
    folder = r'Data\Zfajr'
    data = extractor.extract_all_data(symbol, folder)
    
    # نمایش نمونه داده
    if not data['financial_ratios'].empty:
        print(f"\nنمونه نسبت‌های مالی {symbol}:")
        print(data['financial_ratios'].head())


if __name__ == "__main__":
    test_extractor()
