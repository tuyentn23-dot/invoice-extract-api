# Build Status — 2026-09-21

## Đã xong (100% tự động, không cần bạn)

### Code
- [x] Invoice extraction API (`/v1/invoice/extract`)
- [x] Invoice base64 endpoint (`/v1/invoice/extract/base64`)
- [x] Receipt extraction API (`/v1/receipt/extract`)
- [x] Resume/CV extraction API (`/v1/resume/extract`)
- [x] Heuristic engine (EN + VI) — chạy **không cần API key**, $0 ongoing cost
- [x] LLM fallback (DeepSeek/Groq/Gemini) — tự động dùng nếu key hoạt động
- [x] RapidAPI proxy secret middleware
- [x] FastAPI OpenAPI tự sinh

### Deployment artifacts
- [x] `Dockerfile`
- [x] `render.yaml` (1-click deploy Render.com free tier)
- [x] `requirements.txt`
- [x] `.gitignore`

### Docs
- [x] `README.md` — listing copy sẵn sàng paste
- [x] `DEPLOY.md` — hướng dẫn 4 bước, 20 phút
- [x] `openapi.yaml` — import thẳng vào RapidAPI

### Git
- [x] Local repo khởi tạo, 2 commits
- [ ] **Push lên GitHub — CẦN BẠN**

## Test results

| Endpoint | Input | Output | Status |
|---|---|---|---|
| invoice | EN invoice có Subtotal/VAT/Total | invoice_number, dates, vendor, subtotal, tax, total, 2 line items, conf 0.9 | ✅ |
| invoice | VI "HOA DON GTGT" | HD-00123, 2025-01-05, 5,000,000 VND | ✅ |
| receipt | ACME COFFEE SHOP | store, date, tax, total 13.50, payment VISA, 2 items | ✅ |
| resume | John Smith CV | name, email, phone, linkedin, 6 skills, 2 jobs, 1 degree | ✅ |
| health | GET | 200 `{status:ok}` | ✅ |

## Việc CẦN BẠN làm để ra tiền (20 phút)

Đây là những việc **chỉ bạn làm được** vì cần tài khoản cá nhân:

1. **Push GitHub** — xem DEPLOY.md bước 1 (2 phút)
2. **Deploy Render** — xem DEPLOY.md bước 2 (5 phút)
3. **Đăng RapidAPI** — xem DEPLOY.md bước 3 (10 phút)
4. **Chờ duyệt** — 1-3 ngày

Sau khi live, link RapidAPI của bạn sẽ có dạng:
`https://rapidapi.com/<username>/api/invoice-to-json-extractor`

## Ngưỡng đo lường

| Mốc | Đo | Hành động |
|---|---|---|
| 24h sau live | ≥ 1 test call | OK |
| 7 ngày | ≥ 10 test call | tiếp tục |
| 30 ngày | ≥ 3 subscriber trả tiền | build API #2 (bank statement) |
| 30 ngày | 0 subscriber | build API #2, giữ API #1 chạy |
| 90 ngày | <$100/tháng | dừng RapidAPI, review toàn bộ |

## Chi phí đến giờ

- Code + test: **$0** (AI agent làm)
- GitHub: **$0**
- Render: **$0** (free tier)
- RapidAPI: **$0** (không phí đăng)
- **Tổng: $0**

## Sau khi live — tôi sẽ làm gì tiếp

Khi bạn paste link RapidAPI đã publish, tôi sẽ:
1. Viết launch message cho Reddit/IndieHackers/HN (bạn chỉ cần paste)
2. Viết 6 API tiếp theo dùng chung hạ tầng (bank statement, purchase order, contract, business card, ID doc, receipt ảnh)
3. Build dashboard theo dõi subscriber → báo bạn khi có tín hiệu đầu tiên
