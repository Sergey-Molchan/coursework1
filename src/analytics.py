from datetime import datetime, timedelta
import logging
from typing import Dict, Optional
import pandas as pd
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
load_dotenv()


def spending_by_category(category: str, date: Optional[str] = None) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца

    Returns:
        Dict[str, float]: Словарь с суммами трат по месяцам (месяц: сумма)
        Пример: {'2023-01': 1500.50, '2023-02': 2000.00}

        В случае ошибки возвращает пустой словарь.
    """
    try:
        # Загрузка данных
        file_path = os.getenv("DATA_FILE", "data/operations.xlsx")
        abs_path = os.path.join(os.path.dirname(__file__), file_path)

        if not os.path.exists(abs_path):
            logger.error(f"Файл {abs_path} не найден")
            return {}

        df = pd.read_excel(abs_path)

        # Проверка необходимых колонок
        required_columns = {'Категория', 'Дата', 'Сумма'}
        if not required_columns.issubset(df.columns):
            logger.error(f"В данных отсутствуют необходимые колонки: {required_columns - set(df.columns)}")
            return {}

        # Обработка дат
        end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        # Фильтрация и группировка
        filtered = df[
            (df['Категория'] == category) &
            (df['Дата'] >= start_date) &
            (df['Дата'] <= end_date)
            ].copy()

        if filtered.empty:
            return {}

        filtered['Месяц'] = filtered['Дата'].dt.to_period('M')
        result = filtered.groupby('Месяц')['Сумма'].sum()

        return {str(k): round(abs(v), 2) for k, v in result.items()}

    except ValueError as e:
        logger.error(f"Ошибка формата даты: {e}")
        return {}
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return {}