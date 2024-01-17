import logging
from logging.handlers import RotatingFileHandler

import argparse
from telegram import Bot

from settings import BASE_DIR, LOG_FORMAT, DATETIME_FORMAT, TELEGRAM_TOKEN


tg_bot: Bot = Bot(token=TELEGRAM_TOKEN)


def configure_logging():
    """Конфигурирование логгера."""
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'checker.log'

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )


def configure_argparser():
    parser = argparse.ArgumentParser(description='Order cancel notificator')
    parser.add_argument(
        '-i',
        '--init',
        help='First check not send message',
        action='store_true',
    )
    return parser.parse_args()
