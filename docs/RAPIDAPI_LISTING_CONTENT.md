# RapidAPI Listing - Noi dung copy-paste san

Dung khi dang o RapidAPI Studio > API > tab Description / Examples.

---

## Short description

> Extract clean structured JSON from invoices, receipts, resumes, bank statements and more - bilingual EN/VI, OCR included, no LLM key required.

## Long description

One API, 8+ document types.

Invoice to JSON Extractor turns raw text, images and PDFs into structured JSON you can drop straight into your database or accounting workflow.

Supported documents: invoice, receipt, resume/CV, bank statement, purchase order, contract, business card, utility bill.

Why developers pick it:
- No LLM key required - works out of the box
- Bilingual English / Vietnamese - built for Southeast Asia
- OCR for images and PDFs included
- Response typically under 1 second
- Simple JSON in / JSON out

---

## Code example - curl

```bash
curl --request POST \
 --url https://invoice-to-json-extractor1.p.rapidapi.com/v1/invoice/extract \
 --header "content-type: application/json" \
 --header "X-RapidAPI-Key: YOUR_KEY" \
 --header "X-RapidAPI-Host: invoice-to-json-extractor1.p.rapidapi.com" \
 --data "{\"content\": \"INVOICE #12345 Total: 100.00 USD\"}"
```

## Code example - Python

```python
import requests
url = "https://invoice-to-json-extractor1.p.rapidapi.com/v1/invoice/extract"
headers = {
 "content-type": "application/json",
 "X-RapidAPI-Key": "YOUR_KEY",
 "X-RapidAPI-Host": "invoice-to-json-extractor1.p.rapidapi.com"
}
print(requests.post(url, json={"content": "INVOICE #12345 Total: 100 USD"}, headers=headers).json())
```

## Code example - JavaScript

```javascript
const options = {
 method: "POST",
 headers: {
 "content-type": "application/json",
 "X-RapidAPI-Key": "YOUR_KEY",
 "X-RapidAPI-Host": "invoice-to-json-extractor1.p.rapidapi.com"
 },
 body: JSON.stringify({content: "INVOICE #12345 Total: 100 USD"})
};
fetch("https://invoice-to-json-extractor1.p.rapidapi.com/v1/invoice/extract", options).then(r => r.json()).then(console.log);
```

## Tags

invoice, ocr, receipt, pdf, resume, bank statement, purchase order, contract, business card, utility bill, json, extraction, parser, document ai, vietnamese, billing

## Pricing (sau khi sua trong Studio)

| Plan | Price | Quota | Rate limit |
|---|---|---|---|
| Basic (Free) | $0 | 500 req/month | 5 req/s |
| Pro | $9.99/mo | 10,000 req/month | 20 req/s |
| Mega | $49.00/mo | 100,000 req/month | 50 req/s |
