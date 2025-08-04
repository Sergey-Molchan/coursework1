import pandas as pd
import logging

logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загрузка данных с минимальными требованиями"""
    try:
        df = pd.read_excel(file_path)

        # Абсолютно необходимые колонки
        required_columns = ['Дата операции', 'Сумма операции']
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            raise ValueError(f"Отсутствуют обязательные колонки: {missing_cols}")

        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки файла: {e}")
        raise
