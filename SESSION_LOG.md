# Session Log

## 2026-09-22 — Launch day

### Đã làm

**Build (v1 → v2):**
- v1.0: Invoice extraction API (FastAPI + heuristic + LLM fallback)
- v1.1: Thêm receipt + resume extractors
- v1.2: Thêm bank statement extractor
- v1.3: PDF/OCR support + test suite (29 checks)
- **v2.0: Thêm 5 extractors (purchase order, contract, business card, utility bill, delivery note) + ID document with MRZ — 16 endpoints total**

**Deploy:**
- Render free tier, health check OK
- OpenAPI 3.0.3 compat (fix từ 3.1 để RapidAPI nhận)

**RapidAPI:**
- Upload spec thành công (16 endpoints)
- Base URL configured
- API public
- 4 pricing tiers: BASIC Free / PRO $9 / ULTRA $29 / MEGA $99
- PayPal linked: tuyentn23@gmail.com — Ready
- Playground test: 200 OK

**Tray Monitor:**
- pystray app chạy nền, không console
- Auto-check RapidAPI analytics mỗi 60 phút
- Color icons: 🟡 idle, 🟢 có call, 🔴 lỗi
- Toast notifications
- Auto-launch Chrome debug (chrome_guard)
- Auto-start Windows

**Launch attempts (thất bại):**
- Reddit r/SaaS: AutoMod removed (account <3 tháng)
- Reddit r/webdev: AutoMod removed (account <3 tháng)
- Reddit r/documentAutomation: site-wide filter removed
- Hacker News: block Show HN (account 1 karma)

### Bài học

- Account social mới không thể launch sản phẩm. Cần build history trước.
- RapidAPI Hub organic search là kênh duy nhất không có rule.
- Tăng surface = thêm endpoints vào cùng API (16 endpoints > 6 endpoints ở 6 API riêng).

### Files quan trọng

- `STATE.json` — trạng thái máy đọc
- `HANDOFF_PROMPT.md` (ở venture_foundry/Clawhub/) — entry point phiên sau
- `LAUNCH_LOG.md` — kết quả launch thật
- `DEPLOYED_URLS.txt` — tất cả URLs

### Chi phí

$0

### Doanh thu

$0 (chưa có subscriber)

### Chờ đợi

Traffic từ RapidAPI organic search.


## 2026-09-22 (chiều) — Tích hợp metrics vào API

### Quyết định
Bỏ tray scrape RapidAPI, tích hợp metrics **trong chính backend API**. Tray v3 chỉ gọi `/metrics`.

### Đã làm

**Backend v2.1:**
- Module `app/metrics.py` — MetricsTracker singleton
- Middleware `metrics_middleware` ghi mọi request
- Endpoint `GET /metrics` trả về snapshot đầy đủ:
  - per-endpoint counts (POST /v1/invoice/extract: N)
  - per-subscriber calls (từ `X-RapidAPI-User`)
  - latency avg/p95/p99
  - error rate, status codes
  - daily rollup
  - uptime
- `/health` trả về summary (calls + subscribers)
- Admin token optional qua env `ADMIN_TOKEN`
- Metrics tự flush ra `metrics/YYYY-MM-DD.json` mỗi 60s
- Ẩn `/metrics` khỏi OpenAPI spec (không cho buyer thấy)

**Tray v3:**
- Bỏ Playwright, bỏ Chrome CDP
- Chỉ cần `urllib.request` gọi `/metrics`
- Interval giảm xuống 15 phút (trước 60)
- Cảnh báo khi có subscriber mới (không chỉ call mới)
- Xóa `chrome_guard.py` (không cần nữa)

### Bug đã fix
- ZeroDivisionError khi `total_requests=0` (lần check đầu tiên)

### Lợi ích
- Nhanh hơn: <1s vs 8-10s (scrape)
- Ổn định hơn: không phụ thuộc Chrome CDP
- Chính xác hơn: đếm từ chính API
- Per-subscriber tracking (RapidAPI tự gửi header)
- Zero chi phí thêm

### Giới hạn
- Metrics in-memory, reset khi Render restart
- Chấp nhận cho MVP

