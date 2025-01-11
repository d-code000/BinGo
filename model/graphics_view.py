import string

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPen
from PySide6.QtWidgets import QGraphicsView


class GraphicsView(QGraphicsView):
    def __init__(self, scene, background: QPixmap, parent=None):
        super().__init__(scene, parent)
        self.background = background
        self.board_size = 9

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        pen = QPen(Qt.white)
        pen.setWidth(2)
        painter.setPen(pen)

        # background size
        max_background_size = min(rect.width(), rect.height()) - 20
        x_background = -max_background_size // 2
        y_background = -max_background_size // 2 + 10

        # board size
        indent = 50
        max_board_size = max_background_size - indent
        x_board = x_background + indent
        y_board = y_background + indent
        step_board = max_board_size / (self.board_size + 1)


        cropped_background = self.background.copy(
            (self.background.width() - rect.width()) / 2,
            max_board_size + 10,
            rect.width(),
            rect.width()
        )

        painter.drawPixmap(-rect.width() / 2, y_background - 10, cropped_background)
        painter.drawRect(x_background, y_background, max_background_size, max_background_size)

        for i in range(1, self.board_size + 1):
            painter.drawLine(x_board + i * step_board, y_board + 10, x_board + i * step_board, y_board + max_board_size - 10)
            painter.drawText(x_board + i * step_board - 5, y_board - 10, string.ascii_uppercase[i - 1])
            painter.drawLine(x_board + 10, y_board + i * step_board, x_board + max_board_size - 10, y_board + i * step_board)
            painter.drawText(x_board - indent // 2, y_board + i * step_board + 5, str(self.board_size + 1 - i))
        # new_flag = True
        # white_stone = QPixmap('resources/img/stone/white_stone.png')
        # black_stone = QPixmap('resources/img/stone/black_stone.png')
        # for i in range(1, self.board_size + 1):
        #     flag = new_flag
        #     size = step_board + 5
        #     scaled_white_stone = white_stone.scaled(
        #         size, size,
        #         Qt.AspectRatioMode.KeepAspectRatio,
        #         Qt.SmoothTransformation
        #     )
        #     scaled_black_stone = black_stone.scaled(
        #         size, size,
        #         Qt.AspectRatioMode.KeepAspectRatio,
        #         Qt.SmoothTransformation
        #     )
        #     for j in range(1, self.board_size + 1):
        #         painter.drawPixmap(x_board + i * step_board - size / 2, y_board + j * step_board - size / 2, scaled_white_stone if flag else scaled_black_stone)
        #         flag = not flag
        #     new_flag = not new_flag
                
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)