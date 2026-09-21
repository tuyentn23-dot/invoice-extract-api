# Invoice Extraction API — RapidAPI Listing Package

## What it does
Extract structured JSON from raw invoice text (EN, VI, and others).
LLM-optional: uses LLM if key works, falls back to a zero-cost regex heuristic.

## Endpoints
- `POST /v1/invoice/extract` — main extraction
- `POST /v1/invoice/extract/base64` — same, for base64 PDF/image text
- `GET /health` — health
- `GET /docs` — OpenAPI UI

## Run locally
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test
```
python -c "from app.llm import extract_invoice; print(extract_invoice(open('tests/sample.txt').read()))"
```

## Deploy
Dockerfile included. Push to Render/Fly/Railway.

## Env vars (all optional)
- `RAPIDAPI_PROXY_SECRET` — set after creating the RapidAPI listing, to reject non-RapidAPI calls.
- `DEEPSEEK_API_KEY` / `GROQ_API_KEY` / `GEMINI_API_KEY` — if set, LLM path is used; otherwise heuristic.

## Pricing plan (RapidAPI)
- BASIC: 50 req/mo free
- PRO: $9/mo — 2,000 req
- ULTRA: $29/mo — 15,000 req
- MEGA: $99/mo — 100,000 req

## Listing copy

**Title:** Invoice to JSON Extractor — AI-Powered, Bilingual

**Short description (<=120 chars):**
Convert any invoice text to structured JSON. Bilingual EN/VI. Vendor, dates, totals, line items.

**Long description:**
Paste invoice text, get clean JSON:
- invoice_number, invoice_date, due_date, currency
- vendor_name, vendor_tax_id, customer_name
- subtotal, tax_amount, total
- line_items (description, qty, unit_price, amount)
- confidence score

Works on English and Vietnamese invoices. No signup beyond RapidAPI. Response < 1s typical.

**Tags:** invoice, ocr, pdf, extraction, json, ai, accounting, finance
