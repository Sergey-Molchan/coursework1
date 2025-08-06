import requests
import os
from datetime import datetime
import logging
from typing import Dict, List, Any
import pandas as pd
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


# API Services
@lru_cache(maxsize=32)
def get_currency_rates(base: str = "USD") -> List[Dict[str, float]]:
    """Получение курсов валют через ExchangeRate-API"""
    try:
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not api_key:
            raise ValueError("EXCHANGE_RATE_API_KEY not set in .env")

        response = requests.get(
            f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return [
            {"currency": "USD", "rate": round(data["conversion_rates"]["USD"], 2)},
            {"currency": "EUR", "rate": round(data["conversion_rates"]["EUR"], 2)},
            {"currency": "RUB", "rate": round(data["conversion_rates"]["RUB"], 2)}
        ]
    except Exception as e:
        logger.error(f"Currency API error: {e}")
        return []


@lru_cache(maxsize=32)
def get_sp500_data() -> Dict[str, Any]:
    """Получение данных S&P 500 через Financial Modeling Prep"""
    try:
        api_key = os.getenv("FMP_API_KEY")
        if not api_key:
            raise ValueError("FMP_API_KEY not set in .env")

        # Получаем данные индекса
        index_response = requests.get(
            f"https://financialmodelingprep.com/api/v3/quote/%5EGSPC?apikey={api_key}",
            timeout=10
        )
        index_response.raise_for_status()
        index_data = index_response.json()[0]

        # Получаем топ-5 компаний
        companies_response = requests.get(
            f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={api_key}",
            timeout=10
        )
        companies_response.raise_for_status()
        top_companies = companies_response.json()[:5]

        return {
            "index": {
                "symbol": "^GSPC",
                "price": round(index_data["price"], 2),
                "change": round(index_data["change"], 2),
                "change_percent": round(index_data["changesPercentage"], 2)
            },
            "stocks": [{
                "symbol": company["symbol"],
                "price": round(float(company.get("price", 0)), 2),
                "name": company["name"]
            } for company in top_companies]
        }
    except Exception as e:
        logger.error(f"Stock API error: {e}")
        return {}


# Основные сервисы
def get_greeting() -> str:
    """Приветствие по времени суток"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def process_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Подготовка данных с автозаполнением отсутствующих колонок"""
    try:
        # Базовые преобразования
        df['Дата'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S', errors='coerce')
        df['Сумма'] = pd.to_numeric(df['Сумма операции'].astype(str).str.replace(',', '.'), errors='coerce')

        # Заполняем отсутствующие колонки
        if 'Номер карты' not in df.columns:
            df['Номер карты'] = ''
        else:
            df['Номер карты'] = df['Номер карты'].fillna('').astype(str).str[-4:]

        if 'Статус' not in df.columns:
            df['Статус'] = 'OK'

        if 'Категория' not in df.columns:
            df['Категория'] = 'Другое'

        if 'Описание' not in df.columns:
            df['Описание'] = ''

        if 'Кешбэк' not in df.columns:
            df['Кешбэк'] = 0.0

        return df.dropna(subset=['Дата', 'Сумма'])
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        raise


def get_card_stats(df: pd.DataFrame, date: datetime) -> List[Dict[str, Any]]:
    """Статистика по картам с защитой от отсутствия данных"""
    try:
        day_data = df[df['Дата'].dt.date == date.date()]
        cards = []

        for card in day_data['Номер карты'].unique():
            if not card:
                continue

            card_data = day_data[day_data['Номер карты'] == card]
            spent = card_data[card_data['Сумма'] < 0]['Сумма'].sum() * -1

            cards.append({
                "last_digits": card,
                "total_spent": round(float(spent), 2),
                "cashback": round(float(card_data['Кешбэк'].sum()), 2)
            })

        return cards
    except Exception as e:
        logger.error(f"Ошибка в get_card_stats: {e}")
        return []


def get_top_transactions(df: pd.DataFrame, date: datetime, n: int = 5) -> List[Dict[str, Any]]:
    """Топ транзакций с защитой от отсутствия данных"""
    try:
        day_data = df[
            (df['Дата'].dt.date == date.date())
            & (df['Сумма'] < 0)
        ].copy()

        day_data['Сумма'] = day_data['Сумма'].abs()
        top = day_data.nlargest(n, 'Сумма')

        return [{
            'date': row['Дата'].strftime('%d.%m.%Y'),
            'amount': abs(row['Сумма']),
            'category': row.get('Категория', 'Другое'),
            'description': row.get('Описание', '')
        } for _, row in top.iterrows()]
    except Exception as e:
        logger.error(f"Ошибка в get_top_transactions: {e}")
        return []
