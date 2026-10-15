from enum import Enum

from event.events import GameEvent


class GameStatus(Enum):
    WAITING = 1
    STARTED = 2
    IN_PROGRESS = 3
    FINISHED = 4

class GameStatusChangeEvent(GameEvent):
    def __init__(self, status: GameStatus):
        self.status = status