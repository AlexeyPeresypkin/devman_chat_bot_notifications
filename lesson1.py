import os

import requests
import time
from dotenv import load_dotenv

load_dotenv()


def req(url, headers, timestamp=None):
    response = requests.get(url, headers=headers, params=timestamp)
    return response


params = {
    'timestamp_to_request': None
}
url = 'https://dvmn.org/api/long_polling/'
headers = {'Authorization': os.getenv('TOKEN')}

while True:
    try:
        response = requests.get(url, headers=headers, params=params)
        json_text = response.json()
        if json_text.get('status') == 'timeout':
            params['timestamp_to_request'] = int(json_text['timestamp_to_request'])
            print(params['timestamp_to_request'])
    except requests.exceptions.ReadTimeout:
        print('Timeout')
        time.sleep(30)
    except requests.exceptions.ConnectionError:
        print('Connection error')
        time.sleep(30)

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
