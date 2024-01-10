import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).parent

API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
ROSSKO_API_KEY1 = os.getenv('ROSSKO_API_KEY1')
ROSSKO_API_KEY2 = os.getenv('ROSSKO_API_KEY2')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WA_TEL = os.getenv('WA_TEL')
WA_IDINSTANS = os.getenv('WA_IDINSTANS')
WA_API_TOKEN_INSTANCE = os.getenv('WA_API_TOKEN_INSTANCE')



LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

DATABASE = 'orders.db'
TIME_TO_SLEEP = 600

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
