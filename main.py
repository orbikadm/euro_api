import time
from datetime import datetime
import logging
import traceback

from configs import tg_bot, configure_logging
from models import Order, session
from mock_data import rossko_mock_response, berg_mock_response
from settings import WAIT_TIME, DATETIME_FORMAT, PAUSE_MESSAGE
from berg import get_parts_berg
from rossko import get_parts_rossko
from utils import check_tokens, get_message, send_to_users

from sqlalchemy import and_


if __name__ == '__main__':
    configure_logging()
    check_tokens()

    while True:
        first_start = 0
        try:
            part_list = rossko_mock_response #get_parts_rossko()
            part_list_berg = berg_mock_response # get_parts_berg()
            part_list.extend(part_list_berg)

            for part in part_list:
                order_id = part[0]
                article = part[1]

                exists = session.query(Order).filter(and_(
                    Order.order_id == order_id,
                    Order.article == article
                )).all() #get(order_id, article)
                print(part, exists)
                if not exists:
                    created_date = datetime.strptime(part[3], DATETIME_FORMAT)
                    order = Order(
                        order_id=part[0], # order_id, article
                        article=part[1],
                        supplier=part[2],
                        created_date=created_date,
                        delivery_address=part[4],
                        name=part[5],
                        brand=part[6],
                        price=part[7],
                        count=part[8],
                        status=part[9],
                    )
                    session.add(order)
                    session.commit()

                    if not first_start:
                        message = get_message(order)
                        send_to_users(message, bot=tg_bot, whatsapp=False)
                        print('Отправлено сообщение в Telegram')
                        print(message)

        except Exception as error:
            logging.error('Произошла ошибка в работе скрипта\n{error}')
            traceback.print_exc()
            error_message = f'Произошла ошибка в работе скрипта\n{error}'
            # tg_send_message(bot, error_message)
        logging.info(PAUSE_MESSAGE)
        first_start = 0
        time.sleep(WAIT_TIME)


#TODO Список необходимых изменений

# 1. Сделать единым формат datetime
# 2. Разделить по модулям функционал
# 3. Убрать дублирование кода
# 4. Поправить проверку наличия товара в БД
# 5. Отловить исключения при работе api Berg



