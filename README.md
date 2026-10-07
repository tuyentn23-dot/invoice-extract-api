# Invoice to JSON Extractor API

Convert invoices, receipts, resumes, bank statements and more into clean structured JSON - no LLM key required.

Live on RapidAPI: Invoice to JSON Extractor

Backend: https://invoice-extract-api-4eq9.onrender.com 
Health: https://invoice-extract-api-4eq9.onrender.com/health 
API docs: https://invoice-extract-api-4eq9.onrender.com/docs

---

## What it does

Extract structured JSON from 8+ document types in one API. Bilingual English / Vietnamese. Fast rule-based extractor with optional LLM fallback. Typical response under 1 second.

| Document | Endpoint |
|---|---|
| Invoice | `POST /v1/invoice/extract` |
| Receipt | `POST /v1/receipt/extract` |
| Resume / CV | `POST /v1/resume/extract` |
| Bank statement | `POST /v1/bank-statement/extract` |
| Purchase order | `POST /v1/purchase-order/extract` |
| Contract | `POST /v1/contract/extract` |
| Business card | `POST /v1/business-card/extract` |
| Utility bill | `POST /v1/utility-bill/extract` |

Every endpoint also has a `/base64` variant for images and PDFs (OCR via Tesseract).

---

## Quick start

### curl

```bash
curl -X POST https://invoice-extract-api-4eq9.onrender.com/v1/invoice/extract \
 -H "Content-Type: application/json" \
 -d '{"content": "INVOICE #12345 Vendor: Acme Corp Total: 100.00 USD"}'
```

### Python

```python
import requests

r = requests.post(
 "https://invoice-extract-api-4eq9.onrender.com/v1/invoice/extract",
 json={"content": "INVOICE #12345 Vendor: Acme Corp Total: 100.00 USD"},
)
print(r.json())
```

### Image / PDF (base64)

```python
import base64, requests

b64 = base64.b64encode(open("invoice.png", "rb").read()).decode()
r = requests.post(
 "https://invoice-extract-api-4eq9.onrender.com/v1/invoice/extract/base64",
 json={"content": b64, "content_type": "base64_image"},
)
print(r.json())
```

---

## Example response

```json
{
 "success": true,
 "invoice": {
 "invoice_number": "INV-2026-1042",
 "invoice_date": "2026-10-07",
 "currency": "USD",
 "vendor_name": "Acme Supplies Ltd.",
 "subtotal": 262.5,
 "tax_amount": 26.25,
 "total": 288.75,
 "line_items": [{"description": "Item A", "quantity": 10, "amount": 150.0}],
 "confidence": 0.9
 },
 "model": "heuristic:v1",
 "processing_ms": 1
}
```

---

## Use cases

- Accounting automation and bookkeeping
- Expense management apps
- E-commerce order and receipt parsing
- KYC / onboarding from business cards and IDs
- Loan and bank-statement analysis
- SaaS invoice ingestion

## Why this API

- No LLM key required - works out of the box
- Bilingual EN / VI, built for Southeast Asia
- OCR for images and PDFs included
- Fast: heuristic extraction in ~1ms
- Simple JSON in / JSON out

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs

## License

MIT
