import requests
import telebot
import json
import os
import logging
from utils import TelegramLogsHandler


ATTEMPS_COUNT = 2
SLEEPING_TIME = 5
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
NOTIFICATION_TELEGRAM_TOKEN = os.environ['NOTIFICATION_TELEGRAM_TOKEN']
DVMN_AUTHORIZATION_TOKEN = os.environ['DVMN_AUTHORIZATION_TOKEN']
TELEGRAM_USER_CHAT_ID = os.environ['TELEGRAM_USER_CHAT_ID']
TIMEOUT = 60
bot = telebot.TeleBot(TELEGRAM_TOKEN)
notification_bot = telebot.TeleBot(NOTIFICATION_TELEGRAM_TOKEN)
logger = logging.getLogger('Logger')



def send_result_message(messages):
    positive_message = 'Все хорошо, можно браться за следeущее задание'
    negative_message = "Есть ошибки, надо исправить"
    result_message = negative_message if messages[0]['is_negative'] else positive_message
    feed_back_message = 'Mы проверили Ваше задание "{}" \n {}'.format(messages[0]['lesson_title'], result_message)
    bot.send_message(chat_id=TELEGRAM_USER_CHAT_ID, text=feed_back_message)


def is_server_response_correct(response):
    return response.ok and 'error' not in response.json()


def get_status_and_timestamp(json_response):
    status = json_response['status']
    if status == 'found':
        timestamp = json_response['last_attempt_timestamp']
    else:
        timestamp = json_response['timestamp_to_request']
    return timestamp, status


def get_response_from_server():
    timestamp = None
    connection_attempt = 0
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": DVMN_AUTHORIZATION_TOKEN}
    while True:
        payload = {'timestamp': timestamp}
        try:
            response = requests.get(url, headers=headers, params=payload)
            if is_server_response_correct(response):
                json_response = response.json()
                timestamp, status = get_status_and_timestamp(json_response)
                if status == 'found':
                    send_result_message(json_response['new_attempts'])
            else:
                logger.error('Received Bad response')
        except(requests.exceptions.ReadTimeout):
            continue
        except(ConnectionError):
            if connection_attempt < ATTEMPS_COUNT:
                time.sleep(SLEEPING_TIME)
                connection_attempt += 1
            logger.error('Connection Lost')
            continue
        except Exception as error_msg:
            logger.error('Bot is broken by error: {}'.format(error_msg))

if __name__ == '__main__':
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(notification_bot, TELEGRAM_USER_CHAT_ID))
    get_response_from_server()
