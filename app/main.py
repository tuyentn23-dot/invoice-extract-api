"""FastAPI app: Document extraction API for RapidAPI listing."""
import os
import time
import base64
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from app.schemas import ExtractRequest, ExtractResponse, Invoice
from app.llm import extract_invoice
from app.receipt import extract_receipt_heuristic
from app.resume import extract_resume_heuristic

app = FastAPI(title="Document Extraction API", version="1.1.0")

PROXY_SECRET = os.getenv("RAPIDAPI_PROXY_SECRET", "").strip()


@app.middleware("http")
async def check_rapidapi_secret(request: Request, call_next):
    if PROXY_SECRET and request.url.path not in ("/health", "/docs", "/openapi.json", "/redoc"):
        secret = request.headers.get("X-RapidAPI-Proxy-Secret", "")
        if secret != PROXY_SECRET:
            return JSONResponse(status_code=401, content={"detail": "Invalid RapidAPI proxy secret"})
    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok", "ts": int(time.time()), "version": "1.1.0"}


@app.get("/")
def root():
    return {
        "name": "Document Extraction API",
        "version": "1.1.0",
        "endpoints": {
            "POST /v1/invoice/extract": "Invoice text -> structured JSON",
            "POST /v1/invoice/extract/base64": "Invoice (base64 PDF/image) -> JSON",
            "POST /v1/receipt/extract": "Receipt text -> structured JSON",
            "POST /v1/resume/extract": "Resume/CV text -> structured JSON",
            "GET /health": "Health check",
            "GET /docs": "OpenAPI UI",
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
def extract_invoice_text(req: ExtractRequest):
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
def extract_invoice_b64(req: ExtractRequest):
    req.content_type = "base64_pdf"
    return extract_invoice_text(req)


@app.post("/v1/receipt/extract")
def extract_receipt(req: ExtractRequest):
    if not req.content or len(req.content) < 10:
        raise HTTPException(status_code=400, detail="content too short")
    t0 = time.time()
    text = _prepare_content(req)
    try:
        parsed = extract_receipt_heuristic(text, req.language)
    except Exception as e:
        return {"success": False, "error": str(e), "model": "heuristic:v1", "processing_ms": 0}
    ms = int((time.time() - t0) * 1000)
    return {"success": True, "receipt": parsed, "error": None, "model": "heuristic:v1", "processing_ms": ms}


@app.post("/v1/resume/extract")
def extract_resume(req: ExtractRequest):
    if not req.content or len(req.content) < 20:
        raise HTTPException(status_code=400, detail="content too short")
    t0 = time.time()
    text = _prepare_content(req)
    try:
        parsed = extract_resume_heuristic(text, req.language)
    except Exception as e:
        return {"success": False, "error": str(e), "model": "heuristic:v1", "processing_ms": 0}
    ms = int((time.time() - t0) * 1000)
    return {"success": True, "resume": parsed, "error": None, "model": "heuristic:v1", "processing_ms": ms}
