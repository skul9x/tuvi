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

## ⚡ Vercel CLI Cheatsheet (Các lệnh thường dùng)

Dưới đây là các lệnh "quyền lực" nhất mà anh sẽ dùng thường xuyên:

| Lệnh (Command) | Ý nghĩa | Khi nào dùng? |
| :--- | :--- | :--- |
| `vercel` | **Deploy Nháp (Preview)** | Khi anh vừa sửa code xong, muốn test thử xem lên mạng trông nó thế nào (link này khác link chính, chỉ anh biết thôi). |
| `vercel --prod` | **Deploy Thật (Production)** | Khi anh chốt code đã ngon, muốn đẩy bản này ra link chính (tuvi-lac.vercel.app) cho mọi người dùng. |
| `vercel env pull` | **Tải Environment Variables** | Tải mấy biến môi trường (như `GEMINI_API_KEY`) từ trên web Vercel về máy tính để chạy test dưới local (nó lưu vào file `.env.local`). |
| `vercel logs` | **Xem Log (Nhật ký lỗi)** | Khi web bị lỗi mà không biết tại sao, chạy lệnh này để xem server đang báo lỗi gì trên màn hình đen. |
| `vercel login` | **Đăng nhập lại** | Dùng khi anh đổi tài khoản hoặc lâu quá nó bắt đăng nhập lại. |

### 💡 Mẹo nhỏ:
Nếu anh muốn deploy nhanh mà **không muốn nó hỏi nhiều** (như tên project, setting...), anh có thể thêm cờ `-y` (yes):

```powershell
vercel --prod -y
```
*(Lệnh này nghĩa là: Deploy bản Production ngay và luôn, tôi đồng ý hết các confirm!)*
