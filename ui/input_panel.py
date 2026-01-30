from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLineEdit, QDateEdit,
    QComboBox, QPushButton, QLabel, QFormLayout, QHBoxLayout, QRadioButton, QButtonGroup
)
from PySide6.QtCore import QDate, Qt

class InputPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("THÔNG TIN ĐƯƠNG SỐ", parent)
        self.setObjectName("InputPanel")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Họ tên
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Nhập họ và tên...")
        self.txt_name.editingFinished.connect(self.normalize_name)
        layout.addWidget(QLabel("Họ và Tên"))
        layout.addWidget(self.txt_name)
        
        # Ngày sinh (Combobox cluster)
        date_layout = QHBoxLayout()
        date_layout.setSpacing(5)

        # Day
        self.combo_day = QComboBox()
        self.combo_day.addItems([str(i) for i in range(1, 32)])
        
        # Month
        self.combo_month = QComboBox()
        self.combo_month.addItems([str(i) for i in range(1, 13)])
        
        # Year
        self.combo_year = QComboBox()
        current_year = QDate.currentDate().year()
        # Range from 1900 to current year + 1 (descending for usability)
        years = [str(y) for y in range(current_year + 1, 1900, -1)]
        self.combo_year.addItems(years)
        self.combo_year.setCurrentText("1990") # Default

        # Add to layout with ratios
        date_layout.addWidget(self.combo_day, 1)
        date_layout.addWidget(QLabel("/"))
        date_layout.addWidget(self.combo_month, 1)
        date_layout.addWidget(QLabel("/"))
        date_layout.addWidget(self.combo_year, 1)
        
        # Logic update days
        self.combo_month.currentIndexChanged.connect(self.update_days)
        self.combo_year.currentIndexChanged.connect(self.update_days)

        # Loại lịch toggle
        self.cal_type_group = QButtonGroup(self)
        self.radio_duong = QRadioButton("Dương Lịch")
        self.radio_am = QRadioButton("Âm Lịch")
        self.radio_duong.setChecked(True)
        self.cal_type_group.addButton(self.radio_duong)
        self.cal_type_group.addButton(self.radio_am)
        
        cal_layout = QHBoxLayout()
        cal_layout.addWidget(self.radio_duong)
        cal_layout.addWidget(self.radio_am)
        
        layout.addWidget(QLabel("Ngày Sinh"))
        layout.addLayout(date_layout)
        layout.addLayout(cal_layout)
        
        # Giờ sinh
        # Giờ sinh
        self.combo_gio_sinh = QComboBox()
        self.combo_gio_sinh.addItems([
            "Tí (23g - 1g)", "Sửu (1g - 3g)", "Dần (3g - 5g)", "Mão (5g - 7g)", 
            "Thìn (7g - 9g)", "Tỵ (9g - 11g)", "Ngọ (11g - 13g)", "Mùi (13g - 15g)", 
            "Thân (15g - 17g)", "Dậu (17g - 19g)", "Tuất (19g - 21g)", "Hợi (21g - 23g)"
        ])
        self.combo_gio_sinh.setCurrentIndex(6) # Default Ngọ (11-13g)
        layout.addWidget(QLabel("Giờ Sinh"))
        layout.addWidget(self.combo_gio_sinh)
        
        # Giới tính
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Nam", "Nữ"])
        layout.addWidget(QLabel("Giới Tính"))
        layout.addWidget(self.gender_combo)
        
        # Năm xem
        self.year_view = QComboBox()
        current_year = QDate.currentDate().year()
        self.year_view.addItems([str(y) for y in range(current_year - 5, current_year + 10)])
        self.year_view.setCurrentText(str(current_year))
        layout.addWidget(QLabel("Năm Xem Hạn"))
        layout.addWidget(self.year_view)

        # Phong cách luận giải
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "Nghiêm túc", 
            "Đời thường", 
            "Hài hước", 
            "Kiếm hiệp", 
            "Chữa lành"
        ])
        layout.addWidget(QLabel("Phong cách luận giải"))
        layout.addWidget(self.style_combo)
        
        layout.addStretch()
        
        # Button
        self.btn_action = QPushButton("LẬP LÁ SỐ & LUẬN GIẢI")
        self.btn_action.setObjectName("ActionButton")
        self.btn_action.setCursor(Qt.PointingHandCursor)
        self.btn_action.setFixedHeight(50)
        self.btn_action.setStyleSheet("""
            QPushButton {
                background-color: #d4a017;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #c49007; }
            QPushButton:pressed { background-color: #b48000; }
            QPushButton:disabled { background-color: #ccc; }
        """)
        layout.addWidget(self.btn_action)

        # Settings Button
        self.btn_settings = QPushButton("⚙️ Cài đặt hệ thống")
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #f0f0f0; color: #333; }
        """)
        layout.addWidget(self.btn_settings)

        layout.addStretch()

    def normalize_name(self):
        text = self.txt_name.text()
        if text:
            # Capitalize first letter of each word
            normalized = text.title()
            self.txt_name.setText(normalized)

    def update_days(self):
        month = int(self.combo_month.currentText())
        year = int(self.combo_year.currentText())
        
        # Calculate days in month
        days_in_month = QDate(year, month, 1).daysInMonth()
        
        current_day = self.combo_day.currentIndex()
        if current_day == -1: current_day = 0
            
        self.combo_day.blockSignals(True)
        self.combo_day.clear()
        self.combo_day.addItems([str(i) for i in range(1, days_in_month + 1)])
        
        # Restore selection if possible, else select last
        if current_day < days_in_month:
            self.combo_day.setCurrentIndex(current_day)
        else:
            self.combo_day.setCurrentIndex(days_in_month - 1)
            
        self.combo_day.blockSignals(False)

    def get_data(self):
        return {
            "name": self.txt_name.text(),
            "day": int(self.combo_day.currentText()),
            "month": int(self.combo_month.currentText()),
            "year": int(self.combo_year.currentText()),
            "hour": self.combo_gio_sinh.currentIndex() * 2, # Tí=0, Sửu=2...
            "minute": 0,
            "gender": 1 if self.gender_combo.currentText() == "Nam" else 0, # 1 Nam, 0 Nu
            "is_lunar": self.radio_am.isChecked(),
            "year_view": int(self.year_view.currentText()),
            "reading_style": self.style_combo.currentText()
        }
