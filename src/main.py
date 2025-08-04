import logging
from pathlib import Path
import json
from datetime import datetime
from src.views import home_page
from src.services import get_currency_rates, get_sp500_data, get_greeting
from dotenv import load_dotenv


load_dotenv()


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('finance_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "operations.xlsx"

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Файл не найден: {DATA_FILE}. Проверьте структуру проекта.")

print(f"Файл найден: {DATA_FILE}")  # Для отладки

def generate_response() -> dict:
    """
    Генерирует полный JSON-ответ для веб-страницы
    """
    try:
        # Получаем данные из разных источников
        transactions_data = home_page(str(DATA_FILE))
        currency_data = get_currency_rates()
        sp500_data = get_sp500_data()

        # Формируем итоговый ответ
        response = {
            "greeting": get_greeting(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cards": transactions_data.get('cards', []),
            "top_transactions": transactions_data.get('top_transactions', []),
            "currency_rates": currency_data,
            "sp500": sp500_data,
            "status": "success"
        }

        return response

    except Exception as e:
        logger.error(f"Ошибка при генерации ответа: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


def main():
    """
    Основная функция приложения
    """
    try:
        logger.info("Запуск приложения")

        # Генерируем и выводим JSON-ответ
        response = generate_response()
        print(json.dumps(response, ensure_ascii=False, indent=2))

        logger.info("Приложение завершило работу успешно")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()