# Launch Kit — Copy & Paste khi API đã live

> **Điều kiện dùng:** Chỉ launch sau khi RapidAPI đã **APPROVED** và API có URL public.

---

## 1. Twitter/X (1 tweet, không cần thread)

```
Launched a small API today: invoice/receipt/resume/bank-statement -> clean JSON.

Bilingual EN/VI. Response < 1s. Free tier 50 calls/mo.

Built it solo + AI in a weekend. If you process documents, would love feedback.

<link>
```

---

## 2. Reddit r/SaaS

**Title:** I built a document extraction API solo — invoice/receipt/resume/bank statement → JSON

**Body:**
```
Background: I kept seeing "AI document extraction" startups raising money for something I thought could be a simple API. So I built it.

What it does:
- POST text → structured JSON
- Supports: invoices, receipts, resumes, bank statements
- Bilingual (English + Vietnamese)
- 4 endpoints, same auth
- Response typically < 1s
- Free tier: 50 calls/month

What it doesn't do:
- No UI dashboard (yet)
- No PDF text extraction on the free tier (base64 works but requires clean text)

Stack: FastAPI + heuristic engine that runs on $0. Not using GPT for the base path — the heuristic handles ~70% of typical cases, and I fall back to LLM only when needed.

Would love feedback on: (1) endpoints you'd actually use, (2) fields missing from the output.

<link>
```

---

## 3. Reddit r/Accounting hoặc r/smallbusiness

**Title:** Free tool: extract invoice data to JSON (no signup beyond RapidAPI)

**Body:**
```
Built this for my own side project. Extracts: invoice number, dates, vendor, VAT/tax ID, subtotal, tax, total, line items.

Bilingual EN/VI. Free tier 50 calls/month. Uses text input — paste invoice text, get JSON.

If anyone finds this useful, tell me what fields you'd need next.

<link>
```

---

## 4. Hacker News (Show HN)

**Title:** Show HN: Document extraction API — invoice/receipt/resume → JSON

**Body:**
```
Hi HN,

I built a document extraction API. Text in, structured JSON out. Four endpoints:

- /v1/invoice/extract
- /v1/receipt/extract
- /v1/resume/extract
- /v1/bank-statement/extract

Design notes:
- Runs a heuristic regex engine first (works without LLM keys, $0 ongoing cost)
- Falls back to an LLM only when heuristics fail
- Bilingual EN/VI
- FastAPI + pydantic, deployed on Render free tier
- RapidAPI handles billing, so no Stripe integration

Would love critique on the heuristic approach vs. pure LLM. Also: what other document types would be useful?

<API_URL>
```

---

## 5. Indie Hackers

**Title:** Building a document extraction API solo — $0 to start

**Body:**
```
Spent a weekend building this. Goal: hit $100 MRR as fast as possible, with zero upfront cost.

Plan:
- W1: launch on RapidAPI
- W2-4: measure, add 2 more endpoints
- M2-3: if 3+ paying subscribers, expand

Cost so far: $0.
Revenue so far: $0 (just launched).

Will post updates. Link in comments.
```

---

## 6. LinkedIn (nếu bạn có account, 1 post)

```
Built a small developer tool this weekend.

You send invoice text → get clean JSON back.
Same for receipts, resumes, bank statements.

Bilingual (EN/VI). Free tier. No UI, just an API.

If you build internal tools that process documents, this might save you a day of parsing code.

<link>
```

---

## 7. Discord / Telegram groups

Tìm và join:
- Indie Hackers Discord
- r/webdev Discord
- RapidAPI Discord
- FastAPI Discord

Post ngắn:
```
Made a small API: invoice/receipt/resume/bank-statement → JSON. Bilingual EN/VI. Free tier. Feedback welcome: <link>
```

---

## 8. Không nên làm

- Không spam DM người lạ
- Không post cùng nội dung nhiều subreddit cùng lúc (bị flag spam)
- Không claim "AI-powered" nếu đang chạy heuristic (nói thật là hybrid)
- Không hứa SLA / uptime trên free tier

---

## 9. Thứ tự launch

1. **Ngày 1:** Twitter + Indie Hackers + Show HN
2. **Ngày 2:** Reddit r/SaaS + r/smallbusiness + r/webdev
3. **Ngày 3:** Discord + LinkedIn
4. **Ngày 4-7:** Không post mới, chỉ reply comments
5. **Ngày 8:** Đo số subscriber, quyết định build API tiếp theo hay pivot

---

## 10. Chỉ số quan trọng

| Metric | Đo ở đâu | Ngưỡng tốt |
|---|---|---|
| Test calls | RapidAPI dashboard | ≥ 10/tuần |
| Subscribers free | RapidAPI | ≥ 50 |
| Subscribers paid | RapidAPI | ≥ 1 (tháng 1) |
| MRR | RapidAPI | ≥ $30 (tháng 1) |
| Churn | RapidAPI | < 20% |

Nếu sau 30 ngày MRR = $0 và test calls < 20 → chuyển hướng. Nếu có 1 subscriber trả tiền → tăng tốc build API #5, #6.
