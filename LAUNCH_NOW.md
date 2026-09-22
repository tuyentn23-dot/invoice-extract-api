# LAUNCH NOW — Copy paste theo thứ tự

**URL API:** https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1

**Nguyên tắc:** Đăng 1 chỗ, đợi 2 giờ, xem phản hồi, mới đăng chỗ tiếp. KHÔNG spam cùng lúc.

---

## 1. HACKER NEWS (đăng đầu tiên — impact cao nhất)

**Vào:** https://news.ycombinator.com/submit

**Title:**
```
Show HN: Document extraction API – invoice/receipt/resume to JSON
```

**URL:**
```
https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
```

**Text (optional):**
```
Built this because I kept writing the same invoice-parsing code on every project. Decided to make it a public API instead.

Four endpoints: invoice, receipt, resume, bank statement. Text in, structured JSON out. Bilingual (English + Vietnamese).

The base path runs a regex heuristic engine – no LLM call, sub-second response, zero ongoing cost. Falls back to an LLM only when the heuristic can't parse something clean.

Built solo in a weekend. Deployed on Render free tier. Billing handled by RapidAPI.

Would love feedback on: (1) missing fields, (2) other document types worth adding, (3) heuristic vs LLM tradeoffs.
```

**Sau khi submit:** Reply mọi comment trong 2 giờ đầu. Không spam, không defensive.

---

## 2. REDDIT r/SaaS (đăng 2h sau HN)

**Vào:** https://www.reddit.com/r/SaaS/submit

**Title:**
```
I built a document extraction API solo in a weekend – invoice/receipt/resume → JSON
```

**Body:**
```
I kept rewriting invoice parsing code on every project, so I made it a public API instead.

What it does:
- 4 endpoints: invoice, receipt, resume, bank statement
- Text or base64 PDF/image in → clean JSON out
- Bilingual (EN + VI)
- Free tier: 500 calls/month
- Response < 1s typical

How it works:
- Regex heuristic engine first (zero LLM cost, sub-second)
- Falls back to LLM only when regex fails
- FastAPI + Pydantic, deployed on Render free tier
- RapidAPI handles billing

What it doesn't do:
- No dashboard UI
- OCR on the free tier requires clean text (base64 works but needs pdfplumber/pytesseract installed server-side)

Would love feedback on what fields you'd actually need, and which document types to add next.

Link: https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
```

---

## 3. REDDIT r/webdev (đăng 4h sau r/SaaS)

**Title:**
```
Made a small API for extracting structured data from documents (invoice/receipt/resume)
```

**Body:** Copy từ r/SaaS ở trên, đổi câu cuối thành:
```
Feedback welcome on the heuristic-first approach vs going straight to an LLM.
```

---

## 4. TWITTER/X (đăng cùng ngày)

```
Launched a small API: invoice, receipt, resume, bank statement → clean JSON.

Bilingual EN/VI. Response < 1s. Free tier 500 calls/mo.

Built solo + AI in a weekend, deployed for $0.

https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1
```

---

## 5. INDIEE HACKERS (đăng trong tuần)

**Vào:** https://www.indiehackers.com/new-post

**Title:**
```
Document extraction API – $0 to launch, aiming for $100 MRR
```

**Body:**
```
Weekend project. Built 4 document extraction endpoints (invoice/receipt/resume/bank statement).

Stack: FastAPI + heuristic regex engine (no LLM for base path), RapidAPI for billing, Render free tier for hosting. Total cost so far: $0.

Goal: $100 MRR. Current: $0 (just launched).

Plan:
- W1: launch, measure
- W2-4: add 2 more endpoints if traction
- M2: if 1+ paying subscriber, expand

Will post updates.

Link in comments.
```

---

## Thứ tự thực hiện

**Hôm nay:**
1. Hacker News (bây giờ)
2. Reply comment HN trong 2h

**Sau 2h:**
3. r/SaaS
4. Reply comment

**Tối:**
5. Twitter/X

**Mai:**
6. r/webdev
7. Indie Hackers

---

## Đo lường

Sau 24h, mở RapidAPI dashboard → Analytics:
- Xem **Test calls** (số request)
- Xem **Subscribers** (số người dùng free tier)

Paste số liệu vào đây, tôi sẽ phân tích và đề xuất bước tiếp.

---

## KHÔNG nên làm

- ❌ Đăng cùng lúc 5 chỗ (bị flag spam)
- ❌ DM người lạ
- ❌ Mua upvote
- ❌ Đổi title thành clickbait
- ❌ Nói "AI-powered" nếu base path là heuristic
