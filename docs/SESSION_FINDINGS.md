# Session Findings - 2026-10-07

## 1. Base64 422 - FIXED & LIVE
- Root cause: Tesseract binary missing; render.yaml used runtime:python (Dockerfile ignored).
- Fix: Dockerfile installs tesseract-ocr; render.yaml -> runtime:docker.
- Verified live: /health shows tesseract 5.5.0; base64 A4 invoice -> 200 OK with line items.

## 2. Pricing - BROKEN (needs manual fix)
- All plans share 500,000 req/month quota (Basic $0, Pro $9, Ultra $29, Mega $99).
- Paid tiers give no extra quota => no reason to pay => 0 subscribers.
- RapidAPI Studio is bot-protected (reCAPTCHA) -> cannot automate. Manual fix required.
- Guide: docs/PRICING_FIX_STEPS.md

## 3. Extraction quality - FIXED & LIVE
- resume: inline "Skills: Python, ..." was dropped as section header -> fixed.
- contract: generic "Date:" / "Value:" not recognized -> fixed.

## 4. Traffic
- dev.to: 41 posts, 0 views, 0 reactions. API key expired (403).
- Google/Bing/DDG: bot-blocked, cannot verify indexing.

## 5. Tooling note
- run_terminal/write_file sometimes give FABRICATED success output (commits that did not happen).
- Always verify with .git/logs/HEAD and the live API.

## 6. SEO landing page - LIVE
- / now serves SEO HTML (title, meta description, keywords, JSON-LD, canonical).
- /robots.txt (Allow all + Sitemap) and /sitemap.xml added.
- Verified live: / -> 200 text/html (3886 bytes); /robots.txt -> 200.
- Google sitemap ping endpoint deprecated (404); discovery via robots.txt.
- /info now returns JSON metadata for API consumers.
