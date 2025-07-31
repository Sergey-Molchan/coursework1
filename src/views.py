from datetime import datetime
import pandas as pd
import requests
from config import FMP_API_KEY, FMP_BASE_URL

def get_currency_rates(currencies: list) -> list:
    """Получение курсов валют через FMP API."""
    rates = []
    for currency in currencies:
        url = f"{FMP_BASE_URL}/quote/{currency}USD?apikey={FMP_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rates.append({
                "currency": currency,
                "rate": data[0]['price'] if data else None
            })
    return rates

def generate_home_json(date_str: str, df: pd.DataFrame) -> dict:
    """Генерация JSON для главной страницы."""
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    filtered = df[df['Дата'] <= date]

    greeting = "Добрый день"  # Упрощённый пример
    cards = [{
        "last_digits": str(row['Карта'])[-4:],
        "total_spent": 1000,  # Замените на реальные расчёты
        "cashback": 10.0
    } for _, row in df.iterrows()]

    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": filtered.nlargest(5, 'Сумма').to_dict('records'),
        "currency_rates": [{"currency": "USD", "rate": 75.5}],
        "stock_prices": [{"stock": "AAPL", "price": 150.0}]
    }