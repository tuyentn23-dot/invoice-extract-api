# Pricing Audit — Invoice to JSON Extractor

Ngay: 2026-10-07 
Phuong phap: Playwright render trang pricing public (khong can dang nhap).

## Ket qua: Paid plans DA BAT, nhung dinh gia SAI

| Goi | Gia | Quota | Rate limit |
|---|---|---|---|
| Basic | $0.00/mo | 500,000 req/thang | 10 req/s |
| Pro | $9.00/mo | 500,000 req/thang | 20 req/s |
| Mega | $99.00/mo | 500,000 req/thang | 50 req/s |

## Van de
Ca 3 goi co CUNG quota 500k. Goi tra phi chi khac rate limit.
=> Khong co dong luc tra tien. Khach dung free 500k la du cho hau het use case.
=> Day la nguyen nhan chinh khien 0 subscriber.

## De xuat sua (dung nhu handoff P0.1)
| Goi | Gia | Quota | Rate limit |
|---|---|---|---|
| Basic (Free) | $0 | 500 req/thang | 5 req/s |
| Pro | $9.99/mo | 10,000 req/thang | 20 req/s |
| Mega | $49.00/mo | 100,000 req/thang | 50 req/s |

## Can lam
Vao RapidAPI Studio > API > Monetize > sua quota tung goi.
Yeu cau dang nhap RapidAPI.
