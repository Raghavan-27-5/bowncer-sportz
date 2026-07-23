const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const WORK_DIR = '/home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_1';

async function main() {
  const chrome = spawn('google-chrome', [
    '--headless=new',
    '--disable-gpu',
    '--remote-debugging-port=9222',
    '--window-size=1600,1200',
    'file:///home/raghavan/projects/bowncer_sportz/index.html'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await new Promise((resolve, reject) => {
      http.get('http://127.0.0.1:9222/json', (r) => {
        let body = '';
        r.on('data', chunk => body += chunk);
        r.on('end', () => resolve(JSON.parse(body)));
      }).on('error', reject);
    });

    const pageTarget = res.find(t => t.type === 'page');
    if (!pageTarget) throw new Error('No page target found');

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let msgId = 1;
    const callbacks = new Map();
    const consoleLogs = [];

    ws.onmessage = (evt) => {
      const msg = JSON.parse(evt.data);
      if (msg.method === 'Console.messageAdded') {
        consoleLogs.push(msg.params.message);
      }
      if (msg.method === 'Runtime.consoleAPICalled') {
        consoleLogs.push(msg.params);
      }
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
      }
    };

    await new Promise(r => ws.onopen = r);

    function sendCommand(method, params = {}) {
      return new Promise((resolve) => {
        const id = msgId++;
        callbacks.set(id, resolve);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    await sendCommand('Page.enable');
    await sendCommand('Runtime.enable');

    console.log('--- Navigating to index.html ---');
    await sendCommand('Page.navigate', { url: 'file:///home/raghavan/projects/bowncer_sportz/index.html' });
    await new Promise(r => setTimeout(r, 1000));

    // Hide intro, activate animations, scroll to #media-showcase
    const evalResult = await sendCommand('Runtime.evaluate', {
      expression: `
        (() => {
          sessionStorage.setItem('intro-seen', '1');
          var intro = document.getElementById('intro-cinematic');
          if (intro) intro.style.display = 'none';
          var els = document.querySelectorAll('.showcase-reveal');
          els.forEach(e => e.classList.add('is-visible'));
          var showcase = document.getElementById('media-showcase');
          if (showcase) showcase.scrollIntoView();
          return {
            showcasePresent: !!showcase,
            titleText: showcase ? showcase.querySelector('.showcase-title').innerText : '',
            activeCards: document.querySelectorAll('#media-showcase .video-card.is-active').length
          };
        })()
      `,
      returnByValue: true
    });

    console.log('DOM Evaluation Result:', evalResult.result.value);

    // Capture 1600px desktop screenshot
    await sendCommand('Emulation.setDeviceMetricsOverride', {
      width: 1600,
      height: 1000,
      deviceScaleFactor: 1,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 500));

    const desktopPic = await sendCommand('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(WORK_DIR, 'desktop_showcase_1600.png'), Buffer.from(desktopPic.data, 'base64'));
    console.log('Saved desktop_showcase_1600.png');

    // Test Play button click via Runtime.evaluate
    const playClickResult = await sendCommand('Runtime.evaluate', {
      expression: `
        (() => {
          var btn = document.getElementById('stage-play-btn');
          if (btn) {
            btn.click();
            return { clicked: true, hasOfflineCard: !!document.querySelector('.video-offline-card') };
          }
          return { clicked: false };
        })()
      `,
      returnByValue: true
    });
    console.log('Play Button Click Result:', playClickResult.result.value);

    const playPic = await sendCommand('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(WORK_DIR, 'desktop_showcase_play_clicked.png'), Buffer.from(playPic.data, 'base64'));
    console.log('Saved desktop_showcase_play_clicked.png');

    // Reset poster
    await sendCommand('Runtime.evaluate', {
      expression: `
        (() => {
          var resetBtn = document.getElementById('reset-facade-btn');
          if (resetBtn) resetBtn.click();
        })()
      `
    });

    // Capture 390px mobile screenshot
    await sendCommand('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 500));

    const mobilePic = await sendCommand('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(WORK_DIR, 'mobile_showcase_390.png'), Buffer.from(mobilePic.data, 'base64'));
    console.log('Saved mobile_showcase_390.png');

    // Check horizontal scroll overflow
    const overflowCheck = await sendCommand('Runtime.evaluate', {
      expression: 'document.documentElement.scrollWidth > document.documentElement.clientWidth',
      returnByValue: true
    });
    console.log('Mobile Horizontal Overflow:', overflowCheck.result.value);

    ws.close();
  } finally {
    chrome.kill();
  }
}

main().catch(err => {
  console.error('Error in capture_showcase:', err);
  process.exit(1);
});
