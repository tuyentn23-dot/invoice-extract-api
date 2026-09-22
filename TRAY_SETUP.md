# Tray App — Hướng dẫn

Mini-app chạy trong system tray Windows, theo dõi API live 24/7.

## Cài đặt (đã xong)

Shortcut đã được tạo:
```
C:\Users\DELL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\TNT_RapidAPI_Tray.lnk
```

Từ lần đăng nhập Windows tiếp theo, tray app sẽ tự chạy.

## Chạy thủ công ngay

```powershell
Start-Process "D:\TNT_AI\venv\Scripts\pythonw.exe" "D:\TNT_AI\venture_foundry\rapidapi_extract\scripts\tray_app.py" -WindowStyle Hidden
```

Hoặc double-click file:
```
scripts\tray_app.py
```

## Icon ở tray — ý nghĩa màu

| Màu | Nghĩa |
|---|---|
| 🟢 Xanh | Backend live, latency < 2s |
| 🟡 Vàng | Backend live nhưng chậm (> 2s — Render free tier sleep) |
| 🔴 Đỏ | Backend down |

## Menu chuột phải

- **Check now** — kiểm tra health ngay lập tức
- **Run monitor** — scrape RapidAPI analytics (calls, subscribers)
- **View report** — mở file report
- **Open RapidAPI page** — mở trang public API
- **Open Provider dashboard** — mở analytics dashboard
- **Open GitHub repo**
- **View HANDOFF.md** — mở file handoff cho phiên mới
- **View STATE.json** — mở state hiện tại
- **Open project folder**
- **View tray log** — xem log của tray
- **Quit** — tắt tray app

## Log

```
monitoring/tray.log
```

Tự động ghi mỗi lần health check (60 giây/lần).

## Polling

- Health check: mỗi 60 giây
- Monitor scrape: chỉ khi bấm menu **Run monitor** (không tự động vì cần Chrome debug)

## Gỡ cài đặt

```powershell
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TNT_RapidAPI_Tray.lnk"
```

## Debug

Nếu tray không hiện:
1. Check Python có `pystray` + `Pillow`: `python -c "import pystray, PIL; print('ok')"`
2. Chạy foreground để thấy lỗi:
   ```powershell
   cd D:\TNT_AI\venture_foundry\rapidapi_extract
   D:\TNT_AI\venv\Scripts\python.exe scripts\tray_app.py
   ```
3. Xem log: `notepad monitoring\tray.log`

## Ghi chú

- Tray app dùng `pythonw.exe` (không có cửa sổ console)
- Khi tắt bằng **Quit**, process tự dọn dẹp và ghi log
- Nếu Windows kill process khi sleep mode, mở lại bằng shortcut trong Start Menu
