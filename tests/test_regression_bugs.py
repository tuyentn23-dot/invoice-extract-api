"""Regression tests for two bugs found in production 2026-10-10."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.heuristic import extract_invoice_heuristic

SAMPLE = (
    "INVOICE #INV-2026-042" "\n"
    "Date: 2026-10-09" "\n"
    "Bill To: Acme Corp, 123 Main St" "\n"
    "Item: Widget A   Qty: 5   Unit: $20.00   Total: $100.00" "\n"
    "Subtotal: $100.00" "\n"
    "Tax: $10.00" "\n"
    "Total Due: $110.00" "\n"
)

def test_bug1_total_should_be_grand_total():
    r = extract_invoice_heuristic(SAMPLE)
    assert r["total"] == 110.0, "BUG1 total=%r" % r["total"]

def test_bug2_line_items_not_empty():
    r = extract_invoice_heuristic(SAMPLE)
    assert len(r["line_items"]) == 1, "BUG2 items=%r" % r["line_items"]
    li = r["line_items"][0]
    assert li["quantity"] == 5.0
    assert li["unit_price"] == 20.0
    assert li["amount"] == 100.0

def test_invoice_number_still_works():
    assert extract_invoice_heuristic(SAMPLE)["invoice_number"] == "INV-2026-042"

def test_subtotal_tax_still_work():
    r = extract_invoice_heuristic(SAMPLE)
    assert r["subtotal"] == 100.0
    assert r["tax_amount"] == 10.0

if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except AssertionError as e:
                print("FAIL", name, "-", e)
                fails += 1
    print()
    print("fails:", fails)
