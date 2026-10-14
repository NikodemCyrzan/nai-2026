from enum import Enum

from event.eventbus import GameEventBus
from event.events import BoardStateChangeEvent, PlayerStateChangeEvent, GameStatusChangeEvent, PlayerTurnChangeEvent
from holder.stateholder import StateHolder
from models.board import Board
from models.player import Player

class GameStatus(Enum):
    WAITING = 1
    STARTED = 2
    IN_PROGRESS = 3
    FINISHED = 4

class PlayerState:
    def __init__(self, initial_pawns: int = 0):
        self._pawns_left_to_place: int

class GameStateInitializer:
    def __init__(self,
        board: Board,
        player_white_initial_pawns: int = 0,
        player_black_initial_pawns: int = 0
    ):
        self.board: Board = board
        self.player_white_initial_pawns: int = player_white_initial_pawns
        self.player_black_initial_pawns: int = player_black_initial_pawns

class GameState:
    def __init__(self, bus: GameEventBus, initializer: GameStateInitializer):
        self._status = StateHolder(
            GameStatus.WAITING, bus, lambda s: GameStatusChangeEvent(s)
        )

        self._board_state = StateHolder(
            initializer.board, bus, lambda b: BoardStateChangeEvent(b)
        )

        ws = PlayerState(initializer.player_white_initial_pawns)
        self._white_player_state = StateHolder(
            ws, bus, lambda p: PlayerStateChangeEvent(Player.White, p)
        )

        bs = PlayerState(initializer.player_black_initial_pawns)
        self._black_player_state = StateHolder(
           bs, bus, lambda p: PlayerStateChangeEvent(Player.Black, p)
        )

        self._player_turn = StateHolder(
            Player.Empty, bus, lambda p: PlayerTurnChangeEvent(p)
        )

    @property
    def status(self) -> StateHolder[GameStatus, GameStatusChangeEvent]:
        return self._status

    @property
    def board(self) -> StateHolder[Board, BoardStateChangeEvent]:
        return self._board_state

    @property
    def white_player_state(self) -> StateHolder[PlayerState, PlayerStateChangeEvent]:
        return self._white_player_state

    @property
    def black_player_state(self) -> StateHolder[PlayerState, PlayerStateChangeEvent]:
        return self._black_player_state

    @property
    def player_turn(self) -> StateHolder[Player, PlayerTurnChangeEvent]:
        return self._player_turn


