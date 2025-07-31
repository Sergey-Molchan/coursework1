import unittest
from src.services import (
    profitable_cashback_categories,
    investment_bank,
    find_person_transfers
)


class TestServices(unittest.TestCase):
    def test_cashback_categories(self):
        result = profitable_cashback_categories(2023, 1)
        self.assertIsInstance(result, dict)

    def test_investment_bank(self):
        result = investment_bank("2023-01")
        self.assertIsInstance(result, float)

    def test_find_person_transfers(self):
        result = find_person_transfers()
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()