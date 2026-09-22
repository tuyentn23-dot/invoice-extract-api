"""Python example - Invoice to JSON Extractor API.

Install: pip install requests
Get your key: https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
"""
import requests

API_KEY = "YOUR_RAPIDAPI_KEY"
HOST = "invoice-to-json-extractor1.p.rapidapi.com"
BASE = f"https://{HOST}"
HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": HOST,
}


# === 1. INVOICE ===
response = requests.post(
    f"{BASE}/v1/invoice/extract",
    headers=HEADERS,
    json={
        "content": (
            "INVOICE\n"
            "Invoice #: INV-2024-001\n"
            "Date: 15/03/2024\n"
            "Vendor: Acme Supplies Ltd.\n"
            "VAT: GB123456789\n"
            "Bill To: Widget Corp\n\n"
            "Widget A  10  5.00  50.00\n"
            "Widget B  3   20.00 60.00\n\n"
            "Subtotal: 110.00\n"
            "VAT 20%: 22.00\n"
            "Total: 132.00 GBP"
        ),
        "language": "en",
    },
    timeout=60,
)
print("Invoice:", response.json())


# === 2. RECEIPT ===
response = requests.post(
    f"{BASE}/v1/receipt/extract",
    headers=HEADERS,
    json={
        "content": (
            "ACME COFFEE SHOP\n"
            "Date: 2024-05-10\n"
            "Latte 2 4.50 9.00\n"
            "Muffin 1 3.50 3.50\n"
            "Tax: 1.00\n"
            "Total: 13.50 USD\n"
            "Paid VISA"
        ),
    },
    timeout=60,
)
print("Receipt:", response.json())


# === 3. RESUME ===
response = requests.post(
    f"{BASE}/v1/resume/extract",
    headers=HEADERS,
    json={
        "content": (
            "John Smith\n"
            "john.smith@email.com | +1 555 123 4567\n"
            "linkedin.com/in/johnsmith\n\n"
            "Skills\n"
            "Python, Go, PostgreSQL, Docker\n\n"
            "Experience\n"
            "Senior Engineer at Acme Corp\n"
            "2020 - 2024\n"
            "Led a team of 5."
        ),
    },
    timeout=60,
)
print("Resume:", response.json())


# === 4. BANK STATEMENT ===
response = requests.post(
    f"{BASE}/v1/bank-statement/extract",
    headers=HEADERS,
    json={
        "content": (
            "ACME BANK\n"
            "Account Number: 1234567890\n"
            "Opening Balance: 5,000.00 USD\n\n"
            "2024-01-05  Salary Deposit    +2500.00  7500.00\n"
            "2024-01-12  Rent Payment      -1500.00  6000.00\n\n"
            "Closing Balance: 6,000.00 USD"
        ),
    },
    timeout=60,
)
print("Bank Statement:", response.json())
