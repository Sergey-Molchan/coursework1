import pandas as pd
from datetime import datetime, timedelta
import os

# Создаем тестовые данные
data = []
start_date = datetime.now() - timedelta(days=90)
categories = ['Супермаркеты', 'Кафе', 'Транспорт', 'Развлечения', 'Услуги']

for i in range(100):
    date = start_date + timedelta(days=i)
    category = categories[i % len(categories)]
    amount = round(-(100 + i*10), 2)
    data.append({
        'Дата операции': date.strftime('%d.%m.%Y %H:%M:%S'),
        'Сумма операции': f"{abs(amount):.2f}".replace('.', ','),
        'Категория': category,
        'Описание': f"Тестовая транзакция {i}",
        'Номер карты': '123456******' + str(i%1000).zfill(4),
        'Кэшбэк': str(round(abs(amount)*0.01, 2)).replace('.', ','),
    })

# Создаем DataFrame
df = pd.DataFrame(data)

# Создаем папку data, если ее нет
os.makedirs('data', exist_ok=True)

# Сохраняем в Excel
df.to_excel('data/operations.xlsx', index=False)
print("Тестовые данные созданы в data/operations.xlsx")