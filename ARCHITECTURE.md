# Architecture — Invoice to JSON Extractor v2.1

## Sơ đồ tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  RapidAPI Hub                                                │
│  rapidapi.com/tuyentn23/api/invoice-to-json-extractor1      │
│                                                              │
│  Buyer → Subscribe → RapidAPI proxy → backend               │
│                    ↓                                         │
│                  Billing (Free/$9/$29/$99)                   │
│                    ↓                                         │
│                  PayPal payout (tuyentn23@gmail.com)        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (Render free tier)                                 │
│  invoice-extract-api-4eq9.onrender.com                      │
│                                                              │
│  FastAPI v2.1                                                │
│  ├─ Middleware:                                             │
│  │   ├─ metrics_middleware  → record every request          │
│  │   └─ check_rapidapi_secret → verify proxy secret         │
│  │                                                           │
│  ├─ Extractors (16 endpoints, 10 doc types):                │
│  │   ├─ invoice    → heuristic + LLM fallback               │
│  │   ├─ receipt    → heuristic                              │
│  │   ├─ resume     → heuristic                              │
│  │   ├─ bank_stmt  → heuristic                              │
│  │   ├─ PO         → heuristic                              │
│  │   ├─ contract   → heuristic                              │
│  │   ├─ card       → heuristic                              │
│  │   ├─ utility    → heuristic                              │
│  │   ├─ delivery   → heuristic                              │
│  │   └─ ID         → heuristic (MRZ parse)                  │
│  │                                                           │
│  ├─ Metrics tracker (in-memory):                            │
│  │   ├─ endpoint_counts   {path: n}                         │
│  │   ├─ subscriber_calls  {X-RapidAPI-User: n}              │
│  │   ├─ latency p95/p99   per endpoint                      │
│  │   ├─ error_rate        total                             │
│  │   └─ daily rollup                                        │
│  │                                                           │
│  └─ Endpoints:                                              │
│      ├─ /health   → quick status + counts                   │
│      ├─ /metrics  → full snapshot (admin token optional)    │
│      └─ /v1/*     → extractors                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼ (poll every 15 min)
┌─────────────────────────────────────────────────────────────┐
│  Tray Monitor (Windows, user's machine)                     │
│  tray/monitor_tray.py                                       │
│                                                              │
│  ├─ fetch_metrics() → GET /metrics                          │
│  ├─ Compare with previous state                             │
│  ├─ If delta > 0 → toast notification                       │
│  ├─ If new subscriber → toast notification                  │
│  └─ Update icon color: 🟡 idle / 🟢 traffic / 🔴 error      │
│                                                              │
│  Chạy ẩn qua pythonw.exe, auto-start on Windows boot        │
└─────────────────────────────────────────────────────────────┘
```

## Data flow khi có request

```
1. Buyer gọi qua RapidAPI proxy
   POST https://invoice-to-json-extractor1.p.rapidapi.com/v1/invoice/extract
   Headers: X-RapidAPI-Key, X-RapidAPI-User

2. RapidAPI forward tới backend (nếu subscriber hợp lệ):
   POST https://invoice-extract-api-4eq9.onrender.com/v1/invoice/extract
   Headers: X-RapidAPI-Proxy-Secret, X-RapidAPI-User

3. FastAPI middleware:
   - check_rapidapi_secret: verify proxy secret
   - metrics_middleware: start timer

4. Handler:
   - Parse body
   - _prepare_content (text or base64→PDF/OCR)
   - extract_invoice(text, lang)
     → heuristic regex
     → [optional] LLM fallback
   - Validate schema
   - Return JSON

5. metrics_middleware:
   - Record: endpoint, status, latency, subscriber

6. Response → RapidAPI → Buyer
```

## Data flow khi tray check

```
1. Every 15 min:
   Tray → GET /metrics (timeout 45s)

2. Backend returns in-memory snapshot:
   {
     total_requests, total_errors, error_rate_pct,
     endpoint_counts, subscribers, p95_latency_ms, ...
   }

3. Tray compare với state.json:
   - new_calls = total - last_total
   - new_subs = unique_subscribers - last_subscribers

4. Nếu delta > 0:
   - Toast notification
   - Icon → green

5. Lưu state.json + metrics/YYYY-MM-DD.json
```

## Tại sao kiến trúc này tốt

1. **Metrics trong API, không phải service riêng.** Zero overhead, zero chi phí.
2. **Tray đọc endpoint nội bộ, không scrape RapidAPI.** Nhanh (<1s), không phụ thuộc Chrome CDP.
3. **In-memory metrics.** Không cần database, reset khi restart (chấp nhận được cho MVP).
4. **Per-subscriber tracking.** RapidAPI tự gửi `X-RapidAPI-User` header — ta chỉ cần đọc.
5. **Fail-safe.** Nếu /metrics fail → tray chuyển đỏ, không crash.
6. **Bảo mật.** /metrics có thể bật `ADMIN_TOKEN` để chặn truy cập công khai.

## Giới hạn đã biết

- **Metrics reset khi Render restart.** Render free tier restart mỗi khi deploy hoặc sau 15 phút sleep. Metrics in-memory sẽ mất. Giải pháp: dùng persistent volume (không có trên free tier) hoặc chấp nhận.
- **Per-subscriber chỉ lưu tổng số call**, không lưu chi tiết từng request. Đủ cho MVP.
- **Không có alerting tự động** khi error rate cao. Có thể thêm sau.

## Bảo mật

- `RAPIDAPI_PROXY_SECRET` — chặn bypass RapidAPI (chưa set, xem SECURITY_TODO.md)
- `ADMIN_TOKEN` — bảo vệ /metrics nếu cần (chưa set, tùy chọn)
- Không có API key nào trong repo
