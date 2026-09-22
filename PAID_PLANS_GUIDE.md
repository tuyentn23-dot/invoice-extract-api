# Hướng dẫn tạo 3 gói trả phí (5 phút, làm khi rảnh)

## Không gấp
API đã live với gói **BASIC (Free, 500 req/tháng)**. User đầu tiên sẽ dùng free để thử. Paid plans có thể thêm bất kỳ lúc nào — RapidAPI cho phép thêm/sửa plan ngay cả khi API đang chạy.

## Cách vào đúng trang

### Cách 1 (nhanh nhất)
1. Mở https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/definition/plans
2. Nhìn dòng chữ xanh: *"Monetization functionality is deprecated in Provider Dashboard. Please use the new UI experience."*
3. **Bấm vào "new UI experience"** → nó mở đúng trang tạo plans

### Cách 2 (thủ công)
1. Vào https://rapidapi.com/hub
2. Góc phải trên, bấm **Studio**
3. Trong Studio, tìm **Invoice to JSON Extractor** → bấm vào
4. Sidebar: **Hub Listing** → **Monetize** → **Public Plans**
5. Thấy gói BASIC → bấm **Add Plan**

### Cách 3 (nếu 2 cách trên không được)
1. Vào https://rapidapi.com/provider/12332384/apis/invoice-to-json-extractor1/definition
2. Tab **Plans & Pricing** (sidebar trên cùng)
3. Bấm nút **Switch to new experience** hoặc **Open Studio**

## Thông số 3 gói

### GÓI PRO
| Field | Giá trị |
|---|---|
| Plan name | `Pro` |
| Plan Type | Monthly Subscription |
| Subscription Price | `$9` |
| Tiers → requests/month | `2,000` |
| Rate Limit | `10` requests/second |
| Overage price | `$0.01` per request |
| Require approval | ❌ Tắt |
| Recommended Plan | ✅ BẬT |

### GÓI ULTRA
| Field | Giá trị |
|---|---|
| Plan name | `Ultra` |
| Plan Type | Monthly Subscription |
| Subscription Price | `$29` |
| Tiers → requests/month | `15,000` |
| Rate Limit | `20` requests/second |
| Overage price | `$0.005` per request |
| Require approval | ❌ Tắt |
| Recommended Plan | ❌ Tắt |

### GÓI MEGA
| Field | Giá trị |
|---|---|
| Plan name | `Mega` |
| Plan Type | Monthly Subscription |
| Subscription Price | `$99` |
| Tiers → requests/month | `100,000` |
| Rate Limit | `50` requests/second |
| Overage price | `$0.002` per request |
| Require approval | ❌ Tắt |
| Recommended Plan | ❌ Tắt |

## Sau khi tạo

- Bấm **Save** cho mỗi gói
- Verify: mở https://rapidapi.com/tuyentn23/api/invoice-to-json-extractor1/pricing
- Phải thấy 4 gói: Basic (Free), Pro ($9), Ultra ($29), Mega ($99)

## Nếu gặp khó

Chụp màn hình paste vào đây. Tôi sẽ chỉ chính xác cần điền vào đâu dựa trên giao diện thực tế của bạn.

## Timeline

**Không gấp.** Ưu tiên hiện tại là LAUNCH để có user. Plans sau 3-7 ngày khi có traffic thật.
