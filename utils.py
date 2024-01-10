import logging
from telegram.error import TelegramError

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
    return all(tokens)


def get_message(part):
    """Подготавливаем сообщение для отправки."""
    message = f"""
\u2757\u2757 ОТМЕНА ПОЗИЦИИ \u2757\u2757\n
\U0001F4CBЗаказ:  {part[0][0]}\n
\u23F0Дата заказа:  {part[2]}\n
\U0001F4EDАдрес доставки:  {part[3]}\n
\u274C Отменено:
    Артикул:  {part[0][1]}
    Бренд:  {part[5]} \n
    \U0001F449Наименование:  {part[4]} - {part[8]} шт.

    """
    return message


def tg_send_message(bot, message):
    """Функция отправляет сообщение в Telegram."""
    try:
        logging.debug('Сообщение отправляется в Telegram...')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(f'Сообщение успешно отправлено: \n {message}')
    except TelegramError as error:
        logging.error(f'Ошибка при отправке сообщения в Telegram: {error}')
