import copy
from collections.abc import Callable
from typing import Any

from event.bus import GameEvent, GameEventBus

type GameEventCreator[T, E: GameEvent] = Callable[[T], E]

type ValueUpdater[T] = Callable[[T], Any]

class StateHolder[T, E: GameEvent]:
    def __init__(self,
        value: T,
        bus: GameEventBus,
        creator: GameEventCreator[T, E],
    ):
        self._bus = bus
        self._creator = creator
        self._value = value


    @property
    def value(self) -> T:
        return copy.deepcopy(self._value)

    def update(self, updater: ValueUpdater[T]):
        passed = copy.deepcopy(self._value)
        returned = updater(passed)
        self._value = returned if returned is not None else passed
        self._emit()

    def _emit(self):
        clone = copy.deepcopy(self._value)
        self._bus.emit(self._creator(clone))

