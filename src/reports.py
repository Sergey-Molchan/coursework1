from datetime import datetime, timedelta
import logging
from typing import Dict, Optional
from .utils import load_transactions
from pathlib import Path
logger = logging.getLogger(__name__)


def spending_by_category(category: str, date: Optional[str] = None) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца"""
    try:
        file_path = Path(__file__).parent.parent / "data" / "transactions.xlsx"
        df = load_transactions(str(file_path))

        end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        filtered = df[
            (df['Категория'] == category)
            & (df['Дата'] >= start_date)
            & (df['Дата'] <= end_date)
        ]

        result = filtered.groupby(filtered['Дата'].dt.to_period('M'))['Сумма'].sum()
        return {str(k): round(abs(v), 2) for k, v in result.to_dict().items()}
    except Exception as e:
        logger.error(f"Error in spending_by_category: {e}")
        return {}
