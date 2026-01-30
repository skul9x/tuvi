from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

class LogPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # Log Display
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: Consolas, monospace;
                font-size: 13px;
                border: 1px solid #333;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.txt_log)
        
        # Copy Button
        self.btn_copy = QPushButton("📋 Sao chép Log (Copy)")
        self.btn_copy.setCursor(Qt.PointingHandCursor)
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #444; }
        """)
        self.btn_copy.clicked.connect(self.copy_log)
        layout.addWidget(self.btn_copy)

    def append_log(self, text):
        self.txt_log.moveCursor(QTextCursor.MoveOperation.End)
        self.txt_log.insertPlainText(text + "\n")
        self.txt_log.moveCursor(QTextCursor.MoveOperation.End)

    def copy_log(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.txt_log.toPlainText())
        QMessageBox.information(self, "Thông báo", "Đã sao chép Log vào bộ nhớ tạm!")
