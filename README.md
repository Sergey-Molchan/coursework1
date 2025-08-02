# Финансовый анализатор расходов


Приложение для анализа банковских транзакций с возможностью просмотра:
- Расходов по категориям
- Топовых транзакций
- Курсов валют
- Данных по S&P500

## Установка

1. Клонируйте репозиторий:

git clone https://github.com/Sergey-Molchan/coursework1
cd finance-analyzer
Установите зависимости:
bash
poetry install
Создайте файл .env по образцу:
ini
EXCHANGE_RATE_API_KEY=your_api_key #регистрация по адресу https://app.exchangerate-api.com/activate-account
FMP_API_KEY=your_api_key  #регистрация по адресу https://site.financialmodelingprep.com/developer/docs
Использование

Запуск приложения:


python3 main.py
Тестирование:


pytest tests/
Проверка стиля кода:


Структура проекта

coursework1/
├── data/                  # Файлы с транзакциями (operations.xlsx)
├── src/                   # Исходный код
│   ├── main.py            # Точка входа
│   ├── services.py        # Бизнес-логика и API-интеграции
│   ├── views.py           # Представления и обработка запросов
│   ├── reports.py         # Генерация отчетов
│   └── utils.py           # Вспомогательные функции
├── tests/                 # Тесты
├── .env.example           # Пример конфигурации
├── pyproject.toml         # Конфигурация проекта
└── README.md              # Документация
API

Приложение возвращает JSON с данными:

json
{
  "greeting": "Добрый день",
  "cards": [...],
  "top_transactions": [...],
  "currency_rates": [...],
  "sp500": {...}
}

