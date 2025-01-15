from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QGraphicsScene

from model.go_board import GoBoard
from model.graphics_view import GraphicsView
from ui.migration.main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon("assets/BinGoXDoomEternal.png"))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        level_up_pixmap = QPixmap("resources/level_up.png")
        board_background_pixmap = QPixmap('resources/img/background/volcano_art_wallhaven.jpg')
        self.difficult_pixmap = [
            QPixmap("resources/img/difficult/I_m_too_young_to_die.png"),
            QPixmap("resources/img/difficult/Hunt_me_plenty.png"),
            QPixmap("resources/img/difficult/Ultra-Violence.png"),
            QPixmap("resources/img/difficult/Nightmare.png"),
            QPixmap("resources/img/difficult/Ultra-Nightmare.png")
        ]
        
        self.ui.levelUpImageLable.setPixmap(
            level_up_pixmap.scaled(
                self.ui.levelUpImageLable.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation)
        )

        self.scene = QGraphicsScene()
        self.graphicsView = GraphicsView(self.scene, GoBoard(9), board_background_pixmap)
        self.ui.centralwidget.layout().addWidget(self.graphicsView)
    
        self.ui.difficultComboBox.currentIndexChanged.connect(self.change_difficult)
        self.ui.difficultImageLable.setMinimumSize(QSize(0, 200))
        
        self.ui.startPushButton.clicked.connect(self.start_game)
        
        self.change_difficult(0)
        self.maximumSize()
        
    def change_difficult(self, state):
        self.ui.difficultImageLable.setPixmap(
            self.difficult_pixmap[state].scaled(
                self.ui.difficultImageLable.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
        )
    
    def start_game(self):
        def map_value(value, old_min, old_max, new_min, new_max) -> int:
            return round(new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min))
        komi = self.ui.komiSpinBox.value()
        start_engine = self.ui.AICheckBox.isChecked()
        strong = map_value(self.ui.difficultComboBox.currentIndex(), 
                           0, self.ui.difficultComboBox.count(), 
                           1, 20)
        self.graphicsView.go_board = GoBoard(9, komi, start_engine, strong)
        self.graphicsView.viewport().update()
    
    def closeEvent(self, event):
        if self.graphicsView.go_board.engine is not None:
            self.graphicsView.go_board.engine.stop()
