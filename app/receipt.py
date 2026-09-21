"""Receipt -> JSON heuristic extractor."""
import re
from typing import Optional, Dict, Any, List
from app.heuristic import (
    _to_float, _dates_in_window, _money_in_line, _find_currency,
    MONEY_RE, DATE_PATTERNS, NUM_RE,
)

STORE_KW = ['store', 'merchant', 'shop', 'cua hang', 'cửa hàng', 'seller']
DATE_KW = ['date', 'ngay', 'ngày', 'time', 'giao dịch']
TOTAL_KW = ['total', 'amount', 'tong', 'tổng', 'thanh toan', 'thanh toán', 'grand']
TAX_KW = ['tax', 'vat', 'gst', 'thue', 'thuế']
PAYMENT_KW = ['cash', 'credit', 'debit', 'card', 'visa', 'mastercard', 'momo', 'zalopay', 'vietqr', 'tien mat', 'tiền mặt']

ITEM_PAT = re.compile(
    r'^(?P<desc>[A-Za-zÀ-ỹ0-9][^\n]{1,50}?)\s+'
    r'(?P<qty>\d+(?:\.\d+)?)?\s*[xX×]?\s*'
    r'(?P<amount>' + NUM_RE + r')\s*$'
)


def _find_store(text: str) -> Optional[str]:
    m = re.search(r'(?:Store|Merchant|Shop|Seller|Cửa[ \t]*hàng|Cua[ \t]*hang)[ \t]*[:\-][ \t]*([^\n]{2,80})', text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    for line in text.splitlines()[:5]:
        s = line.strip()
        if s and 3 <= len(s) <= 60 and not re.match(r'^[\d\W]+$', s):
            if not re.match(r'^(receipt|hóa[ \t]*đơn|hoa[ \t]*don|invoice)\b', s, re.IGNORECASE):
                return s
    return None


def _find_payment_method(text: str) -> Optional[str]:
    low = text.lower()
    for k in PAYMENT_KW:
        if k in low:
            return k.upper()
    return None


def _find_items(text: str) -> List[Dict[str, Any]]:
    items = []
    for line in text.splitlines():
        s = line.strip()
        if not s or len(s) > 80:
            continue
        low = s.lower()
        if any(k in low for k in TOTAL_KW + TAX_KW):
            continue
        m = ITEM_PAT.match(s)
        if m:
            amt = _to_float(m.group('amount'))
            if amt is None or amt == 0:
                continue
            items.append({
                'description': m.group('desc').strip(),
                'quantity': _to_float(m.group('qty')) if m.group('qty') else None,
                'amount': amt,
            })
    return items[:50]


def extract_receipt_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    store = _find_store(text)
    date = None
    for line in text.splitlines():
        if any(k in line.lower() for k in DATE_KW):
            d = _dates_in_window(line)
            if d:
                date = d
                break
    if not date:
        d = _dates_in_window(text[:300])
        date = d
    total = None
    for line in text.splitlines():
        if any(k in line.lower() for k in TOTAL_KW):
            v = _money_in_line(line)
            if v is not None:
                total = v
    tax = None
    for line in text.splitlines():
        if any(k in line.lower() for k in TAX_KW):
            v = _money_in_line(line)
            if v is not None:
                tax = v
    currency = _find_currency(text)
    payment = _find_payment_method(text)
    items = _find_items(text)
    filled = sum(1 for x in [store, date, total, currency] if x)
    conf = round(min(1.0, filled / 4.0) * 0.85, 2)
    return {
        'store_name': store,
        'date': date,
        'currency': currency,
        'subtotal': None,
        'tax_amount': tax,
        'total': total,
        'payment_method': payment,
        'items': items,
        'confidence': conf,
    }
