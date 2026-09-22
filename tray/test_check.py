"""Test check_rapidapi without launching tray."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tray'))

from monitor_tray import check_rapidapi
r = check_rapidapi()
print('RESULT:', r)
