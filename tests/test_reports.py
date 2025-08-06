import pytest
from unittest.mock import patch
import pandas as pd
from src.reports import spending_by_category


@pytest.fixture
def report_data():
    data = {
        'Дата операции': pd.date_range(start='2023-01-01', periods=90, freq='D').strftime('%d.%m.%Y %H:%M:%S'),
        'Категория': ['Еда'] * 45 + ['Транспорт'] * 45,
        'Сумма операции': [-100.0] * 45 + [-200.0] * 45,
        'Статус': ['OK'] * 90
    }
    return pd.DataFrame(data)


@pytest.mark.parametrize("category, date", [
    ('Еда', '2023-03-31'),
    ('Транспорт', '2023-03-31'),
])
def test_spending_by_category(report_data, category, date):
    with patch('src.reports.load_transactions') as mock_load:
        # Подготовка тестовых данных в нужном формате
        test_data = report_data.copy()
        test_data['Дата'] = pd.to_datetime(test_data['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        test_data['Сумма'] = test_data['Сумма операции']
        test_data['Категория'] = test_data['Категория']

        mock_load.return_value = test_data

        result = spending_by_category(category, date)

        # Проверки
        assert isinstance(result, dict)
        assert len(result) > 0

        # Проверяем формат ключей (месяцы в формате 'YYYY-MM')
        assert all(len(k.split('-')) == 2 for k in result.keys())

        # Проверяем что значения - числа (int или float)
        assert all(isinstance(v, (int, float)) for v in result.values())


def test_spending_by_category_no_data():
    with patch('src.reports.load_transactions') as mock_load:
        mock_load.return_value = pd.DataFrame(columns=[
            'Дата операции', 'Сумма операции', 'Категория', 'Статус'
        ])
        result = spending_by_category('Еда')
        assert result == {}


def test_spending_by_category_error():
    with patch('src.reports.load_transactions', side_effect=Exception("Test error")):
        result = spending_by_category('Еда')
        assert result == {}