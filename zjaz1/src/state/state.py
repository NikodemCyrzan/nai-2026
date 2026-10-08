from event.eventbus import GameEventBus
from event.events import BoardStateChangeEvent
from holder.stateholder import StateHolder
from models.board import Board
from models.player import Player


class PlayerState():
    def __init__(self, initial_pawns: int = 0):
        self._pawns_left_to_place: int

class GameStateInitializer:
    def __init__(self,
        board: Board,
        _player_white_initial_pawns: int = 0,
        _player_black_initial_pawns: int = 0
    ):
        self.board: Board = board
        self.player_white_initial_pawns: int = _player_white_initial_pawns
        self.player_black_initial_pawns: int = _player_black_initial_pawns

class GameState:
    def __init__(self, bus: GameEventBus, initializer: GameStateInitializer):
        self._board_state = StateHolder[Board, BoardStateChangeEvent](
            initializer.board, bus, lambda b: BoardStateChangeEvent(b))

