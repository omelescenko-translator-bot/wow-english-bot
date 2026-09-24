# -*- coding: utf-8 -*-
import subprocess
import re
import time
import os
import sys

def start_tunnel():
    cf_path = os.path.join(os.path.dirname(__file__), 'cloudflared.exe')
    if not os.path.exists(cf_path):
        print(f"Error: {cf_path} not found")
        return None, None
        
    cmd = [cf_path, 'tunnel', '--url', 'http://127.0.0.1:8000']
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
    # Cloudflare outputs the tunnel url to stderr
    start_time = time.time()
    while time.time() - start_time < 20:
        line = proc.stderr.readline()
        if not line:
            time.sleep(0.1)
            continue
        print("[CF]", line.strip())
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            break
            
    return url, proc

if __name__ == '__main__':
    url, proc = start_tunnel()
    print("Found HTTPS URL:", url)
    if proc:
        proc.terminate()
