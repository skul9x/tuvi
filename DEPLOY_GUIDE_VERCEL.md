# Hướng Dẫn Deploy Lên Vercel 🚀

Anh làm theo các bước sau nhe, cực dễ:

## 1. Chuẩn bị trên Vercel
1.  Truy cập [vercel.com](https://vercel.com) và đăng nhập (bằng GitHub cho tiện).
2.  Bấm nút **"Add New..."** -> **"Project"**.
3.  Chọn repo **`tuvi-main`** (hoặc tên repo anh đã push lên GitHub).
4.  Bấm **Import**.

## 2. Cấu hình Biến Môi Trường (Quan trọng 🔴)
Trong màn hình "Configure Project", tìm mục **Environment Variables**.
Anh copy 2 dòng trong file `web/.env.local` và paste vào đây:

| Key | Value (Lấy từ Supabase) |
|-----|-------------------------|
| `NEXT_PUBLIC_SUPABASE_URL` | `https://...supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJ...` (cái key dài ngoằng) |
| `GEMINI_API_KEY` | `AIza...` (Key của Google Gemini) |

> **Lưu ý**: Nhớ Add đủ 3 cái này nhé anh. Thiếu 1 cái là app không chạy đâu.

## 3. Bấm Deploy
1.  Bấm **Deploy**.
2.  Chờ khoảng 2 phút... ☕
3.  Khi nào pháo giấy bắn bùm bùm là xong!

## 4. Cập nhập lại CORS & URL Bảo Vệ (Sau khi có link thật)
Sau khi deploy, Vercel sẽ cấp cho anh 1 cái link (ví dụ: `https://tuvi-xyz.vercel.app`).
Anh quay lại dashboard Supabase:
1.  Vào **Authentication** -> **URL Configuration**.
2.  Thêm link Vercel vào **Site URL** và **Redirect URLs**.
3.  (Tùy chọn) Vào file `web/api/ansao.py` đổi `Access-Control-Allow-Origin` từ `*` sang link này để bảo mật tuyệt đối.
