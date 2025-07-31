import sys
from pathlib import Path
import pytest


# Добавляем src в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_operations_data():
    return {
        'Дата операции': ['31.12.2021 16:44:00'],
        'Номер карты': ['*7197'],
        'Сумма операции': ['-160,89'],
        'Категория': ['Супермаркеты'],
        'Описание': ['Магнит']
    }