# Hướng Dẫn Cấu Hình Supabase (Miễn Phí)

Để tính năng "Đăng nhập" và "Lưu lá số" hoạt động, bạn cần một nơi lưu trữ dữ liệu. Chúng ta dùng **Supabase** (miễn phí, nhanh, bảo mật).

## Bước 1: Tạo Tài Khoản & Dự Án
1. Truy cập [https://supabase.com/](https://supabase.com/).
2. Nhấn **"Start your project"** và đăng nhập (bằng GitHub hoặc tạo tài khoản mới).
3. Nhấn **"New Project"**.
   - **Name**: `TuViApp` (hoặc tên gì cũng được).
   - **Database Password**: Đặt mật khẩu (nhớ lưu lại, dù chưa cần dùng ngay).
   - **Region**: Chọn `Singapore` (để gần Việt Nam nhất).
4. Nhấn **"Create new project"** và đợi khoảng 1-2 phút để nó khởi tạo.

## Bước 2: Lấy API Key
1. Sau khi Project tạo xong, vào mục **Project Settings** (biểu tượng bánh răng ⚙️ ở dưới cùng bên trái).
2. Chọn menu **API**.
3. Bạn sẽ thấy phần **Project URL** và **Project API keys**.
4. Copy 2 giá trị sau:
   - **Project URL**: Ví dụ `https://xrwq...supabase.co`
   - **anon public** key: Một chuỗi ký tự rất dài.

## Bước 3: Cấu Hình Vào Code
1. Mở file `.env.local` trong thư mục `web` (nếu chưa có thì tạo mới).
2. Dán nội dung sau vào:

```env
NEXT_PUBLIC_SUPABASE_URL=Dan_URL_cua_ban_vao_day
NEXT_PUBLIC_SUPABASE_ANON_KEY=Dan_Key_anon_public_vao_day
```

## Bước 4: Tạo Bảng Dữ Liệu (Table)
Supabase có sẵn trình tạo bảng (Table Editor).
1. Vào mục **Table Editor** (icon hình bảng tính bên trái).
2. Nhấn **"New Table"**, tạo bảng tên `saved_horoscopes`.
   - Enable RLS (Row Level Security): **Checked** (Quan trọng để bảo mật).
   - Columns:
     - `id`: uuid, Primary Key, Default: `gen_random_uuid()`
     - `user_id`: uuid, Foreign Key -> `auth.users.id` (Chọn mục Relation).
     - `name`: text
     - `dob_solar`: text
     - `dob_lunar`: text
     - `gender`: int2
     - `data_json`: jsonb
     - `created_at`: timestamptz, Default: `now()`
3. Nhấn **Save**.

## Bước 5: Cấu Hình Bảo Mật (RLS Policies)
Để người dùng chỉ xem được lá số của chính họ:
1. Trong tab **Authentication** -> **Policies**, tìm bảng `saved_horoscopes`.
2. Nhấn **"New Policy"** -> **"Get started quickly"** -> Chọn "Enable read access for authenticated users only".
   - Sửa câu lệnh `USING` thành: `auth.uid() = user_id`.
   - Đặt tên: "Users can see own horoscopes".
   - Operation: SELECT.
3. Làm tương tự cho **INSERT** và **DELETE**:
   - Create Policy cho INSERT: `auth.uid() = user_id`.
   - Create Policy cho DELETE: `auth.uid() = user_id`.

**Xong!** Giờ App của bạn đã có tính năng đăng nhập xịn xò.
