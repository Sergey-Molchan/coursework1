import re
import logging
from datetime import datetime
from typing import List, Dict, Any
from .utils import load_transactions

logger = logging.getLogger(__name__)


def cashback_analysis(year: int, month: int) -> Dict[str, float]:
    """Анализ выгодных категорий для кешбэка"""
    try:
        df = load_transactions()
        filtered = df[
            (df['Дата'].dt.year == year) &
            (df['Дата'].dt.month == month) &
            (df['Сумма'] < 0)
            ]

        result = filtered.groupby('Категория')['Сумма'].sum().apply(
            lambda x: round(abs(x) * 0.01, 2)
        ).sort_values(ascending=False)

        return result.to_dict()
    except Exception as e:
        logger.error(f"Error in cashback_analysis: {e}")
        return {}