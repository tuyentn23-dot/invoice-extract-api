# SECURITY TODO — Set proxy secret (không gấp, làm trong 24h)

## Vấn đề
Backend Render hiện đang exposed: ai biết URL `invoice-extract-api-4eq9.onrender.com` đều có thể gọi trực tiếp, không qua RapidAPI, không tốn quota.

## Cách fix (3 phút)

### Bước 1: Đặt secret trên Render
1. Vào https://dashboard.render.com
2. Chọn service `invoice-extract-api`
3. Tab **Environment** (sidebar trái)
4. **Add Environment Variable**:
   - Key: `RAPIDAPI_PROXY_SECRET`
   - Value: (dán bất kỳ chuỗi ngẫu nhiên 32+ ký tự, ví dụ dùng lệnh dưới)
5. Bấm **Save Changes** → chờ 2 phút redeploy

### Bước 2: Cấu hình RapidAPI gửi secret đó
1. Vào https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/definition/versions/apiversion_8cc32ff6-a203-49ad-ad16-ee4eb9c5a946/security
2. Tìm mục **Proxy Secret** (hoặc **Security > Secret Headers**)
3. Bật **RapidAPI Proxy Secret** → dán CÙNG giá trị đã đặt ở Render
4. Save

### Bước 3: Verify
```powershell
# Gọi trực tiếp không có secret → phải trả 401
curl https://invoice-extract-api-4eq9.onrender.com/v1/invoice/extract `
  -X POST -H "Content-Type: application/json" `
  -d '{"content":"Invoice #: X\nDate: 2024-01-01\nTotal: 100"}'
# Expected: 401 Invalid RapidAPI proxy secret

# Gọi qua RapidAPI → phải trả 200
# (dùng Playground hoặc API key của subscriber)
```

## Tạo secret ngẫu nhiên

Mở PowerShell:
```powershell
-join ((48..57) + (97..122) | Get-Random -Count 40 | ForEach-Object {[char]$_})
```

## Trạng thái
- [ ] Render env var set
- [ ] RapidAPI proxy secret configured  
- [ ] Verified (direct = 401, via RapidAPI = 200)

## Ghi chú
Trong lúc chưa set, API vẫn hoạt động bình thường qua RapidAPI. Chỉ là risk có người bypass quota. MVP có thể chấp nhận trong 1-2 ngày đầu để đo traffic thật.
