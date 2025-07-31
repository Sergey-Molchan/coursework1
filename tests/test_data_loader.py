import pytest
from src.data_loader import load_transactions
import pandas as pd


def test_load_transactions(tmp_path):
    # Создаем тестовый Excel-файл
    test_data = pd.DataFrame({
        'date': ['2023-01-01'],
        'card': ['1234'],
        'amount': [100],
        'category': ['Test'],
        'description': ['Test desc']
    })

    file_path = tmp_path / "test.xlsx"
    test_data.to_excel(file_path, index=False)

    # Проверяем загрузку
    df = load_transactions(file_path)
    assert not df.empty
    assert 'date' in df.columns