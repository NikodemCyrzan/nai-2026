from enum import Enum

from event.bus import GameEvent


class GameStatus(Enum):
    Waiting = 1
    Starting = 2
    In_Progress = 3
    Ended = 4

class GameStatusChangeEvent(GameEvent):
    def __init__(self, status: GameStatus):
        self.status = status
