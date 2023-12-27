import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
ROSSKO_API_KEY1 = os.getenv('ROSSKO_API_KEY1')
ROSSKO_API_KEY2 = os.getenv('ROSSKO_API_KEY2')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WA_TEL = os.getenv('WA_TEL')
WA_IDINSTANS = os.getenv('WA_IDINSTANS')
WA_API_TOKEN_INSTANCE = os.getenv('WA_API_TOKEN_INSTANCE')

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

DATABASE = 'orders.sqlite3'
TIME_TO_SLEEP = 600

API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
