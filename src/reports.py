import pandas as pd
from datetime import datetime, timedelta
import logging
import json
from functools import wraps
from typing import Optional, Dict
from src.views import load_transactions
from src.utils import get_user_settings


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import os
from pathlib import Path


def report_to_file(filename: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Создаем папку reports если ее нет
            os.makedirs('reports', exist_ok=True)

            file_to_save = filename or f"reports/{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            try:
                with open(file_to_save, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                logging.info(f"Отчёт сохранён в {file_to_save}")
            except Exception as e:
                logging.error(f"Ошибка сохранения отчёта: {e}")

            return result

        return wrapper

    return decorator


def report_to_file(filename: Optional[str] = None):
    """Декоратор для сохранения отчётов в файл"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            file_to_save = filename or f"reports/{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            try:
                with open(file_to_save, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                logging.info(f"Отчёт сохранён в {file_to_save}")
            except Exception as e:
                logging.error(f"Ошибка сохранения отчёта: {e}")
            return result

        return wrapper

    return decorator


def load_report_data() -> pd.DataFrame:
    """Загрузка данных для отчётов"""
    df = pd.read_excel('data/operations.xls')
    df['Дата'] = pd.to_datetime(df['Дата'])
    df['Сумма'] = pd.to_numeric(df['Сумма'].str.replace(',', '.'))
    df['День недели'] = df['Дата'].dt.day_name()
    df['Тип дня'] = df['Дата'].dt.dayofweek.apply(lambda x: 'Выходной' if x >= 5 else 'Рабочий')
    return df


@report_to_file()
def spending_by_category(category: str, date: Optional[str] = None) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца"""
    try:
        df = load_transactions()
        end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        filtered = df[
            (df['Категория'] == category) &
            (df['Дата'] >= start_date) &
            (df['Дата'] <= end_date) &
            (df['Сумма'] < 0)  # Только расходы
            ]

        result = filtered.groupby(filtered['Дата'].dt.to_period('M'))['Сумма'].sum()
        return {str(k): round(abs(v), 2) for k, v in result.to_dict().items()}
    except Exception as e:
        logging.error(f"Ошибка в spending_by_category: {e}")
        return {}


@report_to_file("weekly_spending_report.json")
def spending_by_weekday(date: Optional[str] = None) -> Dict[str, float]:
    """Средние траты по дням недели"""
    try:
        df = load_report_data()
        end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        filtered = df[
            (df['Дата'] >= start_date) &
            (df['Дата'] <= end_date) &
            (df['Сумма'] < 0)
            ]

        result = filtered.groupby('День недели')['Сумма'].mean()
        return {k: round(abs(v), 2) for k, v in result.to_dict().items()}
    except Exception as e:
        logging.error(f"Ошибка в spending_by_weekday: {e}")
        return {}


@report_to_file()
def workday_vs_weekend(date: Optional[str] = None) -> Dict[str, float]:
    """Сравнение трат в рабочие/выходные дни"""
    try:
        df = load_report_data()
        end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        filtered = df[
            (df['Дата'] >= start_date) &
            (df['Дата'] <= end_date) &
            (df['Сумма'] < 0)
            ]

        result = filtered.groupby('Тип дня')['Сумма'].mean()
        return {k: round(abs(v), 2) for k, v in result.to_dict().items()}
    except Exception as e:
        logging.error(f"Ошибка в workday_vs_weekend: {e}")
        return {}