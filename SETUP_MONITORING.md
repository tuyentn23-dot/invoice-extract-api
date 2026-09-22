# Monitoring — Hướng dẫn cài đặt

Mục tiêu: tự động ghi lại metrics (subscribers, calls, revenue) mỗi ngày để theo dõi tiến độ kiếm tiền.

## Cách 1 — Chạy thủ công (đơn giản nhất)

Mở PowerShell:
```powershell
cd D:\TNT_AI\venture_foundry\rapidapi_extract
powershell -ExecutionPolicy Bypass -File scripts\daily_monitor.ps1
```

Xem kết quả:
```
monitoring\last_report.log
monitoring\snapshot_*.json
monitoring\metrics.csv
```

## Cách 2 — Tự động chạy hàng ngày (Task Scheduler)

### Bước 1: Mở Task Scheduler
- Bấm `Win + R` → gõ `taskschd.msc` → Enter

### Bước 2: Tạo task
- Menu phải → **Create Basic Task**
- Name: `TNT Monitor RapidAPI`
- Next → **Daily** → Next
- Start time: `09:00` (hoặc bất kỳ giờ nào bạn muốn)
- Next → **Start a program**
- Program/script:
  ```
  powershell.exe
  ```
- Add arguments:
  ```
  -ExecutionPolicy Bypass -File "D:\TNT_AI\venture_foundry\rapidapi_extract\scripts\daily_monitor.ps1"
  ```
- Next → **Finish**

### Bước 3: Test ngay
- Chuột phải task vừa tạo → **Run**
- Đợi 20 giây → check `monitoring\last_report.log`

## Điều kiện tiên quyết

- Chrome phải đã đăng nhập RapidAPI (session sống trong profile `.chrome_debug`)
- Nếu session hết hạn → script tự mở Chrome, bạn đăng nhập lại 1 lần

## Các file output

| File | Mục đích |
|---|---|
| `monitoring/metrics.csv` | Dữ liệu raw, append mỗi lần chạy |
| `monitoring/snapshot_YYYYMMDD_HHMM.json` | Snapshot đầy đủ |
| `monitoring/analytics.txt` | Text scrape từ analytics page |
| `monitoring/last_report.log` | Output lần chạy gần nhất |
| `monitoring/analytics.png` | Screenshot |

## Ngưỡng hành động

| Metric | Ngưỡng | Hành động |
|---|---|---|
| Total API calls (7 ngày) | ≥ 10 | Bắt đầu build API #2 |
| Paid subscribers | ≥ 1 | Tăng tốc mở rộng |
| MRR | ≥ $30 | Deploy full-time |
| 30 ngày = 0 calls | 0 | Pivot, thử nền tảng khác |

## Debug

Nếu snapshot rỗng:
1. Mở Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\TNT_AI\venture_foundry\rapidapi_extract\.chrome_debug"`
2. Đăng nhập RapidAPI
3. Chạy lại script
