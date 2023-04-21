from datetime import datetime

def get_current_day():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")