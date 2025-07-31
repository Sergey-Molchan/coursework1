import requests
from datetime import datetime, timedelta
import logging
from functools import wraps
logger = logging.getLogger(__name__)


def safe_api_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except ValueError as e:
            logger.error(f"Invalid API response: {e}")
            return None

    return wrapper


class FMPAPI:
    BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._cache = {}
        self._cache_expiry = timedelta(minutes=5)

    def _get_from_cache(self, key: str):
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_expiry:
                return data
        return None

    def _set_to_cache(self, key: str, data):
        self._cache[key] = (data, datetime.now())

    @safe_api_call
    def get_stock_prices(self, symbols: list) -> list:
        cache_key = f"stocks_{'_'.join(sorted(symbols))}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        endpoint = f"{self.BASE_URL}/quote/{','.join(symbols)}"
        response = requests.get(endpoint, params={'apikey': self.api_key})
        response.raise_for_status()
        data = response.json()

        self._set_to_cache(cache_key, data)
        return data

    @safe_api_call
    def get_currency_rates(self, currencies: list) -> list:
        cache_key = f"fx_{'_'.join(sorted(currencies))}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        endpoint = f"{self.BASE_URL}/fx"
        response = requests.get(endpoint, params={'apikey': self.api_key})
        response.raise_for_status()
        data = response.json()

        filtered_data = [fx for fx in data if fx['ticker'] in currencies]
        self._set_to_cache(cache_key, filtered_data)
        return filtered_data