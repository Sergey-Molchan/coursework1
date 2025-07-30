import pandas as pd
from datetime import datetime, timedelta
from functools import wraps


def report_to_file(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            fname = filename or f"{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(f"reports/{fname}", 'w') as f:
                f.write(result.to_json(orient='records', force_ascii=False))

            return result

        return wrapper

    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date=None):
    date = pd.to_datetime(date) if date else datetime.now()
    start_date = date - timedelta(days=90)

    filtered = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= date)
        ]

    return filtered.groupby(
        filtered['Дата операции'].dt.to_period('M')
    )['Сумма операции'].sum().abs()


@report_to_file()
def spending_by_weekday(transactions: pd.DataFrame, date=None):
    date = pd.to_datetime(date) if date else datetime.now()
    start_date = date - timedelta(days=90)

    filtered = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= date)
        ]

    return filtered.groupby(
        filtered['Дата операции'].dt.weekday
    )['Сумма операции'].mean().abs()


@report_to_file(filename='workday_spending.json')
def spending_by_workday(transactions: pd.DataFrame, date=None):
    date = pd.to_datetime(date) if date else datetime.now()
    start_date = date - timedelta(days=90)

    filtered = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= date)
        ]

    is_workday = filtered['Дата операции'].dt.weekday < 5
    return filtered.groupby(is_workday)['Сумма операции'].mean().abs()