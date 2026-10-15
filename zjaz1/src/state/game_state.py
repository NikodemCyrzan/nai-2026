from enum import Enum

from event.bus import GameEventBus
from model.board import Board, BoardStateChangeEvent
from model.player import PlayerState, Player, PlayerStateChangeEvent, PlayerTurnChangeEvent
from model.status import GameStatusChangeEvent, GameStatus
from state.holder import StateHolder


class GameStateInitializer:
    def __init__(self,
        player_white_initial_pawns: int = 0,
        player_black_initial_pawns: int = 0
    ):
        self.player_white_initial_pawns: int = player_white_initial_pawns
        self.player_black_initial_pawns: int = player_black_initial_pawns

class GameState:
    def __init__(self, bus: GameEventBus, board: Board, initializer: GameStateInitializer):
        self._status = StateHolder(
            GameStatus.WAITING, bus, lambda s: GameStatusChangeEvent(s)
        )

        self._board_state = StateHolder(
            board, bus, lambda b: BoardStateChangeEvent(b)
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


