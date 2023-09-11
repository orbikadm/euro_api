from dataclasses import dataclass
import time
from zeep import Client, Settings
import sqlite3
import logging
from telegram import Bot
from telegram.error import TelegramError
import sys

API_URL_GET_ORDERS = 'http://api.rossko.ru/service/v2.1/GetOrders'
TIME_TO_SLEEP = 10
KEY1 = '84eebe2fb3e7b8a79355efc8cbd772de'
KEY2 = 'fbb861504dbd6faf3374fc0d3c8a3e87'
DATABASE = 'orders.sqlite3'
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

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


def send_message(part, message):
    """Функция отправляет сообщение в телеграм."""
    try:
        logger.debug('Сообщение отправляется в телеграмм...')
        # bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'Сообщение успешно отправлено: \n {message}')
    except TelegramError as error:
        logger.error(f'Ошибка при отправке сообщения в телеграмм: {error}')

def get_orders_list():
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client(API_URL_GET_ORDERS, settings=settings)
    return client.service.GetOrders(KEY1=KEY1, KEY2=KEY2, type=4, limit=60).OrdersList.Order


def create_table(cur):
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
    """Парсим заказ, возвращаем объект Part"""
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
                orderid=orderid, created_date=created_date, delivery_address=delivery_address,
                part_number=part_number, name=name, brand=brand, price=price, count=count, status=status)
            parts_list.append(newpart)

    return parts_list

def check_order(order):
    """Возвращает True если заказ есть в БД."""
    return False


def get_parts_from_db(cur):
    check_query = """SELECT * FROM orders WHERE status LIKE 7"""
    cur.execute(check_query)
    db_parts = cur.fetchall()
    # print(db_parts)
    return db_parts


def first_save(con, part):
    values = (part.orderid, part.created_date, part.delivery_address, part.part_number, part.name,
              part.brand, part.price, part.count, part.status)
    query_1 = """
        INSERT INTO orders(
        orderid, created_date, delivery_address, part_number, name, brand, price, count, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cur.execute(query_1, values)
    con.commit()


def save_to_bd(con, part):
    """Сохраняет заказ в БД."""
    values = (
        part.orderid, part.created_date, part.delivery_address, part.part_number, part.name,
        part.brand, part.price, part.count, part.status)
    query_1 = """
        INSERT INTO orders(
        orderid, created_date, delivery_address, part_number, name, brand, price, count, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cur.execute(query_1, values)
    con.commit()



def get_message(order):
    """Подготавливаем сообщение для отправки."""
    return 'Заказ сняли из-за отсутствия на складе'




if __name__ == '__main__':
    # bot: Bot = Bot(token=TELEGRAM_TOKEN)
    while True:
        try:
            # print('Получаем список заказов от Api')
            orders_list = get_orders_list()
            # print('Успешно получили список заказов от Api')
            #  Проверяем есть ли данные в бд, если есть пропускаем, если нет - записываем в бд и отправляем сообщение
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            create_table(cur)

            for order in orders_list:
                # print('Запущен цикл')
                # print(order)
                part_list = parse_order(order)
                print('список запчастюль', part_list)
                parts_in_db = get_parts_from_db(cur)
                for part in part_list:
                    if not parts_in_db:
                        first_save(con=con, part=part)

                    for item in parts_in_db:
                        if part.orderid in item and part.part_number in item:
                            print('НЕ Записываем')
                        else:
                            save_to_bd(con=con, part=part)

                # message = get_message(order)
                # print('Сообщение подготовлено')
                # send_message(message)
                # print('Сообщение отправлено')
        except Exception as error:
            print(error)
            error_message = f'Произошла ошибка в работе скрипта\n{error}'
            send_message(error_message)
        print('Готовимся спать')
        time.sleep(TIME_TO_SLEEP)
        print('Поспали, начинаем новый круг')
