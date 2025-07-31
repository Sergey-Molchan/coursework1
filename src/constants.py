from datetime import datetime
import pytz

def get_greeting(time: datetime) -> str:
    """Определение приветствия по времени суток"""
    try:
        hour = time.astimezone(pytz.timezone('Europe/Moscow')).hour
        if 5 <= hour < 12: return "Доброе утро"
        elif 12 <= hour < 17: return "Добрый день"
        elif 17 <= hour < 23: return "Добрый вечер"
        return "Доброй ночи"
    except Exception as e:
        return "Добрый день"