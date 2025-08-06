import pytest
from datetime import datetime, timedelta
from src.analytics import spending_by_category
import pandas as pd
import os



@pytest.fixture
def sample_data(tmp_path):
    """Создает тестовый Excel файл с транзакциями"""
    data = {
        'Дата': [datetime.now() - timedelta(days=i) for i in range(1, 100)],
        'Категория': ['Еда'] * 50 + ['Транспорт'] * 30 + ['Развлечения'] * 19,
        'Сумма': [100 + i for i in range(1, 100)]
    }
    df = pd.DataFrame(data)
    path = os.path.join(tmp_path, "test_operations.xlsx")
    df.to_excel(path, index=False)
    return path


def test_spending_by_category_with_date(sample_data, monkeypatch):
    """Тест с указанием конкретной даты"""
    monkeypatch.setenv("DATA_FILE", sample_data)
    test_date = datetime.now().strftime("%Y-%m-%d")

    result = spending_by_category("Транспорт", date=test_date)

    assert isinstance(result, dict)
    assert len(result) > 0


def test_spending_by_category_empty_result(sample_data, monkeypatch):
    """Тест для категории без трат"""
    monkeypatch.setenv("DATA_FILE", sample_data)

    result = spending_by_category("Несуществующая категория")

    assert result == {}


def test_spending_by_category_missing_file(monkeypatch):
    """Тест с отсутствующим файлом"""
    monkeypatch.setenv("DATA_FILE", "nonexistent.xlsx")

    result = spending_by_category("Еда")

    assert result == {}


def test_spending_by_category_invalid_columns(tmp_path, monkeypatch):
    """Тест с некорректными колонками"""
    path = os.path.join(tmp_path, "bad_data.xlsx")
    pd.DataFrame({'Wrong_Column': [1, 2]}).to_excel(path, index=False)
    monkeypatch.setenv("DATA_FILE", path)

    result = spending_by_category("Еда")

    assert result == {}


def test_spending_by_category_invalid_date_format(sample_data, monkeypatch):
    """Тест с некорректным форматом даты"""
    monkeypatch.setenv("DATA_FILE", sample_data)

    result = spending_by_category("Еда", date="invalid-date-format")

    assert result == {}