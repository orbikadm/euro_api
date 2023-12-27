import sys
import time
import sqlite3
import logging
import traceback

from telegram import Bot

from wa_api import send_message
from berg import get_parts_berg
from rossko import get_parts_rossko
from classes import Part
from mock_data import rossko_mock_response, berg_mock_response

from constants import DATABASE, TELEGRAM_TOKEN, TIME_TO_SLEEP


from configs import configure_logging
from utils import check_tokens, get_message, tg_send_message


INSERT_QUERY = """
    INSERT INTO orders(
    uniq_id, supplier, created_date, delivery_address,
    name, brand, price, count, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""


def create_table(cur):
    """Функция создаёт таблицу в базе данных если её нет."""

    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        uniq_id TEXT,
        supplier TEXT,
        created_date TEXT,
        delivery_address TEXT,
        name TEXT,
        brand TEXT,
        price REAL,
        count INT,
        status INT);
    """)


def get_parts_from_db(cur):
    """Функция получает из базы даных все товары, по которым была отмена."""

    check_query = """SELECT * FROM orders"""
    cur.execute(check_query)
    db_parts = cur.fetchall()
    return db_parts


def save_to_bd(con, part):
    """Сохраняет заказ в БД."""

    uniq_id = str(part[0])
    values = (
        uniq_id, *part[1:]
    )
    cur.execute(INSERT_QUERY, values)
    con.commit()


if __name__ == '__main__':
    configure_logging()
    if not check_tokens():
        logging.critical('Отсутствует один или несколько токенов')
        sys.exit('Ошибка: токены не прошли валидацию')
    bot: Bot = Bot(token=TELEGRAM_TOKEN)
    while True:
        first_start = 1
        try:
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            create_table(cur)

            part_list = rossko_mock_response #get_parts_rossko()
            part_list_berg = berg_mock_response # get_parts_berg()
            part_list.extend(part_list_berg)

            parts_in_db = get_parts_from_db(cur)
            ids_parts_in_db = [part[0] for part in parts_in_db]

            for num, part in enumerate(part_list):
                # Удалить проверку отправки по необходимости
                if num % 3 == 0:
                    message = get_message(part)
                    tg_send_message(bot, message)
                uniq_id = str(part[0])
                if uniq_id not in ids_parts_in_db:
                    save_to_bd(con=con, part=part)
                    if not first_start:
                        message = get_message(part)
                        tg_send_message(bot, message)
                        print('Отправлено сообщение в Telegram')
                        # send_message(message, WA_TEL, WA_IDINSTANS, WA_API_TOKEN_INSTANCE)
                        print('Отправлено сообщение в Whatsapp')

        except Exception as error:
            logging.error('Произошла ошибка в работе скрипта\n{error}')
            traceback.print_exc()
            error_message = f'Произошла ошибка в работе скрипта\n{error}'
            # tg_send_message(bot, error_message)
        logging.info(
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



