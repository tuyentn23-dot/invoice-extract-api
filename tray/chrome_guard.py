"""Auto-launch Chrome debug if not running. Called by tray before each check."""
import os
import subprocess
import time
import urllib.request
from pathlib import Path

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PROFILE = r'D:\TNT_AI\venture_foundry\rapidapi_extract\.chrome_debug'
CDP_URL = 'http://localhost:9222/json/version'


def is_cdp_alive(timeout=3):
    try:
        r = urllib.request.urlopen(CDP_URL, timeout=timeout)
        return r.status == 200
    except Exception:
        return False


def launch_chrome_debug():
    if not os.path.exists(CHROME):
        return False, 'chrome.exe not found'
    try:
        subprocess.Popen(
            [CHROME, '--remote-debugging-port=9222', f'--user-data-dir={PROFILE}',
             '--no-first-run', '--no-default-browser-check',
             'https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/analytics'],
            creationflags=0x08000000,  # CREATE_NO_WINDOW
            close_fds=True,
        )
        # wait up to 15s for CDP to come alive
        for _ in range(30):
            if is_cdp_alive(timeout=2):
                return True, 'launched'
            time.sleep(0.5)
        return False, 'timeout waiting CDP'
    except Exception as e:
        return False, str(e)


def ensure_chrome():
    """Return (ok, msg). Launch Chrome if needed."""
    if is_cdp_alive():
        return True, 'alive'
    return launch_chrome_debug()


if __name__ == '__main__':
    ok, msg = ensure_chrome()
    print(f'OK={ok} msg={msg}')
