import os
import sys

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication, QMessageBox

from model.main_window import MainWindow

if __name__ == '__main__':

    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS) # noqa
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    font_id = QFontDatabase.addApplicationFont("resources/EternalUiRegular-BWZGd.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    else:
        font_family = "Arial"
        QMessageBox.warning(None, "Warning", 
                            f"Custom font not found. Set font {font_family}", QMessageBox.Ok)
        
    custom_font = QFont(font_family)
    app.setFont(custom_font)
    
    window.show()
    
    sys.exit(app.exec())