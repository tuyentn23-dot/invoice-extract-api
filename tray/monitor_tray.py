"""TNT RapidAPI Monitor - system tray app (v2).
- Runs in background (use pythonw.exe for no console)
- Checks RapidAPI analytics every N minutes
- Color-coded icon: green=new calls, yellow=idle, red=error
- Toast notifications on new traffic
- Auto-start via startup shortcut
"""
import os
import sys
import json
import time
import threading
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAY = ROOT / 'tray'
CONFIG = TRAY / 'config.json'
STATE = TRAY / 'state.json'
LOGS = TRAY / 'logs'
METRICS = ROOT / 'metrics'
for d in (LOGS, METRICS):
    d.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TRAY))

from chrome_guard import ensure_chrome


# ---------- Logging ----------
def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    try:
        print(line, flush=True)
    except Exception:
        pass
    try:
        with open(LOGS / f'{datetime.now().strftime("%Y-%m")}.log', 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        pass


# ---------- State ----------
def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {'last_check': None, 'last_calls': 0, 'total_checks': 0, 'consecutive_errors': 0}


def save_state(s):
    try:
        STATE.write_text(json.dumps(s, indent=2), encoding='utf-8')
    except Exception:
        pass


# ---------- Notification (Windows toast) ----------
def notify(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=10, app_name='TNT Monitor')
        return
    except Exception:
        pass
    try:
        # fallback: PowerShell balloon
        ps = (
            "[reflection.assembly]::loadwithpartialname('System.Windows.Forms')|Out-Null;"
            "[reflection.assembly]::loadwithpartialname('System.Drawing')|Out-Null;"
            "$n=New-Object System.Windows.Forms.NotifyIcon;"
            "$n.Icon=[System.Drawing.SystemIcons]::Information;"
            "$n.Visible=$true;"
            f"$n.ShowBalloonTip(10000,'{title}','{message}',[System.Windows.Forms.ToolTipIcon]::Info);"
            "Start-Sleep -Seconds 11;$n.Dispose()"
        )
        subprocess.Popen(['powershell', '-NoProfile', '-WindowStyle', 'Hidden', '-Command', ps],
                         creationflags=0x08000000)
    except Exception as e:
        log(f'notify failed: {e}')


# ---------- Analytics scrape ----------
def check_rapidapi():
    """Connect to Chrome CDP, scrape analytics. Returns dict or None."""
    # ensure Chrome debug is running
    ok, msg = ensure_chrome()
    if not ok:
        log(f'chrome guard: {msg}')
        return None
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
            import re
            m_calls = re.search(r'API Calls[^\d]*(\d[\d,]*)', txt)
            m_err = re.search(r'Error Rate[^\d]*(\d+(?:\.\d+)?)%', txt)
            m_lat = re.search(r'Latency[^\d]*(\d+(?:\.\d+)?)\s*ms', txt)
            calls = int(m_calls.group(1).replace(',', '')) if m_calls else 0
            err = float(m_err.group(1)) if m_err else 0.0
            lat = float(m_lat.group(1)) if m_lat else 0.0
            date = datetime.now().strftime('%Y-%m-%d')
            (METRICS / f'{date}.json').write_text(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'calls': calls, 'error_rate': err, 'latency_ms': lat,
            }, indent=2), encoding='utf-8')
            return {'calls': calls, 'error_rate': err, 'latency_ms': lat}
    except Exception as e:
        log(f'check failed: {type(e).__name__}: {str(e)[:150]}')
        return None


# ---------- Icon ----------
def load_icon(name):
    """Load colored icon by name: default | green | yellow | red."""
    from PIL import Image
    fname = 'icon.png' if name == 'default' else f'icon_{name}.png'
    p = TRAY / fname
    if not p.exists():
        # generate fallback
        colors = {'green': (34, 139, 34), 'red': (178, 34, 34), 'yellow': (218, 165, 32)}
        img = Image.new('RGB', (64, 64), color=colors.get(name, (25, 55, 130)))
        p.parent.mkdir(exist_ok=True)
        img.save(p)
    return Image.open(p)


# ---------- Main loop ----------
def monitor_loop(stop_event, icon_ref):
    interval_min = 60
    if CONFIG.exists():
        try:
            interval_min = int(json.loads(CONFIG.read_text(encoding='utf-8'))
                               .get('check_interval_minutes', 60))
        except Exception:
            pass
    log(f'monitor started, interval={interval_min} min')
    time.sleep(20)  # initial delay

    while not stop_event.is_set():
        state = load_state()
        result = check_rapidapi()
        icon = icon_ref[0]
        if result is None:
            state['consecutive_errors'] = state.get('consecutive_errors', 0) + 1
            if icon:
                try:
                    icon.icon = load_icon('red')
                    icon.title = 'TNT Monitor | error'
                except Exception:
                    pass
        else:
            state['consecutive_errors'] = 0
            state['total_checks'] = state.get('total_checks', 0) + 1
            state['last_check'] = datetime.now().isoformat()
            prev = state.get('last_calls', 0)
            delta = result['calls'] - prev
            icon_name = 'yellow'
            if prev == 0 and result['calls'] > 0:
                notify('First API call!',
                       f'Someone is using your API. Total: {result["calls"]}')
                icon_name = 'green'
            elif delta > 0:
                notify('New API calls',
                       f'+{delta} calls. Total: {result["calls"]}')
                icon_name = 'green'
            if icon:
                try:
                    icon.icon = load_icon(icon_name)
                    icon.title = f'TNT Monitor | calls: {result["calls"]} | last: {datetime.now().strftime("%H:%M")}'
                except Exception:
                    pass
            state['last_calls'] = result['calls']
            save_state(state)
        # wait interval
        for _ in range(interval_min * 60):
            if stop_event.is_set():
                return
            time.sleep(1)


# ---------- Tray ----------
def run_tray():
    import pystray
    from pystray import Menu, MenuItem

    stop_event = threading.Event()
    icon_ref = [None]

    def on_open_dashboard(icon, item):
        import webbrowser
        webbrowser.open('https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/analytics')

    def on_open_hub(icon, item):
        import webbrowser
        webbrowser.open('https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1')

    def on_check_now(icon, item):
        def _run():
            log('manual check')
            r = check_rapidapi()
            if r:
                notify('Manual check',
                       f'Calls: {r["calls"]} | Errors: {r["error_rate"]}% | Latency: {r["latency_ms"]}ms')
            else:
                notify('Check failed', 'Chrome CDP chưa mở hoặc chưa login RapidAPI. Xem log.')
        threading.Thread(target=_run, daemon=True).start()

    def on_open_logs(icon, item):
        os.startfile(str(LOGS))

    def on_open_metrics(icon, item):
        os.startfile(str(METRICS))

    def on_open_readme(icon, item):
        readme = TRAY / 'README.md'
        if readme.exists():
            os.startfile(str(readme))

    def on_quit(icon, item):
        log('quit requested')
        stop_event.set()
        icon.stop()

    menu = Menu(
        MenuItem('Check now', on_check_now, default=True),
        Menu.SEPARATOR,
        MenuItem('Open RapidAPI dashboard', on_open_dashboard),
        MenuItem('Open public API page', on_open_hub),
        Menu.SEPARATOR,
        MenuItem('Open logs', on_open_logs),
        MenuItem('Open metrics', on_open_metrics),
        MenuItem('Help / README', on_open_readme),
        Menu.SEPARATOR,
        MenuItem('Quit', on_quit),
    )

    icon = pystray.Icon('tnt-monitor', load_icon('default'), 'TNT Monitor', menu)
    icon_ref[0] = icon
    threading.Thread(target=monitor_loop, args=(stop_event, icon_ref), daemon=True).start()
    log('tray started')
    icon.run()


if __name__ == '__main__':
    run_tray()
