from datetime import datetime
from src.views import generate_home_json
from src.constants import get_greeting
import logging
import os
from pathlib import Path
import json


def init_project():
    """Инициализация проекта"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

    if not Path('user_settings.json').exists():
        with open('user_settings.json', 'w') as f:
            json.dump({
                "user_currencies": ["USD", "EUR"],
                "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
            }, f, indent=2)


def main():
    init_project()

    try:
        current_time = datetime.now()
        print("\nТекущее время:", current_time)
        print("Приветствие:", get_greeting(current_time))

        test_date = "2023-05-20 15:30:00"
        print("\nГлавная страница:")
        home_data = generate_home_json(test_date)
        print(home_data)

    except Exception as e:
        logging.error(f"Ошибка в main: {e}")


if __name__ == "__main__":
    main()

    try:
        # Загружаем настройки
        settings = get_user_settings()

        # Пример использования
        test_date = "2023-05-20 15:30:00"
        current_time = datetime.now()

        print("\n1. Главная страница:")
        print(f"Текущее время: {current_time}")
        print(f"Приветствие: {get_greeting(current_time)}")

        home_data = generate_home_json(test_date)
        print(f"Данные главной страницы: {home_data}")

    except Exception as e:
        logging.error(f"Ошибка в main: {e}")


if __name__ == "__main__":
    main()