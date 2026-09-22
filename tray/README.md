# TNT Monitor — system tray app (v3)

Tự động giám sát API metrics, báo toast khi có traffic. Chạy nền, không console.

**Khác biệt v3:** Không scrape RapidAPI nữa — gọi trực tiếp `/metrics` endpoint của backend. Nhanh hơn, ổn định hơn, không cần Chrome CDP.

## Cách dùng

### Chạy lần đầu
```powershell
cd D:\TNT_AI\venture_foundry\rapidapi_extract
.\tray\start_monitor.bat
```
Icon **TNT** xuất hiện trên khay hệ thống.

### Menu chuột phải
- **Check now** — kiểm tra ngay (click trái cũng được)
- **Open /metrics** — mở metrics JSON trên browser
- **Open RapidAPI Hub** — API public page
- **Open logs** — xem log
- **Open metrics** — xem reports folder
- **Help** — mở README này
- **Quit** — thoát

### Auto-start
Đã cài shortcut trong Startup folder. Khởi động máy → tray tự chạy.
Gỡ: xóa `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\TNT-Monitor.lnk`

## Không cần gì thêm

**Không cần Chrome.** Tray gọi trực tiếp:
```
GET https://invoice-extract-api-4eq9.onrender.com/metrics
```

Backend tự đếm: per-endpoint calls, per-subscriber usage, latency p95/p99.

## Metrics backend trả về

```json
{
  "uptime_human": "2h 15m",
  "total_requests": 42,
  "total_errors": 1,
  "error_rate_pct": 2.38,
  "endpoint_counts": {"POST /v1/invoice/extract": 30, ...},
  "endpoint_errors": {"POST /v1/invoice/extract": 1},
  "status_codes": {"200": 41, "400": 1},
  "avg_latency_ms": {...},
  "p95_latency_ms": {...},
  "p99_latency_ms": {...},
  "subscribers": {"user123": 15, "user456": 27},
  "subscriber_last_seen": {"user123": "2026-09-22T13:00:00", ...},
  "unique_subscribers": 2,
  "daily": {"2026-09-22": 42}
}
```

Subscriber ID lấy từ header `X-RapidAPI-User` mà RapidAPI tự gửi.

## Icon màu

- 🟡 **Vàng** — idle, chưa có traffic mới
- 🟢 **Xanh** — có call mới HOẶC có subscriber mới
- 🔴 **Đỏ** — backend không phản hồi (Render sleep, lỗi mạng, v.v.)

Hover icon để xem: `TNT | calls: N | subs: M`

## Config

`tray/config.json`:
```json
{
  "check_interval_minutes": 15,
  "notify_on_new_calls": true,
  "notify_on_new_subscribers": true,
  "admin_token": ""
}
```

- `check_interval_minutes`: 15 (mặc định). Có thể để 5 hoặc 60.
- `admin_token`: **chỉ cần** nếu backend đặt biến môi trường `ADMIN_TOKEN` trên Render. Khi đó `/metrics` yêu cầu `Authorization: Bearer <token>`.

## Files

- `monitor_tray.py` — app chính (v3)
- `start_monitor.bat` — chạy ẩn
- `install_startup.bat` — cài auto-start
- `config.json` — cấu hình
- `state.json` — state runtime (không track git)
- `logs/YYYY-MM.log` — log
- `icon*.png` — icon

## Troubleshooting

**Icon không thấy:** Windows 11 ẩn tray icon. Bấm `^` ở khay, kéo TNT icon ra.

**Icon đỏ liên tục:** Backend đang sleep (Render free tier ngủ sau 15 phút). Gọi thử 1 lần vào backend sẽ đánh thức.

**Notifications không hiện:** Windows Focus Assist có thể đang bật. Tắt tạm.

**Muốn thoát:** chuột phải icon → Quit. Nếu không thấy icon:
```
Get-CimInstance Win32_Process -Filter "name='pythonw.exe'" | Where-Object {$_.CommandLine -like '*monitor_tray*'} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

## Changelog

- **v3** (2026-09-22) — Poll `/metrics` endpoint thay vì scrape RapidAPI. Không cần Chrome CDP. Interval 15 phút.
- **v2** (2026-09-22) — Color icons, chrome_guard.
- **v1** (2026-09-22) — Scrape RapidAPI analytics qua Playwright.
