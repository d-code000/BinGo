import json
import subprocess
import threading
import time
from threading import Thread
from typing import Union, Literal, Tuple
from uuid import uuid4

Color = Union[Literal["b"], Literal["w"]]
Move = Union[None, Literal["pass"], Tuple[int, int]]

class KataGoEngine:
    """
    A class to represent a KataGo engine.
    Docs: https://github.com/lightvector/KataGo/blob/master/docs/Analysis_Engine.md
    Example: https://github.com/lightvector/KataGo/blob/master/python/query_analysis_engine_example.py
    More advanced version: https://github.com/sanderland/katrain/blob/master/katrain/core/engine.py
    """
    def __init__(self, katago_path: str, config_path: str, model_path: str, human_model_path: str = None,
                 additional_args: list[str] = None, size: int = 19, rules: str = "Chinese"):
        
        self.std_err_thread = None
        self.engine_process = None
        self.stop_event = threading.Event()
        self.katago_path = katago_path
        self.config_path = config_path
        self.model_path = model_path
        self.human_model_path = human_model_path
        self.additional_args = additional_args
        self.boardXSize = size
        self.boardYSize = size
        self.rules = rules

        
        
        
    def start(self):
        self.engine_process = subprocess.Popen(
            [self.katago_path, 
             "analysis", "-config", self.config_path, 
             "-model", self.model_path, 
             "-human-model", self.human_model_path] + 
            (self.additional_args or []),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )

        def print_forever():
            while self.engine_process.poll() is None:
                data = self.engine_process.stderr.readline()
                time.sleep(0)
                if data:
                    print("KataGo: ", data.decode(), end="")
            data = self.engine_process.stderr.read()
            if data:
                print("KataGo: ", data.decode(), end="")
        self.std_err_thread = Thread(target=print_forever)
        self.std_err_thread.start()
    
    def next_move(self, moves: list[list[str, str]], komi: float = 6.5, strong: str = "rank_1k") -> str:
        query = {
            "id": str(uuid4()),
            "initialStones": [],
            "moves": moves if moves else [],
            "rules": self.rules,
            "komi": komi,
            "boardXSize": self.boardXSize,
            "boardYSize": self.boardYSize,
            "overrideSettings":{
                "humanSLProfile": strong
            }
            
        }
        json_query = json.dumps(query) + "\n"
        self.engine_process.stdin.write(json_query.encode())
        self.engine_process.stdin.flush()
        
        line = ""
        while line == "":
            if self.engine_process.poll():
                time.sleep(1)
                raise Exception("Engine process died")
            line = self.engine_process.stdout.readline()
            line = line.decode().strip()
        response = json.loads(line)
        return response["moveInfos"][0]["move"]
    
    def stop(self, *args):
        self.engine_process.stdin.close()
        self.stop_event.set()
    
    def __del__(self):
        self.stop()