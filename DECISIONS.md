# DECISIONS — Invoice to JSON Extractor

Quyết định đã đưa ra, lý do, và trade-off. Phiên sau đọc để không lặp lại thảo luận.

---

## D001 — Chọn RapidAPI làm nền tảng (2026-09-22)

**Quyết định:** List API trên RapidAPI, không tự làm SaaS riêng.

**Lý do:**
- RapidAPI có 4M+ devs search nội bộ → không cần marketing
- Billing native → không cần Stripe/Gumroad
- Free đăng ký, chỉ lấy 25% doanh thu
- Buyer tự phục vụ, không cần support khách

**Trade-off:**
- Phí 25% cao
- Payout PayPal chậm (6-8 tuần)
- Phụ thuộc nền tảng

**Loại bỏ:** ClawHub (không billing), Chrome Extension (effort cao), AgenticTrade (quá mới)

---

## D002 — Document extraction làm ngách chính (2026-09-22)

**Quyết định:** Tập trung vào invoice/receipt/resume/bank statement, sau mở rộng lên 10 loại tài liệu.

**Lý do:**
- AI agent (LLM + regex) làm rất tốt
- Buyer trả giá cao ($0.01-0.10/call vs $0.0001 cho utility)
- Nhu cầu B2B thật (mọi công ty có hóa đơn)
- Có thể build 10+ biến thể từ cùng hạ tầng

**Loại bỏ:** Weather, crypto price, IP geolocation (bão hòa)

---

## D003 — Heuristic-first, LLM-fallback (2026-09-22)

**Quyết định:** Regex engine chạy trước, LLM chỉ khi cần.

**Lý do:**
- $0 ongoing cost cho 70% case
- Response <1s (nhanh hơn LLM)
- Không phụ thuộc API key của provider
- LLM key của user hiện bị 402/403, không dùng được

**Trade-off:**
- Độ chính xác thấp hơn pure-LLM ở case phức tạp
- Cần maintain regex patterns

---

## D004 — Không crypto/AI edge, mở rộng mọi ngách (2026-09-22)

**Quyết định:** Bỏ giới hạn "chỉ crypto", mở sang mọi ngành có nhu cầu document extraction.

**Lý do:**
- Crypto = thị trường nhỏ, nhiều regulation
- Document = thị trường lớn, ổn định
- AI agent build được mọi loại extraction

---

## D005 — Tạo 1 API với 16 endpoints thay vì 6 API riêng (2026-09-22)

**Quyết định:** Nhồi tất cả extractors vào cùng API `invoice-to-json-extractor1`.

**Lý do:**
- Tăng surface trên Hub search (16 điểm chạm)
- Chỉ cần 1 lần setup pricing, 1 lần billing
- 1 subscriber trả tiền dùng được cả 16 endpoints

**Trade-off:**
- Tên "Invoice to JSON Extractor" không còn đúng (chỉ là 1/10 loại)
- Có thể đổi tên sau khi có traffic

---

## D006 — Không spam Reddit/HN bằng automation (2026-09-22)

**Quyết định:** Dừng launch qua Reddit và HN sau 3 lần bị remove.

**Lý do:**
- r/SaaS, r/webdev: AutoMod remove vì account <3 tháng
- r/documentAutomation: Reddit **site-wide filter** remove
- HN: block Show HN với account 1 karma
- Cố tiếp = risk ban account

**Kết luận:** Chờ 2-3 tháng build karma, không cố launch bằng account mới.

---

## D007 — Tray monitor thay vì dashboard web (2026-09-22)

**Quyết định:** App system tray (pystray) thay vì web dashboard.

**Lý do:**
- Không cần deploy thêm service
- Chạy ngay trên máy user
- Notification tự nhiên hơn
- Không tốn GPU/RAM

**Trade-off:**
- Chỉ chạy khi user bật máy
- Phụ thuộc Chrome CDP
- Không share được cho team

---

## D008 — OpenAPI 3.0.3 force override (2026-09-22)

**Quyết định:** Convert spec từ 3.1.0 (FastAPI default) xuống 3.0.3.

**Lý do:** RapidAPI chỉ nhận OpenAPI 3.0.x. FastAPI sinh 3.1.0 với `type: [X, "null"]` và `servers` — RapidAPI từ chối.

**Giải pháp:** `app/openapi_compat.py` — recursive transformer: `anyOf: [X, null]` → `nullable: true`.

---

## D009 — Không thêm proxy secret ngay (2026-09-22)

**Quyết định:** Trì hoãn cấu hình `RAPIDAPI_PROXY_SECRET`.

**Lý do:**
- Không ảnh hưởng khách hàng
- MVP exposure 1-3 ngày chấp nhận được
- Ưu tiên launch > security

**TODO:** Xem `SECURITY_TODO.md` — làm khi có thời gian.

---

## Quy tắc rút ra

1. **Platform có buyer tự tìm > tự marketing.** RapidAPI thắng Reddit/HN cho solo dev.
2. **Account mới không launch được.** Cần build history trước.
3. **Tăng surface bằng endpoints > nhiều API nhỏ.** 16 endpoints cùng billing tốt hơn 6 API riêng.
4. **Heuristic-first giảm chi phí.** LLM chỉ khi cần — cắt 70% chi phí inference.
5. **Đo trước khi build thêm.** Traffic là tín hiệu duy nhất để quyết định.
