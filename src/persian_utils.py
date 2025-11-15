"""
تبدیل اعداد و متن‌های فارسی
"""

import re
from typing import Union

# نگاشت اعداد انگلیسی به فارسی
PERSIAN_DIGITS = {
    '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
    '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
}

ENGLISH_DIGITS = {v: k for k, v in PERSIAN_DIGITS.items()}


def to_persian_digits(text: Union[str, int, float]) -> str:
    """تبدیل اعداد انگلیسی به فارسی"""
    text = str(text)
    for eng, per in PERSIAN_DIGITS.items():
        text = text.replace(eng, per)
    return text


def to_english_digits(text: str) -> str:
    """تبدیل اعداد فارسی به انگلیسی"""
    for per, eng in ENGLISH_DIGITS.items():
        text = text.replace(per, eng)
    return text


def format_number(number: Union[int, float], decimals: int = 2) -> str:
    """
    فرمت کردن عدد با جداکننده هزارگان و تبدیل به فارسی
    
    Parameters:
    -----------
    number: عدد ورودی
    decimals: تعداد اعشار
    
    Returns:
    --------
    str: عدد فرمت شده به فارسی
    """
    if number is None or (isinstance(number, float) and (number != number)):  # NaN check
        return '۰'
    
    try:
        # فرمت با جداکننده
        if isinstance(number, float):
            formatted = f"{number:,.{decimals}f}"
        else:
            formatted = f"{number:,}"
        
        # تبدیل به فارسی
        return to_persian_digits(formatted)
    except:
        return to_persian_digits(str(number))


def format_percentage(number: Union[int, float], decimals: int = 2) -> str:
    """فرمت درصد"""
    if number is None:
        return '۰٪'
    return format_number(number, decimals) + '٪'


def format_currency(amount: Union[int, float], unit: str = 'ریال') -> str:
    """فرمت پول"""
    if amount is None:
        return f'۰ {unit}'
    
    # تبدیل به میلیارد یا میلیون برای خوانایی بهتر
    if abs(amount) >= 1_000_000_000:
        value = amount / 1_000_000_000
        return f"{format_number(value, 2)} میلیارد {unit}"
    elif abs(amount) >= 1_000_000:
        value = amount / 1_000_000
        return f"{format_number(value, 2)} میلیون {unit}"
    else:
        return f"{format_number(amount, 0)} {unit}"


def number_to_persian_words(number: int) -> str:
    """تبدیل عدد به حروف فارسی (برای اعداد کوچک)"""
    ones = ['', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه']
    tens = ['', '', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود']
    hundreds = ['', 'یکصد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد']
    
    if number == 0:
        return 'صفر'
    
    if number < 10:
        return ones[number]
    elif number < 20:
        teens = ['ده', 'یازده', 'دوازده', 'سیزده', 'چهارده', 'پانزده', 'شانزده', 'هفده', 'هجده', 'نوزده']
        return teens[number - 10]
    elif number < 100:
        return tens[number // 10] + (' و ' + ones[number % 10] if number % 10 != 0 else '')
    elif number < 1000:
        return hundreds[number // 100] + (' و ' + number_to_persian_words(number % 100) if number % 100 != 0 else '')
    else:
        return to_persian_digits(str(number))


if __name__ == "__main__":
    # تست
    print(format_number(1234567.89))  # ۱,۲۳۴,۵۶۷.۸۹
    print(format_percentage(45.67))  # ۴۵.۶۷٪
    print(format_currency(1500000000))  # ۱.۵۰ میلیارد ریال
    print(number_to_persian_words(123))  # یکصد و بیست و سه
