import pytest
from datetime import datetime
import pandas as pd
from unittest.mock import patch, MagicMock
from src.services import (
    _get_greeting,
    load_transactions,
    get_card_stats,
    get_top_transactions,
    get_stock_prices,
    get_currency_rates,
    get_stock_prices_cached
)

# Фикстуры для тестов
@pytest.fixture
def sample_dataframe():
    """Фиктивный DataFrame для тестирования"""
    data = {
        'Дата операции': ['31.12.2021 16:44:00', '31.12.2021 16:42:04'],
        'Номер карты': ['*7197', '*5091'],
        'Сумма операции': ['-160,89', '-64,00'],
        'Категория': ['Супермаркеты', 'Развлечения'],
        'Описание': ['Магнит', 'Кинотеатр']
    }
    return pd.DataFrame(data)

@pytest.fixture
def mock_env(monkeypatch):
    """Фиктивная среда с API ключом"""
    monkeypatch.setenv('FMP_API_KEY', 'test_api_key')

class TestGreeting:
    def test_morning_greeting(self):
        assert _get_greeting(datetime(2023, 1, 1, 6)) == "Доброе утро"

class TestLoadTransactions:
    def test_load_valid_data(self, tmp_path, sample_dataframe):
        test_file = tmp_path / "test_operations.xlsx"
        sample_dataframe.to_excel(test_file, index=False)
        df = load_transactions(str(test_file))
        assert len(df) == 2

class TestCardStats:
    def test_card_stats_calculation(self, sample_dataframe):
        df = sample_dataframe.copy()
        df['Дата'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
        df['Сумма'] = pd.to_numeric(df['Сумма операции'].str.replace(',', '.'))
        df['Карта'] = df['Номер карты'].str[-4:]
        result = get_card_stats(df, datetime(2021, 12, 31))
        assert len(result) == 2

class TestTopTransactions:
    def test_top_transactions(self, sample_dataframe):
        df = sample_dataframe.copy()
        df['Дата'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
        df['Сумма'] = pd.to_numeric(df['Сумма операции'].str.replace(',', '.'))
        result = get_top_transactions(df, datetime(2021, 12, 31), n=2)
        assert len(result) == 2


class TestStockPrices:
    @patch('src.services.requests.get')
    def test_successful_api_call(self, mock_get, mock_env):
        # Мокируем ответ API
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "symbol": "AAPL",
                "price": 175.50,
                "change": -1.25,
                "changesPercentage": -0.71
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_stock_prices(["AAPL"])
        assert len(result) == 1
        assert result[0]['stock'] == "AAPL"
        assert result[0]['price'] == 175.50

    @patch('src.services.requests.get')
    def test_failed_api_call(self, mock_get, mock_env):
        mock_get.side_effect = Exception("API Error")
        result = get_stock_prices(["AAPL"])
        assert result == []

class TestStockPricesCached:
    @patch('src.services.get_stock_prices')
    def test_caching(self, mock_get):
        mock_get.return_value = [{"stock": "TEST", "price": 100}]
        get_stock_prices_cached("TEST")
        get_stock_prices_cached("TEST")
        mock_get.assert_called_once()

class TestCurrencyRates:
    def test_currency_rates(self):
        result = get_currency_rates(["USD", "EUR"])
        assert len(result) == 2