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
    """Тест успешного формирования главной страницы"""
    # Настраиваем моки
    mock_load.return_value = mock_transactions

    processed_data = mock_transactions.copy()
    processed_data['Дата'] = pd.to_datetime(processed_data['Дата операции'])
    processed_data['Сумма'] = pd.to_numeric(
        processed_data['Сумма операции'].str.replace(',', '.')
    )
    mock_process.return_value = processed_data

    # Вызываем тестируемую функцию
    result = home_page('dummy_path.xlsx')

    # Проверяем результаты
    assert isinstance(result, dict)
    assert 'date' in result
    assert 'cards' in result
    assert 'top_transactions' in result
    assert 'available_columns' in result
    assert isinstance(result['cards'], list)
    assert isinstance(result['top_transactions'], list)
    assert len(result['available_columns']) > 0


@patch('src.views.load_transactions')
def test_home_page_empty_data(mock_load):
    """Тест обработки пустых данных"""
    mock_load.return_value = pd.DataFrame(columns=[
        'Дата операции', 'Сумма операции', 'Номер карты',
        'Категория', 'Описание', 'Кешбэк', 'Статус'
    ])

    result = home_page('dummy_path.xlsx')

    assert isinstance(result, dict)
    assert 'error' in result
    assert 'Нет данных для отображения' in result['error']
    assert 'available_columns' in result


@patch('src.views.load_transactions')
def test_home_page_processing_error(mock_load, mock_transactions):
    """Тест обработки ошибок при загрузке данных"""
    # Настраиваем мок так, чтобы он вызывал исключение
    mock_load.side_effect = Exception("Test error")

    result = home_page('dummy_path.xlsx')

    assert isinstance(result, dict)
    assert 'error' in result
    assert result['error'] == "Test error"  # Проверяем точное соответствие
    assert 'available_columns' in result
    assert result['available_columns'] == []  # Проверяем пустой список колонок