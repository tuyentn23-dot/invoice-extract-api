"""TNT Monitor — system tray app (v4).
- Polls API /metrics + /health
- Full menu: health, endpoints, test, subscribers, logs
- Color icon: yellow=idle, green=traffic, red=error
"""
import os
import sys
import json
import time
import threading
import subprocess
import urllib.request
import urllib.error
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
RAPIDAPI_URL = 'https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1'


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
    return {'check_interval_minutes': 15, 'admin_token': ''}


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


# ---------- API calls ----------
def _get(path, timeout=45):
    cfg = load_config()
    url = f'{API_BASE}{path}'
    req = urllib.request.Request(url)
    token = cfg.get('admin_token', '').strip()
    if token and path == '/metrics':
        req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        log(f'{path} HTTP {e.code}')
        return {'_error': f'HTTP {e.code}'}
    except Exception as e:
        log(f'{path} err: {type(e).__name__}: {str(e)[:120]}')
        return {'_error': f'{type(e).__name__}: {str(e)[:120]}'}


def fetch_metrics():
    return _get('/metrics')


def fetch_health():
    return _get('/health', timeout=30)


def fetch_root():
    return _get('/', timeout=30)


def post_extract(path, body, timeout=45):
    url = f'{API_BASE}{path}'
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'_error': f'HTTP {e.code}', '_body': e.read().decode('utf-8', errors='ignore')[:300]}
    except Exception as e:
        return {'_error': f'{type(e).__name__}: {str(e)[:120]}'}


def save_metrics_file(m):
    try:
        date = datetime.utcnow().strftime('%Y-%m-%d')
        (METRICS_DIR / f'{date}.json').write_text(json.dumps(m, indent=2), encoding='utf-8')
    except Exception as e:
        log(f'save failed: {e}')


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
        m = fetch_metrics()
        icon = icon_ref[0]
        if not m or '_error' in m:
            state['consecutive_errors'] = state.get('consecutive_errors', 0) + 1
            if icon:
                try:
                    icon.icon = load_icon('red')
                    icon.title = f'TNT | ERROR {(m or {}).get("_error", "unknown")}'
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


# ---------- Menu handlers ----------
def menu_check_now(icon, item):
    def _run():
        log('manual check')
        m = fetch_metrics()
        if not m or '_error' in m:
            notify('Check failed', f'{(m or {}).get("_error", "unknown")}')
            return
        notify('Check complete',
               f'Calls: {m["total_requests"]} | Errors: {m["error_rate_pct"]}% | Subs: {m["unique_subscribers"]}')
    threading.Thread(target=_run, daemon=True).start()


def menu_health(icon, item):
    def _run():
        h = fetch_health()
        if '_error' in h:
            notify('Health', f'DOWN: {h["_error"]}')
        else:
            notify('Health OK',
                   f'v{h.get("version")} | uptime {h.get("uptime_human")} | calls {h.get("total_requests")} | subs {h.get("unique_subscribers")}')
    threading.Thread(target=_run, daemon=True).start()


def menu_subscribers(icon, item):
    def _run():
        m = fetch_metrics()
        if '_error' in m:
            notify('Subscribers', 'Metrics unavailable')
            return
        subs = m.get('subscribers', {})
        if not subs:
            notify('Subscribers', 'No subscribers yet')
            return
        lines = [f'{k}: {v} calls' for k, v in list(subs.items())[:8]]
        notify(f'{len(subs)} subscribers', '\n'.join(lines))
    threading.Thread(target=_run, daemon=True).start()


def menu_test_invoice(icon, item):
    def _run():
        sample = ('Invoice #: TRAY-TEST\nDate: 2026-09-22\nVendor: TNT Monitor\n'
                  'Subtotal: 100.00\nVAT 20%: 20.00\nTotal: 120.00 USD')
        r = post_extract('/v1/invoice/extract', {'content': sample})
        if '_error' in r:
            notify('Test failed', r['_error'])
        else:
            inv = r.get('invoice', {})
            notify('Test OK', f'Number: {inv.get("invoice_number")} | Total: {inv.get("total")} {inv.get("currency")}')
    threading.Thread(target=_run, daemon=True).start()


def menu_endpoints(icon, item):
    def _run():
        r = fetch_root()
        eps = r.get('endpoints', {}) if isinstance(r, dict) else {}
        if not eps:
            notify('Endpoints', 'Could not load')
            return
        # count by type
        extract_eps = [k for k in eps if k.startswith('POST /v1/')]
        notify(f'{len(extract_eps)} extraction endpoints',
               f'Invoices, receipts, resumes, bank statements, PO, contracts, cards, utilities, notes, IDs')
    threading.Thread(target=_run, daemon=True).start()


def menu_open_metrics_json(icon, item):
    import webbrowser
    webbrowser.open(f'{API_BASE}/metrics')


def menu_open_health(icon, item):
    import webbrowser
    webbrowser.open(f'{API_BASE}/health')


def menu_open_docs(icon, item):
    import webbrowser
    webbrowser.open(f'{API_BASE}/docs')


def menu_open_hub(icon, item):
    import webbrowser
    webbrowser.open(RAPIDAPI_URL)


def menu_open_dashboard(icon, item):
    import webbrowser
    webbrowser.open('https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/analytics')


def menu_open_logs(icon, item): os.startfile(str(LOGS))


def menu_open_metrics_dir(icon, item): os.startfile(str(METRICS_DIR))


def menu_open_readme(icon, item):
    p = TRAY / 'README.md'
    if p.exists(): os.startfile(str(p))


def run_tray():
    import pystray
    from pystray import Menu, MenuItem
    stop_event = threading.Event()
    icon_ref = [None]

    def quit_(icon, item):
        log('quit requested'); stop_event.set(); icon.stop()

    # submenu: Endpoints
    endpoints_menu = Menu(
        MenuItem('List extractors', menu_endpoints),
        MenuItem('Test invoice (sample)', menu_test_invoice),
        Menu.SEPARATOR,
        MenuItem('Open /docs', menu_open_docs),
        MenuItem('Open /health', menu_open_health),
        MenuItem('Open /metrics', menu_open_metrics_json),
    )

    # submenu: Data
    data_menu = Menu(
        MenuItem('View subscribers', menu_subscribers),
        MenuItem('Open metrics folder', menu_open_metrics_dir),
        MenuItem('Open logs folder', menu_open_logs),
    )

    # submenu: Links
    links_menu = Menu(
        MenuItem('RapidAPI Hub page', menu_open_hub),
        MenuItem('RapidAPI dashboard', menu_open_dashboard),
        MenuItem('OpenAPI docs (/docs)', menu_open_docs),
    )

    menu = Menu(
        MenuItem('Check now', menu_check_now, default=True),
        MenuItem('Health', menu_health),
        Menu.SEPARATOR,
        MenuItem('Endpoints ▸', endpoints_menu),
        MenuItem('Data ▸', data_menu),
        MenuItem('Links ▸', links_menu),
        Menu.SEPARATOR,
        MenuItem('Help', menu_open_readme),
        MenuItem('Quit', quit_),
    )

    icon = pystray.Icon('tnt-monitor', load_icon('default'), 'TNT Monitor', menu)
    icon_ref[0] = icon
    threading.Thread(target=monitor_loop, args=(stop_event, icon_ref), daemon=True).start()
    log('tray v4 started')
    icon.run()


if __name__ == '__main__':
    run_tray()
