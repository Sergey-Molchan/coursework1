import pytest
from unittest.mock import patch
import pandas as pd
from src.views import home_page


@pytest.fixture
def mock_transactions():
    return pd.DataFrame({
        'Дата операции': ['01.01.2023 12:00:00', '02.01.2023 13:00:00'],
        'Сумма операции': ['-1000,50', '500,75'],
        'Номер карты': ['1234567890123456', None],
        'Категория': ['Еда', 'Транспорт'],
        'Описание': ['Покупка в магазине', 'Такси'],
        'Кешбэк': [5.0, 0.0],
        'Статус': ['OK', 'OK']
    })


@patch('src.views.load_transactions')
@patch('src.views.process_transactions')
def test_home_page_success(mock_process, mock_load, mock_transactions):
    # Подготовка моков
    mock_load.return_value = mock_transactions

    processed_data = mock_transactions.copy()
    processed_data['Дата'] = pd.to_datetime(processed_data['Дата операции'])
    processed_data['Сумма'] = pd.to_numeric(
        processed_data['Сумма операции'].str.replace(',', '.')
    )
    mock_process.return_value = processed_data

    # Вызов функции
    result = home_page('dummy_path.xlsx')

    # Проверки
    assert isinstance(result, dict)
    assert 'date' in result
    assert 'cards' in result
    assert 'top_transactions' in result
    assert isinstance(result['cards'], list)
    assert isinstance(result['top_transactions'], list)


@patch('src.views.load_transactions')
def test_home_page_empty_data(mock_load):
    # Пустой DataFrame с нужными колонками
    mock_load.return_value = pd.DataFrame(columns=[
        'Дата операции', 'Сумма операции', 'Номер карты',
        'Категория', 'Описание', 'Кешбэк', 'Статус'
    ])

    result = home_page('dummy_path.xlsx')

    assert isinstance(result, dict)
    assert 'error' in result
    assert 'Нет данных для отображения' in result['error']


@patch('src.views.load_transactions')
def test_home_page_processing_error(mock_load, mock_transactions):
    mock_load.return_value = mock_transactions
    mock_load.side_effect = Exception("Test error")

    result = home_page('dummy_path.xlsx')

    assert isinstance(result, dict)
    assert 'error' in result
    assert 'Test error' in result['error']