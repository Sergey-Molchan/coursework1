import logging
from typing import Dict, Any
from .services import process_transactions, get_card_stats, get_top_transactions
from .utils import load_transactions

logger = logging.getLogger(__name__)


def home_page(data_file: str) -> Dict[str, Any]:
    """Главная страница с максимальной устойчивостью"""
    raw_df = None
    try:
        raw_df = load_transactions(data_file)
        df = process_transactions(raw_df)

        if df.empty:
            return {
                "error": "Нет данных для отображения",
                "available_columns": raw_df.columns.tolist()
            }

        date = df['Дата'].max()
        return {
            "date": date.strftime('%d.%m.%Y'),
            "cards": get_card_stats(df, date),
            "top_transactions": get_top_transactions(df, date),
            "available_columns": raw_df.columns.tolist()
        }
    except Exception as e:
        logger.error(f"Ошибка формирования главной страницы: {e}")
        return {
            "error": str(e),  # Возвращаем оригинальное сообщение об ошибке
            "available_columns": raw_df.columns.tolist() if raw_df is not None else []
        }