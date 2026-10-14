from enum import Enum

from controller.action.actions import GameAction, GameStartAction
from models.player import Player
from state.state import GameState, GameStatus


class GameLogic:
    def __init__(self, state: GameState):
        self._state = state


    def handle[A: GameAction](self, action: A, player: Player) -> None:
        if type(action) == GameStartAction:
            self._start()


    def _start(self) -> None:
        if self._status() == GameStatus.WAITING:
            self._update_status(GameStatus.STARTED)
            self._next_turn()

        pass

    def _status(self) -> GameStatus:
        return self._state.status.value

    def _update_status(self, status: GameStatus) -> None:
        return self._state.status.update(lambda s: status)

    def _current_turn(self) -> Player:
        return self._state.player_turn.value

    def _change_turn(self, player: Player) -> None:
        self._state.player_turn.update(lambda p: player)

    def _next_turn(self) -> Player:
        if self._current_turn() in [Player.Empty, Player.Black]:
            return Player.White
        else:
            return Player.Black








