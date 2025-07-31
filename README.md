Описание проекта

Финансовый дашборд для анализа банковских операций с интеграцией с Financial Modeling Prep API для получения данных об акциях. Проект разработан как курсовая работа и предоставляет:

Анализ расходов по банковским картам
Расчет кэшбэка (1% от суммы расходов)
Топ-5 самых крупных транзакций
Актуальные котировки акций
Особенности

📊 Загрузка и обработка банковских операций из Excel
💳 Анализ расходов по картам
📈 Получение данных об акциях через API
⏳ Кэширование запросов к API (5 минут)
🛠 Гибкая настройка через конфигурационные файлы
Установка и настройка

Требования

Python 3.9+
pip
Клонируйте репозиторий:
git clone https://github.com/yourusername/financial-dashboard.git
cd financial-dashboard
Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
Установите зависимости:
pip install -r requirements.txt
Создайте файл .env и добавьте API ключ:
ini
FMP_API_KEY=your_api_key_here
DATA_FILE=path/to/your/operations.xlsx

Структура проекта


financial-dashboard/
├── data/                   # Папка с данными
│   └── operations.xlsx     # Пример файла с операциями
├── src/
│   ├── __init__.py
│   ├── main.py             # Главный скрипт
│   ├── services.py         # Бизнес-логика
│   └── views.py            # Представления
├── .env.example            # Пример конфигурации
├── requirements.txt        # Зависимости
└── README.md               # Этот файл
