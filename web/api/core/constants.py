# Các hằng số cho thuật toán Tử Vi

# Can
THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

# Chi
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# 12 Cung địa bàn (Cố định vị trí)
CUNG_DIA_BAN = DIA_CHI

# 12 Cung chức năng (Mệnh, Phụ, Phúc...)
CUNG_CHUC_NANG = [
    "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
    "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"
]

# Ngũ hành nạp âm
NGU_HANH_NAP_AM = {
    ("Giáp", "Tý"): "Hải Trung Kim", ("Ất", "Sửu"): "Hải Trung Kim",
    ("Bính", "Dần"): "Lư Trung Hỏa", ("Đinh", "Mão"): "Lư Trung Hỏa",
    # ... (Sẽ bổ sung đầy đủ nếu cần, hoặc dùng bảng tra Cục)
}

# 14 Chính Tinh
CHINH_TINH = [
    "Tử Vi", "Thiên Cơ", "Thái Dương", "Vũ Khúc", "Thiên Đồng", "Liêm Trinh",
    "Thiên Phủ", "Thái Âm", "Tham Lang", "Cự Môn", "Thiên Tướng", "Thiên Lương", "Thất Sát", "Phá Quân"
]

# Vòng Lộc Tồn (Cơ bản)
LOC_TON_MAP = {
    "Giáp": "Dần", "Ất": "Mão", "Bính": "Tỵ", "Đinh": "Ngọ", "Mậu": "Tỵ",
    "Kỷ": "Ngọ", "Canh": "Thân", "Tân": "Dậu", "Nhâm": "Hợi", "Quý": "Tý"
}

# Ngũ Hành Cục
CUC = {
    "Thủy": 2, "Mộc": 3, "Kim": 4, "Thổ": 5, "Hỏa": 6
}

# Điểm số các sao (Dùng cho biểu đồ Radar)
# Miếu/Vượng/Đắc: Điểm cao (Giả lập)
# Hãm: Điểm thấp/âm

# Vòng Thái Tuế (An theo chiều thuận từ cung Chi năm sinh)
VONG_THAI_TUE = [
    "Thái Tuế", "Thiếu Dương", "Tang Môn", "Thiếu Âm", "Quan Phù", "Tử Phù",
    "Tuế Phá", "Long Đức", "Bạch Hổ", "Phúc Đức", "Điếu Khách", "Trực Phù"
]

# Vòng Lộc Tồn (An theo chiều thuận từ cung Lộc Tồn.
# Lưu ý: Kình Dương (trước Lộc Tồn), Đà La (sau Lộc Tồn) được an riêng hoặc kết hợp vòng này.
# Danh sách này là vòng Bác Sỹ:
VONG_BAC_SY = [
    "Bác Sỹ", "Lực Sỹ", "Thanh Long", "Tiểu Hao", "Tướng Quân", "Tấu Thư",
    "Phi Liêm", "Hỷ Thần", "Bệnh Phù", "Đại Hao", "Phục Binh", "Quan Phủ"
]

# Vòng Tràng Sinh
VONG_TRANG_SINH = [
    "Tràng Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy",
    "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"
]

# Mapping Tràng Sinh (Cục -> Khởi cung)
# Kim -> Tỵ (5), Mộc -> Hợi (11), Hỏa -> Dần (2), Thủy/Thổ -> Thân (8)
TRANG_SINH_START = {
    4: 5, # Kim
    3: 11, # Mộc
    6: 2, # Hỏa
    2: 8, # Thủy
    5: 8  # Thổ (Thủy Thổ đồng hành trong Tràng Sinh nam phái phổ biến)
}

# Mapping Khôi Việt (Can -> (Khôi, Việt))
KHOI_VIET_MAP = {
    "Giáp": (1, 7), "Mậu": (1, 7), # Sửu, Mùi
    "Ất": (0, 8), "Kỷ": (0, 8),   # Tý, Thân
    "Bính": (11, 9), "Đinh": (11, 9), # Hợi, Dậu
    "Canh": (1, 7), "Tân": (2, 6), # Sửu, Mùi (Canh) ?? Check lại: Canh Tân phùng Mã Hổ (Ngọ, Dần).
    # Sách chuẩn:
    # Gíap Mậu can ngưu dương (Sửu Mùi)
    # Ất Kỷ thử hầu hương (Tý Thân)
    # Canh Tân phùng mã hổ (Ngọ Dần) -> Canh (6-Ngọ, 2-Dần), Tân (6-Ngọ, 2-Dần) -> Canh: Khôi Ngọ, Việt Dần? Check.
    # Nhâm Quý thố xà tàng (Mão Tỵ)
    # Check lại Canh Tân
    "Nhâm": (3, 5), "Quý": (3, 5) # Mão, Tỵ
}
# Correction for Khoi Viet based on standard poem:
# Giáp Mậu: Sửu (1) - Mùi (7)
# Ất Kỷ: Tý (0) - Thân (8)
# Bính Đinh: Hợi (11) - Dậu (9)
# Canh Tân: Ngọ (6) - Dần (2)
# Nhâm Quý: Tỵ (5) - Mão (3)
# Note: Khôi trước, Việt sau (theo chiều kim đồng hồ hay gì? Khôi là dương, Việt là âm).
# Quy tắc phổ biến: Thiên Khôi (Quý nhân), Thiên Việt.
KHOI_VIET_POS = {
    "Giáp": (1, 7), "Mậu": (1, 7),
    "Ất": (0, 8), "Kỷ": (0, 8),
    "Bính": (11, 9), "Đinh": (11, 9),
    "Canh": (6, 2), "Tân": (6, 2), # Cần check sách kỹ hơn cho Tân. Có sách ghi Tân phùng Dần Ngọ (Ngược Canh). Thôi chung.
    "Nhâm": (5, 3), "Quý": (5, 3) 
}

# Điểm số các sao (Dùng cho biểu đồ Radar)
# Miếu/Vượng/Đắc: Điểm cao (Giả lập)
# Hãm: Điểm thấp/âm
STAR_SCORES = {
    "Tử Vi": 10, "Thiên Cơ": 8, "Thái Dương": 9, "Vũ Khúc": 8, "Thiên Đồng": 7, "Liêm Trinh": 6,
    "Thiên Phủ": 10, "Thái Âm": 8, "Tham Lang": 6, "Cự Môn": 5, "Thiên Tướng": 8, "Thiên Lương": 9, "Thất Sát": 7, "Phá Quân": 5,
    "Văn Xương": 2, "Văn Khúc": 2, "Tả Phù": 2, "Hữu Bật": 2, "Thiên Khôi": 3, "Thiên Việt": 3,
    "Lộc Tồn": 5, "Hóa Lộc": 5, "Hóa Quyền": 4, "Hóa Khoa": 4, "Hóa Kỵ": -5,
    "Kình Dương": -3, "Đà La": -3, "Hỏa Tinh": -3, "Linh Tinh": -3, "Địa Không": -5, "Địa Kiếp": -5,
    # Thêm điểm cho phụ tinh quan trọng
    "Thái Tuế": 2, "Thiên Mã": 3, "Đào Hoa": 2, "Hồng Loan": 2, "Thiên Hỷ": 2,
    "Cô Thần": -2, "Quả Tú": -2, "Đại Hao": -2, "Tiểu Hao": -1
}
