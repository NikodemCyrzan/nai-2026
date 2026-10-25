from __future__ import annotations

from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class Collider(Component):
    def __init__(
        self,
        go: GameObject,
        width: float,
        height: float,
        drag: float,
        offset: Vector2 | None = None,
    ):
        super().__init__(go)
        self._width = width
        self._height = height
        self._drag = drag
        self._offset = offset or Vector2()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def drag(self):
        return self._drag

    @property
    def offset(self) -> Vector2:
        return self._offset
