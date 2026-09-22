#!/usr/bin/env bash
# cURL examples - Invoice to JSON Extractor API
# Get your key: https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1

API_KEY="YOUR_RAPIDAPI_KEY"
HOST="invoice-to-json-extractor1.p.rapidapi.com"

# === 1. INVOICE ===
curl -X POST "https://$HOST/v1/invoice/extract" \
  -H "content-type: application/json" \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $HOST" \
  -d '{"content":"INVOICE\nInvoice #: INV-1\nDate: 2024-01-15\nVendor: Acme\nTotal: 132.00 USD","language":"en"}'

echo ""

# === 2. RECEIPT ===
curl -X POST "https://$HOST/v1/receipt/extract" \
  -H "content-type: application/json" \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $HOST" \
  -d '{"content":"ACME COFFEE\nDate: 2024-05-10\nLatte 1 4.50 4.50\nTotal 4.50 USD\nPaid VISA"}'

echo ""

# === 3. RESUME ===
curl -X POST "https://$HOST/v1/resume/extract" \
  -H "content-type: application/json" \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $HOST" \
  -d '{"content":"John Smith\njohn@email.com\n\nSkills\nPython, Go, Docker"}'

echo ""

# === 4. BANK STATEMENT ===
curl -X POST "https://$HOST/v1/bank-statement/extract" \
  -H "content-type: application/json" \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $HOST" \
  -d '{"content":"ACME BANK\nAccount Number: 12345678\n2024-01-05  Deposit  +100.00  1100.00\nClosing Balance: 1,100.00 USD"}'

echo ""
