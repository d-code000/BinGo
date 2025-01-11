import sys

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication

from model.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()

    font_id = QFontDatabase.addApplicationFont("resources/EternalUiRegular-BWZGd.ttf")
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    custom_font = QFont(font_family)
    app.setFont(custom_font)
    
    window.show()
    
    sys.exit(app.exec())