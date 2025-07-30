from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List
from api_client import FMPAPI
from settings import Settings

def _get_greeting(hour: int) -> str:
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def _process_cards_data(operations: pd.DataFrame, dt: datetime) -> Dict:
    mask = (operations['Дата операции'] >= dt - timedelta(days=30)) & \
           (operations['Дата операции'] <= dt)
    return operations[mask].groupby('Карта')['Сумма операции'].sum().to_dict()


def _get_top_transactions(operations: pd.DataFrame, dt: datetime) -> List[Dict]:
    """Топ-5 операций за месяц."""
    mask = (operations['Дата операции'].dt.month == dt.month) & \
           (operations['Дата операции'].dt.year == dt.year)
    return operations[mask].nlargest(5, 'Сумма операции').to_dict('records')

def _process_expenses(data: pd.DataFrame) -> Dict:
    """Сумма расходов по категориям."""
    return data[data['Сумма операции'] < 0].groupby('Категория')['Сумма операции'].sum().to_dict()

def _process_income(data: pd.DataFrame) -> Dict:
    """Сумма доходов по категориям."""
    return data[data['Сумма операции'] > 0].groupby('Категория')['Сумма операции'].sum().to_dict()

def home_view(input_date: str, operations: pd.DataFrame) -> Dict:
    dt = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    settings = Settings()  # Создаем экземпляр
    api = FMPAPI(settings.API_KEY)
    currencies = [f"USD{c}" for c in settings.USER_CURRENCIES if c != "USD"]
    fx_data = api.get_currency_rates(currencies) or []
    stock_data = api.get_stock_prices(settings.USER_STOCKS) or []

    return {
        "greeting": _get_greeting(dt.hour),
        "cards": _process_cards_data(operations, dt),
        "top_transactions": _get_top_transactions(operations, dt),
        "currency_rates": [{"currency": fx['ticker'][3:], "rate": fx['bid']} for fx in fx_data],
        "stock_prices": [{"stock": s['symbol'], "price": s['price']} for s in stock_data]
    }

def events_view(input_date: str, operations: pd.DataFrame, period: str = 'M') -> Dict:
    dt = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    filtered_data = _filter_by_period(operations, dt, period)
    return {
        "expenses": _process_expenses(filtered_data),
        "income": _process_income(filtered_data),
        "currency_rates": home_view(input_date, operations)["currency_rates"],
        "stock_prices": home_view(input_date, operations)["stock_prices"]
    }

def _filter_by_period(data: pd.DataFrame, dt: datetime, period: str) -> pd.DataFrame:
    if period == 'W':
        start = dt - timedelta(days=dt.weekday())
    elif period == 'M':
        start = dt.replace(day=1)
    elif period == 'Y':
        start = dt.replace(month=1, day=1)
    else:
        return data
    return data[(data['Дата операции'] >= start) & (data['Дата операции'] <= dt)]