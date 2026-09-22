# Examples

Code mẫu để gọi **Invoice to JSON Extractor API** trên RapidAPI.

## Bước 1 — Lấy API key

1. Mở https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
2. Bấm **Subscribe to Basic** (miễn phí, 500 calls/tháng)
3. Vào tab **Endpoints** → copy `X-RapidAPI-Key`

## Bước 2 — Chạy example

### Python
```bash
pip install requests
python python_example.py  # sửa API_KEY trước
```

### JavaScript (Node 18+)
```bash
node javascript_example.js  # sửa API_KEY trước
```

### cURL
```bash
chmod +x curl_example.sh
./curl_example.sh  # sửa API_KEY trước
```

## 4 endpoints

| Endpoint | Input | Output |
|---|---|---|
| `POST /v1/invoice/extract` | Invoice text | Number, dates, vendor, VAT, totals, line items |
| `POST /v1/receipt/extract` | Receipt text | Store, date, items, total, payment method |
| `POST /v1/resume/extract` | Resume/CV text | Name, email, phone, skills, experience, education |
| `POST /v1/bank-statement/extract` | Bank statement text | Account, period, balance, transactions |

## Response format

```json
{
  "success": true,
  "invoice": {
    "invoice_number": "INV-2024-001",
    "invoice_date": "2024-03-15",
    "currency": "GBP",
    "vendor_name": "Acme Supplies Ltd.",
    "total": 132.0,
    "line_items": [...],
    "confidence": 0.9
  },
  "model": "heuristic:v1",
  "processing_ms": 42
}
```

## Ghi chú

- Input là **text**, không phải file ảnh/PDF (trừ khi dùng endpoint `/base64` với PDF sạch)
- Bilingual: English + Vietnamese
- Response time: dưới 1 giây
- Heuristic engine không cần LLM cho hầu hết trường hợp
