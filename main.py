import time
import logging
import traceback

from configs import tg_bot, configure_argparser, configure_logging
from models import Order, session
from settings import WAIT_TIME, PAUSE_MESSAGE
from utils import (
    check_tokens, get_message, send_to_users, get_orders
)

from sqlalchemy import and_


def main(first):
    while True:
        try:
            order_list: list[Order] = get_orders(
                rossko=True,
                berg=True
            )

            for order in order_list:
                # order_id, article = part[0], part[1]
                exists = session.query(Order).filter(and_(
                    Order.order_id == order.order_id,
                    Order.article == order.article
                )).all()

                if not exists:
                    # order = create_order(part)
                    session.add(order)
                    session.commit()

                    if not first:
                        message = get_message(order)
                        send_to_users(message, bot=tg_bot, whatsapp=False)

        except Exception as error:
            logging.error(f'Произошла ошибка в работе скрипта\n{error}')
            traceback.print_exc()
            error_message = f'Произошла ошибка в работе скрипта\n{error}'
            send_to_users(error_message, bot=tg_bot)
        logging.info(PAUSE_MESSAGE)
        first = False
        time.sleep(WAIT_TIME)


if __name__ == '__main__':
    configure_logging()
    check_tokens()
    args = configure_argparser()
    main(first=args.init)
