# Ứng Dụng Luận Giải Tử Vi (AI Powered)

Đây là ứng dụng Desktop mạnh mẽ kết hợp giữa **Thuật toán An Sao Tử Vi truyền thống** và trí tuệ nhân tạo **Google Gemini** để lập và luận giải lá số tử vi chi tiết.

## 🌟 Tính năng Chính

*   **Lập Lá Số Tử Vi Chính Xác**: Tự động tính toán và an sao hơn 100 ngôi sao dựa trên ngày giờ sinh (Dương lịch) theo các quy tắc Tử Vi Đẩu Số Nam Phái.
*   **Chuyển Đổi Lịch Vạn Niên**: Tích hợp thuật toán đổi ngày Dương sang Âm chuẩn xác, tính Can Chi, Cục.
*   **Luận Giải Tự Động bằng AI**: Sử dụng Gemini 1.5 Pro/Flash để đọc lá số, phân tích tính cách, sự nghiệp, tài lộc, tình duyên như một chuyên gia thực thụ.
*   **Giao Diện Hiện Đại**: Viết bằng PySide6 (Qt) với thiết kế sáng sủa, dễ nhìn, hỗ trợ thao tác nhanh.
*   **Xuất Kết Quả**: Hiển thị lời giải theo thời gian thực (Streaming).

## 🛠 Yêu cầu Hệ thống

*   **Hệ điều hành**: Windows 10/11, macOS, hoặc Linux.
*   **Ngôn ngữ**: Python 3.8 trở lên.
*   **API Key**: Cần có API Key của Google Gemini (Miễn phí tại [Google AI Studio](https://aistudio.google.com/)).

## 📦 Hướng dẫn Cài đặt

1.  **Clone hoặc Tải dự án về máy:**
    ```bash
    git clone <repository-url>
    cd tuvi-main
    ```

2.  **Cài đặt các thư viện phụ thuộc:**
    Chạy lệnh sau trong terminal/cmd:
    ```bash
    pip install -r requirements.txt
    ```
    *Nếu chưa có file requirements.txt, bạn có thể cài thủ công:*
    ```bash
    pip install PySide6 google-generativeai lunardate
    ```

## 🚀 Hướng dẫn Sử dụng

1.  **Khởi chạy ứng dụng:**
    ```bash
    python main.py
    ```

2.  **Cấu hình API Key (Lần đầu tiên):**
    *   Vào menu **Cài đặt** (hoặc icon bánh răng).
    *   Dán **Google Gemini API Key** của bạn vào ô tương ứng.
    *   Nhấn **Lưu**.

3.  **Lập và Luận Giải:**
    *   Nhập **Họ tên**, **Ngày sinh**, **Giờ sinh**, **Giới tính** ở khung bên trái.
    *   Nhấn nút **Lập Lá Số**. Hệ thống sẽ hiển thị lá số tử vi ở giữa màn hình.
    *   Nhấn nút **Luận Giải AI** (hoặc tích chọn "Luận giải ngay") để xem bình giải chi tiết ở khung bên phải.

## 📂 Cấu trúc Dự án

Xem file [structure.md](structure.md) để hiểu rõ về kiến trúc mã nguồn.

## ⚠️ Lưu ý

*   Ứng dụng cần kết nối Internet để sử dụng tính năng luận giải AI.
*   Kết quả luận giải mang tính chất tham khảo giải trí.

## 🤝 Đóng góp

Mọi đóng góp (Pull Requests, Issues) đều được hoan nghênh.
