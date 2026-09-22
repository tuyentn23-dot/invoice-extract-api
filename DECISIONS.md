# DECISIONS — Nhật ký quyết định

> Mỗi quyết định lớn append 1 entry. Không sửa entry cũ.

---

## D001 — 2026-09-20: Loại 6 hướng, chọn RapidAPI

**Bối cảnh:** Cần dự án kiếm tiền thứ 2 sau khi trading không khả thi.

**Đã xem xét:**
1. Funding carry → 2.08%/năm, dưới ngân hàng ❌
2. Leverage → blown account ❌
3. Market making retail → spread 0.012bps < phí 2bps ❌
4. Apify sitemap-diff → commodity ❌
5. ClawHub → vòng lặp thu tiền đứt ❌
6. Airdrop → xổ số ❌

**Quyết định:** RapidAPI — vòng lặp khép kín, buyer tự tìm, billing native, AI agent build 100%.

**Lý do:** Chỉ RapidAPI thỏa mãn cả 3 điều kiện (discovery + billing + automation).

---

## D002 — 2026-09-21: Chọn document extraction

**Bối cảnh:** Nhiều ngách có thể làm trên RapidAPI.

**Đã so sánh:** Crypto data, weather, IP geo, validation, SEO, time utils, document extraction.

**Quyết định:** Document extraction (invoice/receipt/resume/bank statement).

**Lý do:**
- Nhu cầu B2B thật (kế toán, HR, fintech)
- Regex heuristic làm được → $0 cost
- Giá cao hơn utility ($9-99/tháng vs $0.0001/call)
- Ít API đủ tốt trên RapidAPI
- Bilingual EN/VI = lợi thế niche

---

## D003 — 2026-09-22: Heuristic regex first, LLM fallback

**Bối cảnh:** Có thể dùng LLM cho mọi request, hoặc regex, hoặc hybrid.

**Quyết định:** Hybrid — regex primary, LLM fallback khi confidence thấp.

**Lý do:**
- ~70% invoices theo 15 layout phổ biến, regex bắt được trong 40-60ms
- LLM cho mọi request → $0.001-0.01/call, không sustainable với free tier
- Fallback tự động khi regex fail → vẫn giữ accuracy cao
- Chi phí trung bình round về 0

**Trade-off:** Regex có thể bỏ sót edge case. Nhưng 95% request dùng regex, 5% escalate.

---

## D004 — 2026-09-22: Publish API public không set proxy secret trước

**Bối cảnh:** RapidAPI khuyến nghị set proxy secret để chặn bypass. Nhưng UI phức tạp, automation tắc.

**Quyết định:** Publish public ngay, set secret sau.

**Lý do:**
- Risk thấp với MVP mới chưa có traffic
- Ưu tiên launch để có dữ liệu
- Secret có thể set trong 2 phút thủ công bất kỳ lúc nào
- Nếu phát hiện abuse → set secret ngay

**Ghi chú:** TODO trong `SECURITY_TODO.md`.

---

## D005 — 2026-09-22: Không dùng HN (temporarily blocked)

**Bối cảnh:** HN đăng show HN bị redirect tới `/showlim` với thông báo "temporarily restricting Show HNs".

**Quyết định:** Bỏ qua HN lúc này. Tập trung Dev.to + Reddit + Twitter.

**Lý do:** Policy toàn cầu của HN, không thể bypass. Có thể thử lại sau 30 ngày.

---

## D006 — 2026-09-22: Build persistence layer trước khi build thêm API

**Bối cảnh:** Sau phiên 1-2, hệ thống đã phức tạp. Phiên mới cần biết ngay trạng thái.

**Quyết định:** Tạo MANIFEST.md + STATE.json + SESSION_LOG.md + DECISIONS.md + HANDOFF.md + tray app.

**Lý do:**
- Tránh mất context giữa các phiên
- AI agent phiên sau không cần đọc lại toàn bộ lịch sử
- Có single source of truth

---

<!-- Template:
## D00N — YYYY-MM-DD: <tiêu đề>

**Bối cảnh:** ...
**Quyết định:** ...
**Lý do:** ...
**Trade-off:** ...
-->