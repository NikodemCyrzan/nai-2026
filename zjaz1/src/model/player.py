from enum import Enum

from event.bus import GameEvent

class PlayerPhase(Enum):
    Placing = 1,
    Moving = 2,
    Removing = 3

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

    @phase.setter
    def phase(self, new_phase: PlayerPhase):
        self._phase = new_phase

    def decrease_pawns_left_to_place(self):
        self._pawns_left_to_place -= 1




class PlayerStateChangeEvent(GameEvent):
    def __init__(self, state: PlayerState):
        self._state = state

class PlayerTurnChangeEvent(GameEvent):
    def __init__(self, player: Player):
        self.player = player

class PlayerPlacedPawnEvent(GameEvent):
    def __init__(self, player: Player, index: int):
        self.player = player
        self.index = index

class PlayerNeedToRemovePawnEvent(GameEvent):
    def __init__(self, player: Player):
        self.player = player

class PlayerRemovedPawnEvent(GameEvent):
    def __init__(self, player: Player, index: int):
        self.player = player
        self.index = index

