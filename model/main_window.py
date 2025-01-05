from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView

from ui.migration.main import Ui_MainWindow

class GraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/BinGoXDoomEternal.png"))
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        level_up_pixmap = QPixmap("resources/level_up.png")
        board_background_pixmap = QPixmap('resources/img/background/lava_background_3.jpg')
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
        self.board_background_item = QGraphicsPixmapItem(board_background_pixmap)
        self.scene.addItem(self.board_background_item)
        self.graphicsView = GraphicsView(self.scene)
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