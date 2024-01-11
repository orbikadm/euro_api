import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


# Общие настройки
BASE_DIR = Path(__file__).parent
WAIT_TIME = 600
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

# Настройки Телеграм
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Настройки WhatsApp
WA_TEL = os.getenv('WA_TEL')
WA_IDINSTANS = os.getenv('WA_IDINSTANS')
WA_API_TOKEN_INSTANCE = os.getenv('WA_API_TOKEN_INSTANCE')

# Настройки логгера
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
PAUSE_MESSAGE = f'Заказы проверены, следующая проверка через {WAIT_TIME} секунд'

# Настройки базы данных
DATABASE = 'orders.db'

# Настройки API Rossko
API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
ROSSKO_API_KEY1 = os.getenv('ROSSKO_API_KEY1')
ROSSKO_API_KEY2 = os.getenv('ROSSKO_API_KEY2')

# Настройки API Berg
BERG_API_URL = 'https://api.berg.ru/ordering/states/active?key='
BERG_KEY = os.getenv('BERG_KEY')
BERG_TIME = '%Y-%m-%dT%H:%M:%S+03:00'
