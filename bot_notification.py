import os
import telegram
import requests
import time
import logging
from dotenv import load_dotenv


def send_message(chat_id, token, response):
    lesson_title = response.json()['new_attempts'][0]['lesson_title']
    is_negative = response.json()['new_attempts'][0]['is_negative']
    if is_negative:
        message = f'У вас проверили работу "{lesson_title}"\n' \
                  f'К сожалению, в работе нашлись ошибки'
    else:
        message = f'У вас проверили работу "{lesson_title}"\n' \
                  f'Преподователю всё понравилось, можно приступать к следующему уроку'
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def send_log_info(chat_id, token, text):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


def main():
    logger.info('Приложение стартовало')
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': os.environ['DEVMAN_TOKEN']}
    params = {}
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.json()['status'] == 'timeout':
                params['timestamp_to_request'] = int(
                    response.json()['timestamp_to_request']
                )
            elif response.json()['status'] == 'found':
                params['timestamp_to_request'] = int(
                    response.json()['new_attempts'][0]['timestamp']
                )
                send_message(chat_id, telegram_token, response)
        except requests.exceptions.ReadTimeout:
            print('Timeout')
            time.sleep(30)
        except requests.exceptions.ConnectionError:
            print('Connection error')
            time.sleep(30)
        except Exception:
            logger.critical('Bot stopped with error')


class BotLogsHandler(logging.Handler):
    def __init__(self, telegram_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.telegram_token = telegram_token

    def emit(self, record):
        log_entry = self.format(record)
        send_log_info(
            chat_id=self.chat_id,
            token=self.telegram_token,
            text=log_entry
        )


logging.basicConfig(format="%(asctime)s %(process)d %(levelname)s %(message)s")
logger = logging.getLogger('TelegramLoger')
logger.setLevel(logging.DEBUG)
handler = BotLogsHandler(os.environ['TELEGRAM_TOKEN'], os.environ['CHAT_ID'])
logger.addHandler(handler)

if __name__ == '__main__':
    main()


