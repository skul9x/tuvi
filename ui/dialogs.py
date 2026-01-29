from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class ApiKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cài đặt API Key")
        self.setFixedWidth(400)
        self.setStyleSheet("""
            QDialog { background-color: #fdfbf7; }
            QLabel { font-size: 14px; color: #333; }
            QLineEdit { border: 1px solid #ccc; border-radius: 8px; padding: 8px; font-size: 14px; }
            QPushButton { background-color: #f59e0b; color: white; border-radius: 8px; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #d97706; }
        """)
        
        layout = QVBoxLayout(self)
        
        lbl_info = QLabel("Ứng dụng cần Google Gemini API Key để luận giải.\nVui lòng nhập Key bên dưới:")
        lbl_info.setWordWrap(True)
        layout.addWidget(lbl_info)
        
        self.txt_key = QLineEdit()
        self.txt_key.setPlaceholderText("Paste API Key here (AIwa...)")
        self.txt_key.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.txt_key)
        
        lbl_link = QLabel('<a href="https://aistudio.google.com/app/apikey">Lấy API Key ở đâu?</a>')
        lbl_link.setOpenExternalLinks(True)
        lbl_link.setAlignment(Qt.AlignRight)
        layout.addWidget(lbl_link)
        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Bỏ qua")
        btn_cancel.setStyleSheet("background-color: #9e9e9e;")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Lưu Key")
        btn_save.clicked.connect(self.save_key)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)
        
        self.api_key = None

    def save_key(self):
        key = self.txt_key.text().strip()
        if key:
            self.api_key = key
            self.accept()
