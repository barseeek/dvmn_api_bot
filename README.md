# dvmn_api_bot


Данный проект реализует Telegram-бота, который использует API сервиса [dvmn.org](dvmn.org) для отслеживания статуса проверки учебных заданий. Бот уведомляет пользователя о результатах проверки.

## Процесс установки и запуска

Прежде всего, убедитесь, что у вас установлен Python версии 3.10 или новее. Затем следуйте инструкциям ниже для установки и запуска бота:

1. Клонируйте репозиторий на свой компьютер:

```bash
git clone https://github.com/barseeek/dvmn_api_bot.git
```

2. Перейдите в каталог с проектом:

```bash
cd dvmn_api_bot
```

3. Создайте и активируйте виртуальное окружение:

Для Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Для Unix или MacOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Установите зависимости:

```bash
pip install -r requirements.txt
```

5. Настройте переменные окружения в файле `.env` (см. описание файла ниже) и константы в коде.
```python
TIMEOUT = 60 # время до разрыва соединения в секундах 
RECONNECT_DELAY = 5 # задержка перед повторным запросом при отсутствии соединения в секундах 
```

6. Запустите бота:

```bash
python main.py
```

## Описание `.env` файла

Для корректной работы бота необходимо наличие файла `.env` в корневом каталоге проекта. Этот файл должен содержать следующие переменные:

- `API_TOKEN` - Токен для доступа к API DVMN.org.

- `TELEGRAM_BOT_TOKEN` - Токен вашего бота в Telegram. Получить этот токен можно у [@BotFather](https://t.me/BotFather) в Telegram после регистрации бота.
- 
- `TELEGRAM_LOG_BOT_TOKEN` - Токен вашего бота-логгера в Telegram. Получить этот токен можно у [@BotFather](https://t.me/BotFather) в Telegram после регистрации бота.

- `TELEGRAM_CHAT_ID` - ID чата, в который бот будет отправлять сообщения. Узнать свой chat_id можно у бота @userinfobot в Telegram.

- `LOG_LEVEL` - Уровень логгирования. Может быть `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` в зависимости от желаемой детализации логов.

Пример файла `.env`:

```
API_TOKEN=secretdvmntoken123456
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_LOG_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx5sad8df7a21
TELEGRAM_CHAT_ID=123456789
LOG_LEVEL=INFO
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).