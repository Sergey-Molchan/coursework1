import re
import pandas as pd

def find_phone_transactions(df: pd.DataFrame) -> list:
    """Поиск транзакций с номерами телефонов."""
    pattern = r'\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2}'
    mask = df['Описание'].str.contains(pattern, regex=True)
    return df[mask].to_dict('records')

def investment_bank(df: pd.DataFrame, limit: int = 50) -> float:
    """Расчёт для Инвесткопилки."""
    rounded = (df['Сумма'] // limit + 1) * limit
    return (rounded - df['Сумма']).sum()