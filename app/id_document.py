"""ID document (passport / national ID / driver license) -> JSON heuristic extractor.
WARNING: Compliance-sensitive. Output includes confidence; caller must verify.
"""
import re
from typing import Optional, Dict, Any, List
from app.heuristic import _dates_in_window, DATE_PATTERNS, _norm_date

MRZ_LINE = re.compile(r'^[A-Z0-9<]{30,44}$')

PASSPORT_KW = ['passport', 'ho chieu', 'hộ chiếu', 'p<', 'p<vnm']
ID_KW = ['identity card', 'id card', 'national id', 'cmnd', 'cccd', 'chung minh', 'chứng minh', 'can cuoc', 'căn cước']
DL_KW = ['driver', 'driving', 'license', 'licence', 'bang lai', 'bằng lái', 'gplx']

NAME_KW = ['name', 'ho ten', 'họ tên', 'holder', 'given names', 'surname']
DOB_KW = ['date of birth', 'birth', 'dob', 'sinh', 'ngay sinh', 'ngày sinh']
ISSUE_KW = ['issue date', 'issued', 'ngay cap', 'ngày cấp']
EXPIRY_KW = ['expiry', 'expires', 'expiration', 'valid until', 'het han', 'hết hạn', 'co gia tri den', 'có giá trị đến']
SEX_KW = ['sex', 'gender', 'gioi tinh', 'giới tính']
NATIONALITY_KW = ['nationality', 'quoc tich', 'quốc tịch']
PLACE_KW = ['place of birth', 'noi sinh', 'nơi sinh', 'place of issue', 'noi cap', 'nơi cấp']
NUMBER_KW = ['number', 'no.', 'so', 'số', 'id no', 'document no']


def _detect_type(text: str) -> Optional[str]:
    low = text.lower()
    for k in PASSPORT_KW:
        if k in low:
            return 'passport'
    for k in ID_KW:
        if k in low:
            return 'national_id'
    for k in DL_KW:
        if k in low:
            return 'driver_license'
    return None


def _parse_mrz(text: str) -> Optional[Dict[str, Any]]:
    """Parse MRZ (machine readable zone) if present - most reliable."""
    lines = [l.strip() for l in text.splitlines() if MRZ_LINE.match(l.strip())]
    if len(lines) < 2:
        return None
    # TD3 (passport) has 2 lines of 44 chars
    if len(lines[0]) == 44 and len(lines[1]) == 44:
        l1, l2 = lines[0], lines[1]
        try:
            passport_num = l2[0:9].replace('<', '').strip()
            nationality = l2[10:13].replace('<', '').strip()
            dob_raw = l2[13:19]
            sex = l2[20:21]
            expiry_raw = l2[21:27]
            names_field = l1[5:44]
            # parse names: SURNAME<<GIVEN<NAMES
            if '<<' in names_field:
                surname, given = names_field.split('<<', 1)
                name = given.replace('<', ' ').strip() + ' ' + surname.replace('<', ' ').strip()
            else:
                name = names_field.replace('<', ' ').strip()
            def mrz_date(s):
                if len(s) != 6 or not s.isdigit():
                    return None
                yy, mm, dd = int(s[0:2]), int(s[2:4]), int(s[4:6])
                yyyy = 2000 + yy if yy < 50 else 1900 + yy
                return f'{yyyy:04d}-{mm:02d}-{dd:02d}'
            return {
                'name': name or None,
                'document_number': passport_num or None,
                'nationality': nationality or None,
                'date_of_birth': mrz_date(dob_raw),
                'sex': 'M' if sex == 'M' else ('F' if sex == 'F' else None),
                'expiry_date': mrz_date(expiry_raw),
                'mrz_detected': True,
            }
        except Exception:
            pass
    return None


def _find_field(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        low = line.lower()
        if any(k in low for k in keywords):
            if ':' in line:
                v = line.split(':', 1)[1].strip()
                if v and len(v) > 1:
                    return v[:120]
    return None


def _find_date(text: str, keywords: List[str]) -> Optional[str]:
    for line in text.splitlines():
        if any(k in line.lower() for k in keywords):
            d = _dates_in_window(line)
            if d:
                return d
    return None


def extract_id_document_heuristic(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    text = text.replace('\r\n', '\n')
    doc_type = _detect_type(text)
    mrz = _parse_mrz(text)

    if mrz:
        return {
            'document_type': doc_type or 'passport',
            'name': mrz.get('name'),
            'document_number': mrz.get('document_number'),
            'nationality': mrz.get('nationality'),
            'date_of_birth': mrz.get('date_of_birth'),
            'sex': mrz.get('sex'),
            'issue_date': None,
            'expiry_date': mrz.get('expiry_date'),
            'place_of_birth': None,
            'place_of_issue': None,
            'mrz_detected': True,
            'confidence': 0.95,
            'warning': 'Auto-extracted. Verify against physical document before use.',
        }

    name = _find_field(text, NAME_KW)
    doc_num = _find_field(text, NUMBER_KW)
    dob = _find_date(text, DOB_KW)
    issue = _find_date(text, ISSUE_KW)
    expiry = _find_date(text, EXPIRY_KW)
    sex = _find_field(text, SEX_KW)
    nationality = _find_field(text, NATIONALITY_KW)
    place_birth = _find_field(text, PLACE_KW)

    filled = sum(1 for x in [name, doc_num, dob, expiry, nationality] if x)
    conf = round(min(1.0, filled / 5.0) * 0.8, 2)

    return {
        'document_type': doc_type,
        'name': name,
        'document_number': doc_num,
        'nationality': nationality,
        'date_of_birth': dob,
        'sex': sex,
        'issue_date': issue,
        'expiry_date': expiry,
        'place_of_birth': place_birth,
        'place_of_issue': None,
        'mrz_detected': False,
        'confidence': conf,
        'warning': 'Auto-extracted. Verify against physical document before use.',
    }
