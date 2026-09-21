"""Extraction pipeline: try LLM (if key works), else fall back to heuristic regex extractor."""
import os
import json
import time
import base64
from typing import Optional, Tuple

from app.heuristic import extract_invoice_heuristic


def _get_provider() -> Optional[Tuple[str, str, str]]:
    if os.getenv("DEEPSEEK_API_KEY"):
        return "deepseek", os.environ["DEEPSEEK_API_KEY"], "deepseek-chat"
    if os.getenv("GROQ_API_KEY"):
        return "groq", os.environ["GROQ_API_KEY"], "llama-3.3-70b-versatile"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini", os.environ["GEMINI_API_KEY"], "gemini-1.5-flash"
    return None


SYSTEM_PROMPT = """You are an invoice data extraction engine.
Given raw invoice text, extract structured fields and return ONLY valid JSON, no markdown, no commentary.

Schema:
{
  "invoice_number": string|null,
  "invoice_date": "YYYY-MM-DD"|null,
  "due_date": "YYYY-MM-DD"|null,
  "currency": "ISO4217"|null,
  "vendor_name": string|null,
  "vendor_tax_id": string|null,
  "vendor_address": string|null,
  "customer_name": string|null,
  "customer_tax_id": string|null,
  "customer_address": string|null,
  "subtotal": number|null,
  "tax_amount": number|null,
  "total": number|null,
  "line_items": [{"description": string, "quantity": number|null, "unit_price": number|null, "amount": number|null, "tax_rate": number|null}],
  "notes": string|null,
  "confidence": number (0-1)
}

Rules:
- Numbers must be numeric (not strings), no currency symbols.
- If a field is missing, use null.
- Dates must be ISO 8601. If format ambiguous, infer from context and lower confidence."""


USER_PROMPT_TEMPLATE = """Extract invoice fields from the following text. Language hint: {lang}.

---BEGIN INVOICE---
{content}
---END INVOICE---"""


def _call_openai_compatible(base_url: str, api_key: str, model: str, system: str, user: str, timeout: int = 45) -> str:
    import urllib.request
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        base_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def _strip_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return raw


def extract_invoice(raw_text: str, language: Optional[str] = None) -> Tuple[dict, str, int]:
    t0 = time.time()
    prov = _get_provider()
    if prov is not None:
        provider, api_key, model = prov
        user = USER_PROMPT_TEMPLATE.format(lang=language or "auto", content=raw_text[:15000])
        try:
            if provider in ("deepseek", "groq"):
                base = "https://api.deepseek.com/v1/chat/completions" if provider == "deepseek" else "https://api.groq.com/openai/v1/chat/completions"
                raw = _call_openai_compatible(base, api_key, model, SYSTEM_PROMPT, user)
            else:
                import urllib.request
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = {
                    "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                    "contents": [{"parts": [{"text": user}]}],
                    "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"},
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=45) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                raw = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(_strip_json(raw))
            ms = int((time.time() - t0) * 1000)
            return parsed, f"{provider}:{model}", ms
        except Exception:
            pass

    parsed = extract_invoice_heuristic(raw_text, language)
    ms = int((time.time() - t0) * 1000)
    return parsed, "heuristic:v1", ms
