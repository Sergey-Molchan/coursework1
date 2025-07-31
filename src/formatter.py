from datetime import datetime
import pytz

def format_greeting() -> str:
    """Форматирование приветствия"""
    hour = datetime.now(pytz.timezone('Europe/Moscow')).hour
    if 5 <= hour < 12: return "Доброе утро"
    elif 12 <= hour < 17: return "Добрый день"
    elif 17 <= hour < 23: return "Добрый вечер"
    return "Доброй ночи"

def format_report(data: dict) -> dict:
    """Форматирование отчета"""
    return {
        "greeting": format_greeting(),
        "stats": {
            "transactions_count": data["total_transactions"],
            "total_amount": round(data["total_amount"], 2)
        },
        "categories": data["categories"]
    }