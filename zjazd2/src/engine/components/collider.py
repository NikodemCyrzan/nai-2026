import math

from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class Collider(Component):
    """Rectangle used for collisions with the terrain."""

    def __init__(
        self,
        go: GameObject,
        width: float,
        height: float,
        drag: float,
        offset: Vector2 | None = None,
    ):
        super().__init__(go)
        assert width > 0.0 and height > 0.0
        self._width = width
        self._height = height
        self._drag = drag
        self._offset = offset or Vector2()

        hw, hh = width / 2, height / 2
        self._corners = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def drag(self) -> float:
        """Friction against the terrain."""
        return self._drag

    @property
    def offset(self) -> Vector2:
        """Position relative to the center of the body."""
        return self._offset

    @property
    def corners(self) -> tuple[tuple[float, float], ...]:
        """Corners relative to the center of the rectangle."""
        return self._corners

    def world_corners(self, position: Vector2, rotation: float) -> list[Vector2]:
        """Corners of the rectangle in world space."""
        c, s = math.cos(rotation), math.sin(rotation)
        ox, oy = self._offset.x, self._offset.y
        cx = position.x + ox * c - oy * s
        cy = position.y + ox * s + oy * c
        return [Vector2(cx + lx * c - ly * s, cy + lx * s + ly * c) for lx, ly in self._corners]
