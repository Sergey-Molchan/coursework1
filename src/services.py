import pandas as pd
from datetime import datetime
import logging
from typing import List, Dict, Any
import requests
import os
from dotenv import load_dotenv
from functools import lru_cache
import time

logger = logging.getLogger(__name__)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


def _get_greeting(time: datetime) -> str:
    """Определение приветствия по времени суток"""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загрузка данных из Excel"""
    try:
        df = pd.read_excel(file_path)
        df['Дата'] = pd.to_datetime(df['Дата операции'], dayfirst=True).dt.normalize()
        df['Сумма'] = pd.to_numeric(df['Сумма операции'].astype(str).str.replace(',', '.'))
        # Обработка NaN в номерах карт
        df['Карта'] = df['Номер карты'].astype(str).str[-4:].replace('nan', 'N/A')
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        raise


def get_card_stats(df: pd.DataFrame, date: datetime) -> List[Dict[str, Any]]:
    """Статистика по картам"""
    try:
        period_data = df[df['Дата'].dt.date == date.date()]

        if period_data.empty:
            logger.warning(f"Нет данных за {date.date()}")
            return []

        cards = []
        for card in period_data['Карта'].unique():
            card_data = period_data[period_data['Карта'] == card]
            spent = card_data[card_data['Сумма'] < 0]['Сумма'].sum() * -1
            cashback = round(spent / 100, 2)
            cards.append({
                "last_digits": card,
                "total_spent": float(round(spent, 2)),  # Преобразуем в float
                "cashback": float(cashback)  # Преобразуем в float
            })
        return cards
    except Exception as e:
        logger.error(f"Ошибка в get_card_stats: {e}")
        return []


def get_top_transactions(df: pd.DataFrame, date: datetime, n: int = 5) -> List[Dict[str, Any]]:
    """Топ транзакций по сумме"""
    try:
        period_data = df[
            (df['Дата'].dt.date == date.date()) &
            (df['Сумма'] < 0)
            ].copy()

        if period_data.empty:
            logger.warning(f"Нет транзакций за {date.date()}")
            return []

        period_data['Сумма'] = period_data['Сумма'].abs()
        top = period_data.nlargest(n, 'Сумма')

        # Преобразуем Timestamp в строку
        return [{
            'Дата': row['Дата'].strftime('%Y-%m-%d %H:%M:%S'),
            'Сумма': row['Сумма'],
            'Категория': row['Категория'],
            'Описание': row['Описание']
        } for _, row in top.iterrows()]
    except Exception as e:
        logger.error(f"Ошибка в get_top_transactions: {e}")
        return []


@lru_cache(maxsize=32)
def get_stock_prices_cached(stocks: str, ttl_hash=None) -> List[Dict[str, Any]]:
    """Кэшированная версия на 5 минут"""
    del ttl_hash
    return get_stock_prices(stocks.split(','))


def get_ttl_hash(seconds=300):
    """Хэш для инвалидации кэша по времени"""
    return round(time.time() / seconds)


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получение цен акций через Financial Modeling Prep API"""
    try:
        api_key = os.getenv('FMP_API_KEY')
        if not api_key:
            raise ValueError("FMP_API_KEY не найден в .env файле")

        response = requests.get(
            f'https://financialmodelingprep.com/api/v3/quote/{",".join(stocks)}',
            params={'apikey': api_key},
            timeout=10
        )
        response.raise_for_status()
        quotes = response.json()

        if isinstance(quotes, dict) and quotes.get('Error Message'):
            raise ValueError(f"API Error: {quotes['Error Message']}")

        return [{
            "stock": q['symbol'],
            "price": round(q['price'], 2),
            "change": round(q['change'], 2),
            "change_percent": round(q['changesPercentage'], 2)
        } for q in quotes]
    except Exception as e:
        logger.error(f"Ошибка получения акций: {e}")
        return []


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Заглушка для курсов валют"""
    return [
        {"currency": "USD", "rate": 75.50},
        {"currency": "EUR", "rate": 85.30}
    ]


