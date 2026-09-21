"""FastAPI app: Invoice -> JSON extraction API for RapidAPI listing."""
import os
import time
import base64
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from app.schemas import ExtractRequest, ExtractResponse, Invoice
from app.llm import extract_invoice

app = FastAPI(title="Invoice Extraction API", version="1.0.0")

PROXY_SECRET = os.getenv("RAPIDAPI_PROXY_SECRET", "").strip()


@app.middleware("http")
async def check_rapidapi_secret(request: Request, call_next):
    if PROXY_SECRET and request.url.path not in ("/health", "/docs", "/openapi.json"):
        secret = request.headers.get("X-RapidAPI-Proxy-Secret", "")
        if secret != PROXY_SECRET:
            return JSONResponse(status_code=401, content={"detail": "Invalid RapidAPI proxy secret"})
    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok", "ts": int(time.time())}


@app.get("/")
def root():
    return {
        "name": "Invoice Extraction API",
        "version": "1.0.0",
        "endpoints": {
            "POST /v1/invoice/extract": "Extract structured data from invoice text",
            "POST /v1/invoice/extract/base64": "Extract from base64-encoded PDF/image",
            "GET /health": "Health check",
        },
    }


def _prepare_content(req: ExtractRequest) -> str:
    c = req.content
    if req.content_type == "text":
        return c
    if req.content_type in ("base64_pdf", "base64_image"):
        if "," in c[:50]:
            c = c.split(",", 1)[1]
        try:
            raw = base64.b64decode(c)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64: {e}")
        return raw.decode("utf-8", errors="ignore")[:20000]
    raise HTTPException(status_code=400, detail=f"Unsupported content_type: {req.content_type}")


@app.post("/v1/invoice/extract", response_model=ExtractResponse)
def extract_text(req: ExtractRequest):
    if not req.content or len(req.content) < 10:
        raise HTTPException(status_code=400, detail="content too short")
    text = _prepare_content(req)
    try:
        parsed, model, ms = extract_invoice(text, req.language)
    except Exception as e:
        return ExtractResponse(success=False, error=str(e), model="n/a", processing_ms=0)
    try:
        inv = Invoice(**parsed)
    except Exception as e:
        return ExtractResponse(success=False, error=f"schema validation failed: {e}", model=model, processing_ms=ms)
    return ExtractResponse(success=True, invoice=inv, model=model, processing_ms=ms)


@app.post("/v1/invoice/extract/base64", response_model=ExtractResponse)
def extract_b64(req: ExtractRequest):
    req.content_type = "base64_pdf"
    return extract_text(req)
