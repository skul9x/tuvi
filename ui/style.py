
LIGHT_THEME = """
QMainWindow {
    background-color: #fdfbf7;
}

/* Input Panel */
QGroupBox#InputPanel {
    background-color: #faebd7; 
    border-radius: 15px;
    border: 1px solid #e0e0e0;
    margin-top: 20px;
}
QGroupBox::title#InputPanel {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 10px;
    color: #5d4037;
    font-weight: bold;
    font-size: 16px;
}

/* Labels */
QLabel {
    color: #333333;
    font-size: 13px;
}
QLabel#TitleHeader {
    color: #8d6e63;
    font-size: 18px;
    font-weight: bold;
}

/* Inputs */
QLineEdit, QDateEdit, QTimeEdit, QComboBox {
    border: 1px solid #ccc;
    border-radius: 15px;
    padding: 8px 12px;
    background-color: white;
    selection-background-color: #f59e0b;
}
QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {
    border: 1px solid #f59e0b;
}

/* Button */
QPushButton#ActionButton {
    background-color: #f59e0b;
    color: white;
    border-radius: 20px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton#ActionButton:hover {
    background-color: #d97706;
}
QPushButton#ActionButton:pressed {
    background-color: #b45309;
}

/* La So Cell */
QFrame#CungCell {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
}
QLabel#CungHeader {
    background-color: #f5f5f5;
    color: #d32f2f; /* Red for Header text sometimes */
    font-weight: bold;
    font-size: 12px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 4px;
    alignment: center;
}
QLabel#StarText {
    font-size: 11px;
    padding: 2px;
}
QLabel#StarTextMain {
    font-size: 11px;
    font-weight: bold;
    color: #512da8; /* Deep Purple for Main Stars */
}
"""
