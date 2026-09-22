# MANIFEST — Nguồn sự thật duy nhất của dự án

> **Đây là file đầu tiên cần đọc trong MỌI phiên mới.**
> Đọc xong file này, phiên sau biết ngay: dự án là gì, đang ở đâu, làm gì tiếp.

---

## 1. Dự án là gì

**Tên:** Invoice to JSON Extractor
**Mục tiêu:** API bán trên RapidAPI để tạo thu nhập thụ động, không cần gặp khách, không content marketing.
**Điều kiện thành công:** Đạt ≥ $30 MRR trong 30 ngày đầu, hoặc pivot nếu 0 calls sau 30 ngày.

---

## 2. Trạng thái hiện tại (cập nhật cuối: 2026-09-22)

| Hạng mục | Trạng thái |
|---|---|
| Backend | ✅ Live trên Render free tier |
| RapidAPI listing | ✅ Public |
| Endpoints | ✅ 10 (4 loại × text/base64) |
| GitHub repo | ✅ Public |
| Monitoring | ✅ Script + PowerShell automation |
| Launch | 🔄 Đang tiến hành (Reddit + Dev.to done) |
| Doanh thu | ❌ $0 |
| Subscribers | ❌ 0 |
| API calls | ❌ 0 |

---

## 3. URL quan trọng

```
Backend:    https://invoice-extract-api-4eq9.onrender.com
Health:     https://invoice-extract-api-4eq9.onrender.com/health
Docs:       https://invoice-extract-api-4eq9.onrender.com/docs
RapidAPI:   https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
Provider:   https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/definition
GitHub:     https://github.com/tuyentn23-dot/invoice-extract-api
Dev.to:     https://dev.to/tuyentn23dot/i-built-a-document-extraction-api-that-runs-on-regex-no-llm-needed-3b0g
```

---

## 4. Cấu trúc thư mục

```
rapidapi_extract/
├── MANIFEST.md              ← BẠN ĐANG ĐỌC — nguồn sự thật
├── HANDOFF.md               ← Prompt để paste vào phiên mới
├── STATE.json               ← State machine-readable
├── SESSION_LOG.md           ← Lịch sử các phiên
├── DECISIONS.md             ← Nhật ký quyết định
├── README.md                ← Hướng dẫn public (cho GitHub)
├── DEPLOY.md                ← Hướng dẫn deploy
├── LAUNCH_NOW.md            ← Copy-paste cho 5 kênh
├── LAUNCH_KIT.md            ← (legacy) copy cũ
├── SETUP_MONITORING.md      ← Cài Task Scheduler
├── SECURITY_TODO.md         ← Việc bảo mật còn nợ
├── app/                     ← FastAPI backend
│   ├── main.py              ← Entry point, 10 routes
│   ├── schemas.py           ← Pydantic models
│   ├── llm.py               ← LLM wrapper + fallback
│   ├── heuristic.py         ← Regex extractor cho invoice
│   ├── receipt.py
│   ├── resume.py
│   ├── bank_statement.py
│   ├── pdf_ocr.py
│   └── openapi_compat.py    ← Convert 3.1 → 3.0.3
├── tests/                   ← pytest suite (29 checks)
├── examples/                ← Python/JS/cURL cho users
├── scripts/                 ← Automation (local only, gitignored)
│   ├── monitor.py           ← Scrape analytics
│   ├── report.py            ← In metrics timeline
│   ├── daily_monitor.ps1    ← Wrapper cho Task Scheduler
│   └── tray_app.py          ← Tray mini-app (sắp có)
├── monitoring/              ← Snapshots, CSV (gitignored)
├── tray/                    ← Tray app resources
│   ├── icon.png
│   └── icon.ico
└── .git/                    ← GitHub
```

---

## 5. Quy tắc bất di bất dịch

1. **Không commit file sau lên GitHub:** `scripts/`, `monitoring/`, `screenshots/`, `.chrome_debug/`, `.proxy_secret`, `openapi.json`
2. **Không tiêu tiền** cho đến khi MRR ≥ $30
3. **Không build thêm API** cho đến khi API #1 có ≥ 10 calls
4. **Mọi quyết định** phải ghi vào `DECISIONS.md`
5. **Mọi phiên** phải append 1 entry vào `SESSION_LOG.md`

---

## 6. Cách làm việc

### Phiên mới bắt đầu thế nào

1. Mở `MANIFEST.md` (file này)
2. Mở `STATE.json` để lấy số liệu mới nhất
3. Mở `SESSION_LOG.md` để biết phiên trước làm gì
4. Chạy `scripts/report.py` để lấy metrics hiện tại
5. Quyết định dựa trên số liệu, không phải cảm hứng

### Phiên kết thúc thế nào

1. Chạy `scripts/monitor.py` để ghi snapshot
2. Append vào `SESSION_LOG.md`:
   - Ngày, giờ
   - Đã làm gì
   - Phát hiện gì
   - Việc còn lại
3. Cập nhật `STATE.json`
4. Git commit với message rõ ràng
5. Nếu có quyết định → ghi vào `DECISIONS.md`

---

## 7. Ngưỡng quyết định

| Metric | Ngưỡng | Hành động |
|---|---|---|
| API calls (7 ngày) | ≥ 10 | Bắt đầu build API #2 |
| Paid subscribers | ≥ 1 | Tăng tốc marketing |
| MRR | ≥ $30 | Deploy full-time |
| 30 ngày, 0 calls | 0 | Pivot nền tảng |
| 90 ngày, < $100 MRR | < $100 | Xem lại toàn bộ chiến lược |

---

## 8. Chi phí

- Render free tier: $0
- RapidAPI: $0 (chỉ thu 25% khi có doanh thu)
- GitHub: $0
- **Tổng cộng: $0**

---

## 9. Nếu bạn là AI agent đọc file này

Bạn đang tiếp quản dự án từ phiên trước. Đọc theo thứ tự:

1. `MANIFEST.md` (file này) — hiểu dự án
2. `STATE.json` — nắm số liệu
3. `SESSION_LOG.md` — xem lịch sử
4. `DECISIONS.md` — hiểu lý do
5. Chạy `scripts/report.py` — số liệu mới nhất
6. **Đọc `HANDOFF.md`** — prompt đầy đủ cho phiên mới

Sau khi đọc xong, hỏi user 3 câu:
- Có gì mới từ phiên trước?
- Ưu tiên hôm nay?
- Có quyết định nào cần thay đổi?

**Không tự ý làm gì trước khi hỏi.**
