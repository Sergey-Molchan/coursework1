import pandas as pd
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def load_transactions() -> pd.DataFrame:
    """Загрузка транзакций из Excel"""
    try:
        file_path = Path('data/operations.xlsx')
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")

        df = pd.read_excel(file_path)

        # Преобразование данных
        df['Дата'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
        df['Сумма'] = pd.to_numeric(df['Сумма операции'].astype(str).str.replace(',', '.'))

        return df
    except Exception as e:
        logger.error(f"Error loading transactions: {e}")
        raise