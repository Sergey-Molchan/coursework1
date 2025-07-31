from unittest.mock import patch
import pytest
import pandas as pd
from src.views import home_page


@pytest.fixture
def sample_data():
    return {
        'Дата операции': ['31.12.2021 16:44:00'],
        'Номер карты': ['*7197'],
        'Сумма операции': ['-160,89'],
        'Категория': ['Супермаркеты'],
        'Описание': ['Магнит']
    }


@patch('src.services.get_stock_prices')  # Мокаем только get_stock_prices
def test_home_page(mock_get_stocks, sample_data, tmp_path):
    # 1. Подготовка тестовых данных
    test_file = tmp_path / "test_operations.xlsx"
    df = pd.DataFrame(sample_data)
    df['Дата'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    df['Сумма'] = pd.to_numeric(df['Сумма операции'].str.replace(',', '.'))
    df['Карта'] = df['Номер карты'].str[-4:]
    df.to_excel(test_file, index=False)

    # 2. Настройка моков
    mock_get_stocks.return_value = [{"stock": "AAPL", "price": 175.50}]

    # 3. Вызов тестируемой функции с реальным файлом
    result = home_page("2021-12-31 15:30:00", str(test_file))

    # 4. Проверки результатов
    assert result['greeting'] == "Добрый день"
    assert len(result['cards']) == 1
    assert result['cards'][0]['last_digits'] == '7197'
    assert len(result['top_transactions']) == 1
    assert len(result['stock_prices']) == 1
    assert result['stock_prices'][0]['stock'] == 'AAPL'

    # 5. Проверка вызова API (без проверки load_transactions)
    mock_get_stocks.assert_called_once()