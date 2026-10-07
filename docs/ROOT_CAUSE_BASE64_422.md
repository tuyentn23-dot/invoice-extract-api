# Root Cause: 422 on /v1/*/extract/base64

Date: 2026-10-07 
Status: FIXED (pending deploy) 

## Symptom
POST /v1/invoice/extract/base64 returns 422 {"detail":"Could not extract text from base64"} for a valid A4 invoice image.

## Chain of causes
1. app/pdf_ocr.py::decode_to_text detects image magic, calls _try_pil_tesseract.
2. _try_pil_tesseract uses pytesseract, which requires the Tesseract OCR system binary.
3. Dockerfile never installed tesseract-ocr. render.yaml used runtime: python, so the Dockerfile was ignored entirely on Render.
4. pytesseract raises TesseractNotFoundError -> caught -> returns None -> decode_to_text returns "".
5. app/main.py::_prepare_content raises HTTPException(422, "Could not extract text from base64").

## NOT the cause
- The request field name. Base64 endpoints take {"content": "<b64>", "content_type": "base64_image"}, not file_base64. Passing file_base64 yields a schema 422 (field required: content), a different error.

## Fix applied
- Dockerfile: apt-get install tesseract-ocr tesseract-ocr-eng poppler-utils; CMD honors $PORT.
- render.yaml: runtime: docker + dockerfilePath: ./Dockerfile.
- app/pdf_ocr.py: added ocr_status() diagnostic (tesseract import/binary/version, pdfplumber, pillow).
- app/main.py: /health now includes "ocr": ocr_status().

## How to verify after deploy

curl https://invoice-extract-api-4eq9.onrender.com/health
# expect: "ocr":{"pytesseract_import":true,"tesseract_binary":true,...}

If tesseract_binary is still false, the deploy did not pick up the Docker runtime.
