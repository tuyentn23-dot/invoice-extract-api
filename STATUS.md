# Build Status — v1.3

## Đã build xong 100%

### 4 API endpoints (8 routes với base64)
- `POST /v1/invoice/extract` — Invoice EN + VI
- `POST /v1/invoice/extract/base64` — PDF/ảnh invoice
- `POST /v1/receipt/extract` — Receipt
- `POST /v1/receipt/extract/base64`
- `POST /v1/resume/extract` — CV/Resume
- `POST /v1/resume/extract/base64`
- `POST /v1/bank-statement/extract` — Bank statement
- `POST /v1/bank-statement/extract/base64`

### Engine
- Heuristic regex: chạy $0, không cần API key, EN + VI
- LLM fallback (DeepSeek/Groq/Gemini) — tự động kích hoạt nếu key OK
- PDF extraction: pdfplumber
- Image OCR: pytesseract
- RapidAPI proxy secret middleware

### Test
- 23 checks, all PASS (`python tests/test_all_endpoints.py`)
- 4 document types × EN/VI
- Error handling

### Deploy
- Dockerfile
- render.yaml (Render free tier)
- requirements.txt (đủ deps)
- openapi.yaml

### Docs
- README.md — listing copy
- DEPLOY.md — 4 bước, 20 phút
- LAUNCH_KIT.md — copy-paste cho 7 kênh

### Git
- 4 commits local

## Blocker — cần bạn

Đây là 3 việc **chỉ bạn làm được** (đều cần account cá nhân):

- [ ] **1. Push GitHub** — DEPLOY.md bước 1 (2 phút)
- [ ] **2. Deploy Render** — DEPLOY.md bước 2 (5 phút)
- [ ] **3. List RapidAPI** — DEPLOY.md bước 3 (10 phút)
- [ ] **4. Chờ duyệt** — 1-3 ngày
- [ ] **5. Launch** — LAUNCH_KIT.md

## Sau khi API live

Paste URL RapidAPI vào chat. Tôi sẽ:
1. Sinh tracking sheet để đo subscriber/calls
2. Chuẩn bị API #5 (purchase order) + #6 (contract)
3. Viết monitoring script (báo khi có subscriber đầu tiên)
4. Viết follow-up Reddit/HN nếu 7 ngày không có traction

## Ngưỡng quyết định

| Mốc | Đo | Hành động |
|---|---|---|
| D+7 | ≥ 10 test calls | tiếp tục |
| D+30 | ≥ 3 subscriber trả tiền | build API #5-6 |
| D+30 | 0 subscriber | giữ API chạy, đổi hướng list chợ khác |
| D+90 | MRR < $100 | pivot nền tảng (Replicate/HF) |

## Chi phí

**$0** cho tới khi có subscriber. RapidAPI thu 25% doanh thu — không phí đăng.

## Repo path

`D:/TNT_AI/venture_foundry/rapidapi_extract/`
