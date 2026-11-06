from __future__ import annotations

from dataclasses import dataclass

from .vector2 import Vector2


@dataclass(frozen=True)
class Drag:
    """Mouse drag in screen pixels (y grows downward)."""
    start: Vector2
    end: Vector2

    @property
    def delta(self) -> Vector2:
        """Drag vector with y pointing up, matching world orientation."""
        return Vector2(self.end.x - self.start.x, self.start.y - self.end.y)


class Input:
    """Raw input state, written by the window layer and read by components."""

    def __init__(self):
        self._drags: list[Drag] = []

    def consume_drags(self) -> list[Drag]:
        """Returns drags since the last call and clears them. Call from physics update."""
        drags, self._drags = self._drags, []
        return drags

    def push_drag(self, drag: Drag) -> None:
        self._drags.append(drag)
