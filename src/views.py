import pandas as pd
from datetime import datetime
import logging
from typing import Dict, Any
from config.settings import get_settings
from config.api_config import get_currency_rates, get_stock_prices
from .utils import load_transactions, format_date

logger = logging.getLogger(__name__)


def home_page(date_str: str) -> Dict[str, Any]:
    """Главная страница - генерация JSON"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        df = load_transactions()
        settings = get_settings()

        return {
            "greeting": _get_greeting(date),
            "cards": _get_card_stats(df, date),
            "top_transactions": _get_top_transactions(df, date),
            "currency_rates": get_currency_rates(settings['currencies']),
            "stock_prices": get_stock_prices(settings['stocks'])
        }
    except Exception as e:
        logger.error(f"Error in home_page: {e}")
        raise


def _get_greeting(time: datetime) -> str:
    """Определение приветствия по времени суток"""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"tr)

