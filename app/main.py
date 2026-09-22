"""FastAPI app: Document extraction API for RapidAPI listing.
Note: openapi_version forced to 3.0.3 for RapidAPI compatibility.
"""
import os
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from app.schemas import ExtractRequest, ExtractResponse, Invoice
from app.llm import extract_invoice
from app.receipt import extract_receipt_heuristic
from app.resume import extract_resume_heuristic
from app.bank_statement import extract_bank_statement_heuristic
from app.purchase_order import extract_purchase_order_heuristic
from app.contract import extract_contract_heuristic
from app.business_card import extract_business_card_heuristic
from app.utility_bill import extract_utility_bill_heuristic
from app.delivery_note import extract_delivery_note_heuristic
from app.id_document import extract_id_document_heuristic
from app.pdf_ocr import decode_to_text
from app.openapi_compat import to_3_0_3

VERSION = '2.0.0'
app = FastAPI(title='Invoice to JSON Extractor', version=VERSION)

PROXY_SECRET = os.getenv('RAPIDAPI_PROXY_SECRET', '').strip()


@app.middleware('http')
async def check_rapidapi_secret(request: Request, call_next):
    if PROXY_SECRET and request.url.path not in ('/health', '/docs', '/openapi.json', '/redoc'):
        secret = request.headers.get('X-RapidAPI-Proxy-Secret', '')
        if secret != PROXY_SECRET:
            return JSONResponse(status_code=401, content={'detail': 'Invalid RapidAPI proxy secret'})
    return await call_next(request)


@app.get('/health')
def health():
    return {'status': 'ok', 'ts': int(time.time()), 'version': VERSION}


@app.get('/')
def root():
    return {
        'name': 'Invoice to JSON Extractor',
        'version': VERSION,
        'endpoints': {
            'POST /v1/invoice/extract': 'Invoice -> JSON',
            'POST /v1/invoice/extract/base64': 'Invoice (base64 PDF/image) -> JSON',
            'POST /v1/receipt/extract': 'Receipt -> JSON',
            'POST /v1/receipt/extract/base64': 'Receipt (base64) -> JSON',
            'POST /v1/resume/extract': 'Resume/CV -> JSON',
            'POST /v1/resume/extract/base64': 'Resume (base64) -> JSON',
            'POST /v1/bank-statement/extract': 'Bank statement -> JSON',
            'POST /v1/bank-statement/extract/base64': 'Bank statement (base64) -> JSON',
            'POST /v1/purchase-order/extract': 'Purchase order -> JSON',
            'POST /v1/contract/extract': 'Contract key terms -> JSON',
            'POST /v1/business-card/extract': 'Business card -> JSON',
            'POST /v1/utility-bill/extract': 'Utility bill -> JSON',
            'POST /v1/delivery-note/extract': 'Delivery note -> JSON',
            'POST /v1/id-document/extract': 'ID document -> JSON',
            'GET /health': 'Health check',
            'GET /docs': 'OpenAPI UI',
        },
    }


def _prepare_content(req: ExtractRequest) -> str:
    c = req.content
    if req.content_type == 'text':
        return c
    if req.content_type in ('base64_pdf', 'base64_image'):
        text = decode_to_text(c)
        if not text:
            raise HTTPException(status_code=422, detail='Could not extract text from base64')
        return text
    raise HTTPException(status_code=400, detail=f'Unsupported content_type: {req.content_type}')


@app.post('/v1/invoice/extract', response_model=ExtractResponse, summary='Extract invoice fields to JSON')
def extract_invoice_text(req: ExtractRequest):
    if not req.content or len(req.content) < 10:
        raise HTTPException(status_code=400, detail='content too short')
    text = _prepare_content(req)
    try:
        parsed, model, ms = extract_invoice(text, req.language)
    except Exception as e:
        return ExtractResponse(success=False, error=str(e), model='n/a', processing_ms=0)
    try:
        inv = Invoice(**parsed)
    except Exception as e:
        return ExtractResponse(success=False, error=f'schema validation failed: {e}', model=model, processing_ms=ms)
    return ExtractResponse(success=True, invoice=inv, model=model, processing_ms=ms)


@app.post('/v1/invoice/extract/base64', response_model=ExtractResponse, summary='Extract invoice from base64 PDF/image')
def extract_invoice_b64(req: ExtractRequest):
    req.content_type = 'base64_pdf'
    return extract_invoice_text(req)


def _wrap(req: ExtractRequest, fn, key: str, min_len: int = 10):
    if not req.content or len(req.content) < min_len:
        raise HTTPException(status_code=400, detail='content too short')
    t0 = time.time()
    text = _prepare_content(req)
    try:
        parsed = fn(text, req.language)
    except Exception as e:
        return {'success': False, 'error': str(e), 'model': 'heuristic:v2', 'processing_ms': 0}
    ms = int((time.time() - t0) * 1000)
    return {'success': True, key: parsed, 'error': None, 'model': 'heuristic:v2', 'processing_ms': ms}


# --- RECEIPT ---
@app.post('/v1/receipt/extract', summary='Extract receipt fields to JSON')
def ep_receipt(req: ExtractRequest):
    return _wrap(req, extract_receipt_heuristic, 'receipt')

@app.post('/v1/receipt/extract/base64', summary='Extract receipt from base64')
def ep_receipt_b64(req: ExtractRequest):
    req.content_type = 'base64_pdf'; return ep_receipt(req)


# --- RESUME ---
@app.post('/v1/resume/extract', summary='Extract resume fields to JSON')
def ep_resume(req: ExtractRequest):
    return _wrap(req, extract_resume_heuristic, 'resume', min_len=20)

@app.post('/v1/resume/extract/base64', summary='Extract resume from base64')
def ep_resume_b64(req: ExtractRequest):
    req.content_type = 'base64_pdf'; return ep_resume(req)


# --- BANK STATEMENT ---
@app.post('/v1/bank-statement/extract', summary='Extract bank statement transactions')
def ep_bank(req: ExtractRequest):
    return _wrap(req, extract_bank_statement_heuristic, 'bank_statement', min_len=20)

@app.post('/v1/bank-statement/extract/base64', summary='Extract bank statement from base64')
def ep_bank_b64(req: ExtractRequest):
    req.content_type = 'base64_pdf'; return ep_bank(req)


# --- PURCHASE ORDER ---
@app.post('/v1/purchase-order/extract', summary='Extract purchase order fields to JSON')
def ep_po(req: ExtractRequest):
    return _wrap(req, extract_purchase_order_heuristic, 'purchase_order')


# --- CONTRACT ---
@app.post('/v1/contract/extract', summary='Extract contract key terms to JSON')
def ep_contract(req: ExtractRequest):
    return _wrap(req, extract_contract_heuristic, 'contract')


# --- BUSINESS CARD ---
@app.post('/v1/business-card/extract', summary='Extract business card fields to JSON')
def ep_card(req: ExtractRequest):
    return _wrap(req, extract_business_card_heuristic, 'business_card')


# --- UTILITY BILL ---
@app.post('/v1/utility-bill/extract', summary='Extract utility bill fields to JSON')
def ep_utility(req: ExtractRequest):
    return _wrap(req, extract_utility_bill_heuristic, 'utility_bill')


# --- DELIVERY NOTE ---
@app.post('/v1/delivery-note/extract', summary='Extract delivery note fields to JSON')
def ep_dn(req: ExtractRequest):
    return _wrap(req, extract_delivery_note_heuristic, 'delivery_note')


# --- ID DOCUMENT ---
@app.post('/v1/id-document/extract', summary='Extract ID document fields to JSON')
def ep_id(req: ExtractRequest):
    return _wrap(req, extract_id_document_heuristic, 'id_document', min_len=15)


# --- OpenAPI 3.0.3 for RapidAPI ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title='Invoice to JSON Extractor',
        version=VERSION,
        description=(
            'Extract structured JSON from 8 document types: invoice, receipt, resume, bank statement, '
            'purchase order, contract, business card, utility bill, delivery note, ID document. '
            'Bilingual EN/VI. Response typically under 1 second.'
        ),
        routes=app.routes,
    )
    schema = to_3_0_3(schema)
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
