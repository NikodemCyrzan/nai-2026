from models.board import Board
from models.player import Player
from state.state import PlayerState, GameStatus


class GameEvent:
    pass

class GameStartEvent(GameEvent):
    pass

class GameStopEvent(GameEvent):
    pass

class GameExceptionEvent(GameEvent):
    def __init__(self, message: str):
        self.message = message

class BoardStateChangeEvent(GameEvent):
    def __init__(self, board: Board):
        self.board = board # temp so that we don't have to rewrite the value each time

class PlayerStateChangeEvent(GameEvent):
    def __init__(self, player: Player, state: PlayerState):
        self.player = player
        self.state = state

class GameStatusChangeEvent(GameEvent):
    def __init__(self, status: GameStatus):
        self.status = status

class PlayerTurnChangeEvent(GameEvent):
    def __init__(self, player: Player):
        self.player = player

