import string

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPen
from PySide6.QtWidgets import QGraphicsView

from model.go_board import GoBoard


class GraphicsView(QGraphicsView):
    def __init__(self, scene, go_board: GoBoard, background: QPixmap, parent=None):
        super().__init__(scene, parent)
        
        self.background = background
        self.go_board = go_board
        self.board_y = None
        self.board_x = None
        self.board_step = None
        
        self.white_stone = QPixmap("resources/img/stone/white_stone.png")
        self.black_stone = QPixmap("resources/img/stone/black_stone.png")

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        pen = QPen(Qt.white)
        pen.setWidth(2)
        painter.setPen(pen)

        # background size
        max_border_size = min(rect.width(), rect.height()) - 20
        x_border = -max_border_size // 2
        y_border = -max_border_size // 2 + 10

        # board size
        indent = 50
        max_board_size = max_border_size - indent
        self.board_x = x_border + indent
        self.board_y = y_border + indent
        self.board_step = max_board_size / (self.go_board.size + 1)

        painter.drawPixmap(-rect.width() / 2,
                           -rect.height() / 2,
                           self.__crop_and_resize_pixmap(self.background, rect.width(), rect.height()))
        painter.drawRect(x_border, y_border, max_border_size, max_border_size)

        for i in range(1, self.go_board.size + 1):
            painter.drawLine(self.board_x + i * self.board_step, self.board_y + 10, self.board_x + i * self.board_step, self.board_y + max_board_size - 10)
            painter.drawText(self.board_x + i * self.board_step - 5, self.board_y - 10, string.ascii_uppercase[i - 1])
            painter.drawLine(self.board_x + 10, self.board_y + i * self.board_step, self.board_x + max_board_size - 10, self.board_y + i * self.board_step)
            painter.drawText(self.board_x - indent // 2, self.board_y + i * self.board_step + 5, str(self.go_board.size + 1 - i))

        size = self.board_step + 5
        scaled_white_stone = self.white_stone.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        scaled_black_stone = self.black_stone.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        for i in range(self.go_board.size):
            for j in range(self.go_board.size):
                if self.go_board.board[j][i] == 1:
                    painter.drawPixmap(self.board_x + (i + 1) * self.board_step - size / 2, self.board_y + (j + 1) * self.board_step - size / 2, scaled_black_stone)
                elif self.go_board.board[j][i] == 2:
                    painter.drawPixmap(self.board_x + (i + 1) * self.board_step - size / 2, self.board_y + (j + 1) * self.board_step - size / 2, scaled_white_stone)
        
                
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        position = self.mapToScene(event.pos())
        
        if (self.board_x < position.x() < self.board_x + self.board_step * self.go_board.size and 
            self.board_y < position.y() < self.board_y + self.board_step * self.go_board.size):
            x = round((position.x() - self.board_x) / self.board_step - 1)
            y = round((position.y() - self.board_y) / self.board_step - 1)
            x = x if x >= 0 else 0
            y = y if y >= 0 else 0
            self.go_board.add_move(x, y)
            self.go_board.next_move()
            self.viewport().update()

    @staticmethod
    def __crop_and_resize_pixmap(pixmap: QPixmap, width: int, height: int) -> QPixmap:
        original_width = pixmap.width()
        original_height = pixmap.height()
    
        target_ratio = width / height
    
        if original_width / original_height > target_ratio:
            new_width = int(original_height * target_ratio)
            new_height = original_height
            x_offset = (original_width - new_width) // 2
            y_offset = 0
        else:
            new_width = original_width
            new_height = int(original_width / target_ratio)
            x_offset = 0
            y_offset = (original_height - new_height) // 2
    
        cropped_pixmap = pixmap.copy(x_offset, y_offset, new_width, new_height)
        resized_pixmap = cropped_pixmap.scaled(width, height)
    
        return resized_pixmap
        
        