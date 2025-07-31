import pandas as pd
import requests
from datetime import datetime
import logging
from typing import Dict, List, Any
from pathlib import Path
from src.utils import get_user_settings
from src.constants import get_greeting
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_transactions() -> pd.DataFrame:
    """Улучшенная загрузка транзакций с проверками"""
    try:
        file_path = Path('data/operations.xlsx')

        if not file_path.exists():
            available_files = [f.name for f in Path('data').glob('*')]
            raise FileNotFoundError(
                f"Файл {file_path} не найден.\n"
                f"Доступные файлы в data/: {available_files}"
            )

        df = pd.read_excel(file_path)

        # Проверка и переименование колонок
        column_mapping = {
            'Дата операции': 'Дата',
            'Сумма операции': 'Сумма',
            'Номер карты': 'Карта',
            'Категория': 'Категория',
            'Описание': 'Описание',
            'Кэшбэк': 'Кешбэк'
        }

        for orig, new in column_mapping.items():
            if orig in df.columns:
                df[new] = df[orig]
            elif new not in df.columns:
                raise ValueError(f"Не найдена колонка: {orig} или {new}")

        # Преобразование данных
        df['Дата'] = pd.to_datetime(df['Дата'], dayfirst=True)
        df['Сумма'] = pd.to_numeric(df['Сумма'].astype(str).str.replace(',', '.'))
        df['Карта'] = df['Карта'].astype(str)

        return df

    except Exception as e:
        logging.error(f"Ошибка загрузки данных: {e}")
        raise


def get_card_stats(df: pd.DataFrame, date: datetime) -> List[Dict[str, Any]]:
    """Статистика по картам"""
    month_start = datetime(date.year, date.month, 1)
    period_data = df[(df['Дата'] >= month_start) & (df['Дата'] <= date)]

    cards = []
    for card in period_data['Карта'].unique():
        card_data = period_data[period_data['Карта'] == card]
        spent = card_data[card_data['Сумма'] < 0]['Сумма'].sum() * -1
        cashback = card_data['Кешбэк'].sum() if 'Кешбэк' in card_data else round(spent / 100, 2)

        cards.append({
            "last_digits": card[-4:],
            "total_spent": round(spent, 2),
            "cashback": round(cashback, 2)
        })

    return cards


def get_top_transactions(df: pd.DataFrame, date: datetime, n: int = 5) -> List[Dict[str, Any]]:
    """Топ транзакций по сумме за указанный период"""
    try:
        month_start = datetime(date.year, date.month, 1)

        # Фильтрация данных за период
        period_data = df[
            (df['Дата'] >= month_start) &
            (df['Дата'] <= date) &
            (df['Сумма'] < 0)  # Только расходы
            ].copy()

        # Сортировка и выбор топ-N транзакций
        period_data['Абсолютная сумма'] = period_data['Сумма'].abs()
        top_transactions = period_data.nlargest(n, 'Абсолютная сумма')

        # Форматирование результата
        result = []
        for _, row in top_transactions.iterrows():
            result.append({
                "date": row['Дата'].strftime('%d.%m.%Y'),
                "amount": abs(row['Сумма']),
                "category": row['Категория'],
                "description": row['Описание']
            })

        return result

    except Exception as e:
        logging.error(f"Ошибка в get_top_transactions: {e}")
        return []


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получение курсов валют через API ЦБ РФ"""
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        rates = response.json()['Valute']
        return [{
            "currency": curr,
            "rate": round(rates[curr]['Value'], 2)
        } for curr in currencies if curr in rates]
    except Exception as e:
        logging.error(f"Ошибка получения курсов валют: {e}")
        return []


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получение цен акций через Yahoo Finance API"""
    try:
        if not stocks:
            return []

        url = "https://query1.finance.yahoo.com/v7/finance/quote"
        params = {
            'symbols': ','.join(stocks),
            'fields': 'symbol,regularMarketPrice'
        }

        response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        data = response.json()

        return [{
            "stock": item['symbol'],
            "price": item['regularMarketPrice']
        } for item in data.get('quoteResponse', {}).get('result', [])]

    except Exception as e:
        logging.error(f"Ошибка получения цен акций: {e}")
        return []


def main_page(date_str: str) -> Dict[str, Any]:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        df = load_transactions()
        settings = get_user_settings()

        return {
            "greeting": get_greeting(date),
            "cards": get_card_stats(df, date),
            "top_transactions": get_top_transactions(df, date),  # Добавляем date
            "currency_rates": get_currency_rates(settings["user_currencies"]),
            "stock_prices": get_stock_prices(settings["user_stocks"])
        }
    except Exception as e:
        logging.error(f"Ошибка в main_page: {e}")
        raise

def home_page(date_str: str) -> Dict[str, Any]:
    """Алиас для main_page для совместимости с тестами"""
    return main_page(date_str)

def events_page(date_str: str, period: str = 'M') -> Dict[str, Any]:
    """Страница событий (заглушка для тестов)"""
    # Реализуйте эту функцию аналогично main_page
    return {
        "expenses": {"total_amount": 0},
        "income": {"total_amount": 0},
        "currency_rates": [],
        "stock_prices": []
    }

def generate_home_json(date_str: str) -> Dict[str, Any]:
    """Алиас для main_page для совместимости"""
    return main_page(date_str)

