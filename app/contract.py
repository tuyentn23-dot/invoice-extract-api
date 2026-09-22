"""Contract key terms -> JSON heuristic extractor."""
import re
from typing import Optional, Dict, Any, List
from app.heuristic import _to_float, _find_currency, _dates_in_window, DATE_PATTERNS, NUM_RE, MONEY_RE

CONTRACT_NUM_P = re.compile(
    r'(?:Contract|Agreement)[ \t]*(?:#|No\.?|Number|N[oº])?[ \t]*[:#.]?[ \t]*([A-Z0-9][A-Z0-9\-\/]{2,30})',
    re.IGNORECASE,
)

PARTY_KW_1 = ['between', 'party a', 'first party', 'ben phia', 'bên a']
PARTY_KW_2 = ['and', 'party b', 'second party', 'bên b', 'ben b']
EFFECTIVE_KW = ['effective date', 'effective', 'commencement', 'ngay hieu luc', 'ngày hiệu lực']
EXPIRY_KW = ['expiry', 'expiration', 'end date', 'termination', 'het han', 'hết hạn']
TERM_KW = ['term', 'duration', 'thoi han', 'thời hạn']
PAYMENT_TERM_KW = ['payment term', 'net ', 'thanh toan trong', 'thanh toán trong']
GOVERNING_KW = ['governing law', 'jurisdiction', 'luat ap dung', 'luật áp dụng']
VALUE_KW = ['total value', 'contract value', 'consideration', 'gia tri hop dong', 'giá trị hợp đồng']


def _find_field(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords) and ':' in line:
            return line.split(':', 1)[1].strip()[:200]
    return None


def _find_amount(text: str, keywords: List[str]) -> Optional[float]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords):
            nums = [m.group(1) for m in MONEY_RE.finditer(line)]
            if nums:
                return _to_float(nums[-1])
    return None


def _find_parties(text: str) -> List[str]:
    parties = []
    for line in text.splitlines()[:30]:
        low = line.lower()
        if any(k in low for k in PARTY_KW_1 + PARTY_KW_2):
            # after 'between'/'and'/':' 
            if ':' in line:
                v = line.split(':', 1)[1].strip()
                if v and len(v) > 3:
                    parties.append(v[:150])
            else:
                m = re.search(r'between\s+(.{3,100}?)\s+and\s+(.{3,100})', line, re.IGNORECASE)
                if m:
                    parties.append(m.group(1).strip()[:100])
                    parties.append(m.group(2).strip()[:100])
    return list(dict.fromkeys(parties))[:6]


def _find_term_months(text: str) -> Optional[int]:
    m = re.search(r'(?:term|duration|thoi[ \t]*han|thời[ \t]*hạn)[^\n]{0,40}?(\d+)\s*(month|months|thang|tháng|year|years|nam|năm)', text, re.IGNORECASE)
    if m:
        n = int(m.group(1))
        unit = m.group(2).lower()
        if unit in ('year', 'years', 'nam', 'năm'):
            n *= 12
        return n
    return None


def _find_governing_law(text: str) -> Optional[str]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in GOVERNING_KW):
            if ':' in line:
                return line.split(':', 1)[1].strip()[:150]
            m = re.search(r'(?:governing law|jurisdiction)[^\n]{0,10}?(.{3,100})', line, re.IGNORECASE)
            if m:
                return m.group(1).strip()[:150]
    return None


def _find_payment_terms(text: str) -> Optional[str]:
    m = re.search(r'(?:net|payment\s*terms?|thanh[ \t]*to[aá]n)[^\n]{0,30}?(\d+)[ \t]*days?', text, re.IGNORECASE)
    if m:
        return f'Net {m.group(1)} days'
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in PAYMENT_TERM_KW):
            if ':' in line:
                return line.split(':', 1)[1].strip()[:100]
    return None


def extract_contract_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    contract_num = None
    for m in CONTRACT_NUM_P.finditer(text):
        v = m.group(1).strip()
        if len(v) >= 3 and v.lower() not in ('contract', 'agreement', 'no'):
            contract_num = v
            break
    effective_date = None
    for line in text.splitlines():
        if any(k in line.lower() for k in EFFECTIVE_KW):
            d = _dates_in_window(line)
            if d:
                effective_date = d
                break
    expiry_date = None
    for line in text.splitlines():
        if any(k in line.lower() for k in EXPIRY_KW):
            d = _dates_in_window(line)
            if d:
                expiry_date = d
                break
    parties = _find_parties(text)
    term_months = _find_term_months(text)
    value = _find_amount(text, VALUE_KW)
    currency = _find_currency(text)
    governing = _find_governing_law(text)
    payment_terms = _find_payment_terms(text)
    filled = sum(1 for x in [contract_num, effective_date, parties, term_months, governing] if x)
    conf = round(min(1.0, filled / 5.0) * 0.85, 2)
    return {
        'contract_number': contract_num,
        'effective_date': effective_date,
        'expiry_date': expiry_date,
        'term_months': term_months,
        'parties': parties,
        'contract_value': value,
        'currency': currency,
        'payment_terms': payment_terms,
        'governing_law': governing,
        'confidence': conf,
    }
