import pandas as pd
import logging
from dotenv import load_dotenv
import os


logger = logging.getLogger(__name__)
load_dotenv()


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла.

    Args:
        file_path: Путь к файлу (.xlsx).

    Returns:
        pd.DataFrame: DataFrame с колонками ['Дата операции', 'Сумма операции'].

    Raises:
        FileNotFoundError: Если файл не существует.
        ValueError: Если данные невалидны.
        Exception: Другие ошибки.
    """
    try:
        # Проверка существования файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        df = pd.read_excel(file_path)

        # Проверка колонок
        required_columns = ['Дата операции', 'Сумма операции']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Отсутствуют колонки: {missing_cols}")

        # Парсинг дат
        df['Дата операции'] = pd.to_datetime(
            df['Дата операции'],
            format='%d.%m.%Y %H:%M:%S',
            dayfirst=True,
            errors='raise'
        )

        return df

    except FileNotFoundError as e:
        logger.error(f"Ошибка: {e}")
        raise
    except ValueError as e:
        logger.error(f"Ошибка данных: {e}")
        raise
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        raise