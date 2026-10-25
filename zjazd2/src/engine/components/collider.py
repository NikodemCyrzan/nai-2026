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
        return self._drag

    @property
    def offset(self) -> Vector2:
        return self._offset

    @property
    def corners(self) -> tuple[tuple[float, float], ...]:
        return self._corners
