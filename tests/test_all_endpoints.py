"""Full regression test suite. Run with: python tests/test_all_endpoints.py"""
import os
import sys
import base64

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


# 1. Health
def test_health():
    r = client.get("/health")
    check("health.status", r.status_code == 200)
    check("health.version", r.json().get("version") == "1.3.0")


# 2. Root
r = client.get("/")
check("root.has_endpoints", "endpoints" in r.json())
check("root.endpoint_count", len(r.json()["endpoints"]) == 10)


# 3. Invoice EN
r = client.post("/v1/invoice/extract", json={
    "content": "INVOICE\nInvoice #: INV-2024-0042\nDate: 15/03/2024\nDue: 15/04/2024\n"
               "Vendor: Acme Supplies Ltd.\nVAT: GB123456789\nBill To: Widget Corp\n"
               "Subtotal: 110.00\nVAT 20%: 22.00\nTotal: 132.00 GBP"
})
j = r.json()
inv = j.get("invoice") or {}
check("invoice.en.success", j.get("success") is True)
check("invoice.en.number", inv.get("invoice_number") == "INV-2024-0042")
check("invoice.en.date", inv.get("invoice_date") == "2024-03-15")
check("invoice.en.total", inv.get("total") == 132.0)
check("invoice.en.currency", inv.get("currency") == "GBP")


# 4. Invoice VI
r = client.post("/v1/invoice/extract", json={
    "content": "HOA DON GTGT\nSo: HD-00123\nNgay: 05/01/2025\nKhach hang: Cong ty ABC\nTong cong: 5,000,000 VND"
})
inv = r.json().get("invoice") or {}
check("invoice.vi.number", inv.get("invoice_number") == "HD-00123")
check("invoice.vi.date", inv.get("invoice_date") == "2025-01-05")
check("invoice.vi.total", inv.get("total") == 5000000.0)
check("invoice.vi.currency", inv.get("currency") == "VND")


# 5. Invoice base64 fallback
b = base64.b64encode(b"Invoice #: INV-2\nDate: 2024-02-01\nTotal: 50 EUR").decode()
r = client.post("/v1/invoice/extract/base64", json={"content": b})
inv = r.json().get("invoice") or {}
check("invoice.b64.number", inv.get("invoice_number") == "INV-2")
check("invoice.b64.currency", inv.get("currency") == "EUR")


# 6. Receipt
r = client.post("/v1/receipt/extract", json={
    "content": "ACME COFFEE\nDate: 2024-05-10\nLatte 2 4.50 9.00\nMuffin 1 3.50 3.50\nTax: 1.00\nTotal: 13.50 USD\nPaid VISA"
})
rec = r.json().get("receipt") or {}
check("receipt.success", r.json().get("success") is True)
check("receipt.total", rec.get("total") == 13.5)
check("receipt.payment", rec.get("payment_method") == "VISA")
check("receipt.store", rec.get("store_name") == "ACME COFFEE")


# 7. Resume
r = client.post("/v1/resume/extract", json={
    "content": "John Smith\njohn.smith@email.com | +1 555 123 4567\nlinkedin.com/in/johnsmith\n\n"
               "Summary\nSenior engineer.\n\nSkills\nPython, Go, PostgreSQL, Docker\n\n"
               "Experience\nSenior Engineer at Acme\n2020 - 2024\nLed team."
})
res = r.json().get("resume") or {}
check("resume.success", r.json().get("success") is True)
check("resume.name", res.get("name") == "John Smith")
check("resume.email", "john.smith@email.com" in (res.get("emails") or []))
check("resume.skills_count", len(res.get("skills") or []) >= 4)
check("resume.linkedin", any("linkedin" in x for x in (res.get("links") or [])))


# 8. Bank statement
r = client.post("/v1/bank-statement/extract", json={
    "content": "ACME BANK\nAccount Number: 1234567890\nOpening Balance: 5,000.00 USD\n"
               "2024-01-05  Salary       +2500.00  7500.00\n"
               "2024-01-12  Rent         -1500.00  6000.00\n"
               "Closing Balance: 6,000.00 USD"
})
bank = r.json().get("bank_statement") or {}
check("bank.success", r.json().get("success") is True)
check("bank.account", bank.get("account_number") == "1234567890")
check("bank.txns", bank.get("transaction_count") == 2)
check("bank.credits", bank.get("total_credits") == 2500.0)
check("bank.debits", bank.get("total_debits") == -1500.0)


# 9. Errors
r = client.post("/v1/invoice/extract", json={"content": "hi"})
check("error.short_content", r.status_code == 400)

r = client.post("/v1/invoice/extract", json={"content": "x" * 30, "content_type": "bogus"})
check("error.bad_content_type", r.status_code == 400)

print(f"\n=== {PASS} passed, {FAIL} failed ===")
sys.exit(0 if FAIL == 0 else 1)
