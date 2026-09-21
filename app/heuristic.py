"""Rule-based invoice extractor. Works without any LLM API key."""
import re
from typing import Optional, List, Dict, Any

DATE_PATTERNS = [
    (r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', 'ymd'),
    (r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', 'dmy_or_mdy'),
    (r'\b(\d{1,2})-(\d{1,2})-(\d{4})\b', 'dmy_or_mdy'),
    (r'\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b', 'dmy'),
]

CURRENCY_MAP = {
    'USD': 'USD', '$': 'USD', 'US$': 'USD',
    'EUR': 'EUR', '€': 'EUR',
    'GBP': 'GBP', '£': 'GBP',
    'VND': 'VND', '₫': 'VND', 'VNĐ': 'VND', 'đ': 'VND',
    'JPY': 'JPY', '¥': 'JPY', '円': 'JPY',
    'CNY': 'CNY', 'RMB': 'CNY',
    'AUD': 'AUD', 'CAD': 'CAD', 'SGD': 'SGD', 'CHF': 'CHF',
}

NUM_RE = r'\d{1,3}(?:[,\s]\d{3})*(?:\.\d{1,2})?'
MONEY_RE = re.compile(r'(?<![\d.])(' + NUM_RE + r')(?![\d])')

DATE_KW = ['date', 'dated', 'issued', 'issue date', 'invoice date', 'ngay', 'ngày']
DUE_KW  = ['due', 'payment due', 'due date', 'han', 'hạn']
SUB_KW  = ['subtotal', 'sub total', 'sub-total', 'net amount', 'tam tinh', 'tạm tính', 'cong tien hang', 'cộng tiền hàng']
TAX_KW  = ['tax', 'vat', 'gst', 'thue', 'thuế', 'gtgt']
TOTAL_KW= ['total', 'grand total', 'amount due', 'tong cong', 'tổng cộng', 'tong thanh toan', 'tổng thanh toán', 'thanh tien', 'thành tiền']

BAD_HEADER = re.compile(
    r'^(invoice|tax[ \t]*invoice|h[oóa][ \t]*đơn(?:[ \t]*gtgt)?|hoa[ \t]*don(?:[ \t]*gtgt)?|receipt|phieu|phiếu)\b',
    re.IGNORECASE,
)

INV_NUM_P1 = re.compile(
    r'(?:Invoice|INV|H[oóa][ \t]*đơn|Số[ \t]*HĐ)[ \t]*'
    r'(?:#|No\.?|Number|N[oº]|Số|So)[ \t]*[:#.]?[ \t]*'
    r'([A-Z0-9][A-Z0-9\-\/]{2,30})',
    re.IGNORECASE,
)
INV_NUM_P2 = re.compile(
    r'(?:Invoice|INV|H[oóa][ \t]*đơn|Hoa[ \t]*don|Số|So)[ \t]*[:#][ \t]*'
    r'([A-Z0-9][A-Z0-9\-\/]{2,30})',
    re.IGNORECASE,
)
BAD_NUM_WORDS = {'invoice', 'inv', 'number', 'no', 'hoa', 'don', 'hoa don', 'hd', 'gtgt'}


def _to_float(s: str) -> Optional[float]:
    if s is None:
        return None
    s = s.strip().replace(' ', '').replace(',', '')
    try:
        return float(s)
    except ValueError:
        return None


def _norm_date(m: re.Match, kind: str) -> Optional[str]:
    g = m.groups()
    try:
        if kind == 'ymd':
            y, mo, d = int(g[0]), int(g[1]), int(g[2])
        elif kind == 'dmy':
            d, mo, y = int(g[0]), int(g[1]), int(g[2])
        else:
            a, b, y = int(g[0]), int(g[1]), int(g[2])
            if a > 12:
                d, mo = a, b
            elif b > 12:
                mo, d = a, b
            else:
                d, mo = a, b
        if not (1 <= mo <= 12 and 1 <= d <= 31 and 1900 <= y <= 2100):
            return None
        return f"{y:04d}-{mo:02d}-{d:02d}"
    except Exception:
        return None


def _dates_in_window(window: str) -> Optional[str]:
    for pat, kind in DATE_PATTERNS:
        for m in re.finditer(pat, window):
            d = _norm_date(m, kind)
            if d:
                return d
    return None


def _find_date(text: str, keywords: List[str]) -> Optional[str]:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        low = line.lower()
        if any(k in low for k in keywords):
            window = ' '.join(lines[i:i+2])
            d = _dates_in_window(window)
            if d:
                return d
    return None


def _money_in_line(line: str) -> Optional[float]:
    vals = []
    for m in MONEY_RE.finditer(line):
        f = _to_float(m.group(1))
        if f is None:
            continue
        after = line[m.end():m.end()+2].strip()
        if after.startswith('%'):
            continue
        vals.append(f)
    return vals[-1] if vals else None


def _find_amount(text: str, keywords: List[str], exclude: List[str] = None) -> Optional[float]:
    exclude = exclude or []
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords) and not any(x in low for x in exclude):
            v = _money_in_line(line)
            if v is not None:
                return v
    return None


def _find_currency(text: str) -> Optional[str]:
    if re.search(r'\bVND\b|VNĐ|\u20ab', text):
        return 'VND'
    for code in CURRENCY_MAP:
        if len(code) == 3 and re.search(r'\b' + re.escape(code) + r'\b', text, re.IGNORECASE):
            return CURRENCY_MAP[code]
    for sym in ['$', '€', '£', '¥']:
        if sym in text:
            return CURRENCY_MAP[sym]
    return None


def _find_tax_id(text: str) -> Optional[str]:
    m = re.search(r'\b(?:VAT|Tax[ \t]*ID|TIN|MST|Mã[ \t]*số[ \t]*thuế)[ \t]*(?:No\.?|#|:)?[ \t]*([A-Z]{0,3}[0-9][A-Z0-9\-]{4,20})', text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def _find_invoice_number(text: str) -> Optional[str]:
    for pat in (INV_NUM_P1, INV_NUM_P2):
        for m in pat.finditer(text):
            val = m.group(1).strip().rstrip(':')
            if val.lower() in BAD_NUM_WORDS:
                continue
            if len(val) < 3:
                continue
            return val
    return None


def _find_vendor(text: str) -> Optional[str]:
    m = re.search(r'(?:Vendor|Seller|Supplier|From|Nhà[ \t]*cung[ \t]*cấp|Công[ \t]*ty)[ \t]*[:\-][ \t]*([^\n]{2,80})', text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    for line in text.splitlines():
        s = line.strip()
        if not s or len(s) < 3 or len(s) > 80:
            continue
        if BAD_HEADER.match(s):
            continue
        if re.match(r'^[\d\W]+$', s):
            continue
        if ':' in s[:20] or '#' in s[:15]:
            continue
        return s
    return None


def _find_customer(text: str) -> Optional[str]:
    m = re.search(r'(?:Bill[ \t]*To|Customer|Buyer|Client|Sold[ \t]*To|Khách[ \t]*hàng|Khach[ \t]*hang)[ \t]*[:\-][ \t]*([^\n]{2,80})', text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def _find_line_items(text: str) -> List[Dict[str, Any]]:
    items = []
    pat = re.compile(
        r'^(?P<desc>[A-Za-zÀ-ỹ0-9][^\n]{2,60}?)\s+'
        r'(?P<qty>\d+(?:\.\d+)?)\s+'
        r'(?P<unit>' + NUM_RE + r')\s+'
        r'(?P<amount>' + NUM_RE + r')\s*$'
    )
    for line in text.splitlines():
        m = pat.match(line.strip())
        if m:
            items.append({
                'description': m.group('desc').strip(),
                'quantity': _to_float(m.group('qty')),
                'unit_price': _to_float(m.group('unit')),
                'amount': _to_float(m.group('amount')),
                'tax_rate': None,
            })
    return items[:100]


def extract_invoice_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    inv_num = _find_invoice_number(text)
    due_date = _find_date(text, DUE_KW)
    inv_date = None
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in DATE_KW) and not any(k in low for k in DUE_KW):
            d = _dates_in_window(line)
            if d:
                inv_date = d
                break
    subtotal = _find_amount(text, SUB_KW)
    tax = _find_amount(text, TAX_KW, exclude=['tax id', 'tax no', 'tax code', 'mst'])
    total = _find_amount(text, TOTAL_KW, exclude=['subtotal', 'sub total', 'sub-total'])
    currency = _find_currency(text)
    vendor = _find_vendor(text)
    customer = _find_customer(text)
    tax_id = _find_tax_id(text)
    items = _find_line_items(text)

    filled = sum(1 for x in [inv_num, inv_date, total, vendor, currency] if x)
    conf = round(min(1.0, filled / 5.0) * 0.9, 2)

    return {
        'invoice_number': inv_num,
        'invoice_date': inv_date,
        'due_date': due_date,
        'currency': currency,
        'vendor_name': vendor,
        'vendor_tax_id': tax_id,
        'vendor_address': None,
        'customer_name': customer,
        'customer_tax_id': None,
        'customer_address': None,
        'subtotal': subtotal,
        'tax_amount': tax,
        'total': total,
        'line_items': items,
        'notes': None,
        'confidence': conf,
    }
