# Cấu trúc Dự án

Dự án **TuVi AI** được tổ chức theo cấu trúc rõ ràng, tách biệt giữa giao diện (UI) và logic hệ thống (Core).

## Cây Thư mục

```
tuvi-main/
├── core/                   # LOGIC NGHIỆP VỤ (BACKEND)
│   ├── constants.py        # Định nghĩa dữ liệu tĩnh (Tên Sao, Can, Chi, Ngũ Hành...)
│   ├── gemini_client.py    # Module giao tiếp với Google Gemini AI (cấu hình, gửi prompt, xử lý stream)
│   ├── logger.py           # Hệ thống ghi Log (ghi ra console và file)
│   ├── lunar.py            # Thư viện chuyển đổi Lịch Dương <-> Lịch Âm
│   ├── tuvi.py             # ALGORITHM CỐT LÕI: Tính toán vị trí các sao (An Sao), Cục, Mệnh...
│   └── config.py           # Quản lý load/save cấu hình ứng dụng
│
├── ui/                     # GIAO DIỆN NGƯỜI DÙNG (FRONTEND - PySide6)
│   ├── main_window.py      # Cửa sổ chính, điều phối các panel
│   ├── input_panel.py      # Form nhập liệu (Ngày giờ sinh, giới tính...)
│   ├── chart_panel.py      # Vẽ Thiên Bàn (Sơ đồ 12 cung)
│   ├── laso_panel.py       # Hiển thị chi tiết các sao trong từng cung
│   ├── log_panel.py        # Hiển thị log và kết quả luận giải từ AI
│   ├── settings_dialog.py  # Màn hình cài đặt (API Key, Model...)
│   ├── dialogs.py          # Các hộp thoại thông báo nhỏ
│   ├── style.py            # Chứa CSS/QSS định dạng giao diện
│   └── workers.py          # Xử lý tát vụ chạy ngầm (Thread) để tránh đơ giao diện
│
├── docs/                   # Tài liệu dự án
├── tests/                  # Các bài kiểm thử (Unit Tests)
├── config.json             # File lưu trữ cài đặt của người dùng (Tự động tạo)
├── main.py                 # FILE KHỞI CHẠY (Entry Point)
├── requirements.txt        # Danh sách các thư viện cần cài đặt
└── README.md               # Hướng dẫn cài đặt và sử dụng
```

## Mô tả Chi tiết các Module chính

### 1. Core (`core/`)
*   **`tuvi.py`**: Đây là trái tim của ứng dụng. Chứa class `TuViLogic`.
    *   Input: Ngày tháng năm sinh (Dương lịch), giờ sinh, giới tính.
    *   Process: Chuyển đổi sang Âm lịch -> Xác định Can Chi -> An Cung Mệnh/Thân -> An 14 Chính Tinh -> An hơn 100 Phụ Tinh -> Tính Ngũ Hành/Cục.
    *   Output: Cấu trúc dữ liệu JSON chứa toàn bộ thông tin lá số.
*   **`gemini_client.py`**:
    *   Quản lý kết nối đến Google Gemini API.
    *   Chứa hàm `construct_prompt`: Tạo câu lệnh prompt chi tiết dựa trên dữ liệu lá số để gửi cho AI luận giải.
    *   Hỗ trợ cơ chế Fallback: Tự động chuyển Model khác nếu Model hiện tại bị quá tải.

### 2. UI (`ui/`)
*   **`main_window.py`**: Khung sườn chính, lắp ghép các panel lại với nhau.
*   **`input_panel.py`**: Xử lý validation dữ liệu đầu vào.
*   **`laso_panel.py`**: Render lá số tử vi lên màn hình theo dạng lưới 12 cung truyền thống.
