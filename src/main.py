import os
from views import home_view, events_view
from services import *
from reports import *
import pandas as pd
import json

# Загрузка данных
operations = pd.read_excel('data/operations.xlsx', sheet_name='Отчет по операциям')
operations['Дата операции'] = pd.to_datetime(
    operations['Дата операции'],
    format='%d.%m.%Y %H:%M:%S',
    dayfirst=True
)

# Проверка столбцов
print("Столбцы в operations:", operations.columns.tolist())

if __name__ == "__main__":
    home_data = home_view("2023-12-20 15:30:00", operations)
    print(json.dumps(home_data, indent=2, ensure_ascii=False))