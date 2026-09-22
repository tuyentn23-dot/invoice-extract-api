"""TNT RapidAPI Monitor - system tray app.
Runs in background, checks RapidAPI analytics daily, notifies on new activity.
Right-click tray icon for menu. No console window (use pythonw.exe).
"""
import os
import sys
import json
import time
import threading
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'tray' / 'config.json'
STATE = ROOT / 'tray' / 'state.json'
METRICS = ROOT / 'metrics'
LOGS = ROOT / 'tray' / 'logs'
METRICS.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

# Add ROOT to path for playwright
sys.path.insert(0, str(ROOT))


def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    try:
        with open(LOGS / f'{datetime.now().strftime("%Y-%m")}.log', 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        pass


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {'last_check': None, 'last_calls': 0, 'last_subscribers': 0, 'last_mrr': 0, 'total_checks': 0}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=2), encoding='utf-8')


def notify(title, message):
    """Try Windows toast via pystray icon, fallback to PowerShell balloon."""
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=10)
        return
    except Exception:
        pass
    try:
        import subprocess
        ps = f'''
[reflection.assembly]::loadwithpartialname('System.Windows.Forms') | Out-Null
[reflection.assembly]::loadwithpartialname('System.Drawing') | Out-Null
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.Visible = $true
$notify.ShowBalloonTip(10000, '{title}', '{message}', [System.Windows.Forms.ToolTipIcon]::Info)
Start-Sleep -Seconds 11
$notify.Dispose()
'''
        subprocess.Popen(['powershell', '-NoProfile', '-WindowStyle', 'Hidden', '-Command', ps],
                         creationflags=0x08000000)
    except Exception as e:
        log(f'notify failed: {e}')


def check_rapidapi():
    """Connect to Chrome via CDP, scrape analytics page."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log('playwright not installed')
        return None
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=15000)
            ctx = browser.contexts[0]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto('https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/analytics',
                      wait_until='domcontentloaded', timeout=45000)
            time.sleep(5)
            txt = page.locator('body').inner_text()
            # parse total calls / errors / latency from analytics UI
            import re
            m_calls = re.search(r'API Calls[^\d]*(\d[\d,]*)', txt)
            m_err = re.search(r'Error Rate[^\d]*(\d+(?:\.\d+)?)%', txt)
            m_lat = re.search(r'Latency[^\d]*(\d+(?:\.\d+)?)\s*ms', txt)
            calls = int(m_calls.group(1).replace(',', '')) if m_calls else 0
            err = float(m_err.group(1)) if m_err else 0.0
            lat = float(m_lat.group(1)) if m_lat else 0.0
            # write daily report
            date = datetime.now().strftime('%Y-%m-%d')
            (METRICS / f'{date}.json').write_text(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'calls': calls, 'error_rate': err, 'latency_ms': lat,
            }, indent=2), encoding='utf-8')
            return {'calls': calls, 'error_rate': err, 'latency_ms': lat}
    except Exception as e:
        log(f'check failed: {type(e).__name__}: {str(e)[:120]}')
        return None


def monitor_loop(stop_event, icon_ref):
    """Main loop: check every N minutes."""
    interval_min = 60
    if CONFIG.exists():
        try:
            cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
            interval_min = int(cfg.get('check_interval_minutes', 60))
        except Exception:
            pass
    log(f'monitor started, interval = {interval_min} min')
    # initial delay 30s
    for _ in range(30):
        if stop_event.is_set():
            return
        time.sleep(1)
    while not stop_event.is_set():
        state = load_state()
        result = check_rapidapi()
        if result:
            state['total_checks'] = state.get('total_checks', 0) + 1
            state['last_check'] = datetime.now().isoformat()
            new_calls = result['calls'] - state.get('last_calls', 0)
            if new_calls > 0 and state.get('last_calls', 0) > 0:
                notify('New API calls', f'+{new_calls} calls since last check. Total: {result["calls"]}')
            elif result['calls'] > 0 and state.get('last_calls', 0) == 0:
                notify('First API call!', f'Someone is using your API. Total: {result["calls"]}')
            state['last_calls'] = result['calls']
            save_state(state)
            try:
                if icon_ref[0]:
                    icon_ref[0].title = f'TNT Monitor | calls: {result["calls"]}'
            except Exception:
                pass
        for _ in range(interval_min * 60):
            if stop_event.is_set():
                return
            time.sleep(1)


def make_icon():
    """Load or generate tray icon."""
    from PIL import Image, ImageDraw
    icon_path = ROOT / 'tray' / 'icon.png'
    if icon_path.exists():
        return Image.open(icon_path)
    # generate simple 64x64 icon: 'TNT' text on dark blue
    img = Image.new('RGB', (64, 64), color=(25, 55, 130))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, 59, 59], outline=(255, 255, 255), width=2)
    try:
        d.text((10, 22), 'TNT', fill=(255, 255, 255))
    except Exception:
        pass
    img.save(icon_path)
    return img


def run_tray():
    import pystray
    from pystray import Menu, MenuItem

    stop_event = threading.Event()
    icon_ref = [None]
    img = make_icon()

    def on_open_dashboard(icon, item):
        import webbrowser
        webbrowser.open('https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/analytics')

    def on_open_hub(icon, item):
        import webbrowser
        webbrowser.open('https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1')

    def on_check_now(icon, item):
        def _check():
            log('manual check triggered')
            r = check_rapidapi()
            if r:
                notify('Manual check', f'Calls: {r["calls"]} | Errors: {r["error_rate"]}% | Latency: {r["latency_ms"]}ms')
            else:
                notify('Check failed', 'See tray logs for details.')
        threading.Thread(target=_check, daemon=True).start()

    def on_open_logs(icon, item):
        os.startfile(str(LOGS))

    def on_open_metrics(icon, item):
        os.startfile(str(METRICS))

    def on_quit(icon, item):
        log('quit requested')
        stop_event.set()
        icon.stop()

    menu = Menu(
        MenuItem('Check now', on_check_now, default=True),
        MenuItem('Open RapidAPI dashboard', on_open_dashboard),
        MenuItem('Open public API page', on_open_hub),
        Menu.SEPARATOR,
        MenuItem('Open logs folder', on_open_logs),
        MenuItem('Open metrics folder', on_open_metrics),
        Menu.SEPARATOR,
        MenuItem('Quit', on_quit),
    )

    icon = pystray.Icon('tnt-monitor', img, 'TNT Monitor', menu)
    icon_ref[0] = icon
    t = threading.Thread(target=monitor_loop, args=(stop_event, icon_ref), daemon=True)
    t.start()
    log('tray started')
    icon.run()


if __name__ == '__main__':
    run_tray()
