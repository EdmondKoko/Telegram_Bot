![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

# Бот - ассистент

## Описание
- раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
- логирует свою работу и сообщать вам о важных проблемах сообщением в Telegram.


### Запуск приложения:

Клонируем проект:

```bash
git clone https://github.com/edmondkoko/tg_bot.git
```

Переходим в папку с проектом:

```bash
cd tg_bot
```

Устанавливаем виртуальное окружение:

```bash
python3 -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/bin/activate
```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

Зарегистрировать чат-бота в Телеграм:

Создать в корневой директории файл .env для хранения переменных окружения

```bash
PRAKTIKUM_TOKEN = 'xxx'
TELEGRAM_TOKEN = 'xxx'
TELEGRAM_CHAT_ID = 'xxx'
```

Запускаем проект:

```bash
python tg_bot.py
```
