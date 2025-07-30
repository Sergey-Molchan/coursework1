from typing import Dict, List
import pandas as pd
from datetime import datetime


def cashback_analysis(data: pd.DataFrame, year: int, month: int) -> Dict:
    filtered = data[
        (data['Дата операции'].dt.year == year) &
        (data['Дата операции'].dt.month == month)
        ]
    cashback = filtered.groupby('Категория')['Бонусы (включая кэшбэк)'].sum()
    return cashback.sort_values(ascending=False).to_dict()


def investment_bank(month: str, transactions: List[Dict], limit: int) -> float:
    year, month = map(int, month.split('-'))
    total = 0

    for t in transactions:
        dt = datetime.strptime(t['Дата операции'], '%Y-%m-%d')
        if dt.year == year and dt.month == month:
            amount = abs(float(t['Сумма операции']))
            rounded = ((amount // limit) + 1) * limit
            total += rounded - amount

    return round(total, 2)


def simple_search(data: pd.DataFrame, query: str) -> List[Dict]:
    mask = data['Описание'].str.contains(query, case=False) | \
           data['Категория'].str.contains(query, case=False)
    return data[mask].to_dict('records')


def phone_search(data: pd.DataFrame) -> List[Dict]:
    phone_regex = r'\+7\s?\d{3}\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}'
    mask = data['Описание'].str.contains(phone_regex, regex=True)
    return data[mask].to_dict('records')


def person_transfers(data: pd.DataFrame) -> List[Dict]:
    mask = (data['Категория'] == 'Переводы') & \
           data['Описание'].str.match(r'^[А-Я][а-я]+\s[А-Я]\.$')
    return data[mask].to_dict('records')