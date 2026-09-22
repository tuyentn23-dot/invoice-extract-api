# HANDOFF — Invoice to JSON Extractor

> **Đọc file này đầu tiên khi bắt đầu phiên mới.**

## Trạng thái ngắn gọn

**Dự án đã LIVE.** Không còn việc kỹ thuật. Đang chờ traffic đầu tiên.

## Việc cần làm ngay khi bắt đầu phiên mới

1. **Hỏi user:** "Từ phiên trước, có gì thay đổi không? Có traffic mới, subscriber, hay lỗi gì?"
2. **Chạy:** `D:/TNT_AI/venv/Scripts/python.exe scripts/monitor.py`
3. **Xem:** `metrics/report_<ngày mới nhất>.json`
4. **Kiểm tra tray:** `Get-CimInstance Win32_Process -Filter "name='pythonw.exe'" | Where-Object {$_.CommandLine -like '*monitor_tray*'}`

Nếu tray chưa chạy → khởi động lại: `tray\start_monitor.bat`


## Metrics tích hợp trong backend (v2.1)

Endpoint: `GET https://invoice-extract-api-4eq9.onrender.com/metrics`

Trả về:
- `total_requests`, `total_errors`, `error_rate_pct`
- `endpoint_counts`: đếm theo từng path
- `subscribers`: đếm theo `X-RapidAPI-User` header (RapidAPI tự gửi)
- `unique_subscribers`: số subscriber khác nhau
- `avg_latency_ms`, `p95_latency_ms`, `p99_latency_ms`
- `daily`: rollup theo ngày
- `uptime_human`

Ẩn khỏi OpenAPI public spec (buyer không thấy).

Tùy chọn bảo vệ bằng env `ADMIN_TOKEN` trên Render.

**Giới hạn:** in-memory, reset khi Render restart (deploy hoặc sau 15 min sleep). Chấp nhận cho MVP.

## URLs

- Public API: https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
- Backend: https://invoice-extract-api-4eq9.onrender.com
- Repo: https://github.com/tuyentn23-dot/invoice-extract-api

## Những gì ĐÃ LÀM (không cần làm lại)

### Build
- ✅ 16 endpoints, 10 loại document
- ✅ Heuristic regex + LLM fallback
- ✅ Bilingual EN/VI
- ✅ PDF/OCR support
- ✅ 29 unit tests pass

### Deploy
- ✅ Render free tier, backend v2.0.0
- ✅ RapidAPI public, 4 pricing tiers
- ✅ PayPal linked & Ready
- ✅ Playground test 200 OK

### Automation
- ✅ Tray monitor (pystray, color icons, toast notif)
- ✅ chrome_guard (auto-launch Chrome debug)
- ✅ Auto-start Windows

## Những gì ĐÃ THỬ VÀ THẤT BẠI (đừng lặp lại)

### Reddit — account bị flag
- r/SaaS, r/webdev: AutoMod remove (account <3 tháng)
- r/documentAutomation: Reddit **site-wide filter** remove
- Account `TNT23HK` giờ bị spam filter toàn cục
- **Không post link từ account này nữa.** Cần 3 tháng + karma.

### Hacker News — account mới không post được
- Account `tuyentn23` có 1 karma
- HN chặn Show HN từ account mới
- **Cần build karma 1-2 tuần trước.**

## QUY TẮC BẮT BUỘC

1. ❌ **KHÔNG post Reddit/HN** với account hiện tại
2. ❌ **KHÔNG thêm API mới** cho tới khi có ≥1 paid subscriber
3. ❌ **KHÔNG sửa pricing** khi chưa có traffic thật
4. ❌ **KHÔNG automation social submit** — risk ban
5. ✅ **Đo trước, build sau** — traffic là tín hiệu duy nhất

## Ngưỡng quyết định

| Mốc | Đo | Hành động |
|---|---|---|
| D+7 | RapidAPI test calls ≥5 | tiếp tục, chờ |
| D+14 | Subscribers ≥1 | build thêm API cùng hạ tầng |
| D+30 | MRR >$0 | tăng tốc build |
| D+30 | MRR =$0 | đổi kênh (dev.to, Indie Hackers) |
| D+90 | MRR <$100 | pivot nền tảng (Replicate/HF) |

## Cấu trúc repo

```
rapidapi_extract/
├── app/          # FastAPI code (16 endpoints)
├── tests/        # 29 unit tests
├── tray/         # System tray monitor
├── metrics/      # Auto-generated reports
├── scripts/      # Playwright automation (gitignored)
├── MANIFEST.md   # File này mô tả toàn bộ
├── STATE.json    # Machine-readable state
├── HANDOFF.md    # File này
├── HANDOFF_PROMPT.md (ở ../Clawhub/) — Prompt đầy đủ
├── STATUS.md     # Trạng thái cho human đọc
├── START_HERE.md # Entry point
├── LAUNCH_LOG.md # Kết quả launch thật
└── DEPLOYED_URLS.txt
```

## Chi phí & doanh thu

- Chi phí: **$0**
- Doanh thu: **$0** (chưa có subscriber)

## Khi có traffic đầu tiên

1. Chạy `python scripts/monitor.py` để log
2. Chụp ảnh dashboard
3. Báo user
4. Cân nhắc build thêm 5 API nữa cùng hạ tầng để tăng surface

## Khi có bug

1. Đọc log: `tray/logs/YYYY-MM.log`
2. Kiểm tra Render dashboard
3. Fix code → push GitHub → Render auto-deploy 2 phút

## Khi hết 30 ngày không traffic

1. Thử **dev.to** — account mới OK, không có rule khắt khe
2. Thử **Indie Hackers** — account mới OK
3. Thử **Hashnode** — account mới OK

Kênh Reddit/HN cần chờ 2-3 tháng. Trong lúc chờ, giữ tray chạy.
