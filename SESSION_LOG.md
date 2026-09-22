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
