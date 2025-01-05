import subprocess
from typing import Union, Literal, Tuple

Color = Union[Literal["b"], Literal["w"]]
Move = Union[None, Literal["pass"], Tuple[int, int]]

class KataGoEngine:
    """
    A class to represent a KataGo engine.
    More advanced version: https://github.com/sanderland/katrain/blob/master/katrain/core/engine.py
    """
    def __init__(self, katago_path: str, config_path: str, model_path: str,
                 additional_args: list[str] = None):
        
        self.engine_process = None
        self.katago_path = katago_path
        self.config_path = config_path
        self.model_path = model_path
        self.additional_args = additional_args
        self.boardXSize = 19
        self.boardYSize = 19
        self.rules = "Chinese"
        
        
    def start(self):
        self.engine_process = subprocess.Popen(
            [self.katago_path, "analysis", "-config", self.config_path, "-model", self.model_path] + (self.additional_args or []),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
    
    def stop(self, *args):
        self.engine_process.stdin.close()