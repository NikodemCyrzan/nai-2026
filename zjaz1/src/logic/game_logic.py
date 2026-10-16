from collections.abc import Callable

from typing import Final

from constants import PLAYER_MINIMUM_PAWNS_COUNT, PLAYER_FLYING_PAWNS_COUNT
from controller.actions import GameAction, GameStartAction, PlayerPlacePawnAction, PlayerMovePawnAction, \
    PlayerRemovePawnAction
from event.bus import GameEventBus, GameEvent
from model import board
from model.board import Board
from model.player import Player, PlayerPlacedPawnEvent, PlayerState, PlayerStateChangeEvent, PlayerPhase, \
    PlayerRemovedPawnEvent, PlayerMovedPawnEvent, PlayerHasMillEvent
from state.game_state import GameState, GameStatus
from state.holder import ValueUpdater, StateHolder

MILLS: Final[tuple[tuple[int, int, int], ...]] = (
    # Outer
    (0, 1, 2),
    (2, 3, 4),
    (4, 5, 6),
    (6, 7, 0),

    # Middle
    (8, 9, 10),
    (10, 11, 12),
    (12, 13, 14),
    (14, 15, 8),

    # Inner
    (16, 17, 18),
    (18, 19, 20),
    (20, 21, 22),
    (22, 23, 16),

    # Connections between layers
    (1, 9, 17),
    (3, 11, 19),
    (5, 13, 21),
    (7, 15, 23),
)

class GameLogic:
    def __init__(self, state: GameState, bus: GameEventBus):
        self._state = state
        self._bus = bus

    def handle[A: GameAction](self, action: A, player: Player) -> None:
        if isinstance(action, GameStartAction):
            if self._status != GameStatus.Waiting:
                self._emit_exception_event("Game has already started!", player)
                return

            self._start()
            return

        if self._status != GameStatus.In_Progress:
            self._emit_exception_event("Game is not in progress!", player)
            return

        if isinstance(action, PlayerPlacePawnAction):
            self._place_pawn(action.at_index, player)

        elif isinstance(action, PlayerMovePawnAction):
            self._move_pawn(action.from_index, action.to_index, player)

        elif isinstance(action, PlayerRemovePawnAction):
            self._remove_pawn(action.at_index, player)

        else:
            raise NoGameActionHandlerFound(action)



    def _start(self) -> None:
        if self._status == GameStatus.Waiting:
            self._update_status(GameStatus.Starting)
            self._emit_event(GameStartedEvent())

            self._update_status(GameStatus.In_Progress)
            self._next_turn()


    def _end(self, winner: Player) -> None:
        self._update_status(GameStatus.Ended)
        self._emit_event(GameEndedEvent(winner))

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

        node: Player = self._board.get(index)

        if node != Player.Empty:
            self._emit_exception_event(f"Position {index} is already occupied!", player)
            return

        state: StateHolder[PlayerState, PlayerStateChangeEvent] = self._identify_player_state_holder(player)

        if state.value.phase != PlayerPhase.Placing:
            self._emit_exception_event(f"{player} is not in the placing phase!", player)
            return

        if state.value.pawns_left_to_place <= 0:
            self._emit_exception_event(f"{player} has no pawns left to place!", player)
            return

        self._update_board(lambda b: b.set(index, player))

        state.update(lambda ps: ps.decrease_pawns_left_to_place())
        state.update(
            lambda ps: ps.set_moving_phase()
            if ps.pawns_left_to_place == 0 else ps
        )

        self._emit_event(PlayerPlacedPawnEvent(player, index))

        has_mill, mill = self._is_3_in_a_row(index, player)

        if has_mill:
            state.update(lambda ps: ps.set_removing_phase())
            self._emit_event(PlayerHasMillEvent(player, mill))
            return

        self._next_turn()

    def _move_pawn(self, from_index: int, to_index: int, player: Player) -> None:
        if self._current_turn() != player:
            self._emit_exception_event(f"It's not {player}'s turn!", player)
            return

        from_node: Player = self._board.get(from_index)
        to_node: Player = self._board.get(to_index)

        state: StateHolder[PlayerState, PlayerStateChangeEvent] = self._identify_player_state_holder(player)

        if state.value.phase not in [PlayerPhase.Moving, PlayerPhase.Flying]:
            self._emit_exception_event(f"{player} is not in the moving or flying phase!", player)
            return

        if from_index == to_index:
            self._emit_exception_event(f"Cannot move to the same position {to_index}!", player)
            return

        if from_node != player:
            self._emit_exception_event(f"Position {from_index} does not contain {player}'s pawn!", player)
            return

        if to_node != Player.Empty:
            self._emit_exception_event(f"Position {to_index} is already occupied!", player)
            return


        if state.value.phase == PlayerPhase.Moving:
            neighbours = self._board.get_neighbours(from_index)
            if to_index not in neighbours:
                self._emit_exception_event(f"Position {to_index} is not a valid move for {player}!", player)
                return

        self._update_board(lambda b: b.set(from_index, Player.Empty))
        self._update_board(lambda b: b.set(to_index, player))

        self._emit_event(PlayerMovedPawnEvent(player, from_index, to_index))

        has_mill, mill = self._is_3_in_a_row(to_index, player)

        if has_mill:
            state.update(lambda ps: ps.set_removing_phase())
            self._emit_event(PlayerHasMillEvent(player, mill))
            return

        self._next_turn()

    def _remove_pawn(self, index: int, player: Player) -> None:
        if self._current_turn() != player:
            self._emit_exception_event(
                f"It's not {player}'s turn!", player
            )
            return

        node: Player = self._board.get(index)

        state = self._identify_player_state_holder(player)

        if not state.value.is_removing():
            self._emit_exception_event(f"{player} is not in the removing phase!", player)
            return

        if node == Player.Empty:
            self._emit_exception_event(f"Position {index} is already empty!", player)
            return

        if node == player:
            self._emit_exception_event(f"{player} cannot remove their own pawn!", player)
            return

        if not self._can_remove_pawn(index, node):
            self._emit_exception_event("Cannot remove a protected pawn!", player)
            return

        # Remove the opponent's pawn exactly once.
        self._update_board(lambda b: b.set(index, Player.Empty))

        self._emit_event(PlayerRemovedPawnEvent(player, index))

        # Check defeat only after the opponent has finished Placing.
        if not self._should_player_place(node):
            if self._should_player_lose(node):
                self._end(player)
                return

            if self._pawns_on_board_count(node) == PLAYER_FLYING_PAWNS_COUNT:
                opponent_state = self._identify_player_state_holder(node)
                opponent_state.update(lambda ps: ps.set_flying_phase())

        # Restore the capturing player's previous gameplay phase.
        if self._should_player_place(player):
            state.update(lambda ps: ps.set_placing_phase())

        elif self._should_player_fly(player):
            state.update(lambda ps: ps.set_flying_phase())

        else:
            state.update(lambda ps: ps.set_moving_phase())

        self._next_turn()

    def _can_remove_pawn(self, index: int, opponent: Player) -> bool:
        if not self._is_3_in_a_row(index, opponent)[0]:
            return True

        return all(self._is_3_in_a_row(i, opponent)[0]
            for i, pawn in enumerate(self._board.get_all_nodes())
            if pawn == opponent
        )

    def _is_3_in_a_row(self, index: int, player: Player) -> tuple[bool, tuple[int, int, int]]:
        for mill in MILLS:
            if index not in mill:
                continue

            if all(self._board.get(i) == player for i in mill):
                return True, mill

        return False, (0, 0, 0)

    def _has_available_moves(self, player: Player) -> bool:
        for index, node in enumerate(self._board.get_all_nodes()):
            if node != player:
                continue

            for neighbour in self._board.get_neighbours(index):
                if self._board.get(neighbour) == Player.Empty:
                    return True

        return False


    def _pawns_on_board_count(self, player: Player) -> int:
        return self._board.get_all_nodes().count(player)

    def _should_player_lose(self, player: Player) -> bool:
        return self._pawns_on_board_count(player) < PLAYER_MINIMUM_PAWNS_COUNT

    def _should_player_fly(self, player: Player) -> bool:
        return self._pawns_on_board_count(player) <= PLAYER_FLYING_PAWNS_COUNT

    def _should_player_place(self, player: Player) -> bool:
        return self._identify_player_state_holder(player).value.pawns_left_to_place > 0

    def _identify_player_state_holder(self, player: Player) -> StateHolder[PlayerState, PlayerStateChangeEvent]:
        if player == Player.White:
            return self._state.white_player_state
        elif player == Player.Black:
            return self._state.black_player_state
        else:
            raise ValueError(f"Invalid player: {player}")

    def _next_turn(self) -> None:
        next_player = (Player.White if self._current_turn() in [Player.Empty, Player.Black] else Player.Black)

        state = self._identify_player_state_holder(next_player).value

        if state.phase == PlayerPhase.Moving:
            if not self._has_available_moves(next_player):
                winner = (Player.Black if next_player == Player.White else Player.White)

                self._end(winner)
                return

        self._change_turn(next_player)

    def _emit_exception_event(self, message: str, player: Player = None) -> None:
        self._emit_event(GameExceptionEvent(message, player))

    def _emit_event(self, event: GameEvent) -> None:
        self._bus.emit(event)

    @property
    def _board(self):
        return self._state.board.value

    @property
    def _status(self) -> GameStatus:
        return self._state.status.value



class GameStartedEvent(GameEvent):
    pass

class GameEndedEvent(GameEvent):
    def __init__(self, winner: Player) -> None:
        self.winner = winner

class GameExceptionEvent(GameEvent):
    def __init__(self, message: str, player: Player = None):
        self.message = message
        self.player = player

class NoGameActionHandlerFound(Exception):
    def __init__(self, action: GameAction) -> None:
        self.action = action







