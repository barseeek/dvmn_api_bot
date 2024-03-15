import logging
from time import sleep

import environs
import requests
from telegram.ext import Updater


TIMEOUT = 60
RECONNECT_DELAY = 5

env = environs.Env()
env.read_env()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=env.str('LOG_LEVEL', 'INFO'))


def run_polling(url, params):
    headers = {
        'Authorization': f'Token {env.str("API_TOKEN")}'
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        response_json = response.json()
        logging.info("Успешный запрос к API, timestamp = {0}".format(params.get('timestamp')))
        return response_json
    except requests.exceptions.ReadTimeout:
        logging.warning('Timeout')
    except requests.exceptions.ConnectionError:
        logging.warning('ConnectionError')
        sleep(RECONNECT_DELAY)


def format_message(message_params) -> str:
    message = 'У вас проверили работу "{}"\n'.format(message_params['lesson_name'])
    if message_params['is_negative']:
        message += 'К сожалению, в работе нашлись ошибки'
    else:
        message += 'Преподавателю всё понравилось, можно приступить к следующему уроку'
    message += '\nСсылка на урок: {} '.format(message_params['lesson_url'])
    return message


def main():
    updater = Updater(token=env.str('TELEGRAM_BOT_TOKEN'))
    logging.info('Бот запущен')
    url = 'https://dvmn.org/api/long_polling/'
    params = {}
    while True:
        payload = run_polling(url,params)
        if payload:
            if payload['status'] == 'found':
                params['timestamp'] = payload['last_attempt_timestamp']
                params_review = {
                    'lesson_name': payload['new_attempts'][0]['lesson_title'],
                    'is_negative': payload['new_attempts'][0]['is_negative'],
                    'lesson_url': payload['new_attempts'][0]['lesson_url']
                }
                logging.debug(payload)
                updater.bot.send_message(chat_id=env.str('TELEGRAM_CHAT_ID'), text=format_message(params_review))
            elif payload['status'] == 'timeout':
                params['timestamp'] = payload['timestamp_to_request']


if __name__ == '__main__':
    main()