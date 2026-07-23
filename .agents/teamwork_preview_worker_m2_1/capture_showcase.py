#!/usr/bin/env python3
import subprocess
import time
import json
import urllib.request
import socket
import base64
import os
import sys

WORK_DIR = "/home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_1"

# Launch Chrome
chrome_proc = subprocess.Popen([
    "google-chrome",
    "--headless=new",
    "--disable-gpu",
    "--remote-debugging-port=9222",
    "--window-size=1600,1000",
    "file:///home/raghavan/projects/bowncer_sportz/index.html"
])

time.sleep(1.5)

class MinimalCDP:
    def __init__(self, ws_url):
        # Parse ws://127.0.0.1:9222/devtools/page/...
        url_part = ws_url.replace("ws://", "")
        host_port, self.path = url_part.split("/", 1)
        self.path = "/" + self.path
        host, port = host_port.split(":")
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, int(port)))
        
        # Handshake
        key = base64.b64encode(b"bowncersportzkey").decode()
        handshake = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {host_port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode())
        res = self.sock.recv(4096)
        if b"101 Switching Protocols" not in res:
            raise RuntimeError("WebSocket handshake failed")
        
        self.msg_id = 1

    def send_cmd(self, method, params=None):
        mid = self.msg_id
        self.msg_id += 1
        payload = json.dumps({"id": mid, "method": method, "params": params or {}}).encode()
        
        # Encode WS frame (masked from client)
        header = bytearray()
        header.append(0x81) # Text frame
        length = len(payload)
        mask = b"1234"
        
        if length <= 125:
            header.append(length | 0x80)
        elif length <= 65535:
            header.append(126 | 0x80)
            header.extend(length.to_bytes(2, "big"))
        else:
            header.append(127 | 0x80)
            header.extend(length.to_bytes(8, "big"))
            
        header.extend(mask)
        masked_payload = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
        
        self.sock.sendall(header + masked_payload)
        
        # Read response
        raw_resp = bytearray()
        while True:
            chunk = self.sock.recv(65536)
            if not chunk:
                break
            raw_resp.extend(chunk)
            # Simple payload search
            try:
                # Find JSON payload after WS header
                text = raw_resp.decode("utf-8", errors="ignore")
                for line in text.splitlines():
                    if f'"id":{mid}' in line or f'"id": {mid}' in line:
                        start_idx = line.find("{")
                        end_idx = line.rfind("}")
                        if start_idx != -1 and end_idx != -1:
                            return json.loads(line[start_idx:end_idx+1])
            except Exception:
                pass
            time.sleep(0.05)
        return {}

    def close(self):
        self.sock.close()

try:
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    targets = json.loads(req.read().decode())
    page_target = [t for t in targets if t.get("type") == "page"][0]
    ws_url = page_target["webSocketDebuggerUrl"]
    
    cdp = MinimalCDP(ws_url)
    print("CDP WebSocket Connected Successfully!")
    
    cdp.send_cmd("Page.enable")
    cdp.send_cmd("Runtime.enable")
    
    # Hide intro, show showcase reveal, scroll to showcase
    res = cdp.send_cmd("Runtime.evaluate", {
        "expression": """
            (() => {
                sessionStorage.setItem('intro-seen', '1');
                var intro = document.getElementById('intro-cinematic');
                if (intro) intro.style.display = 'none';
                var els = document.querySelectorAll('.showcase-reveal');
                els.forEach(e => e.classList.add('is-visible'));
                var showcase = document.getElementById('media-showcase');
                if (showcase) showcase.scrollIntoView();
                return {
                    title: showcase ? showcase.querySelector('.showcase-title').innerText : 'NOT FOUND',
                    cards: document.querySelectorAll('#media-showcase .video-card').length
                };
            })()
        """,
        "returnByValue": True
    })
    print("CDP Eval Result:", res.get("result", {}).get("result", {}).get("value"))
    
    # 1. Desktop Screenshot
    cdp.send_cmd("Emulation.setDeviceMetricsOverride", {"width": 1600, "height": 1000, "deviceScaleFactor": 1, "mobile": False})
    time.sleep(0.5)
    pic_res = cdp.send_cmd("Page.captureScreenshot", {"format": "png"})
    pic_b64 = pic_res.get("result", {}).get("data")
    if pic_b64:
        with open(os.path.join(WORK_DIR, "desktop_showcase_1600.png"), "wb") as f:
            f.write(base64.b64decode(pic_b64))
        print("Saved desktop_showcase_1600.png")

    # 2. Test Play button click
    click_res = cdp.send_cmd("Runtime.evaluate", {
        "expression": """
            (() => {
                var playBtn = document.getElementById('stage-play-btn');
                if (playBtn) {
                    playBtn.click();
                    return { clicked: True, hasOfflineNotice: !!document.querySelector('.video-offline-card') };
                }
                return { clicked: False };
            })()
        """,
        "returnByValue": True
    })
    print("Play Click Eval Result:", click_res.get("result", {}).get("result", {}).get("value"))

    play_pic = cdp.send_cmd("Page.captureScreenshot", {"format": "png"})
    play_b64 = play_pic.get("result", {}).get("data")
    if play_b64:
        with open(os.path.join(WORK_DIR, "desktop_showcase_play_clicked.png"), "wb") as f:
            f.write(base64.b64decode(play_b64))
        print("Saved desktop_showcase_play_clicked.png")

    # 3. Mobile Screenshot & Overflow check
    cdp.send_cmd("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
    time.sleep(0.5)
    mob_pic = cdp.send_cmd("Page.captureScreenshot", {"format": "png"})
    mob_b64 = mob_pic.get("result", {}).get("data")
    if mob_b64:
        with open(os.path.join(WORK_DIR, "mobile_showcase_390.png"), "wb") as f:
            f.write(base64.b64decode(mob_b64))
        print("Saved mobile_showcase_390.png")

    overflow_res = cdp.send_cmd("Runtime.evaluate", {
        "expression": "document.documentElement.scrollWidth > document.documentElement.clientWidth",
        "returnByValue": True
    })
    print("Mobile Horizontal Overflow Result:", overflow_res.get("result", {}).get("result", {}).get("value"))

    cdp.close()
finally:
    chrome_proc.terminate()
