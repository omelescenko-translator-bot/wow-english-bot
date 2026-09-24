# 🚀 Инструкция по запуску бота и Mini App 24/7 в облаке

Чтобы бот и приложение работали **непрерывно 24 часа в сутки 7 дней в неделю**, даже когда ваш компьютер полностью выключен, проект полностью подготовлен для бесплатного облачного хостинга (Render.com или Railway.app).

---

## 🌟 Вариант 1: Бесплатный запуск на Render.com (Рекомендуется, 2 минуты)

1. Зайдите на сайт **[render.com](https://render.com)** и авторизуйтесь (через GitHub или почту).
2. Нажмите синюю кнопку **«New +»** ➔ выберите **«Web Service»**.
3. Выберите ваш репозиторий с проектом (или подключите GitHub).
4. Укажите параметры:
   - **Name:** `wow-english-bot`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python cloud_run.py`
   - **Instance Type:** `Free`
5. В разделе **«Environment Variables»** (Переменные окружения) добавьте:
   - `BOT_TOKEN` = `8979320080:AAGrNzTOizem6F0t26uli59t7AepTj5Zduo`
   - `GEMINI_API_KEY` = `ваш ключ Gemini API`
   - `WEBAPP_URL` = `https://wow-english-bot.onrender.com` (адрес, который выдаст Render)
6. Нажмите **«Deploy Web Service»**.

> ✅ **Готово!** Сервер и бот запустятся в облаке. Render выдаст постоянный защищённый HTTPS-адрес, бот автоматически обновит кнопку Mini App в Telegram, и всё будет работать 24/7 без вашего компьютера!

---

## 🚂 Вариант 2: Запуск на Railway.app

1. Перейдите на **[railway.app](https://railway.app)**.
2. Нажмите **«New Project»** ➔ **«Deploy from GitHub repo»**.
3. Добавьте переменные `BOT_TOKEN` и `GEMINI_API_KEY`.
4. Нажмите **«Generate Domain»** в настройках сервиса.
5. Railway автоматически соберет проект по `Dockerfile` или `Procfile` и запустит `cloud_run.py`.

---

## 📦 Файлы, созданные для облака:
* `cloud_run.py` — единый асинхронный запуск WebApp (FastAPI на порту `$PORT`) и Telegram-бота одновременно.
* `Procfile` — автозапуск веб-воркера для Render / Heroku / Railway.
* `Dockerfile` — контейнерная сборка Python 3.10.
* `render.yaml` — Blueprint для мгновенного импорта.
* `requirements.txt` — все необходимые библиотеки.
