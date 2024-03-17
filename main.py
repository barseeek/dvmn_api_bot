import logging
from time import sleep

import environs
import requests
from telegram import Bot

TIMEOUT = 60
RECONNECT_DELAY = 5

logger = logging.getLogger(__file__)


def fetch_payload(url, params, api_token):
    headers = {
        'Authorization': f'Token {api_token}'
    }
    response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    logger.info("Успешный запрос к API, timestamp = {0}".format(params.get('timestamp')))
    return payload


def format_message(message_params) -> str:
    message = 'У вас проверили работу "{}"\n'.format(message_params['lesson_name'])
    if message_params['is_negative']:
        message += 'К сожалению, в работе нашлись ошибки'
    else:
        message += 'Преподавателю всё понравилось, можно приступить к следующему уроку'
    message += '\nСсылка на урок: {} '.format(message_params['lesson_url'])
    return message


def main():
    env = environs.Env()
    env.read_env()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=env.str('LOG_LEVEL', 'INFO'))
    bot = Bot(token=env.str('TELEGRAM_BOT_TOKEN'))
    logger.info('Бот запущен')
    url = 'https://dvmn.org/api/long_polling/'
    params = {}
    dvmn_token = env.str("API_TOKEN")
    while True:
        payload = None
        try:
            payload = fetch_payload(url, params, dvmn_token)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout')
        except requests.exceptions.ConnectionError:
            logger.warning('ConnectionError')
            sleep(RECONNECT_DELAY)
        if payload:
            if payload['status'] == 'found':
                params['timestamp'] = payload['last_attempt_timestamp']
                params_review = {
                    'lesson_name': payload['new_attempts'][0]['lesson_title'],
                    'is_negative': payload['new_attempts'][0]['is_negative'],
                    'lesson_url': payload['new_attempts'][0]['lesson_url']
                }
                logger.debug(payload)
                bot.send_message(chat_id=env.str('TELEGRAM_CHAT_ID'), text=format_message(params_review))
            elif payload['status'] == 'timeout':
                params['timestamp'] = payload['timestamp_to_request']


if __name__ == '__main__':
    main()
