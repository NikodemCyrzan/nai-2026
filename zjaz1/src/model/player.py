from enum import Enum

from event.bus import GameEvent

class PlayerPhase(Enum):
    Placing = 1,
    Moving = 2,
    Flying = 3,
    Removing = 4

class Player(Enum):
    Empty = 0,
    White = 1,
    Black = 2


class PlayerState:
    def __init__(self, initial_pawns: int = 0):
        self._pawns_left_to_place: int = initial_pawns
        self._phase = PlayerPhase.Placing


    @property
    def pawns_left_to_place(self) -> int:
        return self._pawns_left_to_place

    @property
    def phase(self) -> PlayerPhase:
        return self._phase

    def decrease_pawns_left_to_place(self) -> None:
        if self._pawns_left_to_place > 0:
            self._pawns_left_to_place -= 1
        else:
            raise ValueError("No pawns left to place.")

    def is_moving(self) -> bool:
        return self._phase == PlayerPhase.Moving

    def is_flying(self) -> bool:
        return self._phase == PlayerPhase.Flying

    def is_removing(self) -> bool:
        return self._phase == PlayerPhase.Removing

    def is_placing(self) -> bool:
        return self._phase == PlayerPhase.Placing

    def set_moving_phase(self):
        self._phase = PlayerPhase.Moving

    def set_flying_phase(self):
        self._phase = PlayerPhase.Flying

    def set_removing_phase(self):
        self._phase = PlayerPhase.Removing

    def set_placing_phase(self):
        self._phase = PlayerPhase.Placing



class PlayerStateChangeEvent(GameEvent):
    def __init__(self, player: Player, state: PlayerState):
        self.player = player
        self._state = state

class PlayerTurnChangeEvent(GameEvent):
    def __init__(self, player: Player):
        self.player = player

class PlayerPlacedPawnEvent(GameEvent):
    def __init__(self, player: Player, index: int):
        self.player = player
        self.index = index

class PlayerMovedPawnEvent(GameEvent):
    def __init__(self, player: Player, from_index: int, to_index: int):
        self.player = player
        self.from_index = from_index
        self.to_index = to_index

class PlayerHasMillEvent(GameEvent):
    def __init__(self, player: Player, mill: tuple[int, int, int]):
        self.player = player
        self.mill = mill

class PlayerRemovedPawnEvent(GameEvent):
    def __init__(self, player: Player, index: int):
        self.player = player
        self.index = index

