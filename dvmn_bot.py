import requests
import telebot
import json
import os


BOT_TOKEN = os.environ['BOT_TOKEN']
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
TIMEOUT = 60
bot = telebot.TeleBot(BOT_TOKEN)


def send_message_to_client(response):
    messages = response['new_attempts']
    for message in messages:
        lesson_name = message['lesson_title']
        result_is_negative = message['is_negative']
    if result_is_negative:
        result_message = "Есть ошибки надо исправить"
    else:
        result_message = 'Все хорошо можно браться за след задание'
    feed_back_message = 'Mы проверили Ваше задание "{}" \n {}'.format(lesson_name, result_message)
    bot.send_message(chat_id=CHAT_ID, text=feed_back_message)


def get_response_from_server():
    timestamp = None
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": TOKEN}
    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, params=payload, timeout=TIMEOUT).json()
            if response['status'] == 'found':
                timestamp = response['last_attempt_timestamp']
                send_message_to_client(response)
        except(requests.exceptions.ReadTimeout, ConnectionError):
            continue


if __name__ == '__main__':
    get_response_from_server()
