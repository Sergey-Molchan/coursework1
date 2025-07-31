from datetime import datetime
from typing import Dict, Any
from src.services import (
    load_transactions,
    get_card_stats,
    get_top_transactions,
    get_stock_prices_cached,
    get_ttl_hash,
    _get_greeting
)

def home_page(date_str: str, data_file: str) -> Dict[str, Any]:
    """Главная страница - генерация JSON"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        df = load_transactions(data_file)

        return {
            "greeting": _get_greeting(date),
            "cards": get_card_stats(df, date),
            "top_transactions": get_top_transactions(df, date),
            "stock_prices": get_stock_prices_cached(','.join(["AAPL", "GOOGL"]), get_ttl_hash())
        }
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error in home_page: {e}")
        raise