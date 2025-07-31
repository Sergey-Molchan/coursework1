import pytest
from src.services import (
    profitable_cashback_categories,
    investment_bank
)
import pandas as pd
from src.services import find_phone_transactions

def test_phone_search():
    test_data = pd.DataFrame([{"Описание": "Платеж +7 999 123-45-67"}])
    assert len(find_phone_transactions(test_data)) == 1


@pytest.fixture
def sample_transactions():
    return [
        {
            "Дата операции": "2023-01-10",
            "Сумма операции": 1000,
            "Кешбэк": 10,
            "Категория": "Супермаркеты"
        },
        {
            "Дата операции": "2023-01-15",
            "Сумма операции": 500,
            "Кешбэк": 5,
            "Категория": "Кафе"
        },
        {
            "Дата операции": "2023-02-01",
            "Сумма операции": 2000,
            "Кешбэк": 20,
            "Категория": "Супермаркеты"
        }
    ]

def test_profitable_cashback_categories(sample_transactions):
    result = profitable_cashback_categories(sample_transactions, 2023, 1)
    assert "Супермаркеты" in result
    assert "Кафе" in result
    assert result["Супермаркеты"] == 10
    assert result["Кафе"] == 5

def test_investment_bank(sample_transactions):
    result = investment_bank("2023-01", sample_transactions, 100)
    assert isinstance(result, float)
    assert result > 0
