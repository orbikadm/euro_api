import sys
import time
import datetime
import logging
import traceback

from telegram import Bot

from wa_api import send_message
from berg import get_parts_berg
from rossko import get_parts_rossko
from mock_data import rossko_mock_response, berg_mock_response

from settings import DATABASE, TELEGRAM_TOKEN, TIME_TO_SLEEP, DATETIME_FORMAT


from configs import configure_logging
from utils import check_tokens, get_message, tg_send_message

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, Session


Base = declarative_base()


class Order(Base):
    __tablename__ = 'order'
    uniq_id = Column(String, primary_key=True)
    supplier = Column(String)
    created_date = Column(DateTime)
    delivery_address = Column(Text)
    name = Column(String)
    brand = Column(String)
    price = Column(String)
    count = Column(Integer)
    status = Column(Integer)


def check_order_in_db(order):
    return session.query(order).count()


if __name__ == '__main__':
    configure_logging()
    if not check_tokens():
        logging.critical('Отсутствует один или несколько токенов')
        sys.exit('Ошибка: токены не прошли валидацию')

    engine = create_engine(f'sqlite:///{DATABASE}')
    Base.metadata.create_all(engine)
    session = Session(engine)

    bot: Bot = Bot(token=TELEGRAM_TOKEN)
    while True:
        first_start = 1
        try:
            part_list = rossko_mock_response #get_parts_rossko()
            part_list_berg = berg_mock_response # get_parts_berg()
            part_list.extend(part_list_berg)

            for num, part in enumerate(part_list):
                # Удалить проверку отправки по необходимости
                # if num % 4 == 0:
                #     message = get_message(part)
                #     # tg_send_message(bot, message)
                uniq_id = str(part[0])

                count = session.query(Order).get(uniq_id)
                if not count:
                    order = Order(
                            uniq_id=uniq_id,
                            supplier=part[1],
                            created_date=datetime.datetime.strptime(part[2], DATETIME_FORMAT),
                            delivery_address=part[3],
                            name=part[4],
                            brand=part[5],
                            price=part[6],
                            count=part[7],
                            status=part[8],
                    )
                    session.add(order)
                    session.commit()

                    # Сюда перенести отправку сообщений

                    if not first_start:
                        message = get_message(part)
                        # tg_send_message(bot, message)
                        print('Отправлено сообщение в Telegram')
                        print(message)
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



