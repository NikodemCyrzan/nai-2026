from __future__ import annotations

from dataclasses import dataclass

from .vector2 import Vector2


@dataclass(frozen=True)
class Drag:
    """Mouse drag in screen pixels."""

    start: Vector2
    end: Vector2

    @property
    def delta(self) -> Vector2:
        """Drag vector with y pointing up."""
        return Vector2(self.end.x - self.start.x, self.start.y - self.end.y)


class Input:
    """Player input state."""

    def __init__(self):
        self._drags: list[Drag] = []

    def consume_drags(self) -> list[Drag]:
        """Returns new drags and clears them."""
        drags, self._drags = self._drags, []
        return drags

    def push_drag(self, drag: Drag) -> None:
        self._drags.append(drag)
