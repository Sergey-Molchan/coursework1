import requests
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получение курсов валют через API"""
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        rates = response.json()['rates']
        return [{"currency": curr, "rate": rates.get(curr)} for curr in currencies]
    except Exception as e:
        logger.error(f"Currency API error: {e}")
        return []

def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получение цен акций через API"""
    try:
        symbols = ','.join(stocks)
        response = requests.get(f'https://api.stockdata.org/v1/data/quote?symbols={symbols}')
        return [{"stock": item['symbol'], "price": item['price']} for item in response.json()['data']]
    except Exception as e:
        logger.error(f"Stocks API error: {e}")
        return []