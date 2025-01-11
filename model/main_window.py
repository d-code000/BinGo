from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QGraphicsScene

from katago.engine import KataGoEngine
from model.go_board import GoBoard
from model.graphics_view import GraphicsView
from ui.migration.main import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.engine = KataGoEngine(
            katago_path="/katago/source/katago.exe",
            config_path="/katago/source/analysis_example.cfg",
            model_path="/katago/source/models/kata1-b28c512nbt-s7944987392-d4526094999.bin.gz"
        )
        self.go_board = GoBoard(9)
        
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
        self.graphicsView = GraphicsView(self.scene, self.go_board, board_background_pixmap)
        self.ui.centralwidget.layout().addWidget(self.graphicsView)
    
        self.ui.difficultComboBox.currentIndexChanged.connect(self.change_difficult)
        self.ui.difficultImageLable.setMinimumSize(QSize(0, 200))
        self.change_difficult(0)
        self.showMaximized()
        
    def change_difficult(self, state):
        self.ui.difficultImageLable.setPixmap(
            self.difficult_pixmap[state].scaled(
                self.ui.difficultImageLable.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
        )
    
    def start_game(self):
        self.engine.start()
        
        
        
        