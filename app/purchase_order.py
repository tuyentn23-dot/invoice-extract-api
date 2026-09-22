"""Purchase Order -> JSON heuristic extractor."""
import re
from typing import Optional, Dict, Any, List
from app.heuristic import (
    _to_float, _find_currency, _dates_in_window,
    DATE_PATTERNS, NUM_RE, MONEY_RE,
    DATE_KW, DUE_KW, TAX_KW,
)

PO_NUM_P1 = re.compile(
    r'(?:P\.?O\.?|Purchase[ \t]*Order|Don[ \t]*dat[ \t]*hang)[ \t]*'
    r'(?:#|No\.?|Number|N[oº])?[ \t]*[:#.]?[ \t]*'
    r'([A-Z0-9][A-Z0-9\-\/]{2,30})',
    re.IGNORECASE,
)
PO_NUM_P2 = re.compile(
    r'(?:P\.?O\.?|Purchase[ \t]*Order)[ \t]*[:#][ \t]*'
    r'([A-Z0-9][A-Z0-9\-\/]{2,30})',
    re.IGNORECASE,
)

VENDOR_KW = ['vendor', 'seller', 'supplier', 'nha cung cap', 'nhà cung cấp', 'from']
BUYER_KW = ['buyer', 'bill to', 'ship to', 'customer', 'khach hang', 'khách hàng', 'ship-to']
DELIVERY_KW = ['delivery', 'ship', 'giao hang', 'giao hàng', 'expected']
SUBTOTAL_KW = ['subtotal', 'sub total', 'sub-total', 'net', 'tam tinh', 'tạm tính']
TOTAL_KW = ['total', 'grand total', 'tong cong', 'tổng cộng']


LINE_PAT = re.compile(
    r'^(?P<desc>[A-Za-zÀ-ỹ0-9][^\n]{2,60}?)\s+'
    r'(?P<qty>\d+(?:\.\d+)?)\s+'
    r'(?P<unit>' + NUM_RE + r')\s+'
    r'(?P<amount>' + NUM_RE + r')\s*$'
)


def _find_po_number(text: str) -> Optional[str]:
    for pat in (PO_NUM_P1, PO_NUM_P2):
        for m in pat.finditer(text):
            val = m.group(1).strip()
            if len(val) < 3:
                continue
            if val.lower() in ('po', 'no', 'number', 'order'):
                continue
            return val
    return None


def _find_field_by_kw(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords):
            # after colon
            if ':' in line:
                val = line.split(':', 1)[1].strip()
                if val and len(val) > 2:
                    return val[:150]
    return None


def _find_date_by_kw(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords):
            d = _dates_in_window(line)
            if d:
                return d
    return None


def _find_amount(text: str, keywords: List[str], exclude: List[str] = None) -> Optional[float]:
    exclude = exclude or []
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords) and not any(x in low for x in exclude):
            nums = [m.group(1) for m in MONEY_RE.finditer(line)]
            if nums:
                return _to_float(nums[-1])
    return None


def _find_line_items(text: str) -> List[Dict[str, Any]]:
    items = []
    for line in text.splitlines():
        s = line.strip()
        if not s or len(s) > 120:
            continue
        if any(k in s.lower() for k in SUBTOTAL_KW + TOTAL_KW + TAX_KW):
            continue
        m = LINE_PAT.match(s)
        if m:
            items.append({
                'description': m.group('desc').strip(),
                'quantity': _to_float(m.group('qty')),
                'unit_price': _to_float(m.group('unit')),
                'amount': _to_float(m.group('amount')),
            })
    return items[:100]


def extract_purchase_order_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    po_number = _find_po_number(text)
    order_date = _find_date_by_kw(text, DATE_KW)
    delivery_date = _find_date_by_kw(text, DELIVERY_KW)
    due_date = _find_date_by_kw(text, DUE_KW)
    vendor = _find_field_by_kw(text, VENDOR_KW)
    buyer = _find_field_by_kw(text, BUYER_KW)
    subtotal = _find_amount(text, SUBTOTAL_KW)
    tax = _find_amount(text, TAX_KW, exclude=['tax id', 'tax code', 'mst'])
    total = _find_amount(text, TOTAL_KW, exclude=['subtotal', 'sub total', 'sub-total'])
    currency = _find_currency(text)
    items = _find_line_items(text)
    filled = sum(1 for x in [po_number, order_date, vendor, total, currency] if x)
    conf = round(min(1.0, filled / 5.0) * 0.9, 2)
    return {
        'po_number': po_number,
        'order_date': order_date,
        'delivery_date': delivery_date,
        'due_date': due_date,
        'currency': currency,
        'vendor_name': vendor,
        'buyer_name': buyer,
        'subtotal': subtotal,
        'tax_amount': tax,
        'total': total,
        'line_items': items,
        'confidence': conf,
    }
