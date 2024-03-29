"""Разрабатывается бот, уведомляющий о статусе проверки работы ревьюером."""

import logging
import os
import sys
import time
from http import HTTPStatus
from json.decoder import JSONDecodeError
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.',
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
}

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(message)s'
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
rotating_handler = RotatingFileHandler(
    'bot_yandex_logger.log', maxBytes=50000000, backupCount=5
)
logger.addHandler(rotating_handler)


class ErrorM(Exception):
    """Собственное исключение."""

    pass


def send_message(bot, message):
    """Отправка сообщения в Telegram чат."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logger.info(f'Отправлено сообщение: {message}')
    except telegram.TelegramError:
        logger.error(f'Ошибка отправления сообщения: {message}')


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        logger.info(f'[Запрос к API] Статуc: {response.status_code}')
        if response.status_code != HTTPStatus.OK.value:
            logger.error(
                f'[Запрос к API] Ошибочка! запроса к эндпоинту API-сервиса.'
                f'Статус ответа сервера {response.status_code}'
            )
            raise ErrorM(
                f'[Запрос к API] Статус, отличный от 200: '
                f'{response.status_code}'
            )
        return response.json()
    except JSONDecodeError:
        logger.error('Запрос к API вернулся не в формате JSON')
        raise JSONDecodeError(
            'Запрос к API вернулся не в формате JSON'
        )
    except requests.exceptions.HTTPError as err:
        logger.error(
            f'[Запрос к API] Ошибочка Ex запроса к эндпоинту API-сервиса:{err}'
        )
        raise requests.exceptions.HTTPError(
            f'[Запрос к API] Статус: {response.status_code},'
            f'Ошибка: {err}'
        )


def check_response(response):
    """Проверяет ответ API на корректность."""
    try:
        homeworks = response['homeworks']
    except KeyError as error:
        raise KeyError(f'[Корректность] ошибка ключа: {error}')
    if not homeworks:
        logger.debug('[Корректность] Статус работы прежний')
    if not isinstance(homeworks, list):
        logger.error('[Корректность] Ошибка типа в списке работ.')
        raise TypeError('[Корректность] Ошибка типа.')
    return homeworks


def parse_status(homework):
    """Изменение информации о проверке работы."""
    try:
        if len(homework) == 0:
            message = f'[Статус] Проект не в обработке: {homework}'
            logger.info(message)
            return message
        else:
            homework_name = homework['homework_name']
            homework_status = homework['status']
            if homework_status in HOMEWORK_STATUSES:
                verdict = HOMEWORK_STATUSES[homework_status]
                mes_verdict = (
                    f'Изменился статус проверки работы "{homework_name}". '
                    f'{verdict}'
                )
                logger.info(mes_verdict)
                return mes_verdict
            raise KeyError('[Статус] Ошибка ключа')
    except KeyError:
        logger.error('[Статус] Хьюстон, у нас проблем-с.')
        raise KeyError('[Статус] ERROR: Ошибка ключа')


def check_tokens():
    """Проверка доступности переменных окружения."""
    try:
        tokens = {
            'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
            'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
            'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
        }
        for key, value in tokens.items():
            if not value:
                logger.critical(
                    f'Отсутствует переменная окружения: {value} для {key}'
                )
                return False
        return True
    except NameError:
        message = 'Ошибка доступности переменной. Остановка программы'
        logger.critical(message)


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if len(homeworks) == 0:
                parse_status(homeworks)
                send_message(bot, f'Работа не в обработке: {homeworks}')
            else:
                if homeworks[0]['status'] in HOMEWORK_STATUSES:
                    status = homeworks[0]['status']
                    parse_status(homeworks[0])
                    send_message(bot, HOMEWORK_STATUSES[status])
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            send_message(bot, message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
