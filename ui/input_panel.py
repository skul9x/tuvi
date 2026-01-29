from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLineEdit, QDateEdit, QTimeEdit, 
    QComboBox, QPushButton, QLabel, QFormLayout, QHBoxLayout, QRadioButton, QButtonGroup
)
from PySide6.QtCore import QDate, QTime, Qt

class InputPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("THÔNG TIN ĐƯƠNG SỐ", parent)
        self.setObjectName("InputPanel")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Họ tên
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Nhập họ và tên...")
        layout.addWidget(QLabel("Họ và Tên"))
        layout.addWidget(self.txt_name)
        
        # Ngày sinh
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        
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
        layout.addWidget(self.date_edit)
        layout.addLayout(cal_layout)
        
        # Giờ sinh
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(12, 0)) # Mặc định giờ Ngọ
        layout.addWidget(QLabel("Giờ Sinh"))
        layout.addWidget(self.time_edit)
        
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

    def get_data(self):
        return {
            "name": self.txt_name.text(),
            "day": self.date_edit.date().day(),
            "month": self.date_edit.date().month(),
            "year": self.date_edit.date().year(),
            "hour": self.time_edit.time().hour(),
            "minute": self.time_edit.time().minute(),
            "gender": 1 if self.gender_combo.currentText() == "Nam" else 0, # 1 Nam, 0 Nu
            "is_lunar": self.radio_am.isChecked(),
            "year_view": int(self.year_view.currentText())
        }
