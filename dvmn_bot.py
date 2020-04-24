import requests
import telebot
import json
import os


COUNT_OF_ATTEMP = 2
SLEEPING_TIME = 5
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
AUTHORIZATION_TOKEN = os.environ['AUTHORIZATION_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
TIMEOUT = 60
bot = telebot.TeleBot(TELEGRAM_TOKEN)


def send_message_to_client(final_message):
    bot.send_message(chat_id=CHAT_ID, text=final_message)


def prepare_message(messages):
    positiv_message = 'Все хорошо, можно браться за следeущее задание'
    negative_message = "Есть ошибки, надо исправить"
    for message in messages:
        lesson_name = message['lesson_title']
        result_message = negative_message if message['is_negative'] else positiv_message
    feed_back_message = 'Mы проверили Ваше задание "{}" \n {}'.format(lesson_name, result_message)
    return feed_back_message


def is_server_response_correct(response, json_response):
    return response.status_code == 200 and 'error' not in json_response


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
    headers = {"Authorization": AUTHORIZATION_TOKEN}
    while True:
        payload = {'timestamp': timestamp}
        try:
            response = requests.get(url, headers=headers, params=payload, timeout=60)
            json_response = response.json()
            if is_server_response_correct(response, json_response):
                timestamp, status = get_status_and_timestamp(json_response)
                if status == 'found':
                    prepared_message = prepare_message(json_response['new_attempts'])
                    send_message_to_client(prepared_message)
        except(requests.exceptions.ReadTimeout, ConnectionError):
            if connection_attempt < COUNT_OF_ATTEMP:
                time.sleep(SLEEPING_TIME)
                connection_attempt += 1
            continue


if __name__ == '__main__':
    get_response_from_server()
