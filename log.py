import logging

import environs

from telegram import Bot


class TelegramLogsHandler(logging.Handler):

    def __init__(self):
        env = environs.Env()
        env.read_env()
        super().__init__()
        self.chat_id = env.str('TELEGRAM_CHAT_ID')
        self.tg_bot = Bot(token=env.str('TELEGRAM_LOG_BOT_TOKEN'))

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)