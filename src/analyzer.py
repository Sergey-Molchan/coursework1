from datetime import datetime
from .data_loader import load_transactions


def analyze_data(file_path: str, report_date: str):
    """Основная функция анализа"""
    df = load_transactions(file_path)

    # Фильтрация по дате
    report_dt = datetime.strptime(report_date, "%Y-%m-%d %H:%M:%S")
    month_start = datetime(report_dt.year, report_dt.month, 1)

    filtered = df[
        (df['date'] >= month_start) &
        (df['date'] <= report_dt)
        ]

    # Пример анализа
    result = {
        "total_transactions": len(filtered),
        "total_amount": filtered['amount'].sum(),
        "categories": filtered['category'].value_counts().to_dict()
    }

    return result