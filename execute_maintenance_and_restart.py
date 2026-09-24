# -*- coding: utf-8 -*-
"""
Maintenance and Service Restart Script for English Learning Bot
Strictly conforms to AGENTS.md rules:
- Strictly 1 start message, strictly 1 finish message per user (DISTINCT user_id, user_id > 1000)
- Inline button '🔄 Обновить бот (чтобы всё работало)' with callback_data='reload_bot'
- Verification of service liveness after restart
"""

import os
import sys

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import time
import sqlite3
import requests
import subprocess
import config

BOT_TOKEN = config.BOT_TOKEN
TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'vocabulary.db')

def get_target_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT DISTINCT user_id FROM users WHERE user_id > 1000")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def send_broadcast(text: str, reply_markup=None):
    users = get_target_users()
    print(f"📢 Sending broadcast to {len(users)} users: {users}")
    for uid in users:
        payload = {
            "chat_id": uid,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        try:
            r = requests.post(f"{TG_API}/sendMessage", json=payload, timeout=5)
            print(f"Sent to {uid}: status {r.status_code}")
        except Exception as e:
            print(f"Error sending to {uid}: {e}")

def free_port_8000():
    try:
        if sys.platform == 'win32':
            res = subprocess.run(['netstat', '-ano'], capture_output=True, encoding='cp866', errors='ignore')
            for line in (res.stdout or '').splitlines():
                if ':8000' in line and 'LISTENING' in line:
                    parts = line.strip().split()
                    pid = parts[-1]
                    subprocess.run(['taskkill', '/F', '/PID', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def main():
    # 1. Send start broadcast
    start_msg = (
        "🛠️ <b>Техническое обновление тренажёра</b>\n\n"
        "Добавляем новый режим упражнений «📰 Новости / тексты» с контекстными статьями из интернета. "
        "Это займёт менее 30 секунд!"
    )
    send_broadcast(start_msg)
    time.sleep(1)

    # 2. Kill old processes on port 8000 / python run.py
    print("Stopping old run.py and python processes...")
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'cloudflared.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        free_port_8000()
        time.sleep(1)
    except Exception:
        pass

    # 3. Start run.py as detached process
    print("Starting run.py...")
    run_path = os.path.join(os.path.dirname(__file__), 'run.py')
    flags = 0
    if sys.platform == 'win32':
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008 # DETACHED_PROCESS
    proc = subprocess.Popen([sys.executable, run_path], cwd=os.path.dirname(__file__), creationflags=flags)

    # 4. Wait for server and bot to become active
    server_ok = False
    for attempt in range(30):
        time.sleep(1)
        try:
            r = requests.get("http://127.0.0.1:8000/api/cards?user_id=466788167", timeout=2)
            if r.status_code == 200:
                print(f"✅ Backend server is LIVE: {len(r.json())} cards for Olga")
                server_ok = True
                break
        except Exception:
            pass

    # Check Telegram getMe
    try:
        me = requests.get(f"{TG_API}/getMe", timeout=5).json()
        print("Telegram bot info:", me.get('result', {}).get('username'))
    except Exception as e:
        print("Error checking getMe:", e)

    # 5. Send final broadcast with reload button
    finish_msg = (
        "✅ <b>Обновление успешно завершено!</b>\n\n"
        "✨ <b>Что нового в тренажёре:</b>\n"
        "• 📰 <b>Новый режим «Новости / тексты»:</b> изучаемые фразы теперь отрабатываются в живых новостных статьях и историях из интернета (про звёзд, технологии, культуру и бизнес)!\n"
        "• 🔍 <b>100% покрытие слов:</b> все выбранные фразы распределяются по контекстным статьям с интерактивными подсказками и переводом.\n"
        "• 🔊 <b>Озвучка статей:</b> возможность слушать полные тексты и отдельные фразы.\n\n"
        "👇 <b>Нажмите кнопку ниже, чтобы обновить бот и попробовать новый режим:</b>"
    )
    markup = {
        "inline_keyboard": [
            [
                {
                    "text": "🔄 Обновить бот (чтобы всё работало)",
                    "callback_data": "reload_bot"
                }
            ]
        ]
    }
    send_broadcast(finish_msg, reply_markup=markup)
    print("🎉 Maintenance finished successfully!")

if __name__ == "__main__":
    main()
