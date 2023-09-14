import sys
import os
import time
import sqlite3
import logging


from zeep import Client, Settings
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

from wa_api import send_message
from berg import get_parts_berg
from rossko import get_parts_rossko
from classes import Part

load_dotenv()

API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
ROSSKO_API_KEY1 = os.getenv('ROSSKO_API_KEY1')
ROSSKO_API_KEY2 = os.getenv('ROSSKO_API_KEY2')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WA_TEL = os.getenv('WA_TEL')
WA_IDINSTANS = os.getenv('WA_IDINSTANS')
WA_API_TOKEN_INSTANCE = os.getenv('WA_API_TOKEN_INSTANCE')

DATABASE = 'orders.sqlite3'
TIME_TO_SLEEP = 600
INSERT_QUERY = """
    INSERT INTO orders(
    supplier, orderid, created_date, delivery_address,
    part_number, name, brand, price, count, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""


logger = logging.getLogger(__name__)


def config_logger(logger):
    """Конфигурирование логгера."""
    logger.setLevel(logging.DEBUG)
    f_handler = logging.FileHandler(
        filename="euro_api.log", mode='w', encoding='utf-8'
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
    )
    f_handler.setFormatter(formatter)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)

    logger.addHandler(f_handler)
    logger.addHandler(stderr_handler)


def check_tokens():
    """Проверка наличия всех токенов в ENV."""
    tokens: tuple = (
        ROSSKO_API_KEY1, ROSSKO_API_KEY2, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID,
        WA_TEL, WA_IDINSTANS, WA_API_TOKEN_INSTANCE
    )
    return all(tokens)


def create_table(cur):
    """Функция создаёт таблицу в базе данных если её нет."""
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        supplier TEXT,
        orderid INT,
        created_date TEXT,
        delivery_address TEXT,
        part_number TEXT,
        name TEXT,
        brand TEXT,
        price REAL,
        count INT,
        status INT);
    """)


def get_parts_from_db(cur, supplier):
    """Функция получает из базы даных все товары, по которым была отмена."""
    if supplier == 'ROSSKO':
        check_query = """SELECT * FROM orders WHERE status LIKE 7"""
    else:  # Если не росско то Берг
        check_query = """SELECT * FROM orders WHERE status LIKE 3"""
    cur.execute(check_query)
    db_parts = cur.fetchall()
    return db_parts


def save_to_bd(con, part):
    """Сохраняет заказ в БД."""
    values = (
        part.supplier, part.orderid, part.created_date, part.delivery_address,
        part.part_number, part.name, part.brand, part.price, part.count,
        part.status
        )
    cur.execute(INSERT_QUERY, values)
    con.commit()


def get_message(order):
    """Подготавливаем сообщение для отправки."""
    message = f"""
\u2757\u2757 ОТМЕНА ПОЗИЦИИ \u2757\u2757\n
\U0001F4CBЗаказ:  {order.orderid}\n
\u23F0Дата заказа:  {part.created_date}\n
\U0001F4EDАдрес доставки:  {part.delivery_address}\n
\u274C Отменено:
    Артикул:  {part.part_number}
    Бренд:  {part.brand}
    \U0001F449Наименование:  {part.name} - {part.count} шт.

    """
    return message


def tg_send_message(bot, message):
    """Функция отправляет сообщение в Telegram."""
    try:
        logger.debug('Сообщение отправляется в Telegram...')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'Сообщение успешно отправлено: \n {message}')
    except TelegramError as error:
        logger.error(f'Ошибка при отправке сообщения в Telegram: {error}')


if __name__ == '__main__':
    config_logger(logger=logger)
    if not check_tokens():
        logger.critical('Отсутствует один или несколько токенов')
        sys.exit('Ошибка: токены не прошли валидацию')
    bot: Bot = Bot(token=TELEGRAM_TOKEN)
    while True:
        first_start = 1
        try:
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            create_table(cur)


            part_list = get_parts_rossko()  # Получаем новый список отмененных товаров
            part_list_berg = get_parts_berg()
            part_list.extend(part_list_berg)
            print(part_list_berg)

            parts_in_db = get_parts_from_db(cur, 'ROSSKO') # получаем товары, которые уже есть в бд
            parts_in_db_berg = get_parts_from_db(cur, 'BERG')
            parts_in_db.extend(parts_in_db_berg)
            print(parts_in_db)

            for part in part_list:
                if not parts_in_db:
                    save_to_bd(con=con, part=part)
                    message = get_message(part)
                    if not first_start:
                        # tg_send_message(bot, message)
                        print('Отправлено сообщение в Telegram')
                        # send_message(message, WA_TEL, WA_IDINSTANS, WA_API_TOKEN_INSTANCE)
                        print('Отправлено сообщение в Whatsapp')

                for item in parts_in_db:
                    if part.orderid in item and part.part_number in item:
                        logger.debug('Новых отмененных товаров не найдено.')
                    else:
                        save_to_bd(con=con, part=part)
                        message = get_message(part)
                        if not first_start:
                            # tg_send_message(bot, message)
                            print('Отправлено сообщение в Telegram')
                            # send_message(message, WA_TEL, WA_IDINSTANS, WA_API_TOKEN_INSTANCE)
                            print('Отправлено сообщение в Whatsapp')
       
        except Exception as error:
            logger.error('Произошла ошибка в работе скрипта\n{error}')
            error_message = f'Произошла ошибка в работе скрипта\n{error}'
            tg_send_message(bot, error_message)
        logger.debug(
            f'Заказы проверены, следующая проверка через {TIME_TO_SLEEP} секунд'
            )
        first_start = 0
        time.sleep(TIME_TO_SLEEP)



#TODO Список необходимых изменений

# 1. Сделать единым формат datetime
# 2. Разделить по модулям функционал
# 3. Убрать дублирование кода
# 4. Поправить проверку наличия товара в БД
# 5. Отловить исключения при работе api Berg



