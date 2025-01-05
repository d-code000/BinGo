from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow

from ui.migration.main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/BinGoXDoomEternal.png"))
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        level_up_pixmap = QPixmap("resources/level_up.png")
        self.difficult_pixmap = [
            QPixmap("resources/difficult/remove-bg-crop-size/I_m_too_young_to_die-transformed.png"),
            QPixmap("resources/difficult/remove-bg-crop-size/Hunt_me_plenty.png"),
            QPixmap("resources/difficult/remove-bg-crop-size/Ultra-Violence.png"),
            QPixmap("resources/difficult/remove-bg-crop-size/Nightmare.png"),
            QPixmap("resources/difficult/remove-bg-crop-size/Ultra-Nightmare.png")
        ]
        
        self.ui.levelUpImageLable.setPixmap(
            level_up_pixmap.scaled(
                self.ui.levelUpImageLable.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation)
        )
        
        self.ui.difficultComboBox.currentIndexChanged.connect(self.change_difficult)
        self.ui.difficultImageLable.setMinimumSize(QSize(0, 200))
        self.change_difficult(0)
        
    def change_difficult(self, state):
        self.ui.difficultImageLable.setPixmap(
            self.difficult_pixmap[state].scaled(
                self.ui.difficultImageLable.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
        )