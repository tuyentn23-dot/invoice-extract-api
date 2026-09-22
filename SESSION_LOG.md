# SESSION LOG

> Mỗi phiên làm việc append 1 entry ở đây. Không sửa entry cũ.

---

## 2026-09-22 — Phiên 1: Khởi tạo dự án

**Đã làm:**
- Chọn hướng RapidAPI + document extraction (sau khi loại 6 hướng khác)
- Build FastAPI backend với 4 extractors: invoice, receipt, resume, bank statement
- Viết heuristic regex engine (không cần LLM, $0 ongoing)
- LLM fallback qua DeepSeek/Groq/Gemini (tự động nếu có key)
- Test suite 29 checks, all pass
- Deploy Render free tier
- Fix OpenAPI 3.1 → 3.0.3 để RapidAPI import được
- Upload 10 endpoints lên RapidAPI
- Set visibility Public

**Phát hiện:**
- RapidAPI UI rất phức tạp, OneTrust cookie banner chặn automation
- Cần dùng Chrome thật với `--remote-debugging-port` cho OAuth Google
- Upload spec cần click đúng Save trong upload form

**Việc còn lại:**
- Launch Twitter/LinkedIn/IndieHackers
- Set proxy secret
- Monitoring tự động

---

## 2026-09-22 — Phiên 2: Launch và Monitoring

**Đã làm:**
- Đăng Dev.to article: https://dev.to/tuyentn23dot/i-built-a-document-extraction-api-that-runs-on-regex-no-llm-needed-3b0g
- Đăng Reddit r/SaaS (user confirm)
- HackerNews: bị block tạm thời (policy "massive influx")
- Build monitoring script: `scripts/monitor.py`, `scripts/report.py`
- PowerShell wrapper: `scripts/daily_monitor.ps1`
- Baseline metrics: 0 calls, 0 subscribers

**Phát hiện:**
- Reddit account cần karma để post ở subreddit lớn
- HN đang tạm chặn Show HN
- Dev.to không có karma gate, publish thành công ngay

**Việc còn lại:**
- Twitter/X, LinkedIn, Indie Hackers
- Set proxy secret
- Setup Task Scheduler

---

## 2026-09-22 — Phiên 3: Persistence system

**Đã làm:**
- Tạo `MANIFEST.md`, `STATE.json`, `HANDOFF.md`, `SESSION_LOG.md`, `DECISIONS.md`
- Tạo tray mini-app (sẽ hoàn thành sau)

**Lý do:**
- User yêu cầu cơ chế để phiên sau luôn nhớ hệ thống đang có gì, làm từ đâu

**Việc còn lại:**
- Hoàn thành tray app
- Test tray app khởi động cùng Windows
- Set proxy secret

---

<!-- Template cho entry mới — copy từ đây xuống:

## YYYY-MM-DD — Phiên N: <mô tả ngắn>

**Đã làm:**
- 

**Phát hiện:**
- 

**Việc còn lại:**
- 

-->
