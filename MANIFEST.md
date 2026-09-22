# MANIFEST — Invoice to JSON Extractor

## Tổng quan

Document extraction API. 10 loại tài liệu → JSON. Bilingual EN/VI. Live trên RapidAPI.

**Trạng thái:** ✅ LIVE — đang chờ khách đầu tiên
**Version:** 2.0.0
**Chi phí:** $0

## URLs

| Mục | URL |
|---|---|
| Public API | https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1 |
| Backend | https://invoice-extract-api-4eq9.onrender.com |
| GitHub | https://github.com/tuyentn23-dot/invoice-extract-api |

## Endpoints (16)

### Invoice
- `POST /v1/invoice/extract`
- `POST /v1/invoice/extract/base64`

### Receipt
- `POST /v1/receipt/extract`
- `POST /v1/receipt/extract/base64`

### Resume
- `POST /v1/resume/extract`
- `POST /v1/resume/extract/base64`

### Bank statement
- `POST /v1/bank-statement/extract`
- `POST /v1/bank-statement/extract/base64`

### Mới trong v2
- `POST /v1/purchase-order/extract`
- `POST /v1/contract/extract`
- `POST /v1/business-card/extract`
- `POST /v1/utility-bill/extract`
- `POST /v1/delivery-note/extract`
- `POST /v1/id-document/extract`

### Utility
- `GET /health`
- `GET /`

## Pricing

| Gói | Giá/tháng | Requests |
|---|---|---|
| BASIC | Free | 500 |
| PRO | $9 | 2,000 |
| ULTRA | $29 | 15,000 |
| MEGA | $99 | 100,000 |

Payout: PayPal tuyentn23@gmail.com — Ready.

## Kiến trúc

```
Request → FastAPI → _prepare_content (text or base64 PDF/OCR)
         → heuristic extractor (regex engine, $0)
         → [optional] LLM fallback (DeepSeek/Groq/Gemini)
         → Pydantic validation → JSON response
```

## Files

### Code
- `app/main.py` — FastAPI app, 16 endpoints
- `app/heuristic.py` — base regex engine
- `app/llm.py` — LLM fallback (nếu có API key)
- `app/pdf_ocr.py` — PDF/image decode
- `app/schemas.py` — Pydantic models
- `app/openapi_compat.py` — convert OpenAPI 3.1 → 3.0.3 cho RapidAPI
- `app/{invoice,receipt,resume,bank_statement,purchase_order,contract,business_card,utility_bill,delivery_note,id_document}.py`

### Tray
- `tray/monitor_tray.py` — system tray app
- `tray/chrome_guard.py` — auto-launch Chrome debug
- `tray/config.json` — cấu hình
- `tray/start_monitor.bat` — chạy ẩn
- `tray/install_startup.bat` — cài auto-start

### Deploy
- `Dockerfile`
- `render.yaml`
- `requirements.txt`
- `openapi.yaml`

### Docs
- `README.md` — listing copy
- `DEPLOY.md` — deploy guide
- `LAUNCH_NOW.md` — launch content
- `LAUNCH_LOG.md` — kết quả launch thật
- `START_HERE.md` — entry point
- `STATUS.md` — trạng thái
- `SECURITY_TODO.md` — proxy secret
- `PAID_PLANS_GUIDE.md` — tạo plans
- `STATE.json` — state machine-readable
- `SESSION_LOG.md` — log phiên
- `MANIFEST.md` (file này)

### Tests
- `tests/test_all_endpoints.py` — 29 checks

### Metrics
- `metrics/report_*.json` — report hàng ngày

## Chạy local

```
cd D:/TNT_AI/venture_foundry/rapidapi_extract
D:/TNT_AI/venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

Test: http://localhost:8000/docs

## Tray

```
.\tray\start_monitor.bat
```

Icon TNT xuất hiện trên khay. Chuột phải để menu.

## Test

```
D:/TNT_AI/venv/Scripts/python.exe tests/test_all_endpoints.py
```

## Ngưỡng dừng

- 30 ngày: 0 subscriber → giữ, đổi kênh traffic
- 90 ngày: MRR <$100 → pivot nền tảng (Replicate/HF)
