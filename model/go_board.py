import string

from katago.engine import KataGoEngine


class GoBoard:
    """
    Class to represent a Go board.
    self.board: 0 - empty, 1 - black, 2 - white
    """
    def __init__(self, size: int = 19, komi: float = 6.5, start_engine: bool = False):
        self.size = size
        self.komi = komi
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.history = []
        self.current_color = 1
        self.engine = None
        
        if start_engine:
            self.engine = KataGoEngine(
                katago_path="katago/source/katago.exe",
                config_path="katago/source/analysis_example.cfg",
                model_path="katago/source/models/kata1-b28c512nbt-s7944987392-d4526094999.bin.gz",
                size=self.size
            )
            self.engine.start()
    
    def add_move(self, x: int, y: int) -> bool:
        """
        Add a move to the board.
        """
        if x >= self.size or y >= self.size:
            return False
        if self.board[y][x] != 0:
            return False
        self.board[y][x] = self.current_color
        self.history.append(["W" if self.current_color == 2 else "B", f"{string.ascii_uppercase[x]}{self.size - y}"])
        self.current_color = 1 if self.current_color == 2 else 2
        return True
    
    def next_move(self):
        """
        Get the next move from the AI.
        """
        if self.engine is not None:
            move = self.engine.next_move(self.history)
            move_x= ord(move[0]) - ord('A')
            move_y = self.size - int(move[1])
            self.add_move(move_x, move_y)
    
    def clear(self):
        """
        Clear the board.
        """
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.history = []
        self.current_color = 1
        