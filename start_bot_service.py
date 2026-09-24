# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import requests

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(root, "service.log")
    
    # 1. Kill any existing cloudflared or port 8000 listeners
    print("Stopping any existing services...", flush=True)
    subprocess.run(["taskkill", "/F", "/IM", "cloudflared.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Free port 8000
    try:
        res = subprocess.run(['netstat', '-ano'], capture_output=True, encoding='cp866', errors='ignore')
        for line in (res.stdout or '').splitlines():
            if ':8000' in line and 'LISTENING' in line:
                parts = line.strip().split()
                pid = parts[-1]
                subprocess.run(['taskkill', '/F', '/PID', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    time.sleep(1)

    # 2. Launch run.py detached with stdout/stderr to log
    print("Launching run.py...", flush=True)
    log_out = open(log_file, "a", encoding="utf-8")
    flags = 0
    if sys.platform == "win32":
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008 # DETACHED_PROCESS
        
    proc = subprocess.Popen(
        [sys.executable, "-u", os.path.join(root, "run.py")],
        cwd=root,
        stdout=log_out,
        stderr=subprocess.STDOUT,
        creationflags=flags
    )
    print(f"Spawned PID: {proc.pid}", flush=True)

    # 3. Wait for local FastAPI server
    print("Waiting for local server (port 8000)...", flush=True)
    server_live = False
    for i in range(20):
        time.sleep(1)
        try:
            r = requests.get("http://127.0.0.1:8000/api/cards?user_id=466788167", timeout=2)
            if r.status_code == 200:
                print("✅ Backend server is live!", flush=True)
                server_live = True
                break
        except Exception:
            pass

    if not server_live:
        print("❌ Backend server failed to respond within 20s", flush=True)
        return

    # 4. Wait for Tunnel and Telegram Menu Button update
    print("Waiting for Tunnel URL to be generated...", flush=True)
    tunnel_url = None
    for i in range(30):
        time.sleep(1)
        if os.path.exists(os.path.join(root, ".env")):
            with open(os.path.join(root, ".env"), "r", encoding="utf-8") as f:
                content = f.read()
                for line in content.splitlines():
                    if line.startswith("WEBAPP_URL="):
                        val = line.split("=", 1)[1].strip()
                        if val.startswith("https://") and ("trycloudflare.com" in val or "lhr.life" in val):
                            tunnel_url = val
                            break
        if tunnel_url:
            break

    print(f"Current WEBAPP_URL in .env: {tunnel_url}", flush=True)

if __name__ == "__main__":
    main()
