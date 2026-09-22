"""Utility bill -> JSON heuristic extractor."""
import re
from typing import Optional, Dict, Any, List
from app.heuristic import _to_float, _find_currency, _dates_in_window, DATE_PATTERNS, MONEY_RE

BILL_NUM_P = re.compile(
    r'(?:Bill|Invoice|Account|Customer)[ \t]*(?:#|No\.?|Number|N[oº])?[ \t]*[:#.]?[ \t]*([A-Z0-9][A-Z0-9\-\/]{2,30})',
    re.IGNORECASE,
)

TYPE_KW = ['electricity', 'electric', 'gas', 'water', 'internet', 'phone', 'mobile', 'cable', 'dien', 'điện', 'nuoc', 'nước', 'gas', 'internet']
PERIOD_KW = ['billing period', 'period', 'ky', 'kỳ', 'from', 'to']
DUE_KW = ['due date', 'payment due', 'han thanh toan', 'hạn thanh toán']
ISSUE_KW = ['issue date', 'bill date', 'invoice date', 'ngay phat hanh', 'ngày phát hành']
TOTAL_KW = ['total', 'amount due', 'tong cong', 'tổng cộng', 'thanh toan', 'thanh toán']
USAGE_KW = ['usage', 'consumption', 'kwh', 'm3', 'so dien', 'số điện']
PREV_KW = ['previous', 'prev', 'chi so cu', 'chỉ số cũ', 'old reading']
CURR_KW = ['current', 'curr', 'chi so moi', 'chỉ số mới', 'new reading']
METER_KW = ['meter', 'dong ho', 'đồng hồ', 'serial']


def _find_amount(text: str, keywords: List[str], exclude: List[str] = None) -> Optional[float]:
    exclude = exclude or []
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords) and not any(x in low for x in exclude):
            nums = [m.group(1) for m in MONEY_RE.finditer(line)]
            if nums:
                return _to_float(nums[-1])
    return None


def _find_date(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        if any(k in line.lower() for k in keywords):
            d = _dates_in_window(line)
            if d:
                return d
    return None


def _find_number(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords):
            if ':' in line:
                val = line.split(':', 1)[1].strip()
                if val and len(val) > 1:
                    return val[:60]
    return None


def _detect_utility_type(text: str) -> Optional[str]:
    low = text.lower()
    for k in TYPE_KW:
        if k in low:
            return k.title()
    return None


def _find_period(text: str) -> Dict[str, Optional[str]]:
    period_start = None
    period_end = None
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in PERIOD_KW):
            # try to find two dates
            dates = []
            for pat, kind in DATE_PATTERNS:
                for m in re.finditer(pat, line):
                    from app.heuristic import _norm_date
                    d = _norm_date(m, kind)
                    if d:
                        dates.append(d)
            if len(dates) >= 2:
                period_start, period_end = dates[0], dates[1]
                break
            elif dates:
                period_start = dates[0]
    return {'period_start': period_start, 'period_end': period_end}


def _find_usage(text: str) -> Optional[float]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in USAGE_KW):
            m = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:kwh|m3|kwh|units?|đơn vị)', line, re.IGNORECASE)
            if m:
                return _to_float(m.group(1).replace(',', '.'))
    return None


def extract_utility_bill_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    bill_num = None
    for m in BILL_NUM_P.finditer(text):
        v = m.group(1).strip()
        if len(v) >= 3 and v.lower() not in ('bill', 'invoice', 'no', 'account'):
            bill_num = v
            break
    utility_type = _detect_utility_type(text)
    period = _find_period(text)
    issue_date = _find_date(text, ISSUE_KW)
    due_date = _find_date(text, DUE_KW)
    total = _find_amount(text, TOTAL_KW)
    currency = _find_currency(text)
    usage = _find_usage(text)
    meter = _find_number(text, METER_KW)
    prev_reading = _find_amount(text, PREV_KW)
    curr_reading = _find_amount(text, CURR_KW)
    filled = sum(1 for x in [bill_num, utility_type, period['period_start'], due_date, total] if x)
    conf = round(min(1.0, filled / 5.0) * 0.85, 2)
    return {
        'bill_number': bill_num,
        'utility_type': utility_type,
        'period_start': period['period_start'],
        'period_end': period['period_end'],
        'issue_date': issue_date,
        'due_date': due_date,
        'currency': currency,
        'total': total,
        'usage': usage,
        'meter_number': meter,
        'previous_reading': prev_reading,
        'current_reading': curr_reading,
        'confidence': conf,
    }
