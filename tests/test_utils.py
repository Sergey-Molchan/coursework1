import pytest
import pandas as pd
from src.utils import load_transactions
import os
from unittest.mock import patch


@pytest.fixture
def sample_excel_path(tmp_path):
    """Создаем временный Excel-файл для тестов"""
    data = {
        'Дата операции': ['01.01.2023 12:00:00', '02.01.2023 13:30:00'],
        'Сумма операции': [100.50, 200.75],
        'Категория': ['Еда', 'Транспорт']
    }
    df = pd.DataFrame(data)
    path = os.path.join(tmp_path, "test_transactions.xlsx")
    df.to_excel(path, index=False)
    return path


def test_load_valid_file(sample_excel_path):
    """Тест загрузки корректного файла"""
    df = load_transactions(sample_excel_path)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'Дата операции' in df.columns
    assert 'Сумма операции' in df.columns
    assert df['Дата операции'].dt.day[0] == 1  # Проверяем парсинг даты


def test_file_not_found():
    """Тест на отсутствие файла"""
    with pytest.raises(FileNotFoundError):
        load_transactions("nonexistent_file.xlsx")


def test_missing_columns(tmp_path):
    """Тест на отсутствие обязательных колонок"""
    # Создаем файл без нужных колонок
    path = os.path.join(tmp_path, "bad_data.xlsx")
    pd.DataFrame({'Wrong_Column': [1, 2]}).to_excel(path, index=False)

    with pytest.raises(ValueError) as excinfo:
        load_transactions(path)
    assert "Отсутствуют колонки" in str(excinfo.value)


@patch('pandas.read_excel')
def test_unexpected_error(mock_read):
    """Тест на неожиданные ошибки"""
    mock_read.side_effect = Exception("Unexpected error")

    with pytest.raises(Exception):
        load_transactions("any_file.xlsx")