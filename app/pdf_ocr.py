"""PDF/image -> text extraction. Uses pdfplumber for PDFs, pytesseract for images.
All optional: if not installed, returns empty string and caller falls back to raw decode.
"""
import base64
import io
from typing import Optional


def _try_pdfplumber(data: bytes) -> Optional[str]:
    try:
        import pdfplumber
    except ImportError:
        return None
    try:
        parts = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages[:20]:
                t = page.extract_text() or ''
                parts.append(t)
        text = '\n'.join(parts).strip()
        return text or None
    except Exception:
        return None


def _try_pil_tesseract(data: bytes) -> Optional[str]:
    try:
        from PIL import Image
        import pytesseract
    except ImportError:
        return None
    try:
        img = Image.open(io.BytesIO(data))
        text = pytesseract.image_to_string(img)
        return text.strip() or None
    except Exception:
        return None


def decode_to_text(b64_or_datauri: str) -> str:
    """Decode base64 (optionally data URI) and return extracted text.
    Order: PDF -> image OCR -> utf-8 raw decode."""
    c = b64_or_datauri
    if ',' in c[:80] and c.strip().startswith('data:'):
        c = c.split(',', 1)[1]
    try:
        data = base64.b64decode(c, validate=False)
    except Exception:
        return ''

    # PDF magic
    if data[:4] == b'%PDF':
        t = _try_pdfplumber(data)
        if t:
            return t[:20000]
        return ''

    # Image magic
    IMG_MAGIC = (b'\x89PNG', b'\xff\xd8\xff', b'GIF87a', b'GIF89a', b'RIFF', b'BM')
    if any(data.startswith(m) for m in IMG_MAGIC):
        t = _try_pil_tesseract(data)
        if t:
            return t[:20000]
        return ''

    # Fallback: treat as text
    try:
        return data.decode('utf-8', errors='ignore')[:20000]
    except Exception:
        return ''
