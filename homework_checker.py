import asyncio
import json
import time

import requests

from config import PRACTICUM_TOKENS
from create_bot import bot

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена и одобрена! Поздравляю!',
    'reviewing': 'Ревьюер взял работу на проверку.',
    'rejected': 'В работе найдены недочеты, смотри ошибки.',
}

async def scrap_homework():
    for user_id, token in PRACTICUM_TOKENS:
        timestamp = _read_timestamp(user_id)
        api_response = _parse_api(token, timestamp)
        new_timestamp = api_response.get('current_date')
        _write_timestamp(new_timestamp, user_id)
        new_homeworks = api_response.get('homeworks')
        if new_homeworks:
            message = (
                f"{HOMEWORK_STATUSES[new_homeworks[0].get('status')]}\n"
                f"Комментарий ревьюера: "
                f"{new_homeworks[0].get('reviewer_comment')}\n"
                f"Урок: {new_homeworks[0].get('lesson_name')}"
            )
            await bot.send_message(user_id, message)

def _parse_api(token: str, timestamp: int) -> dict:
    url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
    data = {'Authorization': f'OAuth {token}'}
    payload = {'from_date': timestamp}
    response = requests.get(url, headers=data, params=payload)
    return response.json()

def _read_timestamp(file_name):
    with open(f'timestamp{file_name}.txt', 'r') as f:
        return f.read()

def _write_timestamp(timestamp: int, file_name: str):
    with open(f'timestamp{file_name}.txt', 'w') as f:
        f.write(str(timestamp))


def _write_last_work():
    with open(f'homework.json', 'r') as f:
        result = json.load(f)
    return result

if __name__ == '__main__':
    for user_id, _ in PRACTICUM_TOKENS:
        _write_timestamp(0, user_id)
#    print(_write_last_work())
