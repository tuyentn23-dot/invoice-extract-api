# TNT Monitor — system tray app

Tự động giám sát RapidAPI analytics, báo toast khi có traffic mới. Chạy nền, không hiện console.

## Cách dùng

### Lần đầu
```powershell
cd D:\TNT_AI\venture_foundry\rapidapi_extract
.\tray\start_monitor.bat
```
Sẽ thấy icon **TNT** trong khay hệ thống (góc phải dưới, có thể ẩn trong mũi tên mở rộng).

### Menu chuột phải trên icon
- **Check now** — kiểm tra ngay (mặc định khi click trái)
- **Open RapidAPI dashboard** — mở analytics
- **Open public API page** — mở Hub listing
- **Open logs folder** — xem log
- **Open metrics folder** — xem reports
- **Quit** — thoát

### Auto-start khi boot
Đã cài sẵn shortcut `TNT-Monitor.lnk` vào Startup folder. Lần sau mở máy sẽ tự chạy.

Gỡ bỏ: xóa file `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\TNT-Monitor.lnk`

## Yêu cầu

Tray cần **Chrome đang mở với cổng debug 9222** để lấy analytics. Nếu Chrome đóng, tray vẫn chạy nhưng chỉ ghi log lỗi.

Mở Chrome debug:
```powershell
Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--remote-debugging-port=9222','--user-data-dir=D:\TNT_AI\venture_foundry\rapidapi_extract\.chrome_debug'
```

Đăng nhập RapidAPI 1 lần — session lưu lại.

## Config

`tray/config.json`:
- `check_interval_minutes`: 60 (mặc định 1 giờ/lần)
- `notify_on_new_calls`: true
- `notify_on_error_rate_above`: 5.0 (%)
- `chrome_cdp_port`: 9222

Sửa interval thành 15 hoặc 30 nếu muốn check thường xuyên hơn.

## Files

- `monitor_tray.py` — app chính
- `start_monitor.bat` — chạy ẩn (khuyến nghị)
- `install_startup.bat` — cài auto-start
- `config.json` — cấu hình
- `state.json` — state tự lưu (không sửa)
- `logs/YYYY-MM.log` — log theo tháng
- `icon.png` — icon tray

## Metrics output

`metrics/YYYY-MM-DD.json` — mỗi ngày 1 file, chứa:
```json
{
  "timestamp": "2026-09-22T12:30:00",
  "calls": 0,
  "error_rate": 0.0,
  "latency_ms": 0.0
}
```

## Notifications

Khi có traffic mới:
- **Lần đầu tiên có call**: "First API call! Someone is using your API. Total: N"
- **Có call mới**: "+N calls since last check. Total: M"

## Troubleshooting

**Icon không hiện**: Windows 11 ẩn tray icon mặc định. Bấm mũi tên `^` ở khay, kéo TNT icon ra ngoài.

**Check failed**: Chrome chưa mở hoặc chưa login RapidAPI. Mở Chrome debug, login, chờ kỳ check tiếp theo.

**Xem log**: chuột phải icon → Open logs folder.

**Muốn thoát hẳn**: chuột phải icon → Quit. Nếu không thấy icon, kill process: `Get-Process pythonw | Where-Object {$_.Path -like '*pythonw*'} | Stop-Process`
