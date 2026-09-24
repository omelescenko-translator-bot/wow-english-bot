# 🇬🇧 English Learning Bot & Mini App

Персональный Telegram-бот и встроенное мини-приложение (Telegram Mini App / WebApp) для эффективного изучения английского языка по системе интервальных повторений (Spaced Repetition SM-2), разговорной практики и подготовки к собеседованиям.

---

## 🎯 3 простых способа добавлять новые слова и фразы

Вы можете пополнять свой словарь любым удобным способом:

### 1. Способ 1: Прямо в чат с ботом (Текст, пачки строк, пересылка)
* **Одна фраза:** просто напишите боту в чат:  
  `Let's meet between Ljubljana and Vienna - Давай встретимся между Любляной и Веной`
* **Сразу пачка фраз:** скопируйте несколько строк из таблицы и отправьте одним сообщением — бот мгновенно добавит все карточки оптом!
* **Пересылка (Forward):** перешлите любое сообщение из английских каналов или чатов боту.

### 2. Способ 2: Через Excel-файл [my_words.xlsx](file:///c:/PROJECTS/English_Learning_Bot/data/my_words.xlsx)
* В папке `data/` лежит готовый шаблон: [my_words.xlsx](file:///c:/PROJECTS/English_Learning_Bot/data/my_words.xlsx) с вашими 76 фразами.
* Просто откройте его в Excel, допишите новые строки внизу и:
  * Либо отправьте этот `.xlsx` файл боту в Telegram как документ (скрепка 📎);
  * Либо выполните команду: `python import_my_words.py`.

### 3. Способ 3: Внутри Telegram Mini App
* Откройте приложение по кнопке `[ 📱 Открыть словарь / Карточки ]`.
* Перейдите во вкладку **«Словарь»** и нажмите синюю кнопку **«➕ Добавить»**.

---

## 🚀 Запуск проекта

### Шаг 1. Укажите токен бота
1. Откройте Telegram и напишите боту **@BotFather**.
2. Отправьте команду `/newbot`, придумайте имя и юзернейм (например, `MyEnglishStudyBot`).
3. Скопируйте полученный API Token и вставьте его в [config.py](file:///c:/PROJECTS/English_Learning_Bot/config.py) в строку `BOT_TOKEN = "ВАШ_ТОКЕН"`.

### Шаг 2. Запуск веб-сервера Mini App
```bash
cd c:\PROJECTS\English_Learning_Bot
python server.py
```
*(Сервер запустится на `http://localhost:8000`)*

### Шаг 3. Запуск Telegram бота
```bash
python bot.py
```

---

## 📂 Структура проекта
* [data/vocabulary.db](file:///c:/PROJECTS/English_Learning_Bot/data/vocabulary.db) — база данных SQLite (пользователи, карточки, интервалы).
* [data/my_words.xlsx](file:///c:/PROJECTS/English_Learning_Bot/data/my_words.xlsx) — ваш персональный Excel-словарь.
* [webapp/](file:///c:/PROJECTS/English_Learning_Bot/webapp/) — современное Mini App приложение (HTML5/CSS/JS, 3D flip, озвучка, свайпы).
* [handlers/](file:///c:/PROJECTS/English_Learning_Bot/handlers/) — логика меню, добавления фраз, разговорного тренажёра и симулятора интервью.
* [import_my_words.py](file:///c:/PROJECTS/English_Learning_Bot/import_my_words.py) — утилита быстрого импорта из Excel и текста.
