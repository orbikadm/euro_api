import json
import logging
import sys

import requests
from telegram.error import TelegramError

from exceptions import WhatsAppException
from settings import (
    ROSSKO_API_KEY1, ROSSKO_API_KEY2, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, WA_TEL,
    WA_IDINSTANS, WA_API_TOKEN_INSTANCE
)


def check_tokens():
    """Проверка наличия всех токенов в ENV."""
    tokens: tuple = (
        ROSSKO_API_KEY1, ROSSKO_API_KEY2, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID,
        WA_TEL, WA_IDINSTANS, WA_API_TOKEN_INSTANCE
    )
    if not all(tokens):
        logging.critical('Отсутствует один или несколько токенов')
        sys.exit('Ошибка: токены не прошли валидацию')


def get_message(order):
    """Подготавливаем сообщение для отправки."""
    message = f"""
\u2757\u2757 ОТМЕНА ПОЗИЦИИ \u2757\u2757\n
\U0001F4CBЗаказ:  {order.order_id}\n
\u23F0Дата заказа:  {order.created_date}\n
\U0001F4EDАдрес доставки:  {order.delivery_address}\n
\u274C {order.status}:
    Артикул:  {order.article}
    Бренд:  {order.brand} \n
    \U0001F449Наименование:  {order.name} - {order.count} шт.

    """
    return message


def tg_send_message(bot, message):
    """Функция отправляет сообщение в Telegram."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(f'Сообщение успешно отправлено: \n {message}')
    except TelegramError as error:
        logging.error(f'Ошибка при отправке сообщения в Telegram: {error}')


def wa_send_message(message):
    url = f'https://api.green-api.com/waInstance{WA_IDINSTANS}/sendMessage/{WA_API_TOKEN_INSTANCE}'
    chat_id = WA_TEL + '@c.us'

    payload = {
        'chatId': chat_id,
        'message': message
        }

    json_payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json_payload)
    if response.status_code != '200':
        raise WhatsAppException('Ошибка отправки в WhatsApp')
    logging.debug(f'Сообщение успешно отправлено в WhatsApp: \n {message}')


def send_to_users(message, bot=None, whatsapp=False):
    if bot:
        tg_send_message(bot, message)
    if whatsapp:
        wa_send_message(message)
