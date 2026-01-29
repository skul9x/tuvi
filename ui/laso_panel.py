from PySide6.QtWidgets import QWidget, QGridLayout, QFrame, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from core.constants import DIA_CHI

class LaSoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setSpacing(5) # Khoảng cách nhỏ giữa các ô
        
        # Grid Mapping
        # Tỵ (0,0) Ngọ (0,1) Mùi (0,2) Thân (0,3)
        # Thìn(1,0)               Dậu (1,3)
        # Mão (2,0)               Tuất(2,3)
        # Dần (3,0) Sửu (3,1) Tý (3,2) Hợi (3,3)
        
        self.pos_map = {
            5: (0, 0), 6: (0, 1), 7: (0, 2), 8: (0, 3), # Tỵ Ngọ Mùi Thân
            4: (1, 0),                   9: (1, 3), # Thìn       Dậu
            3: (2, 0),                   10:(2, 3), # Mão        Tuất
            2: (3, 0), 1: (3, 1), 0: (3, 2), 11:(3, 3)  # Dần Sửu Tý Hợi
        } # Lưu ý index trong code: Tý=0, Sửu=1...
        
        self.cells = {}
        self._init_grid()
        self._init_center()

    def _init_grid(self):
        for index, (row, col) in self.pos_map.items():
            cell = QFrame()
            cell.setObjectName("CungCell")
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(2, 2, 2, 2)
            cell_layout.setSpacing(2)
            
            # Header (Cung Name + Chi)
            header = QLabel(f"{DIA_CHI[index]}")
            header.setObjectName("CungHeader")
            header.setAlignment(Qt.AlignCenter)
            cell_layout.addWidget(header)
            
            # Content Area (Stars)
            content = QLabel("")
            content.setObjectName("StarText")
            content.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            content.setWordWrap(True)
            cell_layout.addWidget(content, 1) # Stretch content
            
            self.layout.addWidget(cell, row, col)
            self.cells[index] = {"header": header, "content": content}

    def _init_center(self):
        # Center Panel (User Info) spanning 2x2 in the middle
        self.center_frame = QFrame()
        self.center_frame.setStyleSheet("background-color: transparent;") 
        center_layout = QVBoxLayout(self.center_frame)
        
        self.lbl_name = QLabel("Tên: ...")
        self.lbl_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #d32f2f;")
        self.lbl_info = QLabel("Ngày sinh: ...\nGiờ sinh: ...\nCục: ...")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        
        center_layout.addWidget(self.lbl_name, 0, Qt.AlignCenter)
        center_layout.addWidget(self.lbl_info, 0, Qt.AlignCenter)
        
        # Center occupies rows 1-2, cols 1-2
        self.layout.addWidget(self.center_frame, 1, 1, 2, 2)

    def update_data(self, data):
        info = data["info"]
        cung_data = data["cung"]
        
        # Center info is already updated by MainWindow manually or we can update here if full info provided.
        # But MainWindow does it better. Removing the conflicting lines.
        pass # Let MainWindow handle center text update for now or just update Cells here.
        
        # Update Cells
        for i in range(12):
            c = cung_data[i]
            # Header: Tên Cung + Tên Chi (VD: MỆNH - DẦN)
            header_text = f"{c.get('chuc_nang', '').upper()} - {c['name']}"
            self.cells[i]["header"].setText(header_text)
            
            # Content: Stars
            # Format: Main stars bold, others normal
            main_stars = "\n".join([f"★ {s}" for s in c['chinh_tinh']])
            phu_tinh = ", ".join(c['phu_tinh'])
            
            # Use HTML for rich text in QLabel
            html = ""
            if main_stars:
                html += f"<b style='color:#b71c1c; font-size:12px;'>{main_stars.replace(chr(10), '<br>')}</b><br>"
            if phu_tinh:
                html += f"<span style='color:#333;'>{phu_tinh}</span>"
                
            self.cells[i]["content"].setText(html)
