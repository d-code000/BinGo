

class GoBoard:
    """
    Class to represent a Go board.
    self.board: 0 - empty, 1 - black, 2 - white
    """
    def __init__(self, size: int = 19, komi: float = 6.5):
        self.size = size
        self.komi = komi
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.history = []
        self.current_color = 1
    
    def add_motion(self, x: int, y: int) -> bool:
        """
        Add a motion to the board.
        """
        if self.board[y][x] != 0:
            return False
        self.board[y][x] = self.current_color
        self.current_color = 1 if self.current_color == 2 else 2
        return True
        