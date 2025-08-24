from datetime import datetime

def format_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    result = date.strftime("%d.%m.%Y")
    return result

def format_date_time(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    result = date.strftime("%d.%m.%Y %H:%M")
    return result
