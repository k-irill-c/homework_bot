# homework_bot
Реализован телеграм-бот для автоматической проверки и извещения о статусе проверки домашней работы в Яндекс.Практикум.
### Стек технологий
* python - язык программирования
* python-telegram-bot - Python-библиотека для создания Telegram-бота
* telegram - основной пакет, содержит все методы Bot API, перенесённые на Python
* API сервиса Практикум.Домашка

# Описание проекта
* раз в 10 минут бот опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
* при обновлении статуса бот анализирует ответ API и отправляет соответствующее уведомление в Telegram;
* бот логирует свою работу и сообщает о важных проблемах сообщением в Telegram.
### Функция main():
в ней описана основная логика работы программы. Все остальные функции должны запускаться из неё. Последовательность действий должна быть примерно такой:
Сделать запрос к API.
Проверить ответ.
Если есть обновления — получить статус работы из обновления и отправить сообщение в Telegram.
Подождать некоторое время и сделать новый запрос.
### Функция check_tokens()
проверяет доступность переменных окружения, которые необходимы для работы программы. Если отсутствует хотя бы одна переменная окружения — функция должна вернуть False, иначе — True.
### Функция get_api_answer()
делает запрос к единственному эндпоинту API-сервиса. В качестве параметра функция получает временную метку. В случае успешного запроса должна вернуть ответ API, преобразовав его из формата JSON к типам данных Python.
### Функция check_response()
проверяет ответ API на корректность. В качестве параметра функция получает ответ API, приведенный к типам данных Python. Если ответ API соответствует ожиданиям, то функция должна вернуть список домашних работ (он может быть и пустым), доступный в ответе API по ключу 'homeworks'.
Функция parse_status() извлекает из информации о конкретной домашней работе статус этой работы. В качестве параметра функция получает только один элемент из списка домашних работ. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_STATUSES.
### Функция send_message()
отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.
### Логирование
Реализован журнал логирования следующих событий:
* отсутствие обязательных переменных окружения во время запуска бота (уровень CRITICAL).
* удачная отправка любого сообщения в Telegram (уровень INFO);
* сбой при отправке сообщения в Telegram (уровень ERROR);
* недоступность эндпоинта https://practicum.yandex.ru/api/user_api/homework_statuses/ (уровень ERROR);
* любые другие сбои при запросе к эндпоинту (уровень ERROR);
* отсутствие ожидаемых ключей в ответе API (уровень ERROR);
* недокументированный статус домашней работы, обнаруженный в ответе API (уровень ERROR);
* отсутствие в ответе новых статусов (уровень DEBUG).

## Разворачивание проекта

* Склонировать репозиторий, перейти в проект:
```bash
git clone https://github.com/k-irill-c/homework_bot
```

```bash
cd homework_bot
```

* Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```

```bash
. venv/bin/activate
```

* Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
* Зарегистрироваться в telegram (https://telegram.org/)

* Найти в Telegram бота @BotFather: в окно поиска над списком контактов введите его имя.
(внимание! на иконке возле имени бота должна быть белая галочка на голубом фоне.)

* Зарегистрировать бота
Начните диалог с ботом @BotFather: нажмите кнопку Start («Запустить»).
Затем отправьте команду /newbot и укажите параметры нового бота:
    имя (на любом языке), под которым ваш бот будет отображаться в списке контактов;
    техническое имя вашего бота, по которому его можно будет найти в Telegram. 
    Имя должно оканчиваться на слово bot в любом регистре, например goodbot, good_bot. Имена ботов должны быть уникальны.
    При регистрации бота @BotFather поздравит вас и отправит в чат токен для работы с Bot API. 
    Токен выглядит примерно так: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11.
* Получить 
PRACTICUM_TOKEN:
Получить токен можно по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.
TELEGRAM_TOKEN: 
Получен при регистрации бота.
TELEGRAM_CHAT_ID
Чтобы бот отправил сообщение именно вам, нужно узнать ID своего Telegram-аккаунта. Telegram-бот @userinfobot подскажет.

* Создать в папке проекта файл .env
```bash
touch .env
```
* Открыть файл .env
```bash
nano .env
```
* Вписать соответствующие значения следующим переменным:
PRACTICUM_TOKEN = '<Ваш PRACTICUM_TOKEN>'
TELEGRAM_TOKEN = '<Ваш TELEGRAM_TOKEN>'
TELEGRAM_CHAT_ID = '<Ваш TELEGRAM_CHAT_ID>'
Вписывать значения в кавычках и без <> скобок.

```bash
PRACTICUM_TOKEN = ''
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''
```

* Заустить код файла homework.py
```bash
python homework.py
```
##### Автор
Кирилл С. - студет Яндекс.Практикума
