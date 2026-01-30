# 🚀 Hướng Dẫn Deploy Lên Vercel

Cách đơn giản nhất để đưa web app của anh lên mạng là dùng **Vercel CLI**. Dưới đây là 3 bước chi tiết:

## Bước 1: Cài đặt Vercel CLI
Vì máy anh chưa có Vercel, hãy mở Terminal (PowerShell) và chạy lệnh này:

```powershell
npm install -g vercel
```
*Chờ một chút để nó tải về...*

## Bước 2: Đăng nhập & Deploy
Sau khi cài xong, anh chạy các lệnh sau trong thư mục `web`:

1.  **Đăng nhập vào Vercel:**
    ```powershell
    vercel login
    ```
    *Nó sẽ hiện các lựa chọn (GitHub, Email...). Anh chọn cái nào cũng được (dùng phím mũi tên), sau đó nó mở trình duyệt để anh xác nhận.*

2.  **Bắt đầu Deploy:**
    ```powershell
    vercel
    ```
    *(Gõ đúng chữ `vercel` rồi Enter)*

    Vercel sẽ hỏi một vài câu, anh cứ Enter để chọn mặc định (Set up and deploy? [Y], Scope? [Admin]...).
    
    ⚠️ **Lưu ý quan trọng**: Khi nó hỏi `Link to existing project?` -> Chọn **No**.

3.  **Deploy Chính Thức (Production):**
    Lệnh trên chỉ là bản nháp (Preview). Để chạy bản thật cho mọi người dùng:
    ```powershell
    vercel --prod
    ```

## Bước 3: Cấu hình API Key (Quan trọng!)
Web app cần `GEMINI_API_KEY` để trả lời. Nếu không cấu hình, AI sẽ bị lỗi.

1.  Vào Dashboard Vercel (https://vercel.com/dashboard).
2.  Chọn dự án **web** vừa tạo.
3.  Vào **Settings** > **Environment Variables**.
4.  Thêm biến mới:
    *   **Key**: `GEMINI_API_KEY`
    *   **Value**: (Copy Key Gemini của anh vào đây)
5.  Bấm **Save**.
6.  **Redeploy**: Vào tab **Deployments**, bấm dấu 3 chấm ở cái trên cùng -> **Redeploy** để nó nhận Key mới.

---
## ✅ Xong!
Vercel sẽ cấp cho anh một đường link kiểu `https://tuvi-huyenbi.vercel.app`. Anh có thể gửi link này cho bạn bè dùng thử!
