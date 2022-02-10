# Бот для телеграм уведомлений

### Описание

Бот позволяет получать уведомления о сданных работах с сайта [dvmn.org](https://dvmn.org/)      
А так же реализовано логирование приложения в телеграм

### Подготовка проекта
- Склонируйте репозиторий:

`git clone https://github.com/AlexeyPeresypkin/devman_chat_bots.git`

- Установите зависимости:

`pip install -r requirements.txt`

- Добавьте в корневую директорию файл `.env` с переменными окружения

```
DEVMAN_TOKEN=<Токен с сайта https://dvmn.org/api/docs/>
TELEGRAM_TOKEN=<Ваш токен от телеграм бота, BotFather подскажет>
CHAT_ID=<Ваш id в телеграм, можно спросить у userinfobot>
```
### Локальный запуск

`python bot_notification.py`

