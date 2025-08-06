import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pandas as pd
from src.services import (
    process_transactions,
    get_card_stats,
    get_currency_rates,
    get_sp500_data
)


# Фикстуры для тестовых данных
@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        'Дата операции': ['01.01.2023 12:00:00', '02.01.2023 13:00:00'],
        'Сумма операции': ['-1000,50', '500,75'],
        'Номер карты': ['1234567890123456', None],
        'Категория': ['Еда', 'Транспорт'],
        'Описание': ['Покупка в магазине', 'Такси'],
        'Кешбэк': [5.0, 0.0]
    })


# Тесты для process_transactions
def test_process_transactions(sample_transactions):
    with patch('pandas.to_datetime') as mock_datetime:
        mock_datetime.return_value = pd.Series([
            datetime(2023, 1, 1),
            datetime(2023, 1, 2)
        ])

        result = process_transactions(sample_transactions)

        assert not result.empty
        assert 'Дата' in result.columns
        assert 'Сумма' in result.columns
        assert result['Номер карты'].iloc[0] == '3456'


# Тесты для get_card_stats
def test_get_card_stats(sample_transactions):
    processed = process_transactions(sample_transactions)
    date = datetime(2023, 1, 1)

    result = get_card_stats(processed, date)

    assert isinstance(result, list)
    if result:  # Если есть данные
        assert 'last_digits' in result[0]
        assert 'total_spent' in result[0]


# Тесты для API функций
@patch('requests.get')
def test_get_currency_rates(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'conversion_rates': {'USD': 1.0, 'EUR': 0.9, 'RUB': 70.0}
    }
    mock_get.return_value = mock_response

    result = get_currency_rates()

    assert len(result) == 3
    assert any(r['currency'] == 'USD' for r in result)


@patch('requests.get')
def test_get_sp500_data(mock_get):
    mock_response_index = MagicMock()
    mock_response_index.json.return_value = [{
        'price': 4000.0,
        'change': 50.0,
        'changesPercentage': 1.25
    }]

    mock_response_companies = MagicMock()
    mock_response_companies.json.return_value = [
        {'symbol': 'AAPL', 'name': 'Apple', 'price': 150.0},
        {'symbol': 'MSFT', 'name': 'Microsoft', 'price': 250.0}
    ]

    mock_get.side_effect = [mock_response_index, mock_response_companies]

    result = get_sp500_data()

    assert 'index' in result
    assert 'stocks' in result
    assert len(result['stocks']) > 0