# -*- coding: utf-8 -*-
import subprocess
import time
import re
import requests
import sys

def get_serveo_tunnel():
    print("Starting Serveo SSH tunnel...")
    cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'ServerAliveInterval=30', '-R', '80:127.0.0.1:8000', 'serveo.net']
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding='utf-8',
        errors='ignore'
    )
    
    url = None
    start_time = time.time()
    while time.time() - start_time < 20:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        print("[SERVEO]", line.strip())
        match = re.search(r'https://[a-zA-Z0-9-.]+\.serveousercontent\.com', line)
        if match:
            url = match.group(0)
            break
            
    return url, proc

if __name__ == '__main__':
    url, proc = get_serveo_tunnel()
    print("Found Serveo URL:", url)
    if url:
        time.sleep(1)
        res = requests.get(url + "/api/cards")
        print("Status code:", res.status_code)
        print("Cards:", len(res.json()))
    if proc:
        proc.terminate()
