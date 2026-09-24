# -*- coding: utf-8 -*-
import sys
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database.db import init_db
from handlers import start, vocabulary, speaking, interview, settings, admin, support

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    init_db()
    
    if not BOT_TOKEN:
        print("BOT_TOKEN is empty in config.py")
        return

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(support.router)
    dp.include_router(start.router)
    dp.include_router(speaking.router)
    dp.include_router(interview.router)
    dp.include_router(settings.router)
    dp.include_router(vocabulary.router)

    print("Bot polling started...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
