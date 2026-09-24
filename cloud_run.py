# -*- coding: utf-8 -*-
"""
Единый скрипт для автономного запуска 24/7 в облаке (Render, Railway, Fly.io, Heroku, VPS, Docker).
Запускает FastAPI WebApp сервер и Aiogram Telegram бота одновременно в одном процессе.
"""
import sys
import os
import asyncio
import logging
import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import MenuButtonWebApp, WebAppInfo

import config
from database.db import init_db
from handlers import start, vocabulary, speaking, interview, settings, admin, support
from server import app as fastapi_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def run_fastapi(port: int):
    """Запуск FastAPI сервера WebApp & REST API"""
    uvicorn_config = uvicorn.Config(
        app=fastapi_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )
    server = uvicorn.Server(uvicorn_config)
    logger.info(f"🚀 FastAPI WebApp запущен на 0.0.0.0:{port}")
    await server.serve()

async def run_bot(public_url: str):
    """Запуск Telegram бота и автоматическая настройка кнопки Mini App"""
    if not config.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не указан в переменных окружения!")
        return

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(support.router)
    dp.include_router(start.router)
    dp.include_router(speaking.router)
    dp.include_router(interview.router)
    dp.include_router(settings.router)
    dp.include_router(vocabulary.router)

    if public_url and public_url.startswith("https://"):
        try:
            await bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(
                    text="Mini App",
                    web_app=WebAppInfo(url=public_url)
                )
            )
            logger.info(f"✅ Кнопка Mini App в Telegram настроена на: {public_url}")
        except Exception as e:
            logger.warning(f"⚠️ Не удалось обновить глобальную кнопку меню: {e}")

    logger.info("🤖 Telegram бот запущен и слушает сообщения (polling)...")
    await dp.start_polling(bot)

async def main():
    init_db()
    
    # Получаем порт от облачной платформы (Render, Railway и др.)
    port = int(os.getenv("PORT", 8000))
    
    # Определяем публичный HTTPS URL в облаке
    public_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("RAILWAY_STATIC_URL") or os.getenv("WEBAPP_URL") or ""
    if public_url and not public_url.startswith("http"):
        public_url = f"https://{public_url}"

    logger.info("=" * 60)
    logger.info("🌟 ЗАПУСК WOW LANGUAGES & TELEGRAM MINI APP В ОБЛАКЕ 24/7")
    logger.info(f"🌐 Публичный URL: {public_url or 'Не задан (локальный режим)'}")
    logger.info(f"🔌 Порт сервера: {port}")
    logger.info("=" * 60)

    # Запускаем FastAPI и бота параллельно в одном асинхронном цикле
    await asyncio.gather(
        run_fastapi(port),
        run_bot(public_url)
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Сервер и бот остановлены.")
