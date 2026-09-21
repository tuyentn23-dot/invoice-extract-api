"""Resume/CV -> JSON heuristic extractor."""
import re
from typing import Optional, Dict, Any, List

EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
PHONE_RE = re.compile(r'(?:\+?\d{1,3}[\s\-.]?)?\(?\d{2,4}\)?[\s\-.]?\d{3,4}[\s\-.]?\d{3,4}')
# URL: require scheme or www. or a known TLD followed by /path or end-of-token not preceded by @
URL_RE = re.compile(r'(?<![@\w])(?:https?://[^\s]+|www\.[^\s]+|[a-z0-9-]+\.(?:com|net|org|io|dev|me|co|vn|ai|info|xyz)(?:/[\w\-./?%&=]*)?)', re.IGNORECASE)
YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')

SECTION_HEADERS = {
    'experience': ['experience', 'work history', 'employment', 'kinh nghiem', 'kinh nghiệm'],
    'education': ['education', 'hoc van', 'học vấn', 'qualifications'],
    'skills': ['skills', 'technologies', 'ky nang', 'kỹ năng', 'technical skills'],
    'projects': ['projects', 'du an', 'dự án'],
    'certifications': ['certifications', 'certificates', 'chung chi', 'chứng chỉ'],
    'summary': ['summary', 'objective', 'profile', 'about', 'gioi thieu', 'giới thiệu'],
    'languages': ['languages', 'ngon ngu', 'ngôn ngữ'],
}


def _detect_sections(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    sections: Dict[str, List[str]] = {}
    current = 'header'
    sections[current] = []
    for line in lines:
        s = line.strip()
        low = s.lower().rstrip(':')
        matched = None
        for sec, keys in SECTION_HEADERS.items():
            if any(low == k or low.startswith(k + ':') for k in keys):
                matched = sec
                break
        if matched:
            current = matched
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)
    return {k: '\n'.join(v).strip() for k, v in sections.items()}


def _find_name(text: str) -> Optional[str]:
    for line in text.splitlines()[:8]:
        s = line.strip()
        if not s or len(s) > 50 or len(s) < 3:
            continue
        if EMAIL_RE.search(s) or PHONE_RE.search(s) or URL_RE.search(s):
            continue
        if re.match(r'^(resume|curriculum vitae|cv|sơ yếu|so yeu)', s, re.IGNORECASE):
            continue
        if s.isupper() and len(s) > 25:
            continue
        return s
    return None


def _find_emails(text: str) -> List[str]:
    return list(dict.fromkeys(EMAIL_RE.findall(text)))[:5]


def _find_phones(text: str) -> List[str]:
    out = []
    for m in PHONE_RE.finditer(text):
        v = m.group().strip()
        digits = re.sub(r'\D', '', v)
        if 7 <= len(digits) <= 15:
            out.append(v)
    return list(dict.fromkeys(out))[:5]


def _find_links(text: str) -> List[str]:
    # strip emails first to avoid domain matches inside emails
    stripped = EMAIL_RE.sub(' ', text)
    raw = URL_RE.findall(stripped)
    # filter out bare domains that are likely email fragments
    out = []
    for u in raw:
        if '@' in u:
            continue
        out.append(u)
    return list(dict.fromkeys(out))[:10]


def _extract_skills(text: str, sections: Dict[str, str]) -> List[str]:
    blob = sections.get('skills', '')
    if not blob:
        return []
    parts = re.split(r'[,;|\u2022\u00b7\-/\n]', blob)
    out = []
    for p in parts:
        p = p.strip(' \t-\u2022\u00b7')
        if 2 <= len(p) <= 40 and not re.match(r'^[\W\d]+$', p):
            out.append(p)
    return out[:40]


def _extract_experience(sections: Dict[str, str]) -> List[Dict[str, Any]]:
    blob = sections.get('experience', '')
    if not blob:
        return []
    blocks = re.split(r'\n\s*\n', blob)
    out = []
    for b in blocks:
        years = YEAR_RE.findall(b)
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if not lines:
            continue
        title = lines[0][:120]
        company = None
        if len(lines) > 1:
            company = lines[1][:120]
        out.append({
            'title': title,
            'company': company,
            'years': sorted(set(years)),
            'description': ' '.join(lines[2:])[:600] if len(lines) > 2 else None,
        })
    return out[:10]


def _extract_education(sections: Dict[str, str]) -> List[Dict[str, Any]]:
    blob = sections.get('education', '')
    if not blob:
        return []
    blocks = re.split(r'\n\s*\n', blob)
    out = []
    for b in blocks:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if not lines:
            continue
        out.append({
            'institution': lines[0][:120],
            'degree': lines[1][:120] if len(lines) > 1 else None,
            'years': sorted(set(YEAR_RE.findall(b))),
        })
    return out[:10]


def extract_resume_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    sections = _detect_sections(text)
    name = _find_name(text)
    emails = _find_emails(text)
    phones = _find_phones(text)
    links = _find_links(text)
    skills = _extract_skills(text, sections)
    experience = _extract_experience(sections)
    education = _extract_education(sections)
    summary = sections.get('summary', '')[:600] or None

    filled = sum(1 for x in [name, emails, phones, skills, experience] if x)
    conf = round(min(1.0, filled / 5.0) * 0.85, 2)

    return {
        'name': name,
        'emails': emails,
        'phones': phones,
        'links': links,
        'summary': summary,
        'skills': skills,
        'experience': experience,
        'education': education,
        'certifications': (sections.get('certifications', '') or '').split('\n')[:10],
        'languages': (sections.get('languages', '') or '').split('\n')[:10],
        'confidence': conf,
    }
