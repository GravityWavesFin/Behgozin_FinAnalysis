"""
استخراج داده‌های قیمتی تاریخی با استفاده از finpy-tse
شامل سیستم کش هوشمند داده‌ها برای کار آفلاین
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import jdatetime
import warnings
warnings.filterwarnings('ignore')
import json

# import finpy_tse
try:
    from finpy_tse import get_price_history, get_tse_webid
except:
    print("خطا در وارد کردن finpy_tse")

from config import SYMBOLS, SYMBOL_NAMES_EN


class PriceDataExtractor:
    """کلاس استخراج داده‌های قیمتی تاریخی با سیستم کش"""
    
    def __init__(self, cache_dir: str = 'Data/PriceHistory'):
        self.price_data = {}
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def _get_cache_path(self, symbol: str) -> str:
        """مسیر فایل کش برای یک نماد"""
        safe_symbol = symbol.replace('/', '_')
        return os.path.join(self.cache_dir, f"{safe_symbol}.csv")
    
    def _load_from_cache(self, symbol: str) -> tuple:
        """
        بارگذاری داده از کش
        
        Returns:
        --------
        tuple: (DataFrame یا None, تاریخ آخرین داده)
        """
        cache_path = self._get_cache_path(symbol)
        
        if not os.path.exists(cache_path):
            return None, None
        
        try:
            # خواندن CSV با تبدیل صحیح index به datetime
            df = pd.read_csv(cache_path, index_col=0)
            
            # تبدیل index به datetime اگر string است
            if df.index.dtype == 'object':
                df.index = pd.to_datetime(df.index)
            
            if df.empty:
                return None, None
            
            # آخرین تاریخ در کش - تبدیل به فرمت شمسی برای مقایسه با finpy-tse
            last_date = df.index[-1]
            jalali_date = jdatetime.date.fromgregorian(date=last_date.date())
            last_date_str = f'{jalali_date.year:04d}-{jalali_date.month:02d}-{jalali_date.day:02d}'
            
            return df, last_date_str
            
        except Exception as e:
            print(f"⚠️ خطا در خواندن کش {symbol}: {e}")
            return None, None
    
    def _save_to_cache(self, symbol: str, df: pd.DataFrame):
        """ذخیره داده در کش"""
        if df is None or df.empty:
            return
        
        try:
            cache_path = self._get_cache_path(symbol)
            # اطمینان از datetime index قبل از ذخیره
            df_to_save = df.copy()
            if not isinstance(df_to_save.index, pd.DatetimeIndex):
                df_to_save.index = pd.to_datetime(df_to_save.index)
            
            df_to_save.to_csv(cache_path, encoding='utf-8-sig')
            print(f"💾 کش ذخیره شد: {cache_path}")
        except Exception as e:
            print(f"⚠️ خطا در ذخیره کش {symbol}: {e}")
    
    def get_symbol_price_history(self, 
                                  symbol: str,
                                  start_date: str = '1400-01-01',
                                  end_date: str = None,
                                  adjust_price: bool = True,
                                  use_cache: bool = True) -> pd.DataFrame:
        """
        استخراج تاریخچه قیمت یک نماد با سیستم کش هوشمند
        
        Parameters:
        -----------
        symbol: نماد سهم (فارسی)
        start_date: تاریخ شروع (شمسی) به فرمت YYYY-MM-DD
        end_date: تاریخ پایان (شمسی) به فرمت YYYY-MM-DD
        adjust_price: استفاده از قیمت تعدیل شده (برای افزایش سرمایه و تقسیم سود)
        use_cache: استفاده از داده‌های کش شده
        
        Returns:
        --------
        pd.DataFrame: داده‌های قیمتی شامل Open, High, Low, Close, Volume و...
        """
        
        try:
            # اگر تاریخ پایان مشخص نشده، تاریخ امروز را استفاده کن
            if end_date is None:
                today = jdatetime.date.today()
                end_date = f'{today.year:04d}-{today.month:02d}-{today.day:02d}'
            
            # بررسی کش
            cached_df = None
            last_cached_date = None
            
            if use_cache:
                cached_df, last_cached_date = self._load_from_cache(symbol)
                
                if cached_df is not None:
                    print(f"📦 کش یافت شد برای {symbol} (تا تاریخ {last_cached_date})")
                    
                    # اگر کش کامل است
                    if last_cached_date >= end_date:
                        print(f"✓ استفاده از کش کامل - {len(cached_df)} روز")
                        self.price_data[symbol] = cached_df
                        return cached_df
                    
                    # اگر نیاز به به‌روزرسانی است
                    print(f"🔄 به‌روزرسانی کش از {last_cached_date} تا {end_date}...")
                    start_date = last_cached_date  # فقط داده‌های جدید
            
            print(f"\n🌐 دریافت داده‌های آنلاین {symbol} از {start_date} تا {end_date}...")
            
            # استخراج داده با finpy-tse
            df = get_price_history(
                stock=symbol,
                start_date=start_date,
                end_date=end_date,
                ignore_date=False,
                adjust_price=adjust_price,
                show_weekday=True,
                double_date=True
            )
            
            if df is None or df.empty:
                if cached_df is not None:
                    print(f"⚠️ داده جدید نیافت شد - استفاده از کش")
                    self.price_data[symbol] = cached_df
                    return cached_df
                else:
                    print(f"⚠️ داده‌ای برای {symbol} یافت نشد")
                    return pd.DataFrame()
            
            # ترکیب با کش قبلی
            if cached_df is not None:
                # حذف تکراری‌ها
                df = pd.concat([cached_df, df])
                df = df[~df.index.duplicated(keep='last')]
                df = df.sort_index()
                print(f"✓ کش به‌روز شد: {len(df)} روز معاملاتی")
            else:
                print(f"✓ {len(df)} روز معاملاتی دریافت شد")
            
            # ذخیره کش
            if use_cache:
                self._save_to_cache(symbol, df)
            
            # ذخیره در حافظه
            self.price_data[symbol] = df
            
            return df
            
        except Exception as e:
            print(f"✗ خطا در دریافت داده‌های {symbol}: {e}")
            
            # در صورت خطا، سعی کن از کش استفاده کنی
            if use_cache:
                cached_df, _ = self._load_from_cache(symbol)
                if cached_df is not None:
                    print(f"📦 استفاده از کش به دلیل خطای آنلاین")
                    self.price_data[symbol] = cached_df
                    return cached_df
            
            return pd.DataFrame()
    
    def get_all_symbols_price_history(self, 
                                       symbols: list = None,
                                       start_date: str = '1400-01-01',
                                       end_date: str = None,
                                       adjust_price: bool = True,
                                       use_cache: bool = True) -> dict:
        """
        استخراج تاریخچه قیمت تمام نمادها
        
        Parameters:
        -----------
        symbols: لیست نمادها (اگر None باشد، همه نمادهای پروژه را دریافت می‌کند)
        start_date: تاریخ شروع
        end_date: تاریخ پایان
        adjust_price: استفاده از قیمت تعدیل شده
        
        Returns:
        --------
        dict: دیکشنری شامل DataFrame قیمت هر نماد
        """
        
        if symbols is None:
            # استفاده از همه نمادهای پروژه
            symbols = SYMBOLS['با_مازاد_منابع'] + SYMBOLS['با_کمبود_منابع']
        
        print("\n" + "="*70)
        print(f"استخراج داده‌های قیمتی {len(symbols)} نماد")
        print("="*70)
        
        all_data = {}
        
        for symbol in symbols:
            df = self.get_symbol_price_history(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                adjust_price=adjust_price,
                use_cache=use_cache
            )
            
            if not df.empty:
                all_data[symbol] = df
        
        self.price_data = all_data
        
        print("\n" + "="*70)
        print(f"✓ داده‌های قیمتی {len(all_data)} نماد دریافت شد")
        print("="*70)
        
        return all_data
    
    def calculate_returns(self, symbol: str, period: int = 1) -> pd.Series:
        """
        محاسبه بازده
        
        Parameters:
        -----------
        symbol: نماد سهم
        period: دوره محاسبه بازده (1 = روزانه، 5 = هفتگی، ...)
        
        Returns:
        --------
        pd.Series: سری بازده
        """
        
        if symbol not in self.price_data or self.price_data[symbol].empty:
            print(f"داده‌ای برای {symbol} موجود نیست")
            return pd.Series()
        
        df = self.price_data[symbol]
        
        # استفاده از قیمت تعدیل شده اگر موجود باشد
        if 'Adj Close' in df.columns:
            price_col = 'Adj Close'
        else:
            price_col = 'Close'
        
        returns = df[price_col].pct_change(period)
        
        return returns
    
    def calculate_volatility(self, symbol: str, window: int = 30) -> pd.Series:
        """
        محاسبه نوسان‌پذیری (Volatility)
        
        Parameters:
        -----------
        symbol: نماد سهم
        window: پنجره زمانی برای محاسبه (روز)
        
        Returns:
        --------
        pd.Series: سری نوسان‌پذیری
        """
        
        returns = self.calculate_returns(symbol)
        
        if returns.empty:
            return pd.Series()
        
        volatility = returns.rolling(window=window).std() * np.sqrt(252)  # سالانه
        
        return volatility
    
    def calculate_technical_indicators(self, symbol: str) -> pd.DataFrame:
        """
        محاسبه اندیکاتورهای تکنیکال
        
        Parameters:
        -----------
        symbol: نماد سهم
        
        Returns:
        --------
        pd.DataFrame: DataFrame شامل اندیکاتورهای مختلف
        """
        
        if symbol not in self.price_data or self.price_data[symbol].empty:
            print(f"داده‌ای برای {symbol} موجود نیست")
            return pd.DataFrame()
        
        df = self.price_data[symbol].copy()
        
        # استفاده از قیمت تعدیل شده
        if 'Adj Close' in df.columns:
            close_col = 'Adj Close'
        else:
            close_col = 'Close'
        
        # میانگین متحرک ساده (SMA)
        df['SMA_20'] = df[close_col].rolling(window=20).mean()
        df['SMA_50'] = df[close_col].rolling(window=50).mean()
        df['SMA_200'] = df[close_col].rolling(window=200).mean()
        
        # میانگین متحرک نمایی (EMA)
        df['EMA_12'] = df[close_col].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df[close_col].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # RSI (Relative Strength Index)
        delta = df[close_col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df[close_col].rolling(window=20).mean()
        bb_std = df[close_col].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # بازده
        df['Returns'] = df[close_col].pct_change()
        
        # نوسان‌پذیری
        df['Volatility_30'] = df['Returns'].rolling(window=30).std() * np.sqrt(252)
        
        return df
    
    def get_price_summary(self, symbol: str) -> dict:
        """
        خلاصه آماری داده‌های قیمتی
        
        Parameters:
        -----------
        symbol: نماد سهم
        
        Returns:
        --------
        dict: دیکشنری شامل آمار خلاصه
        """
        
        if symbol not in self.price_data or self.price_data[symbol].empty:
            print(f"داده‌ای برای {symbol} موجود نیست")
            return {}
        
        df = self.price_data[symbol]
        
        # استفاده از قیمت تعدیل شده
        if 'Adj Close' in df.columns:
            close_col = 'Adj Close'
        else:
            close_col = 'Close'
        
        returns = self.calculate_returns(symbol)
        
        summary = {
            'نماد': symbol,
            'تعداد روزهای معاملاتی': len(df),
            'اولین قیمت': df[close_col].iloc[0],
            'آخرین قیمت': df[close_col].iloc[-1],
            'حداقل قیمت': df[close_col].min(),
            'حداکثر قیمت': df[close_col].max(),
            'میانگین قیمت': df[close_col].mean(),
            'بازده کل': ((df[close_col].iloc[-1] / df[close_col].iloc[0]) - 1) * 100,
            'میانگین بازده روزانه': returns.mean() * 100,
            'نوسان روزانه': returns.std() * 100,
            'نوسان سالانه': returns.std() * np.sqrt(252) * 100,
            'میانگین حجم معاملات': df['Volume'].mean(),
            'میانگین ارزش معاملات': df['Value'].mean() if 'Value' in df.columns else 0
        }
        
        return summary
    
    def save_price_data(self, output_dir: str = 'output'):
        """
        ذخیره داده‌های قیمتی در فایل‌های Excel
        
        Parameters:
        -----------
        output_dir: مسیر پوشه خروجی
        """
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nذخیره داده‌های قیمتی در {output_dir}...")
        
        for symbol, df in self.price_data.items():
            if not df.empty:
                file_path = os.path.join(output_dir, f'price_history_{symbol}.xlsx')
                df.to_excel(file_path)
                print(f"✓ {symbol} ذخیره شد")
        
        print(f"\n✓ تمام داده‌ها در {output_dir} ذخیره شدند")


def test_price_extractor():
    """تست استخراج‌کننده قیمت"""
    
    extractor = PriceDataExtractor()
    
    # تست برای یک نماد
    symbol = 'زفجر'
    df = extractor.get_symbol_price_history(
        symbol=symbol,
        start_date='1402-01-01',
        adjust_price=True  # استفاده از قیمت تعدیل شده
    )
    
    if not df.empty:
        print(f"\nنمونه داده‌های قیمتی {symbol}:")
        print(df.head())
        
        # محاسبه اندیکاتورها
        df_indicators = extractor.calculate_technical_indicators(symbol)
        print(f"\nاندیکاتورهای تکنیکال {symbol}:")
        print(df_indicators[['Close', 'SMA_20', 'RSI', 'MACD']].tail())
        
        # خلاصه آماری
        summary = extractor.get_price_summary(symbol)
        print(f"\nخلاصه آماری {symbol}:")
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"  {key}: {value:,.2f}")
            else:
                print(f"  {key}: {value}")


if __name__ == "__main__":
    test_price_extractor()
