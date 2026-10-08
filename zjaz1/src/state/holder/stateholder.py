import copy
from collections.abc import Callable

from event.eventbus import GameEvent, GameEventBus

type GameEventCreator[T, E: GameEvent] = Callable[[T], E]

type ValueUpdater[T] = Callable[[T], None]

class StateHolder[T, E: GameEvent]:
    def __init__(self,
        value: T,
        bus: GameEventBus,
        creator: GameEventCreator[T, E],
    ):
        self._bus = bus
        self._creator = creator
        self._value = value


    def update(self, updater: ValueUpdater[T]):
        clone = copy.deepcopy(self._value)
        updater(clone)
        self._value = clone
        self.emit()

    def emit(self):
        clone = copy.deepcopy(self._value)
        self._bus.emit(self._creator(clone))

