import pandas as pd


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загрузка транзакций из Excel с проверкой колонок."""
    df = pd.read_excel(file_path)

    # Приводим названия колонок к нижнему регистру и заменяем пробелы
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Проверяем обязательные колонки
    required_columns = {'date', 'card', 'amount', 'category', 'description'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Отсутствуют обязательные колонки: {missing}")

    df['date'] = pd.to_datetime(df['date'])
    return df