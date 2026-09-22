"""Internal metrics tracker. In-memory + periodic disk flush.
Tracks: per-endpoint calls, error counts, latency percentiles, per-subscriber usage.
"""
import json
import time
import threading
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'metrics'
DATA_DIR.mkdir(exist_ok=True)
SNAPSHOT = DATA_DIR / '_live_state.json'


class MetricsTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self.started_at = time.time()
        self.total_requests = 0
        self.total_errors = 0
        self.endpoint_counts: Dict[str, int] = defaultdict(int)
        self.endpoint_errors: Dict[str, int] = defaultdict(int)
        self.status_codes: Dict[str, int] = defaultdict(int)
        # latency ring buffer per endpoint (last 500 samples)
        self.latency_samples: Dict[str, deque] = defaultdict(lambda: deque(maxlen=500))
        # per-subscriber usage (X-RapidAPI-User header)
        self.subscriber_calls: Dict[str, int] = defaultdict(int)
        self.subscriber_last_seen: Dict[str, str] = {}
        # daily rollup
        self.daily: Dict[str, int] = defaultdict(int)
        self._load()
        self._start_flusher()

    def _key(self, path: str) -> str:
        """Normalize path so /v1/invoice/extract/base64 doesn't pollute /v1/invoice/extract."""
        return path.split('?', 1)[0]

    def record(self, path: str, method: str, status: int, latency_ms: float,
               subscriber: Optional[str] = None):
        k = f'{method} {self._key(path)}'
        now = datetime.utcnow().isoformat()
        with self._lock:
            self.total_requests += 1
            self.endpoint_counts[k] += 1
            self.status_codes[str(status)] += 1
            if status >= 400:
                self.total_errors += 1
                self.endpoint_errors[k] += 1
            self.latency_samples[k].append(round(latency_ms, 1))
            self.daily[datetime.utcnow().strftime('%Y-%m-%d')] += 1
            if subscriber:
                self.subscriber_calls[subscriber] += 1
                self.subscriber_last_seen[subscriber] = now

    @staticmethod
    def _percentile(samples, pct: float) -> Optional[float]:
        if not samples:
            return None
        s = sorted(samples)
        i = int(round((pct / 100.0) * (len(s) - 1)))
        return s[i]

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            uptime_s = int(time.time() - self.started_at)
            avg_latency = {}
            p95_latency = {}
            p99_latency = {}
            for k, buf in self.latency_samples.items():
                if buf:
                    vals = list(buf)
                    avg_latency[k] = round(sum(vals) / len(vals), 1)
                    p95_latency[k] = self._percentile(vals, 95)
                    p99_latency[k] = self._percentile(vals, 99)
            err_rate = (self.total_errors / self.total_requests * 100.0)
            return {
                'uptime_seconds': uptime_s,
                'uptime_human': self._human(uptime_s),
                'started_at': datetime.fromtimestamp(self.started_at).isoformat(),
                'total_requests': self.total_requests,
                'total_errors': self.total_errors,
                'error_rate_pct': round(err_rate, 2),
                'endpoint_counts': dict(self.endpoint_counts),
                'endpoint_errors': dict(self.endpoint_errors),
                'status_codes': dict(self.status_codes),
                'avg_latency_ms': avg_latency,
                'p95_latency_ms': p95_latency,
                'p99_latency_ms': p99_latency,
                'subscribers': dict(self.subscriber_calls),
                'subscriber_last_seen': dict(self.subscriber_last_seen),
                'unique_subscribers': len(self.subscriber_calls),
                'daily': dict(self.daily),
            }

    @staticmethod
    def _human(s: int) -> str:
        if s < 60:
            return f'{s}s'
        if s < 3600:
            return f'{s // 60}m {s % 60}s'
        if s < 86400:
            return f'{s // 3600}h {(s % 3600) // 60}m'
        return f'{s // 86400}d {(s % 86400) // 3600}h'

    def _save(self):
        try:
            snap = self.snapshot()
            SNAPSHOT.write_text(json.dumps(snap, indent=2), encoding='utf-8')
            # also daily file
            date = datetime.utcnow().strftime('%Y-%m-%d')
            (DATA_DIR / f'{date}.json').write_text(json.dumps(snap, indent=2), encoding='utf-8')
        except Exception:
            pass

    def _load(self):
        # intentionally do not load — metrics reset on restart, that's OK for MVP
        pass

    def _start_flusher(self):
        def loop():
            while True:
                time.sleep(60)
                self._save()
        t = threading.Thread(target=loop, daemon=True)
        t.start()


# Singleton
tracker = MetricsTracker()
