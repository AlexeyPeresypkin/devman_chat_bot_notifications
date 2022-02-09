import os
import telegram
import requests
import time
from dotenv import load_dotenv


def send_message(chat_id, token, response):
    lesson_title = response.json()['new_attempts']['lesson_title']
    is_negative = response.json()['new_attempts']['is_negative']
    if is_negative:
        message = f'У вас проверили работу "{lesson_title}"\n' \
                  f'К сожалению, в работе нашлись ошибки'
    else:
        message = f'У вас проверили работу "{lesson_title}"\n' \
                  f'Преподователю всё понравилось, можно приступать к следующему уроку'
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def main():
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': os.getenv('DEVMAN_TOKEN')}
    params = {}
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.json()['status'] == 'timeout':
                params['timestamp_to_request'] = int(
                    response.json()['timestamp_to_request']
                )
            elif response.json()['status'] == 'found':
                params['timestamp_to_request'] = int(
                    response.json()['new_attempts']['timestamp']
                )
                send_message(chat_id, telegram_token, response)
        except requests.exceptions.ReadTimeout:
            print('Timeout')
            time.sleep(30)
        except requests.exceptions.ConnectionError:
            print('Connection error')
            time.sleep(30)


if __name__ == '__main__':
    main()

d = {
    "request_query": [],
    "status": "timeout",
    "timestamp_to_request": 1644339121.1714048
}

d2 = {
    "status": "found",
    "new_attempts": [
        {
            "submitted_at": "2019-03-28...",
            "is_negative": False,
            "lesson_title": "Готовим речь",
            "timestamp": 1455609162.580245
        }
    ],
    "last_attempt_timestamp": 1455609162.580245
}
