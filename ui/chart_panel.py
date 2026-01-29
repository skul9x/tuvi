from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class ChartPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Matplotlib Figure
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.figure.patch.set_facecolor('#fdfbf7') # Match App Background
        self.canvas = FigureCanvas(self.figure)
        
        self.layout.addWidget(self.canvas)
        self.ax = None

    def plot(self, scores):
        self.figure.clear()
        
        # Data Preparation
        # 12 Cung Labels
        labels = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
        # Scores list matches 0=Tý, 1=Sửu (as per TuViLogic structure)
        data = scores
        
        # Radar Chart requires standardizing data to close the loop
        N = len(labels)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1] # Close loop
        data += data[:1]     # Close loop
        
        # Draw
        self.ax = self.figure.add_subplot(111, polar=True)
        self.ax.set_facecolor('none') # Transparent inner
        
        # Draw Lines & Fill
        self.ax.plot(angles, data, color='#f59e0b', linewidth=2, linestyle='solid') # Orange Line
        self.ax.fill(angles, data, color='#f59e0b', alpha=0.4) # Semi-trans orange fill
        
        # Labels
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(labels)
        
        # Y labels (Circles)
        self.ax.set_rlabel_position(0)
        self.ax.set_rticks([0, 10, 20, 30]) 
        self.ax.grid(True, color='#cccccc', linestyle='--')
        
        # Title
        self.ax.set_title("BIỂU ĐỒ SỨC MẠNH CÁC CUNG", size=12, color='#5d4037', weight='bold', pad=20)
        
        self.canvas.draw()
