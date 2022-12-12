import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s',
    handlers=[
        logging.FileHandler('output.log'),
        logging.StreamHandler(sys.stdout)
    ]
)


def check_tokens():
    """Проверка токена"""
    if not PRACTICUM_TOKEN or not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logging.critical('Отсутствует одна из переменных окружения')
        return False
    return True


def send_message(bot, message):
    """Отправка сообщения в Telegram"""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug('Отправка сообщения')
    except Exception as error:
        logging.error(f'Не удалось отправить сообщение: {error}')
        raise Exception(error)


def get_api_answer(timestamp):
    """Запрос к API-сервису"""
    try:
        response = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except requests.RequestException as error:
        logging.error(f'Ошибка при запросе к API: {error}')
    if response.status_code != HTTPStatus.OK:
        raise ConnectionError
    response = response.json()
    if not isinstance(response, dict):
        raise TypeError
    return response


def check_response(response):
    """Проверка ответа API"""
    try:
        homeworks = response['homeworks']
    except KeyError as error:
        logging.error(f'Ошибка доступа по ключу: {error}')
    if not isinstance(homeworks, list):
        logging.error('Не верный формат ответа')
        raise TypeError('Не верный формат ответа')
    return homeworks


def parse_status(homework):
    """Получение статуса работы"""
    status = homework.get('status')
    if status is None:
        raise TypeError
    if status not in HOMEWORK_VERDICTS:
        raise TypeError
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise TypeError
    verdict = HOMEWORK_VERDICTS.get(status)
    if verdict is None:
        logging.error(f'Неожиданный статус домашней работы - {status}')
        return None
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота"""
    logging.info('Старт')
    if not check_tokens():
        sys.exit()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = 0
    prev_message: str = ''
    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
            else:
                message = prev_message
                logging.debug('Нет изменений')
            if message != prev_message:
                send_message(bot, message)
                prev_message = message
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if message != prev_message:
                send_message(bot, message)
                prev_message = message
        finally:
            timestamp += RETRY_PERIOD
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
