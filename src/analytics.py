from datetime import datetime, timedelta
import logging
from typing import Dict, Optional
import pandas as pd

logger = logging.getLogger(__name__)


def spending_by_category(category: str, date: Optional[str] = None) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца"""
    try:
        # Загрузка данных (ваша реализация может отличаться)
        df = pd.read_excel("data/transactions.xlsx")

        end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        filtered = df[
            (df['Категория'] == category) &
            (df['Дата'] >= start_date) &
            (df['Дата'] <= end_date)
            ]

        result = filtered.groupby(filtered['Дата'].dt.to_period('M'))['Сумма'].sum()
        return {str(k): round(abs(v), 2) for k, v in result.to_dict().items()}

    except Exception as e:
        logger.error(f"Error in spending_by_category: {e}")
        return {}