import copy
from collections.abc import Callable
from collections import defaultdict

from event.events import GameEvent

type GameEventListener[E: GameEvent] = Callable[[E], None]

class GameEventBus:
    def __init__(self):
        self._listeners: dict[
            type[GameEvent],
            set[Callable[[GameEvent], None]]
        ] = defaultdict(set)

    def subscribe[E: GameEvent](self,
        event_type: type[E],
        listener: GameEventListener[E],
    ) -> None:
        self._listeners[event_type].add(listener)

    def unsubscribe[E: GameEvent](self,
        event_type: type[E],
        listener: GameEventListener[E],
    ) -> None:
        self._listeners[event_type].discard(listener)

    def emit[E: GameEvent](self, event: E) -> None:
        for listener in self._listeners[type(event)]:
            listener(copy.deepcopy(event))


