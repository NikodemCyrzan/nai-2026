from collections.abc import Callable

from controller.actions import GameAction, GameStartAction, PlayerPlacePawnAction, PlayerMovePawnAction
from event.bus import GameEventBus, GameEvent
from model.board import Board
from model.player import Player, PlayerPlacedPawnEvent
from state.game_state import GameState, GameStatus
from state.holder import ValueUpdater


class NoGameActionHandlerFound(Exception):
    def __init__(self, action: GameAction) -> None:
        self.action = action

class GameLogic:
    def __init__(self, state: GameState, bus: GameEventBus):
        self._state = state
        self._bus = bus


    def handle[A: GameAction](self, action: A, player: Player) -> None:
        if isinstance(action, GameStartAction):
            self._start()

        elif isinstance(action, PlayerPlacePawnAction):
            self._place_pawn(action.at_index, player)

        elif isinstance(action, PlayerMovePawnAction):
            # Implement the logic for moving a pawn here
            pass

        elif isinstance(action, GameAction):
            raise NoGameActionHandlerFound(action)



    def _start(self) -> None:
        if self._status == GameStatus.Waiting:
            self._update_status(GameStatus.Starting)
            self._emit_event(GameStartedEvent())

            self._update_status(GameStatus.In_Progress)
            self._next_turn()

        pass

    @property
    def _board(self):
        return self._state.board.value

    @property
    def _status(self) -> GameStatus:
        return self._state.status.value

    def _update_status(self, status: GameStatus) -> None:
        return self._state.status.update(lambda s: status)

    def _update_board(self, updater: ValueUpdater[Board]) -> None:
        return self._state.board.update(updater)

    def _current_turn(self) -> Player:
        return self._state.player_turn.value

    def _change_turn(self, player: Player) -> None:
        self._state.player_turn.update(lambda p: player)

    def _place_pawn(self, index: int, player: Player) -> None:
        if self._current_turn() != player:
            self._emit_exception_event(f"It's not {player}'s turn!", player)
            return

        node = self._board.get(index)

        if node != Player.Empty:
            self._emit_exception_event(f"Position {index} is already occupied!", player)
            return

        self._update_board(lambda b: b.set(index, player))

        print(f"{player} placed a pawn at {index}")
        self._emit_event(PlayerPlacedPawnEvent(player, index))

        self._next_turn()

    def _next_turn(self) -> None:
        turn = Player.White if self._current_turn() in [Player.Empty, Player.Black] else Player.Black
        self._change_turn(turn)

    def _emit_exception_event(self, message: str, player: Player = None) -> None:
        self._emit_event(GameExceptionEvent(message, player))

    def _emit_event(self, event: GameEvent) -> None:
        self._bus.emit(event)



class GameStartedEvent(GameEvent):
    pass

class GameEndedEvent(GameEvent):
    pass

class GameExceptionEvent(GameEvent):
    def __init__(self, message: str, player: Player = None):
        self.message = message
        self.player = player








