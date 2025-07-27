from typing import List, Dict, Any
import pandas as pd
from datetime import datetime
import logging
import math

logger = logging.getLogger(__name__)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для Инвесткопилки через округление трат
    :param month: Месяц в формате 'YYYY-MM'
    :param transactions: Список транзакций
    :param limit: Шаг округления (10, 50, 100)
    :return: Сумма накоплений
    """
    try:
        df = pd.DataFrame(transactions)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])
        target_month = datetime.strptime(month, "%Y-%m")

        filtered = df[
            (df["Дата операции"].dt.month == target_month.month) &
            (df["Дата операции"].dt.year == target_month.year)
            ]

        total_saved = 0
        for amount in filtered["Сумма операции"]:
            rounded = math.ceil(amount / limit) * limit
            total_saved += rounded - amount

        return round(total_saved, 2)
    except Exception as e:
        logger.error(f"Investment error: {e}")
        return 0.0