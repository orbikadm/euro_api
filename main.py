import sys
import os
import time
import sqlite3
import logging
from dataclasses import dataclass

from zeep import Client, Settings
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv


load_dotenv()
API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
ROSSKO_API_KEY1 = os.getenv('ROSSKO_API_KEY1')
ROSSKO_API_KEY2 = os.getenv('ROSSKO_API_KEY2')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DATABASE = 'orders.sqlite3'
TIME_TO_SLEEP = 10
INSERT_QUERY = """
    INSERT INTO orders(
    orderid, created_date, delivery_address, part_number, name, brand,
    price, count, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.CRITICAL
)
handler = logging.StreamHandler(stream=sys.stderr)
logger.addHandler(handler)


@dataclass
class Part:
    orderid: int
    created_date: str
    delivery_address: str
    status: int
    part_number: str
    name: str
    brand: str
    price: float
    count: int


def send_message(bot, message):
    """Функция отправляет сообщение в телеграм."""
    try:
        logger.debug('Сообщение отправляется в телеграмм...')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'Сообщение успешно отправлено: \n {message}')
    except TelegramError as error:
        logger.error(f'Ошибка при отправке сообщения в телеграмм: {error}')


def get_orders_list():
    try:
        settings = Settings(strict=False, xml_huge_tree=True)
        client = Client(API_URL_GET_ORDERS, settings=settings)
        return client.service.GetOrders(
            KEY1=ROSSKO_API_KEY1,
            KEY2=ROSSKO_API_KEY2,
            type=4,
            limit=60
        ).OrdersList.Order
    except Exception as error:
        logger.error(f'Ошибка при получении ответа от Api Rossko: {error}')


def create_table(cur):
    """Функция создаёт таблицу в базе данных если её нет."""
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
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


def parse_order(order) -> list[Part]:
    """Парсим заказ, возвращаем объект Part."""
    parts_list = []
    orderid = order.id
    created_date = order.created_date
    detail = order.detail
    delivery_address = detail.delivery_address
    parts = order.parts.part
    for part in parts:
        status = part.status
        if status == 7:
            part_number = part.partnumber
            name = part.name
            brand = part.brand
            price = part.price
            count = part.count
            newpart = Part(
                orderid=orderid, created_date=created_date, status=status,
                delivery_address=delivery_address, part_number=part_number,
                name=name, brand=brand, price=price, count=count)
            parts_list.append(newpart)
    return parts_list


def get_parts_from_db(cur):
    """Функция получает из базы даных все товары, по которым была отмена."""
    check_query = """SELECT * FROM orders WHERE status LIKE 7"""
    cur.execute(check_query)
    db_parts = cur.fetchall()
    return db_parts


def save_to_bd(con, part):
    """Сохраняет заказ в БД."""
    values = (
        part.orderid, part.created_date, part.delivery_address,
        part.part_number, part.name, part.brand, part.price, part.count,
        part.status
        )
    cur.execute(INSERT_QUERY, values)
    con.commit()


def get_message(order):
    """Подготавливаем сообщение для отправки."""
    message = f"""
\u2757\u2757\u2757 ОТМЕНА ПОЗИЦИИ \u2757\u2757\u2757\n
\U0001F4CBЗаказ:  {order.orderid}\n
\u23F0Дата заказа:  {part.created_date}\n
\U0001F4EDАдрес доставки:  {part.delivery_address}\n
\u274C Отменено:
    Артикул:  {part.part_number}
    Бренд:  {part.brand}
    \U0001F449Наименование:  {part.name} - {part.count} шт.

    """
    return message


if __name__ == '__main__':
    bot: Bot = Bot(token=TELEGRAM_TOKEN)
    while True:
        try:
            orders_list = get_orders_list()
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            create_table(cur)

            for order in orders_list:
                part_list = parse_order(order)
                print('список запчастюль', part_list)
                parts_in_db = get_parts_from_db(cur)
                for part in part_list:
                    if not parts_in_db:
                        save_to_bd(con=con, part=part)
                        message = get_message(part)
                        send_message(bot, message)

                    for item in parts_in_db:
                        if part.orderid in item and part.part_number in item:
                            print('НЕ Записываем')
                        else:
                            save_to_bd(con=con, part=part)
                            message = get_message(part)
                            send_message(bot, message)
        except Exception as error:
            print(error)
            error_message = f'Произошла ошибка в работе скрипта\n{error}'
            send_message(bot, error_message)
        logger.debug(
            'Заказы проверены, следующая проверка через {TIME_TO_SLEEP} секунд'
            )
        time.sleep(TIME_TO_SLEEP)
