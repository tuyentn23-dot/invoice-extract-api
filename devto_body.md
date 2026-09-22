I kept rewriting invoice parsing code on every freelance project. Same regex, same edge cases, same pain. So I made it a public API instead.

It's called **Invoice to JSON Extractor**. Four endpoints, one auth, text in, structured JSON out.

The interesting part: the base path doesn't use an LLM. It's a regex heuristic engine that handles ~70% of typical invoices in under 50ms, for zero ongoing cost.

## What it does

| Endpoint | Input | Output |
|---|---|---|
| `POST /v1/invoice/extract` | Invoice text | number, dates, vendor, VAT, totals, line items |
| `POST /v1/receipt/extract` | Receipt text | store, date, items, total, payment method |
| `POST /v1/resume/extract` | CV/resume text | name, email, phone, skills, experience |
| `POST /v1/bank-statement/extract` | Bank statement text | account, transactions, running balance |

Bilingual out of the box (English + Vietnamese).

## Why regex first

When I started, I assumed I'd need an LLM for this. But most invoices follow one of maybe 15 common layouts. Regex handles these in 40-60ms with zero API calls.

The LLM is a **fallback**, not the primary engine. If the regex extractor returns a low confidence score, the API escalates to DeepSeek or Groq for that specific request.

Result: ~95% of requests never hit an LLM. Average cost per request rounds to zero.

## Example

Input:

```
INVOICE
Invoice #: INV-2024-001
Date: 15/03/2024
Vendor: Acme Supplies Ltd.
VAT: GB123456789
Bill To: Widget Corp

Widget A  10  5.00  50.00
Widget B  3   20.00 60.00

Subtotal: 110.00
VAT 20%: 22.00
Total: 132.00 GBP
```

Output:

```json
{
  "success": true,
  "invoice": {
    "invoice_number": "INV-2024-001",
    "invoice_date": "2024-03-15",
    "currency": "GBP",
    "vendor_name": "Acme Supplies Ltd.",
    "vendor_tax_id": "GB123456789",
    "customer_name": "Widget Corp",
    "subtotal": 110.0,
    "tax_amount": 22.0,
    "total": 132.0,
    "line_items": [
      {"description": "Widget A", "quantity": 10.0, "unit_price": 5.0, "amount": 50.0},
      {"description": "Widget B", "quantity": 3.0, "unit_price": 20.0, "amount": 60.0}
    ],
    "confidence": 0.9
  },
  "model": "heuristic:v1",
  "processing_ms": 42
}
```

## Try it in 30 seconds

```bash
curl -X POST "https://invoice-to-json-extractor1.p.rapidapi.com/v1/invoice/extract" \
  -H "content-type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: invoice-to-json-extractor1.p.rapidapi.com" \
  -d '{"content":"Invoice #: INV-1\nDate: 2024-01-15\nTotal: 132.00 USD"}'
```

Get a free key here: [Invoice to JSON Extractor](https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1)

Free tier: 500 calls/month. Paid tiers start at $9/month for 2,000 calls.

## What I'd add next

- More document types: purchase orders, contracts, business cards
- Better OCR for photographed receipts
- Webhook mode (send URL, get called back with JSON)

If you build anything that processes invoices or receipts, I'd love feedback on what fields you actually need. The API is small and I can iterate fast.

---

*Stack: FastAPI + Pydantic, deployed on Render free tier, billing via RapidAPI. Total monthly cost so far: $0.*
