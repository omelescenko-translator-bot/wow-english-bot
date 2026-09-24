# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8979320080:AAGrNzTOizem6F0t26uli59t7AepTj5Zduo")
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:8000")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Admin user IDs allowed to view platform analytics and reports
ADMIN_USER_IDS = [466788167]
MAIN_ADMIN_ID = 466788167
DEV_USERNAME = "Hitrova_Olga"

SUPPORTED_LANGS = {
    'en': {'name': 'English (Английский)', 'flag': '🇬🇧', 'short': 'EN', 'speech_code': 'en-US'},
    'ru': {'name': 'Русский', 'flag': '🇷🇺', 'short': 'RU', 'speech_code': 'ru-RU'},
    'uk': {'name': 'Українська (Украинский)', 'flag': '🇺🇦', 'short': 'UK', 'speech_code': 'uk-UA'},
    'es': {'name': 'Español (Испанский)', 'flag': '🇪🇸', 'short': 'ES', 'speech_code': 'es-ES'},
    'fr': {'name': 'Français (Французский)', 'flag': '🇫🇷', 'short': 'FR', 'speech_code': 'fr-FR'},
    'de': {'name': 'Deutsch (Немецкий)', 'flag': '🇩🇪', 'short': 'DE', 'speech_code': 'de-DE'},
    'it': {'name': 'Italiano (Итальянский)', 'flag': '🇮🇹', 'short': 'IT', 'speech_code': 'it-IT'},
    'sl': {'name': 'Slovenščina (Словенский)', 'flag': '🇸🇮', 'short': 'SL', 'speech_code': 'sl-SI'}
}

def is_admin(user_id) -> bool:
    try:
        if not user_id:
            return False
        return int(user_id) in ADMIN_USER_IDS
    except Exception:
        return False

def get_webapp_url() -> str:
    load_dotenv(override=True)
    # Check common cloud platform environment variables first
    cloud_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("RAILWAY_STATIC_URL") or os.getenv("WEBAPP_URL")
    return cloud_url or WEBAPP_URL

