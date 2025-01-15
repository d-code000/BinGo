import json
import subprocess
from typing import Union, Literal, Tuple
from uuid import uuid4

Color = Union[Literal["b"], Literal["w"]]
Move = Union[None, Literal["pass"], Tuple[int, int]]

class KataGoEngine:
    """
    A class to represent a KataGo engine.
    Example: https://github.com/lightvector/KataGo/blob/master/python/query_analysis_engine_example.py
    More advanced version: https://github.com/sanderland/katrain/blob/master/katrain/core/engine.py
    """
    def __init__(self, katago_path: str, config_path: str, model_path: str,
                 additional_args: list[str] = None, size: int = 19, rules: str = "Chinese"):
        
        self.engine_process = None
        self.katago_path = katago_path
        self.config_path = config_path
        self.model_path = model_path
        self.additional_args = additional_args
        self.boardXSize = size
        self.boardYSize = size
        self.rules = rules
        
        
    def start(self):
        self.engine_process = subprocess.Popen(
            [self.katago_path, "analysis", "-config", self.config_path, "-model", self.model_path] + (self.additional_args or []),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
    
    def next_move(self, moves: list[list[str, str]], komi: float = 6.5) -> str:
        query = {
            "id": str(uuid4()),
            "initialStones": [],
            "moves": moves if moves else [],
            "rules": self.rules,
            "komi": komi,
            "boardXSize": self.boardXSize,
            "boardYSize": self.boardYSize,
        }
        json_query = json.dumps(query) + "\n"
        self.engine_process.stdin.write(json_query.encode())
        self.engine_process.stdin.flush()
        
        line = ""
        while line == "":
            if self.engine_process.poll():
                raise Exception("Engine process died")
            line = self.engine_process.stdout.readline().decode().strip()
        response = json.loads(line)
        return response["moveInfos"][0]["move"]
    
    def stop(self, *args):
        self.engine_process.stdin.close()
    
    def __del__(self):
        self.stop()