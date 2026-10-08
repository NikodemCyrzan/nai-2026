from models.board import Board


class GameEvent:
    pass

class GameStartEvent(GameEvent):
    pass

class GameStopEvent(GameEvent):
    pass

class BoardStateChangeEvent(GameEvent):
    def __init__(self, board: Board):
        self._board = board # temp so that we don't have to rewrite the value each time

