# HANDOFF — Prompt cho phiên mới

> Copy toàn bộ file này và paste vào phiên mới của TNT AI Agent.

---

## BỐI CẢNH

Bạn đang tiếp quản dự án **Invoice to JSON Extractor** — một API bán trên RapidAPI.

**Mục tiêu:** Tạo thu nhập thụ động $30+ MRR, không cần gặp khách, không content marketing.

**Đã live:** 2026-09-22.

---

## VIỆC ĐẦU TIÊN — ĐỌC THEO THỨ TỰ

1. `MANIFEST.md` — hiểu tổng quan dự án
2. `STATE.json` — số liệu mới nhất
3. `SESSION_LOG.md` — lịch sử các phiên trước
4. `DECISIONS.md` — lý do các quyết định

**Sau đó chạy:**
```
python scripts/report.py
```
để lấy metrics hiện tại từ RapidAPI analytics.

---

## TRẠNG THÁI HIỆN TẠI (tính đến 2026-09-22)

- ✅ Backend live trên Render free
- ✅ 10 endpoints trên RapidAPI, public
- ✅ GitHub repo public
- ✅ Dev.to article published
- ✅ Reddit r/SaaS posted
- 🔄 Monitoring script chạy được, đang chờ dữ liệu
- ❌ $0 doanh thu, 0 subscribers

---

## CẤU TRÚC QUAN TRỌNG

```
D:\TNT_AI\venture_foundry\rapidapi_extract\
├── MANIFEST.md          ← đọc đầu tiên
├── STATE.json           ← số liệu
├── SESSION_LOG.md       ← lịch sử
├── DECISIONS.md         ← lý do
├── HANDOFF.md           ← file này
├── app/                 ← code FastAPI
├── tests/               ← test suite
├── scripts/             ← automation (gitignored)
└── monitoring/          ← snapshots (gitignored)
```

---

## QUY TẮC BẤT DI BẤT DỊCH

1. **Không tiêu tiền** cho đến khi MRR ≥ $30
2. **Không build thêm API** cho đến khi API #1 có ≥ 10 calls/7 ngày
3. **Mọi quyết định** ghi vào `DECISIONS.md`
4. **Mọi phiên** append 1 entry vào `SESSION_LOG.md`
5. **Không commit** thư mục `scripts/`, `monitoring/`, `screenshots/`
6. **Không sửa** URL backend trừ khi có lý do chính đáng

---

## NGƯỠNG QUYẾT ĐỊNH

| Metric | Ngưỡng | Hành động |
|---|---|---|
| API calls/7 ngày | ≥ 10 | Build API #2 |
| Paid subscribers | ≥ 1 | Tăng tốc marketing |
| MRR | ≥ $30 | Deploy full-time |
| 30 ngày, 0 calls | 0 | Pivot nền tảng |
| 90 ngày, < $100 MRR | < $100 | Xem lại toàn bộ chiến lược |

---

## VIỆC CẦN LÀM NGAY

1. **Set RAPIDAPI_PROXY_SECRET** — xem `SECURITY_TODO.md`
2. **Đăng Twitter/X** — copy từ `LAUNCH_NOW.md`
3. **Đăng LinkedIn** — copy từ `LAUNCH_NOW.md`
4. **Setup Task Scheduler** cho monitoring — xem `SETUP_MONITORING.md`

---

## CÁCH LÀM VIỆC VỚI USER

**Người dùng:**
- Không muốn gặp khách
- Không muốn xuất hiện public
- Không có content
- Có hiểu biết crypto + AI agent
- Muốn tự động hóa tối đa

**Quy tắc giao tiếp:**
- Nói thẳng, không vòng vo
- Không làm giả định khi có dữ liệu — chạy `report.py` trước
- Khi bế tắc, đề xuất A/B/C, không tự chọn
- Mọi dự đoán phải có bằng chứng

---

## CÔNG CỤ ĐÃ CÀI

- Python: `D:/TNT_AI/venv/Scripts/python.exe`
- Playwright + Chromium + real Chrome
- FastAPI + Pydantic + uvicorn + pytest
- pystray + PIL (cho tray app)

---

## LƯU Ý VỀ ENCODING

- Windows PowerShell console đôi khi không hiển thị được Unicode tiếng Việt
- Khi cần debug, dùng `base64.b64encode()` để tránh lỗi charmap
- File `SESSION_LOG.md` phải ghi UTF-8

---

## BẮT ĐẦU NHƯ THẾ NÀO

Khi user paste prompt này vào phiên mới:

1. Đọc 4 file theo thứ tự trên
2. Chạy `python scripts/report.py` (có thể cần Chrome debug port nếu muốn scrape)
3. Báo cáo tình hình cho user trong 5 dòng
4. Hỏi user 3 câu:
   - Có gì mới từ phiên trước?
   - Ưu tiên hôm nay?
   - Có quyết định nào cần thay đổi?
5. **Đợi user trả lời rồi mới làm**

**Không tự ý build gì trước khi user xác nhận.**

---

## TRƯỜNG HỢP KHẨN CẤP

Nếu API down:
1. Kiểm tra https://invoice-extract-api-4eq9.onrender.com/health
2. Nếu 404/500 → vào https://dashboard.render.com → service `invoice-extract-api` → Events → xem log
3. Render free tier sleep sau 15 phút → lần gọi đầu chậm 30s là bình thường

Nếu RapidAPI listing bị gỡ:
1. Vào Provider Dashboard → xem notification
2. Nếu do policy → sửa theo yêu cầu
3. Nếu do billing → check Payment Settings

---

**Chúc may mắn. Không có gì bí ẩn — mọi thứ đều nằm trong các file `.md` và `.json` trong thư mục này.**
