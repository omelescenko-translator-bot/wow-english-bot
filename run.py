# -*- coding: utf-8 -*-
"""
Единый скрипт запуска English Learning Bot & Mini App:
1. Запускает FastAPI сервер для WebApp (на http://127.0.0.1:8000)
2. Запускает постоянный чистый HTTPS туннель (Serveo - Tier 1, Localhost.run - Tier 2)
3. Запускает активный фоновый сторож-пинг (Watchdog), предотвращающий отключение туннелей по таймауту
4. Автоматически регистрирует актуальную кнопку Mini App в Telegram для всех пользователей
5. Запускает Telegram-бота с фоновым мониторингом стабильности 24/7
"""
import sys
import os
import time
import subprocess
import re
import requests
import asyncio
import threading

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import config
from database.db import get_all_user_ids
from bot import main as bot_main

CURRENT_TUNNEL_PROC = None
CURRENT_TUNNEL_URL = None
SERVER_PROC = None

def kill_process_tree(proc):
    if not proc:
        return
    try:
        if sys.platform == 'win32':
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            proc.terminate()
    except Exception:
        pass

def drain_pipe(proc):
    def _drain():
        try:
            for _ in iter(proc.stdout.readline, ''):
                pass
        except Exception:
            pass
    t = threading.Thread(target=_drain, daemon=True)
    t.start()

def free_port_8000():
    try:
        if sys.platform == 'win32':
            subprocess.run(['taskkill', '/F', '/IM', 'cloudflared.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['taskkill', '/F', '/IM', 'ssh.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            res = subprocess.run(['netstat', '-ano'], capture_output=True, encoding='cp866', errors='ignore')
            for line in (res.stdout or '').splitlines():
                if ':8000' in line and 'LISTENING' in line:
                    parts = line.strip().split()
                    pid = parts[-1]
                    subprocess.run(['taskkill', '/F', '/PID', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def start_server_process():
    port = int(os.getenv("PORT", "8000"))
    if not (os.getenv("RENDER") or os.getenv("PORT") or sys.platform != 'win32'):
        free_port_8000()
    server_path = os.path.join(os.path.dirname(__file__), 'server.py')
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.Popen([sys.executable, server_path], env=env)
    
    # Wait for server to be ready
    check_host = "127.0.0.1"
    for _ in range(15):
        try:
            res = requests.get(f'http://{check_host}:{port}/api/cards?user_id=1', timeout=1)
            if res.status_code == 200:
                print(f"✅ FastAPI сервер успешно запущен на порту {port}", flush=True)
                return proc
        except Exception:
            time.sleep(0.5)
            
    print(f"⚠️ Предупреждение: сервер запустился на порту {port}, ответ с задержкой.", flush=True)
    return proc

def check_tunnel_health(url: str, max_retries: int = 8, delay: float = 0.5) -> bool:
    if not url:
        return False
    for i in range(max_retries):
        try:
            r = requests.get(f"{url}/health", timeout=4)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(delay)
    return False

def start_serveo_tunnel():
    print("🚀 [1/2] Запуск постоянного SSH HTTPS туннеля (Serveo)...", flush=True)
    try:
        cmd = [
            'ssh',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null',
            '-o', 'ServerAliveInterval=5',
            '-o', 'ServerAliveCountMax=2',
            '-o', 'TCPKeepAlive=yes',
            '-o', 'ConnectTimeout=5',
            '-o', 'ExitOnForwardFailure=yes',
            '-R', '80:127.0.0.1:8000',
            'serveo.net'
        ]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            encoding='utf-8',
            errors='ignore'
        )
        start_time = time.time()
        url = None
        while time.time() - start_time < 12:
            line = proc.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            match = re.search(r'https://[a-zA-Z0-9-.]+\.serveousercontent\.com', line)
            if match:
                url = match.group(0)
                break
                
        if url:
            drain_pipe(proc)
            if check_tunnel_health(url, max_retries=8, delay=0.5):
                print(f"✅ Serveo туннель активен (200 OK): {url}", flush=True)
                return url, proc
            else:
                print(f"⚠️ Serveo туннель ({url}) не отвечает, пробуем резервный...", flush=True)
                if proc:
                    kill_process_tree(proc)
        if proc:
            kill_process_tree(proc)
    except Exception as e:
        print(f"⚠️ Serveo error: {e}", flush=True)
    return None, None

def start_localhost_run_tunnel():
    print("🚀 [2/2] Запуск резервного SSH HTTPS туннеля (localhost.run)...", flush=True)
    try:
        cmd = [
            'ssh',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null',
            '-o', 'ServerAliveInterval=5',
            '-o', 'ServerAliveCountMax=2',
            '-o', 'TCPKeepAlive=yes',
            '-o', 'ConnectTimeout=5',
            '-R', '80:127.0.0.1:8000',
            'nokey@localhost.run'
        ]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding='utf-8',
            errors='ignore'
        )
        start_time = time.time()
        url = None
        while time.time() - start_time < 12:
            line = proc.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            match = re.search(r'https://[a-zA-Z0-9-.]+\.lhr\.life', line)
            if match:
                url = match.group(0)
                break
                
        if url:
            drain_pipe(proc)
            if check_tunnel_health(url, max_retries=8, delay=0.5):
                print(f"✅ Localhost.run туннель активен (200 OK): {url}", flush=True)
                return url, proc
            else:
                print(f"⚠️ Localhost.run туннель ({url}) не отвечает, закрываем...", flush=True)
                if proc:
                    kill_process_tree(proc)
        if proc:
            kill_process_tree(proc)
    except Exception as e:
        print(f"⚠️ Localhost.run error: {e}", flush=True)
    return None, None

def start_stable_tunnel():
    print("⏳ Подключение постоянного и чистого HTTPS туннеля...", flush=True)
    
    # 1. Serveo (Tier 1 - fast & direct HTTPS)
    url, proc = start_serveo_tunnel()
    if url and proc:
        return url, proc

    # 2. Localhost.run (Tier 2 - fallback)
    url, proc = start_localhost_run_tunnel()
    if url and proc:
        return url, proc
        
    return None, None

def register_telegram_menu_button(token: str, url: str):
    try:
        final_url = f"{url}?v=17.0" if "?v=" not in url else url
        res = requests.post(f'https://api.telegram.org/bot{token}/setChatMenuButton', json={
            'menu_button': {
                'type': 'web_app',
                'text': 'Mini App',
                'web_app': {'url': final_url}
            }
        }, timeout=10).json()
        
        # Also update for all registered users in DB
        try:
            user_ids = set(get_all_user_ids() + [49367425, 466788167])
            for uid in user_ids:
                try:
                    requests.post(f'https://api.telegram.org/bot{token}/setChatMenuButton', json={
                        'chat_id': uid,
                        'menu_button': {
                            'type': 'web_app',
                            'text': 'Mini App',
                            'web_app': {'url': f"{url}?v=17.0&uid={uid}"}
                        }
                    }, timeout=3)
                except Exception:
                    pass
        except Exception as e:
            print(f"⚠️ User menu buttons update error: {e}", flush=True)
            
        print(f"✅ Кнопка Mini App в Telegram обновлена ({final_url}): {res.get('ok')}", flush=True)
    except Exception as e:
        print(f"⚠️ Ошибка обновления кнопки меню: {e}", flush=True)

def apply_tunnel_url(url: str):
    global CURRENT_TUNNEL_URL
    CURRENT_TUNNEL_URL = url
    config.WEBAPP_URL = url
    os.environ["WEBAPP_URL"] = url
    with open(os.path.join(os.path.dirname(__file__), '.env'), 'w', encoding='utf-8') as f:
        f.write(f"BOT_TOKEN={config.BOT_TOKEN}\nWEBAPP_URL={url}\n")
    register_telegram_menu_button(config.BOT_TOKEN, url)

async def active_tunnel_watchdog():
    """
    Непрерывный активный пинг и мониторинг туннеля:
    1. Каждые 5 секунд отправляет GET /health через публичный HTTPS туннель.
       Это гарантирует активный трафик и предотвращает сброс SSH-сессии по idle таймауту.
    2. Если 2 проверки подряд провалились (таймаут или ошибка сети), мгновенно перезапускает туннель.
    """
    global CURRENT_TUNNEL_PROC, CURRENT_TUNNEL_URL
    fail_count = 0
    loop = asyncio.get_running_loop()
    
    while True:
        await asyncio.sleep(5)
        if not CURRENT_TUNNEL_URL:
            continue
            
        # If on Render / Railway / static URL, no need to manage SSH tunnels
        if os.getenv("RENDER") or os.getenv("PORT") or sys.platform != 'win32':
            continue
            
        is_healthy = False
        try:
            def _probe():
                try:
                    r = requests.get(f"{CURRENT_TUNNEL_URL}/health", timeout=4)
                    return r.status_code == 200
                except Exception:
                    return False
            is_healthy = await loop.run_in_executor(None, _probe)
        except Exception:
            is_healthy = False
            
        if is_healthy:
            fail_count = 0
        else:
            fail_count += 1
            print(f"⚠️ Туннель {CURRENT_TUNNEL_URL} не ответил на пинг (сбой {fail_count}/2)...", flush=True)
            
            if fail_count >= 2:
                print("⚡ Активный сторожевой таймер: туннель завис или отключился. Мгновенный перезапуск!", flush=True)
                fail_count = 0
                if CURRENT_TUNNEL_PROC:
                    kill_process_tree(CURRENT_TUNNEL_PROC)
                    CURRENT_TUNNEL_PROC = None
                
                new_url, new_proc = await loop.run_in_executor(None, start_stable_tunnel)
                if new_url and new_proc:
                    CURRENT_TUNNEL_PROC = new_proc
                    CURRENT_TUNNEL_URL = new_url
                    apply_tunnel_url(new_url)
                    print(f"🌟 Восстановлен активный туннель: {new_url}", flush=True)

async def tunnel_manager():
    """Фоновый менеджер туннелей: быстро поднимает постоянный туннель и следит за его работой."""
    global CURRENT_TUNNEL_PROC, CURRENT_TUNNEL_URL
    loop = asyncio.get_running_loop()
    
    # Check if running on cloud platform (Render / Railway / etc.)
    cloud_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("RAILWAY_STATIC_URL") or os.getenv("WEBAPP_URL")
    if cloud_url and (os.getenv("RENDER") or os.getenv("PORT") or sys.platform != 'win32'):
        CURRENT_TUNNEL_URL = cloud_url
        apply_tunnel_url(cloud_url)
        print(f"🌟 Cloud Production WebApp URL (HTTPS): {cloud_url}", flush=True)
        while True:
            await asyncio.sleep(60)
            continue
    
    print("⏳ Подключение стабильного HTTPS туннеля в фоне...", flush=True)
    url, proc = await loop.run_in_executor(None, start_stable_tunnel)
    if url and proc:
        CURRENT_TUNNEL_URL = url
        CURRENT_TUNNEL_PROC = proc
        apply_tunnel_url(url)
        print(f"🌟 Telegram Mini App URL (HTTPS): {url}", flush=True)
    else:
        print("⚠️ Не удалось поднять HTTPS туннель. Повторная попытка через 5 секунд...", flush=True)
        
    while True:
        await asyncio.sleep(8)
        try:
            if not CURRENT_TUNNEL_PROC or CURRENT_TUNNEL_PROC.poll() is not None:
                print("🔄 Туннельный процесс завершился, переподключение...", flush=True)
                new_url, new_proc = await loop.run_in_executor(None, start_stable_tunnel)
                if new_url and new_proc:
                    CURRENT_TUNNEL_PROC = new_proc
                    CURRENT_TUNNEL_URL = new_url
                    apply_tunnel_url(new_url)
                    print(f"🌟 Новый активный туннель: {new_url}", flush=True)
        except Exception as e:
            print(f"⚠️ Ошибка в tunnel_manager: {e}", flush=True)

async def run_all():
    global CURRENT_TUNNEL_PROC, CURRENT_TUNNEL_URL, SERVER_PROC
    
    # Запускаем туннель и активный сторож в фоне
    asyncio.create_task(tunnel_manager())
    asyncio.create_task(active_tunnel_watchdog())
    
    while True:
        try:
            print(f"🤖 Telegram бот @WOWEnglishAI_bot запускается...", flush=True)
            await bot_main()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"⚠️ Telegram bot polling error (cloud instance may be active): {e}", flush=True)
            await asyncio.sleep(10)

if __name__ == '__main__':
    print("=" * 60, flush=True)
    print("🚀 ЗАПУСК ENGLISH LEARNING BOT & TELEGRAM MINI APP", flush=True)
    print("=" * 60, flush=True)
    
    # 1. Start WebApp server
    SERVER_PROC = start_server_process()
    
    try:
        asyncio.run(run_all())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Остановка сервисов...", flush=True)
    finally:
        if CURRENT_TUNNEL_PROC:
            kill_process_tree(CURRENT_TUNNEL_PROC)
        if SERVER_PROC:
            kill_process_tree(SERVER_PROC)
