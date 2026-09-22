"""TNT Monitor - system tray app (v3).
Polls the API's own /metrics endpoint (not RapidAPI scrape).
Color icon: yellow=idle, green=traffic, red=error.
"""
import os
import sys
import json
import time
import threading
import subprocess
import urllib.request
import base64
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAY = ROOT / 'tray'
CONFIG = TRAY / 'config.json'
STATE = TRAY / 'state.json'
LOGS = TRAY / 'logs'
METRICS_DIR = ROOT / 'metrics'
for d in (LOGS, METRICS_DIR):
    d.mkdir(exist_ok=True)

API_BASE = 'https://invoice-extract-api-4eq9.onrender.com'


def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    try: print(line, flush=True)
    except Exception: pass
    try:
        with open(LOGS / f'{datetime.now().strftime("%Y-%m")}.log', 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception: pass


def load_config():
    if CONFIG.exists():
        try: return json.loads(CONFIG.read_text(encoding='utf-8'))
        except Exception: pass
    return {'check_interval_minutes': 15, 'notify_on_new_calls': True, 'admin_token': ''}


def load_state():
    if STATE.exists():
        try: return json.loads(STATE.read_text(encoding='utf-8'))
        except Exception: pass
    return {'last_check': None, 'last_total_requests': 0, 'last_subscribers': 0, 'consecutive_errors': 0, 'total_checks': 0}


def save_state(s):
    try: STATE.write_text(json.dumps(s, indent=2), encoding='utf-8')
    except Exception: pass


def notify(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=10, app_name='TNT Monitor')
        return
    except Exception: pass
    try:
        ps = (
            "[reflection.assembly]::loadwithpartialname('System.Windows.Forms')|Out-Null;"
            "[reflection.assembly]::loadwithpartialname('System.Drawing')|Out-Null;"
            "$n=New-Object System.Windows.Forms.NotifyIcon;"
            "$n.Icon=[System.Drawing.SystemIcons]::Information;$n.Visible=$true;"
            f"$n.ShowBalloonTip(10000,'{title}','{message}',[System.Windows.Forms.ToolTipIcon]::Info);"
            "Start-Sleep -Seconds 11;$n.Dispose()"
        )
        subprocess.Popen(['powershell','-NoProfile','-WindowStyle','Hidden','-Command',ps],
                         creationflags=0x08000000)
    except Exception as e:
        log(f'notify failed: {e}')


def fetch_metrics(cfg):
    """Call /metrics on backend. Returns dict or None."""
    token = cfg.get('admin_token', '').strip()
    url = f'{API_BASE}/metrics'
    req = urllib.request.Request(url)
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        log(f'metrics HTTP {e.code}')
        return None
    except Exception as e:
        log(f'metrics err: {type(e).__name__}: {str(e)[:120]}')
        return None


def save_metrics_file(m):
    try:
        date = datetime.utcnow().strftime('%Y-%m-%d')
        out = METRICS_DIR / f'{date}.json'
        out.write_text(json.dumps(m, indent=2), encoding='utf-8')
    except Exception as e:
        log(f'save_metrics failed: {e}')


def load_icon(name):
    from PIL import Image
    fname = 'icon.png' if name == 'default' else f'icon_{name}.png'
    p = TRAY / fname
    if not p.exists():
        colors = {'green': (34, 139, 34), 'red': (178, 34, 34), 'yellow': (218, 165, 32)}
        img = Image.new('RGB', (64, 64), color=colors.get(name, (25, 55, 130)))
        img.save(p)
    return Image.open(p)


def monitor_loop(stop_event, icon_ref):
    cfg = load_config()
    interval_min = max(1, int(cfg.get('check_interval_minutes', 15)))
    log(f'monitor started, interval={interval_min} min')
    time.sleep(10)
    while not stop_event.is_set():
        state = load_state()
        m = fetch_metrics(cfg)
        icon = icon_ref[0]
        if m is None:
            state['consecutive_errors'] = state.get('consecutive_errors', 0) + 1
            if icon:
                try:
                    icon.icon = load_icon('red')
                    icon.title = 'TNT Monitor | error'
                except Exception: pass
        else:
            state['consecutive_errors'] = 0
            state['total_checks'] = state.get('total_checks', 0) + 1
            state['last_check'] = datetime.now().isoformat()
            total = int(m.get('total_requests', 0))
            subs = int(m.get('unique_subscribers', 0))
            prev_total = state.get('last_total_requests', 0)
            prev_subs = state.get('last_subscribers', 0)
            delta = total - prev_total
            icon_name = 'yellow'
            if prev_total == 0 and total > 0:
                notify('First API request!', f'Total: {total} | Subscribers: {subs}')
                icon_name = 'green'
            elif delta > 0:
                notify(f'+{delta} API calls', f'Total: {total} | Subscribers: {subs}')
                icon_name = 'green'
            if subs > prev_subs:
                notify('New subscriber!', f'Total subscribers: {subs}')
                icon_name = 'green'
            state['last_total_requests'] = total
            state['last_subscribers'] = subs
            save_metrics_file(m)
            save_state(state)
            if icon:
                try:
                    icon.icon = load_icon(icon_name)
                    icon.title = f'TNT | calls: {total} | subs: {subs}'
                except Exception: pass
        for _ in range(interval_min * 60):
            if stop_event.is_set(): return
            time.sleep(1)


def run_tray():
    import pystray
    from pystray import Menu, MenuItem
    stop_event = threading.Event()
    icon_ref = [None]

    def open_dashboard(icon, item):
        import webbrowser
        webbrowser.open(f'{API_BASE}/metrics')
    def open_hub(icon, item):
        import webbrowser
        webbrowser.open('https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1')
    def check_now(icon, item):
        def _run():
            log('manual check')
            m = fetch_metrics(load_config())
            if m:
                notify('Manual check',
                       f'Calls: {m["total_requests"]} | Errors: {m["error_rate_pct"]}% | Subs: {m["unique_subscribers"]}')
            else:
                notify('Check failed', 'See logs.')
        threading.Thread(target=_run, daemon=True).start()
    def open_logs(icon, item): os.startfile(str(LOGS))
    def open_metrics(icon, item): os.startfile(str(METRICS_DIR))
    def open_readme(icon, item):
        p = TRAY / 'README.md'
        if p.exists(): os.startfile(str(p))
    def quit_(icon, item):
        log('quit requested'); stop_event.set(); icon.stop()

    menu = Menu(
        MenuItem('Check now', check_now, default=True),
        Menu.SEPARATOR,
        MenuItem('Open /metrics', open_dashboard),
        MenuItem('Open RapidAPI Hub', open_hub),
        Menu.SEPARATOR,
        MenuItem('Open logs', open_logs),
        MenuItem('Open metrics', open_metrics),
        MenuItem('Help', open_readme),
        Menu.SEPARATOR,
        MenuItem('Quit', quit_),
    )
    icon = pystray.Icon('tnt-monitor', load_icon('default'), 'TNT Monitor', menu)
    icon_ref[0] = icon
    threading.Thread(target=monitor_loop, args=(stop_event, icon_ref), daemon=True).start()
    log('tray v3 started (metrics endpoint)')
    icon.run()


if __name__ == '__main__':
    run_tray()
