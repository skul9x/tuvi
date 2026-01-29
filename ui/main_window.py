import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QTextEdit, QMessageBox, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QThread, Signal

from ui.style import LIGHT_THEME
from ui.input_panel import InputPanel
from ui.laso_panel import LaSoPanel
from ui.chart_panel import ChartPanel
from core.tuvi import TuViLogic
from core.gemini_client import GeminiClient
from core.config import ConfigManager
from ui.dialogs import ApiKeyDialog
from ui.workers import AnSaoWorker, GeminiWorker
from ui.log_panel import LogPanel # Import LogPanel
from core.logger import setup_logger # Import Logger Setup
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QTextCursor

# Setup Logger globally
logger, qt_handler = setup_logger()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TU VI PRO - AI HOROSCOPE MANAGER")
        self.resize(1280, 800)
        self.setStyleSheet(LIGHT_THEME)
        
        # Connect Logger to LogPanel (will be init below)
        self.log_handler = qt_handler
        
        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left: Input
        self.input_panel = InputPanel()
        self.input_panel.setFixedWidth(320)
        self.input_panel.btn_action.clicked.connect(self.on_analyze)
        main_layout.addWidget(self.input_panel)
        
        # Right: Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Tab 1: La So
        self.laso_panel = LaSoPanel()
        self.tabs.addTab(self.laso_panel, "LÁ SỐ TỬ VI")

        # Tab 2: Bieu Do (New)
        self.chart_panel = ChartPanel()
        self.tabs.addTab(self.chart_panel, "BIỂU ĐỒ 12 CUNG")
        
        # Tab 3: Loi Phan
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setPlaceholderText("Lời luận giải của AI sẽ xuất hiện tại đây...")
        self.chat_area.setStyleSheet("font-size: 14px; line-height: 1.6; color: #333; padding: 10px;")
        self.tabs.addTab(self.chat_area, "LUẬN GIẢI CHI TIẾT")
        
        # Tab 4: Content AI (Debug)
        self.debug_widget = QWidget()
        debug_layout = QVBoxLayout(self.debug_widget)
        
        # Text Area
        self.txt_debug_ai = QTextEdit()
        self.txt_debug_ai.setReadOnly(True)
        self.txt_debug_ai.setPlaceholderText("Nội dung Prompt gửi cho AI sẽ hiển thị tại đây...")
        debug_layout.addWidget(self.txt_debug_ai)
        
        # Copy Button
        self.btn_copy_debug = QPushButton("Sao chép nội dung")
        self.btn_copy_debug.setFixedWidth(150)
        self.btn_copy_debug.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; font-weight: bold;")
        self.btn_copy_debug.clicked.connect(self.copy_debug_content)
        
        # Layout for Button (Right aligned)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_copy_debug)
        debug_layout.addLayout(btn_layout)
        
        self.tabs.addTab(self.debug_widget, "CONTENT GỬI AI")

        # Tab 5: Logs (New)
        self.log_panel = LogPanel()
        self.tabs.addTab(self.log_panel, "SYSTEM LOGS")
        self.log_handler.log_signal.connect(self.log_panel.append_log)
        
        main_layout.addWidget(self.tabs)
        
        logger.info("Application Started. Waiting for user input...")
        
        # Logic Clients
        self.config = ConfigManager()
        # Load API Key and Model from Config
        api_key = self.config.get("api_key")
        model_name = self.config.get("model", "models/gemini-2.0-flash")
        
        self.gemini_client = GeminiClient(api_key=api_key, model_name=model_name)
        
        # Check API Key
        if not api_key:
            # Show Dialog if no key
            dialog = ApiKeyDialog(self)
            if dialog.exec():
                new_key = self.config.get("api_key")
                self.gemini_client.set_config(new_key, model_name)
            else:
                QMessageBox.warning(self, "Cảnh báo", "Bạn chưa nhập API Key. Chức năng luận giải sẽ không hoạt động.")

        # Connect Settings Button
        self.input_panel.btn_settings.clicked.connect(self.open_settings)

    def open_settings(self):
        from ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        if dialog.exec():
            # Reload config after save
            new_key = self.config.get("api_key")
            new_model = self.config.get("model")
            self.gemini_client.set_config(new_key, new_model)
            logger.info("Settings updated via Settings Dialog.")
            QMessageBox.information(self, "Thành công", f"Đã cập nhật cài đặt.\nModel: {new_model}")

    def copy_debug_content(self):
        content = self.txt_debug_ai.toPlainText()
        if content:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            QMessageBox.information(self, "Đã sao chép", "Đã sao chép nội dung prompt vào Clipboard!")
        else:
            QMessageBox.warning(self, "Trống", "Chưa có nội dung để sao chép.")

    def on_analyze(self):
        data = self.input_panel.get_data()
        
        if not data["name"]:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập họ tên.")
            logger.warning("User attempted analysis without entering Name.")
            return

        logger.info(f"Starting analysis for: {data['name']} ({data['year']})")

        # Disable button to prevent double click
        self.input_panel.btn_action.setEnabled(False)
        self.input_panel.btn_action.setText("ĐANG TÍNH TOÁN...")
        
        # 1. Start An Sao Worker
        logger.debug("Starting An Sao Worker thread...")
        self.ansao_worker = AnSaoWorker(data)
        self.ansao_worker.finished_signal.connect(self.on_ansao_finished)
        self.ansao_worker.error_signal.connect(self.on_worker_error)
        self.ansao_worker.start()

    
    def on_ansao_finished(self, result):
        logger.info("An Sao calculations completed successfully.")
        try:
            # Update UI Logic
            self.laso_panel.lbl_name.setText(result["info"]["name"])
            self.laso_panel.lbl_info.setText(
                f"Dương lịch: ...\n" 
                f"Âm lịch: {result['info']['lunar_date']} ({result['info']['can_chi']})\n"
                f"{result['info']['cuc']}\n"
                f"Mệnh tại {result['info']['menh_tai']} - Thân tại {result['info']['than_tai']}"
            )
            self.laso_panel.update_data(result)
            self.chart_panel.plot(result["scores"])
            self.tabs.setCurrentIndex(2) # Switch to Luan Giai tab
            
            # --- POPULATE DEBUG TAB ---
            # Generate the prompt string without sending it (for display)
            try:
                debug_prompt = self.gemini_client.construct_prompt(result)
                self.txt_debug_ai.setText(debug_prompt)
            except Exception as e:
                logger.error(f"Error generating debug prompt: {e}")
                self.txt_debug_ai.setText(f"Error generating prompt: {e}")
            # --------------------------
            
            # 2. Start Gemini Worker
            self.chat_area.clear()
            self.ai_response_buffer = "" # Reset Buffer
            self.chat_area.setPlaceholderText("⏳ Đang kết nối với Thiên Đình (Gemini AI)... Xin chờ giây lát...")
            
            logger.info("Initializing Gemini Worker...")
            self.gemini_worker = GeminiWorker(self.gemini_client, result)
            self.gemini_worker.text_received.connect(self.append_ai_text)
            self.gemini_worker.finished_signal.connect(self.on_ai_finished)
            self.gemini_worker.error_signal.connect(self.on_worker_error)
            self.gemini_worker.start()
            
        except Exception as e:
            logger.error(f"Error updating UI: {e}")
            self.on_worker_error(str(e))

    def on_ai_finished(self):
        logger.info("AI Reading completed.")
        # Render final Markdown
        self.chat_area.setMarkdown(self.ai_response_buffer)
        self.chat_area.append("\n\n✅ **Đã luận giải xong.**")
        
        self.input_panel.btn_action.setEnabled(True)
        self.input_panel.btn_action.setText("LẬP LÁ SỐ & LUẬN GIẢI")

    def on_worker_error(self, error_msg):
        logger.error(f"Worker Error: {error_msg}")
        QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra: {error_msg}")
        self.input_panel.btn_action.setEnabled(True)
        self.input_panel.btn_action.setText("LẬP LÁ SỐ & LUẬN GIẢI")

    def append_ai_text(self, text):
        self.ai_response_buffer += text
        # Show raw text for "streaming" effect (User sees movement)
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)
        self.chat_area.insertPlainText(text)
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
