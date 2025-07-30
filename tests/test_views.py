import pytest
from datetime import datetime, timedelta
from src.views import home_page, events_page
from src.utils import get_greeting

def test_get_greeting():
    assert get_greeting("2023-01-01 05:00:00") == "Доброй ночи"
    assert get_greeting("2023-01-01 11:00:00") == "Доброе утро"
    assert get_greeting("2023-01-01 15:00:00") == "Добрый день"
    assert get_greeting("2023-01-01 20:00:00") == "Добрый вечер"

def test_home_page_structure():
    result = home_page("2023-01-15 12:00:00")
    assert isinstance(result, dict)
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result

def test_events_page_structure():
    result = events_page("2023-01-15 12:00:00")
    assert isinstance(result, dict)
    assert "expenses" in result
    assert "income" in result
    assert "currency_rates" in result
    assert "stock_prices" in result

@pytest.mark.parametrize("period,expected", [
    ('W', "week"),
    ('M', "month"),
    ('Y', "year"),
    ('ALL', "all")
])
def test_events_page_periods(period, expected):
    # Здесь можно добавить более конкретные проверки для каждого периода
    result = events_page("2023-01-15 12:00:00", period)
    assert isinstance(result, dict)