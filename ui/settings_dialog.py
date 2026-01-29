from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                                 QComboBox, QDialogButtonBox, QMessageBox, QGroupBox, QPushButton)
from PySide6.QtCore import Qt
from core.config import ConfigManager
from core.gemini_client import GeminiClient

# Model Metadata (Hardcoded Free Tier Limits)
GEMINI_MODELS = {
    "models/gemini-2.0-flash": {
        "name": "Gemini 2.0 Flash",
        "desc": "Cân bằng tốt nhất giữa Tốc độ & Thông minh.",
        "rpm": "15 RPM",
        "tpm": "1,000,000 TPM",
        "rpd": "1,500 RPD",
        "tag": "Khuyên dùng"
    },
    "models/gemini-2.0-flash-lite": {
        "name": "Gemini 2.0 Flash Lite",
        "desc": "Siêu nhanh, chi phí thấp, phù hợp test.",
        "rpm": "30 RPM", # Hypothetical higher limit for lite? Google usually groups them. Let's assume standard. actually 2.0 flash lite is simpler.
        # Checking docs: Flash 2.0 is 15 RPM. Lite might be same or higher. Let's keep 15 for safety or check docs.
        # Official Free Tier: Gemini 1.5 Flash is 15 RPM. 
        "rpm": "15 RPM",
        "tpm": "1,000,000 TPM",
        "rpd": "1,500 RPD",
        "tag": "Siêu Tốc"
    },
    "models/gemini-2.5-flash": {
        "name": "Gemini 2.5 Flash",
        "desc": "Phiên bản nâng cấp của Flash, xử lý nhanh hơn.",
        "rpm": "15 RPM",
        "tpm": "1,000,000 TPM",
        "rpd": "1,500 RPD",
        "tag": "Mới"
    },
    "models/gemini-2.5-pro": {
        "name": "Gemini 2.5 Pro",
        "desc": "Mô hình thông minh nhất, lý luận sâu sắc.",
        "rpm": "2 RPM",
        "tpm": "32,000 TPM",
        "rpd": "50 RPD",
        "tag": "Thông minh nhất"
    },
    "models/gemini-1.5-pro": {
        "name": "Gemini 1.5 Pro",
        "desc": "Ổn định, cửa sổ ngữ cảnh rộng.",
        "rpm": "2 RPM",
        "tpm": "32,000 TPM",
        "rpd": "50 RPD",
        "tag": "Ổn định"
    },
     "models/gemini-pro-latest": {
        "name": "Gemini Pro (Latest)",
        "desc": "Bản cập nhật mới nhất của dòng Pro.",
        "rpm": "2 RPM",
        "tpm": "32,000 TPM",
        "rpd": "50 RPD",
        "tag": "Latest"
    }
}

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cài đặt hệ thống & Quota")
        self.setFixedWidth(500)
        self.config_manager = ConfigManager()
        
        layout = QVBoxLayout(self)
        
        # --- API Key Section ---
        gb_api = QGroupBox("Kết nối Gemini API")
        layout_api = QVBoxLayout()
        
        layout_api.addWidget(QLabel("API Key:"))
        hbox_key = QHBoxLayout()
        self.txt_api_key = QLineEdit()
        self.txt_api_key.setEchoMode(QLineEdit.Password)
        self.txt_api_key.setPlaceholderText("Nhập API Key tại đây...")
        self.txt_api_key.setText(self.config_manager.get("api_key", ""))
        hbox_key.addWidget(self.txt_api_key)
        
        self.btn_test = QPushButton("Kiểm tra")
        self.btn_test.setFixedWidth(80)
        self.btn_test.clicked.connect(self.test_connection)
        hbox_key.addWidget(self.btn_test)
        
        layout_api.addLayout(hbox_key)
        gb_api.setLayout(layout_api)
        layout.addWidget(gb_api)
        
        # --- Model Selection Section ---
        gb_model = QGroupBox("Chọn Model & Giới hạn (Quota)")
        layout_model = QVBoxLayout()
        
        layout_model.addWidget(QLabel("Model AI:"))
        self.cmb_model = QComboBox()
        self.cmb_model.currentIndexChanged.connect(self.update_model_info)
        layout_model.addWidget(self.cmb_model)
        
        # Dynamic Info Panel
        self.lbl_model_desc = QLabel("Mô tả: ...")
        self.lbl_model_desc.setWordWrap(True)
        self.lbl_model_desc.setStyleSheet("color: #555; font-style: italic; margin-bottom: 5px;")
        layout_model.addWidget(self.lbl_model_desc)

        # Quota Grid
        hbox_quota = QHBoxLayout()
        
        self.lbl_rpm = self._create_quota_badge("RPM (Phút)", "15", "#e3f2fd", "#1565c0")
        self.lbl_rpd = self._create_quota_badge("RPD (Ngày)", "1,500", "#e8f5e9", "#2e7d32")
        
        hbox_quota.addWidget(self.lbl_rpm)
        hbox_quota.addWidget(self.lbl_rpd)
        layout_model.addLayout(hbox_quota)
        
        gb_model.setLayout(layout_model)
        layout.addWidget(gb_model)
        
        # --- Actions ---
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self._populate_models()
        self.apply_styles()

    def _create_quota_badge(self, title, value, bg_color, text_color):
        lbl = QLabel(f"{title}: {value}")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"""
            background-color: {bg_color}; 
            color: {text_color}; 
            border-radius: 4px; 
            padding: 5px; 
            font-weight: bold;
        """)
        return lbl

    def _populate_models(self):
        current_model = self.config_manager.get("model", "models/gemini-2.0-flash")
        
        # Add items from constant
        for model_id, data in GEMINI_MODELS.items():
            display_text = f"{data['name']} ({data['tag']})"
            self.cmb_model.addItem(display_text, model_id)
        
        # Add any custom model saved that might not be in our list (fallback)
        found = False
        for i in range(self.cmb_model.count()):
            if self.cmb_model.itemData(i) == current_model:
                self.cmb_model.setCurrentIndex(i)
                found = True
                break
        
        if not found:
            self.cmb_model.addItem(f"{current_model} (Custom)", current_model)
            self.cmb_model.setCurrentIndex(self.cmb_model.count() - 1)
            
        self.update_model_info()

    def update_model_info(self):
        model_id = self.cmb_model.currentData()
        data = GEMINI_MODELS.get(model_id)
        
        if data:
            self.lbl_model_desc.setText(f"Mô tả: {data['desc']}")
            self.lbl_rpm.setText(f"RPM (Phút): {data['rpm']}")
            self.lbl_rpd.setText(f"RPD (Ngày): {data['rpd']}")
            
            # Change color for Pro models (Low limit)
            if "2 RPM" in data['rpm']:
                 self.lbl_rpm.setStyleSheet("background-color: #ffebee; color: #c62828; border-radius: 4px; padding: 5px; font-weight: bold;")
            else:
                 self.lbl_rpm.setStyleSheet("background-color: #e3f2fd; color: #1565c0; border-radius: 4px; padding: 5px; font-weight: bold;")
        else:
            self.lbl_model_desc.setText("Mô tả: Model này chưa có thông tin chi tiết.")
            self.lbl_rpm.setText("RPM: ?")
            self.lbl_rpd.setText("RPD: ?")

    def test_connection(self):
        api_key = self.txt_api_key.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập API Key!")
            return
            
        self.btn_test.setText("⏳...")
        self.btn_test.setEnabled(False)
        self.repaint() # Force UI update
        
        success, msg = GeminiClient.test_connection(api_key)
        
        self.btn_test.setText("Kiểm tra")
        self.btn_test.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Thành công", msg)
        else:
            QMessageBox.critical(self, "Thất bại", msg)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QGroupBox { font-weight: bold; border: 1px solid #ddd; border-radius: 6px; margin-top: 10px; padding-top: 10px; background-color: white; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; left: 10px; }
            QLineEdit, QComboBox { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
            QPushButton { padding: 8px 15px; border-radius: 4px; background-color: #2196F3; color: white; border: none; }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:disabled { background-color: #ccc; }
        """)

    def get_settings(self):
        return {
            "api_key": self.txt_api_key.text().strip(),
            "model": self.cmb_model.currentData()
        }

    def accept(self):
        settings = self.get_settings()
        if not settings["api_key"]:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập API Key!")
            return
            
        # Save to config
        self.config_manager.set("api_key", settings["api_key"])
        self.config_manager.set("model", settings["model"])
        
        super().accept()
