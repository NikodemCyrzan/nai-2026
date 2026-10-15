from enum import Enum

from event.events import GameEvent


class Player(Enum):
    Empty = 0,
    White = 1,
    Black = 2


class PlayerState:
    def __init__(self, initial_pawns: int = 0):
        self._pawns_left_to_place: int = initial_pawns

    @property
    def pawns_left_to_place(self) -> int:
        return self._pawns_left_to_place

    @pawns_left_to_place.setter
    def pawns_left_to_place(self, value: int):
        self._pawns_left_to_place = value



class PlayerStateChangeEvent(GameEvent):
    def __init__(self, state: PlayerState):
        self._state = state

class PlayerTurnChangeEvent(GameEvent):
    def __init__(self, player: Player):
        self.player = player