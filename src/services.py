from typing import List, Dict, Any
import logging
from src.views import load_transactions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def profitable_cashback_categories(year: int, month: int) -> Dict[str, float]:
    """Анализ выгодных категорий для кешбэка"""
    try:
        df = load_transactions()
        filtered = df[
            (df['Дата'].dt.year == year) &
            (df['Дата'].dt.month == month) &
            (df['Сумма'] < 0)  # Только расходы
            ]

        # Используем колонку кешбэка, если она есть
        if 'Кешбэк' in filtered.columns:
            result = filtered.groupby('Категория')['Кешбэк'].sum().sort_values(ascending=False)
        else:
            # Если нет колонки кешбэка, рассчитываем 1% от суммы
            result = filtered.groupby('Категория')['Сумма'].sum().apply(
                lambda x: round(abs(x) * 0.01, 2)
            ).sort_values(ascending=False)

        return result.to_dict()
    except Exception as e:
        logging.error(f"Ошибка в profitable_cashback_categories: {e}")
        return {}


def investment_bank(month: str, limit: int = 50) -> float:
    """Расчёт инвесткопилки с округлением"""
    try:
        df = load_transactions()
        year, month = map(int, month.split('-'))

        filtered = df[
            (df['Дата'].dt.year == year) &
            (df['Дата'].dt.month == month) &
            (df['Сумма'] < 0)  # Только расходы
            ]

        # Используем колонку округления, если она есть
        if 'Округление' in filtered.columns:
            return round(filtered['Округление'].sum(), 2)

        # Если колонки округления нет, рассчитываем вручную
        def round_amount(x):
            return limit * round(abs(x) / limit)

        total_round = filtered['Сумма'].apply(
            lambda x: round_amount(x) + x
        ).sum()

        return round(abs(total_round), 2)
    except Exception as e:
        logging.error(f"Ошибка в investment_bank: {e}")
        return 0.0


def search_transactions(query: str) -> List[Dict[str, Any]]:
    """Поиск транзакций по строке"""
    try:
        df = load_transactions()
        mask = df['Описание'].str.contains(query, case=False, na=False) | \
               df['Категория'].str.contains(query, case=False, na=False)
        return df[mask].to_dict('records')
    except Exception as e:
        logging.error(f"Ошибка в search_transactions: {e}")
        return []


def find_phone_transactions() -> List[Dict[str, Any]]:
    """Поиск транзакций с номерами телефонов"""
    try:
        df = load_transactions()
        phone_pattern = r'(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
        mask = df['Описание'].str.contains(phone_pattern, regex=True, na=False)
        return df[mask].to_dict('records')
    except Exception as e:
        logging.error(f"Ошибка в find_phone_transactions: {e}")
        return []


def find_person_transfers() -> List[Dict[str, Any]]:
    """Поиск переводов физлицам"""
    try:
        df = load_transactions()
        pattern = r'[А-Я][а-я]+\s[А-Я]\.'  # Имя и первая буква фамилии с точкой
        mask = (df['Категория'] == 'Переводы') & \
               (df['Описание'].str.contains(pattern, na=False))
        return df[mask].to_dict('records')
    except Exception as e:
        logging.error(f"Ошибка в find_person_transfers: {e}")
        return []