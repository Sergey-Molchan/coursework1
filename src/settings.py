import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY = os.getenv('FMP_API_KEY')
    USER_CURRENCIES = ['EUR', 'GBP']
    USER_STOCKS = ['AAPL', 'MSFT', 'GOOGL']