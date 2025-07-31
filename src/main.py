import logging
from pathlib import Path
import sys

# Добавляем путь к src в PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from views import home_page
from services import load_transactions, get_stock_prices

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)


def main():
    try:
        print("Запуск программы...")  # Отладочное сообщение

        data_file = "/Users/sergejmolcan/coursework1/data/operations.xlsx"

        # 1. Проверка загрузки данных
        print("\n1. Проверка загрузки данных...")
        df = load_transactions(data_file)
        print(f"Успешно загружено {len(df)} записей")
        print(f"Диапазон дат: {df['Дата'].min()} - {df['Дата'].max()}")

        # 2. Тестирование home_page с датой из данных
        print("\n2. Тестирование home_page...")
        test_date = "2021-12-31 15:30:00"  # Используем дату, которая есть в данных
        result = home_page(test_date, data_file)

        # 3. Вывод результатов
        print("\n3. Результаты:")
        import json
        from datetime import datetime

        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime):
                    return obj.strftime('%Y-%m-%d %H:%M:%S')
                return super().default(obj)

        print(json.dumps(result, indent=2, ensure_ascii=False, cls=DateTimeEncoder))

        # 4. Тест FMP API
        print("\n4. Тестирование FMP API...")
        stocks = get_stock_prices(["AAPL", "GOOGL"])
        print(stocks)

    except Exception as e:
        logging.error(f"Ошибка в main: {e}", exc_info=True)
    finally:
        print("\nПрограмма завершена")


if __name__ == "__main__":
    main()