from data_loader import load_transactions
from views import generate_home_json
from services import find_phone_transactions
import logging


def main():
    try:
        # Загрузка данных
        df = load_transactions("../data/operations.xlsx")

        # Пример использования
        print("Главная страница JSON:", generate_home_json("2023-10-15 12:00:00", df))
        print("Транзакции с телефонами:", find_phone_transactions(df))

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}")
        print(f"Произошла ошибка: {e}. Проверьте логи для деталей.")


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.ERROR)
    main()