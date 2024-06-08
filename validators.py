from datetime import datetime
import re

def coupone_add_validator(text):
    pattern = r"^(['\"])(.*?)\1(?:\s+(.*))?$"
    
    match = re.match(pattern, text)
    if not match:
        raise ValueError("Неверный формат строки.")

def date_validator(date):
    # Формат
    date_pattern = re.compile(r'^\d{2}\.\d{2}\.(\d{2}|\d{4})$')

    if not date_pattern.match(date):
        return False

    try:
        day, month, year = date.split('.')

        day = int(day)
        month = int(month)
        year = int(year)
        
        if not (1 <= day <= 31):
            return False
        if not (1 <= month <= 12):
            return False
        
        # Check the length of the year and adjust if necessary
        if len(str(year)) == 2:
            year += 2000  # Преобразуем двузначный год в четырехзначный, если он меньше 20
            
        # Format the date and return it
        formatted_date = f"{day:02d}.{month:02d}.{year}"
        return formatted_date
        
    except ValueError:
        # If any value is invalid, return False
        return False