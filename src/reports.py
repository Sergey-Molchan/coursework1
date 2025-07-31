import pandas as pd
import json
from datetime import datetime
from typing import Optional

def report_to_file(filename: Optional[str] = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output_file = filename or f"{func.__name__}_report.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            return result
        return wrapper
    return decorator

@report_to_file()
def spending_by_weekday(df: pd.DataFrame, date: Optional[str] = None) -> Dict:
    """Средние траты по дням недели."""
    target_date = datetime.now() if date is None else datetime.strptime(date, "%Y-%m-%d")
    three_months = df[df['дата'] >= (target_date - pd.DateOffset(months=3))]
    return three_months.groupby(three_months['дата'].dt.day_name())['сумма'].mean().to_dict()