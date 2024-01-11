import time
import logging
import traceback

from configs import tg_bot, configure_logging
from models import Order, session
from settings import WAIT_TIME, PAUSE_MESSAGE
from utils import check_tokens, create_order, get_message, send_to_users, get_orders

from sqlalchemy import and_


if __name__ == '__main__':
    configure_logging()
    check_tokens()

    while True:
        first_start = 1
        try:
            part_list = get_orders(
                rossko=True,
                berg=True
            )

            for part in part_list:
                order_id, article = part[0], part[1]
                exists = session.query(Order).filter(and_(
                    Order.order_id == order_id,
                    Order.article == article
                )).all()

                if not exists:
                    order = create_order(part)
                    session.add(order)
                    session.commit()

                    if not first_start:
                        message = get_message(order)
                        send_to_users(message, bot=tg_bot, whatsapp=False)

        except Exception as error:
            logging.error(f'Произошла ошибка в работе скрипта\n{error}')
            traceback.print_exc()
            error_message = f'Произошла ошибка в работе скрипта\n{error}'
            send_to_users(message, bot=tg_bot)
        logging.info(PAUSE_MESSAGE)
        first_start = 0
        time.sleep(WAIT_TIME)
