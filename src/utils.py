import json
import logging
from pathlib import Path
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_user_settings() -> Dict[str, Any]:
    """Загрузка пользовательских настроек"""
    try:
        settings_path = Path('user_settings.json')
        if not settings_path.exists():
            default_settings = {
                "user_currencies": ["USD", "EUR"],
                "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
            }
            with open(settings_path, 'w') as f:
                json.dump(default_settings, f, indent=2)
            return default_settings

        with open(settings_path) as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Ошибка загрузки настроек: {e}")
        return {}