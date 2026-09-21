"""Bank statement -> JSON heuristic extractor.
Handles common bank CSV/text statement layouts (EN + VI).
"""
import re
from typing import Optional, Dict, Any, List
from app.heuristic import _to_float, _find_currency

DATE_PATTERNS = [
    (r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', 'ymd'),
    (r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', 'dmy_or_mdy'),
    (r'\b(\d{1,2})-(\d{1,2})-(\d{4})\b', 'dmy_or_mdy'),
    (r'\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b', 'dmy'),
]

NUM = r'\d+(?:[,\s]\d{3})*(?:\.\d{1,2})?'
MONEY_RE = re.compile(r'(?<![\d.])(' + NUM + r')(?![\d])')

TXN_PAT = re.compile(
    r'^\s*(?P<date>\d{1,4}[-/\.]\d{1,2}[-/\.]\d{1,4})\s+'
    r'(?P<desc>.+?)\s{2,}'
    r'(?P<amount>[+-]?' + NUM + r')\s*'
    r'(?P<balance>[+-]?' + NUM + r')?\s*$'
)


def _norm_date(m, kind):
    g = m.groups()
    try:
        if kind == 'ymd':
            y, mo, d = int(g[0]), int(g[1]), int(g[2])
        elif kind == 'dmy':
            d, mo, y = int(g[0]), int(g[1]), int(g[2])
        else:
            a, b, y = int(g[0]), int(g[1]), int(g[2])
            if a > 12: d, mo = a, b
            elif b > 12: mo, d = a, b
            else: d, mo = a, b
        if not (1 <= mo <= 12 and 1 <= d <= 31 and 1900 <= y <= 2100):
            return None
        return f"{y:04d}-{mo:02d}-{d:02d}"
    except Exception:
        return None


def _find_first_date(text):
    for pat, kind in DATE_PATTERNS:
        for m in re.finditer(pat, text):
            d = _norm_date(m, kind)
            if d:
                return d
    return None


def _find_account_number(text):
    m = re.search(r'(?:Account\s*(?:Number|No\.?)|Số\s*tài\s*khoản|IBAN|STK)[\s:#]*([A-Z0-9\- ]{6,34})', text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def _find_balance(text, keywords):
    for line in text.splitlines():
        if any(k in line.lower() for k in keywords):
            nums = [m.group(1) for m in MONEY_RE.finditer(line)]
            if nums:
                return _to_float(nums[-1])
    return None


def _parse_txns(text):
    txns = []
    for line in text.splitlines():
        m = TXN_PAT.match(line)
        if not m:
            continue
        d = None
        for pat, kind in DATE_PATTERNS:
            mm = re.match(pat, m.group('date'))
            if mm:
                d = _norm_date(mm, kind)
                break
        amt = _to_float(m.group('amount'))
        bal = _to_float(m.group('balance')) if m.group('balance') else None
        if amt is None:
            continue
        txns.append({
            'date': d,
            'description': m.group('desc').strip()[:200],
            'amount': amt,
            'balance': bal,
        })
    return txns[:200]


def extract_bank_statement_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    account = _find_account_number(text)
    currency = _find_currency(text)
    opening = _find_balance(text, ['opening balance', 'số dư đầu', 'so du dau'])
    closing = _find_balance(text, ['closing balance', 'số dư cuối', 'so du cuoi', 'ending balance'])
    period_start = _find_first_date(text[:500])
    txns = _parse_txns(text)
    period_end = None
    for t in reversed(txns):
        if t['date']:
            period_end = t['date']
            break
    total_in = round(sum(t['amount'] for t in txns if t['amount'] and t['amount'] > 0), 2)
    total_out = round(sum(t['amount'] for t in txns if t['amount'] and t['amount'] < 0), 2)
    filled = sum(1 for x in [account, currency, opening, closing, txns] if x)
    conf = round(min(1.0, filled / 5.0) * 0.85, 2)
    return {
        'account_number': account,
        'currency': currency,
        'period_start': period_start,
        'period_end': period_end,
        'opening_balance': opening,
        'closing_balance': closing,
        'total_credits': total_in,
        'total_debits': total_out,
        'transaction_count': len(txns),
        'transactions': txns,
        'confidence': conf,
    }
