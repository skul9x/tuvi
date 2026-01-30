# 💡 BRIEF: AI Tử Vi Desktop App

**Ngày tạo:** 2026-01-29
**Brainstorm cùng:** User

---

## 1. VẤN ĐỀ CẦN GIẢI QUYẾT
Người dùng muốn xem tử vi nhanh chóng trên Desktop, kết hợp giữa tính toán chính xác của môn Tử Vi và khả năng luận giải ngôn ngữ tự nhiên của AI, thay vì phải tra cứu sách hoặc web thủ công.

## 2. GIẢI PHÁP ĐỀ XUẤT
Xây dựng Desktop Application sử dụng **PySide6** (Qt) để nhập liệu và hiển thị.
- **Logic:** Sử dụng Python thuần để tính toán vị trí các sao (An Sao) + Chuyển đổi lịch Dương/Âm.
- **Luận giải:** Sử dụng **Google Gemini API** đóng vai một chuyên gia tử vi để bình giải lá số.

## 3. PHONG CÁCH & ĐỐI TƯỢNG
- **Phong cách AI:** Nghiêm túc, Cổ điển (Văn phong: "Đương số...", "Mệnh Hỏa...", "Cục Thổ...").
- **Giao diện:** Tập trung vào Text/Danh sách (List), rõ ràng, dễ đọc. Không vẽ đồ họa lá số phức tạp.

## 4. TÍNH NĂNG (SCOPE)

### 🚀 MVP (Bắt buộc có):
- [ ] **Nhập liệu:** Form nhập Họ tên, Ngày, Tháng, Năm (Dương lịch), Giờ sinh, Giới tính.
- [ ] **Xử lý số liệu:** 
    - Tự động đổi Dương lịch -> Âm lịch (Can/Chi).
    - Thuật toán An các sao chính (14 Chính tinh + các Phụ tinh quan trọng).
- [ ] **Kết nối AI:** Gửi danh sách sao và thông tin người dùng tới Gemini API.
- [ ] **Hiển thị:** 
    - Cột trái: Form nhập.
    - Cột phải (Tab 1): Danh sách các Cung và Sao (Dữ liệu thô).
    - Cột phải (Tab 2): Lời bình giải của AI.

### 🎁 Phase 2 (Nice-to-have):
- [ ] Lưu lịch sử các lá số đã xem.
- [ ] Xuất file PDF/Text.
- [ ] Tùy chỉnh Prompt (chọn phong cách khác).

## 5. KỸ THUẬT (TECH STACK)
- **Language:** Python 3.x
- **GUI:** PySide6 (Qt for Python).
- **AI:** Google Generative AI SDK (Gemini).
- **Algo:** Code thuật toán An Sao thủ công (Custom implementation).

## 6. BƯỚC TIẾP THEO
→ Chạy `/plan` để lên thiết kế chi tiết kiến trúc code và thuật toán.
