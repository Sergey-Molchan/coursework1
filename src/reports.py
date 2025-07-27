from typing import Optional, Dict
import pandas as pd
from datetime import datetime, timedelta
import logging
import json
import functools

logger = logging.getLogger(__name__)


def report_decorator(func=None, *, filename=None):
    """Декоратор для сохранения отчётов в файл"""

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            output_file = filename or f"report_{f.__name__}_{datetime.now().date()}.json"
            with open(output_file, "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=2)
            return result

        return wrapper

    return decorator(func) if func else decorator


@report_decorator
def spending_by_category(
        df: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> Dict[str, float]:
    """
    Анализ трат по категории за последние 3 месяца
    :param df: DataFrame с транзакциями
    :param category: Название категории
    :param date: Опорная дата в формате 'YYYY-MM-DD'
    :return: Словарь с суммами по месяцам
    """
    try:
        end_date = pd.to_datetime(date) if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        filtered = df[
            (df["Категория"] == category) &
            (df["Дата операции"] >= start_date) &
            (df["Дата операции"] <= end_date)
            ]

        return filtered.groupby(
            filtered["Дата операции"].dt.to_period("M")
        )["Сумма платежа"].sum().to_dict()
    except Exception as e:
        logger.error(f"Spending report error: {e}")
        return {}