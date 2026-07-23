#!/usr/bin/env python3
import subprocess
import time
import json
import urllib.request
import asyncio
from pathlib import Path

# Start Chrome in background with remote debugging port
chrome_proc = subprocess.Popen([
    "google-chrome",
    "--headless",
    "--disable-gpu",
    "--remote-debugging-port=9222",
    "--window-size=1600,1000",
    "file:///home/raghavan/projects/bowncer_sportz/index.html"
])

time.sleep(1.5)

try:
    # Query targets from CDP
    req = urllib.request.urlopen("http://localhost:9222/json")
    targets = json.loads(req.read().decode())
    print("Found CDP targets:", len(targets))
    page_target = [t for t in targets if t.get("type") == "page"][0]
    ws_url = page_target["webSocketDebuggerUrl"]
    print("WebSocket Debugger URL:", ws_url)
finally:
    chrome_proc.terminate()
