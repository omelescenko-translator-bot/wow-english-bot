# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import requests

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

def cleanup_old_processes():
    print("Stopping any existing services...", flush=True)
    subprocess.run(["taskkill", "/F", "/IM", "cloudflared.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["taskkill", "/F", "/IM", "ssh.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    current_pid = os.getpid()
    try:
        out = subprocess.check_output(['wmic', 'process', 'where', "name='python.exe'", 'get', 'processid,commandline'], encoding='cp866', errors='ignore')
        for line in out.splitlines():
            line = line.strip()
            if not line or 'CommandLine' in line:
                continue
            parts = line.split()
            pid = parts[-1]
            cmd = " ".join(parts[:-1])
            if pid.isdigit() and int(pid) != current_pid and ('run.py' in cmd or 'server.py' in cmd or 'bot.py' in cmd):
                print(f"Killing old python process {pid} ({cmd})", flush=True)
                subprocess.run(['taskkill', '/F', '/T', '/PID', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    try:
        res = subprocess.run(['netstat', '-ano'], capture_output=True, encoding='cp866', errors='ignore')
        for line in (res.stdout or '').splitlines():
            if ':8000' in line and 'LISTENING' in line:
                parts = line.strip().split()
                pid = parts[-1]
                if pid.isdigit() and int(pid) != current_pid:
                    subprocess.run(['taskkill', '/F', '/PID', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(root, "service.log")
    
    cleanup_old_processes()
    time.sleep(1)

    print("Launching run.py...", flush=True)
    log_out = open(log_file, "a", encoding="utf-8")
    flags = 0
    if sys.platform == "win32":
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000008 # DETACHED_PROCESS
        
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.Popen(
        [sys.executable, "-u", os.path.join(root, "run.py")],
        cwd=root,
        stdout=log_out,
        stderr=subprocess.STDOUT,
        creationflags=flags,
        env=env
    )
    print(f"Spawned PID: {proc.pid}", flush=True)

    print("Waiting for local server (port 8000)...", flush=True)
    server_live = False
    for i in range(25):
        time.sleep(1)
        try:
            r = requests.get("http://127.0.0.1:8000/health", timeout=2)
            if r.status_code == 200:
                print("✅ Backend server is live!", flush=True)
                server_live = True
                break
        except Exception:
            pass

    if not server_live:
        print("❌ Backend server failed to respond within 25s", flush=True)
        return

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
                        if val.startswith("https://") and ("trycloudflare.com" in val or "lhr.life" in val or "serveousercontent.com" in val):
                            tunnel_url = val
                            break
        if tunnel_url:
            break

    print(f"Current WEBAPP_URL in .env: {tunnel_url}", flush=True)

if __name__ == "__main__":
    main()
