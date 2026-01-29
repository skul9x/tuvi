from PySide6.QtCore import QThread, Signal
from core.tuvi import TuViLogic
from core.gemini_client import GeminiClient

class AnSaoWorker(QThread):
    finished_signal = Signal(dict)
    error_signal = Signal(str)

    def __init__(self, data_input):
        super().__init__()
        self.data_input = data_input

    def run(self):
        try:
            # Logic calculation
            # TuViLogic.__init__ calls LunarConverter which might raise Error
            logic = TuViLogic(
                self.data_input["day"], 
                self.data_input["month"], 
                self.data_input["year"], 
                self.data_input["hour"], 
                self.data_input["gender"], 
                name=self.data_input["name"]
            )
            result = logic.an_sao()
            self.finished_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))

class GeminiWorker(QThread):
    text_received = Signal(str)
    finished_signal = Signal()
    error_signal = Signal(str)
    
    def __init__(self, client: GeminiClient, data_json):
        super().__init__()
        self.client = client
        self.data_json = data_json
        
    def run(self):
        try:
            stream = self.client.generate_reading_stream(self.data_json)
            for chunk in stream:
                self.text_received.emit(chunk)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))
