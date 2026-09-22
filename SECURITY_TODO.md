# SECURITY TODO — Proxy Secret

## Trạng thái hiện tại
- ✅ Backend Render: chưa set secret (vẫn nhận mọi request)
- ⚠️ RapidAPI: đã CÓ secret tự sinh, hiển thị ở:
  https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/definition/security
  → Mục: **X-RapidAPI-Proxy-Secret**

## Cách lấy secret (bạn làm, 20 giây)

1. Mở link trên
2. Tìm dòng **X-RapidAPI-Proxy-Secret:**
3. Bấm icon **con mắt** (👁) cạnh đó để hiện
4. Copy chuỗi đó (dạng: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` hoặc ngẫu nhiên)
5. **Paste vào chat cho tôi** — tôi sẽ ghi vào file `.proxy_secret` để không quên

## Cách set secret (2 phút)

### Bước A — Set trên Render
1. Mở https://dashboard.render.com
2. Chọn service `invoice-extract-api`
3. Tab **Environment** (sidebar trái)
4. **Add Environment Variable**:
   - Key: `RAPIDAPI_PROXY_SECRET`
   - Value: (secret vừa copy)
5. **Save Changes** → chờ 2 phút redeploy

### Bước B — Verify
```powershell
# Không có secret → 401
curl https://invoice-extract-api-4eq9.onrender.com/v1/invoice/extract `
  -X POST -H "Content-Type: application/json" `
  -d '{"content":"test"}'

# Qua RapidAPI → 200
# (dùng Playground trên RapidAPI Hub)
```

## Priority
**KHÔNG GẤP.** MVP chấp nhận exposure 1-3 ngày đầu. Ưu tiên hiện tại là LAUNCH.

## Checklist
- [ ] User copy proxy secret từ RapidAPI
- [ ] Set trên Render env
- [ ] Verify
- [ ] Xóa file `.proxy_secret` (không commit)
