"""Delivery note / packing slip -> JSON heuristic extractor."""
import re
from typing import Optional, Dict, Any, List
from app.heuristic import _to_float, NUM_RE, DATE_PATTERNS, _norm_date

DN_NUM_P = re.compile(
    r'(?:Delivery[ \t]*Note|D\.?N\.?|Packing[ \t]*Slip|Phieu[ \t]*giao[ \t]*hang|Phiếu[ \t]*giao[ \t]*hàng)[ \t]*'
    r'(?:#|No\.?|Number|N[oº])?[ \t]*[:#.]?[ \t]*([A-Z0-9][A-Z0-9\-\/]{2,30})',
    re.IGNORECASE,
)

DATE_KW = ['date', 'ngay', 'ngày', 'issued']
SHIP_DATE_KW = ['ship date', 'shipped', 'dispatch', 'giao']
VENDOR_KW = ['from', 'supplier', 'vendor', 'shipper', 'nha cung cap', 'nhà cung cấp']
RECIPIENT_KW = ['to', 'recipient', 'ship to', 'customer', 'consignee', 'khach hang', 'khách hàng']
CARRIER_KW = ['carrier', 'shipper', 'courier', 'van chuyen', 'vận chuyển', 'ship via']
TRACKING_KW = ['tracking', 'awb', 'waybill', 'van don', 'vận đơn']
PO_REF_P = re.compile(r'(?:P\.?O\.?|Order)[ \t]*(?:#|No\.?|Number)?[ \t]*[:#.]?[ \t]*([A-Z0-9][A-Z0-9\-\/]{2,30})', re.IGNORECASE)

LINE_PAT = re.compile(
    r'^(?P<desc>[A-Za-z\u00c0-\u1ef90-9][^\n]{2,60}?)\s+'
    r'(?P<qty>\d+(?:\.\d+)?)\s+'
    r'(?P<unit>[A-Za-z]+)?\s*$'
)


def _find_field(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords) and ':' in line:
            v = line.split(':', 1)[1].strip()
            if v and len(v) > 2:
                return v[:150]
    return None


def _find_date(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        if any(k in line.lower() for k in keywords):
            for pat, kind in DATE_PATTERNS:
                for m in re.finditer(pat, line):
                    d = _norm_date(m, kind)
                    if d:
                        return d
    return None


def _find_dn_number(text: str) -> Optional[str]:
    for m in DN_NUM_P.finditer(text):
        v = m.group(1).strip()
        if len(v) >= 3 and v.lower() not in ('dn', 'no', 'number'):
            return v
    return None


def _find_po_ref(text: str) -> Optional[str]:
    for m in PO_REF_P.finditer(text):
        v = m.group(1).strip()
        if len(v) >= 3:
            return v
    return None


def _find_items(text: str) -> List[Dict[str, Any]]:
    items = []
    for line in text.splitlines():
        s = line.strip()
        if not s or len(s) > 100:
            continue
        m = LINE_PAT.match(s)
        if m:
            qty = _to_float(m.group('qty'))
            if qty is None:
                continue
            items.append({
                'description': m.group('desc').strip(),
                'quantity': qty,
                'unit': (m.group('unit') or '').strip() or None,
            })
    return items[:100]


def extract_delivery_note_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    dn_number = _find_dn_number(text)
    issue_date = _find_date(text, DATE_KW)
    ship_date = _find_date(text, SHIP_DATE_KW)
    vendor = _find_field(text, VENDOR_KW)
    recipient = _find_field(text, RECIPIENT_KW)
    carrier = _find_field(text, CARRIER_KW)
    tracking = _find_field(text, TRACKING_KW)
    po_ref = _find_po_ref(text)
    items = _find_items(text)
    filled = sum(1 for x in [dn_number, issue_date, vendor, recipient, items] if x)
    conf = round(min(1.0, filled / 5.0) * 0.85, 2)
    return {
        'delivery_note_number': dn_number,
        'issue_date': issue_date,
        'ship_date': ship_date,
        'vendor_name': vendor,
        'recipient_name': recipient,
        'carrier': carrier,
        'tracking_number': tracking,
        'po_reference': po_ref,
        'items': items,
        'confidence': conf,
    }
