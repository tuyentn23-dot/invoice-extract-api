# Deploy Guide — từ code đến tiền

## Bước 1: Push lên GitHub (5 phút)

1. Mở https://github.com/new
2. Tạo repo: `invoice-extract-api`, chọn **Public** (miễn phí)
3. **KHÔNG** tick "Add README" (vì đã có)
4. Trong terminal, chạy:
   ```
   cd D:/TNT_AI/venture_foundry/rapidapi_extract
   git remote add origin https://github.com/<USERNAME>/invoice-extract-api.git
   git branch -M main
   git push -u origin main
   ```

## Bước 2: Deploy lên Render (5 phút, miễn phí)

1. Mở https://render.com, đăng ký bằng GitHub
2. **New +** → **Web Service**
3. Chọn repo `invoice-extract-api`
4. Điền:
   - **Name:** `invoice-extract-api`
   - **Region:** Singapore (gần VN)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
5. **Create Web Service** → chờ 2-3 phút
6. Copy URL dạng: `https://invoice-extract-api.onrender.com`

**Test:** Mở `https://<your-url>/docs` → thấy Swagger UI là OK.

**Lưu ý Free tier:** Render sleep sau 15 phút không dùng. Lần gọi đầu chậm ~30s, sau đó nhanh. Đủ cho MVP.

## Bước 3: Đăng RapidAPI (10 phút)

1. Mở https://rapidapi.com → **Sign Up** (miễn phí, có thể login Google)
2. Vào https://rapidapi.com/provider → **Add New API**
3. **Import from OpenAPI** → paste URL:
   `https://<your-render-url>/openapi.json`
   (FastAPI tự sinh)
   Hoặc upload file `openapi.yaml` trong repo này
4. Điền listing:
   - **Name:** Invoice to JSON Extractor
   - **Category:** Data
   - **Description:** (copy từ README.md, phần "Long description")
   - **Base URL:** `https://<your-render-url>`
5. **RapidAPI Proxy Secret:**
   - Trong RapidAPI dashboard, vào tab **Settings** → copy `X-RapidAPI-Proxy-Secret`
   - Quay lại Render → Environment → thêm biến `RAPIDAPI_PROXY_SECRET` = giá trị đó
   - Render tự redeploy
6. **Pricing Plans:** tạo 4 gói (xem README.md)
7. **Publish** → chờ RapidAPI duyệt 1-3 ngày

## Bước 4: Sau khi live

- Test trên chính RapidAPI bằng "Test Endpoint"
- Chia sẻ link lên:
  - Reddit: r/SaaS, r/Accounting, r/smallbusiness
  - Indie Hackers
  - Twitter/X (không cần content phức tạp, chỉ link)
- Theo dõi dashboard RapidAPI → analytics → subscriber

## Ngưỡng thành công / dừng

- **7 ngày:** ≥ 10 test calls = có traction
- **30 ngày:** ≥ 3 subscriber trả tiền = tiếp tục mở rộng
- **30 ngày:** 0 subscriber = giữ API chạy nhưng chuyển sang build API #2 (Receipt)
- **90 ngày:** portfolio < $100/tháng = dừng RapidAPI, xem lại

## Chi phí

- GitHub: $0
- Render free tier: $0 (đủ cho MVP)
- RapidAPI: $0 (chỉ lấy 25% doanh thu)
- **Tổng chi phí ban đầu: $0**
