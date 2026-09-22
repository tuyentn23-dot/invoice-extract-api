"""Business card -> JSON heuristic extractor."""
import re
from typing import Optional, Dict, Any, List

EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
PHONE_RE = re.compile(r'(?:\+?\d{1,3}[\s\-.]?)?\(?\d{2,4}\)?[\s\-.]?\d{3,4}[\s\-.]?\d{3,4}')
URL_RE = re.compile(r'(?<![@\w])(?:https?://[^\s]+|www\.[^\s]+|[a-z0-9-]+\.(?:com|net|org|io|dev|me|co|vn|ai|info|xyz)(?:/[\w\-./?%&=]*)?)', re.IGNORECASE)

TITLE_KW = ['ceo', 'cto', 'cfo', 'coo', 'founder', 'manager', 'director', 'engineer', 'developer', 'designer', 'analyst', 'consultant', 'president', 'head of', 'lead', 'specialist', 'executive', 'giam doc', 'giám đốc', 'truong phong', 'trưởng phòng']
COMPANY_KW = ['inc', 'llc', 'ltd', 'corp', 'corporation', 'company', 'co.', 'group', 'technologies', 'solutions', 'systems', 'pvt', 'gmbh', 'plc', 'jsc', 'cong ty', 'công ty']


def _find_name(lines: List[str]) -> Optional[str]:
    for line in lines[:8]:
        s = line.strip()
        if not s or len(s) < 3 or len(s) > 60:
            continue
        if EMAIL_RE.search(s) or PHONE_RE.search(s) or URL_RE.search(s):
            continue
        # skip if looks like title or company
        low = s.lower()
        if any(k in low for k in TITLE_KW):
            continue
        if any(k in low for k in COMPANY_KW):
            continue
        if s.isupper() and len(s) > 30:
            continue
        return s
    return None


def _find_title(lines: List[str]) -> Optional[str]:
    for line in lines:
        low = line.lower()
        if any(k in low for k in TITLE_KW):
            return line.strip()[:100]
    return None


def _find_company(lines: List[str]) -> Optional[str]:
    for line in lines:
        low = line.lower()
        if any(k in low for k in COMPANY_KW):
            return line.strip()[:120]
    return None


def _find_address(text: str) -> Optional[str]:
    # look for typical address pattern: number + street, or PO Box
    m = re.search(r'(\d+[^\n]{5,80}(?:street|st\.?|road|rd\.?|avenue|ave\.?|lane|ln\.?|drive|dr\.?|boulevard|blvd\.?|way|district|ward|quan|quận|phuong|phường))', text, re.IGNORECASE)
    if m:
        return m.group(1).strip()[:200]
    return None


def extract_business_card_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    lines = text.splitlines()
    name = _find_name(lines)
    title = _find_title(lines)
    company = _find_company(lines)
    emails = list(dict.fromkeys(EMAIL_RE.findall(text)))[:3]
    phones = []
    for m in PHONE_RE.finditer(text):
        v = m.group().strip()
        digits = re.sub(r'\D', '', v)
        if 7 <= len(digits) <= 15:
            phones.append(v)
    phones = list(dict.fromkeys(phones))[:3]
    websites = list(dict.fromkeys(URL_RE.findall(text)))[:3]
    address = _find_address(text)
    filled = sum(1 for x in [name, title, company, emails, phones] if x)
    conf = round(min(1.0, filled / 5.0) * 0.85, 2)
    return {
        'name': name,
        'title': title,
        'company': company,
        'emails': emails,
        'phones': phones,
        'websites': websites,
        'address': address,
        'confidence': conf,
    }
