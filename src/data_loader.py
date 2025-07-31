import pandas as pd
from pathlib import Path


def load_transactions(file_path: str):
    """Загрузка данных из Excel"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {path} не найден")

    df = pd.read_excel(path)

    # Преобразование колонок
    df = df.rename(columns={
        'Дата операции': 'date',
        'Сумма операции': 'amount',
        'Категория': 'category'
    })

    return df