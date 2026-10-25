from ..models.component import Component
from ..models.game_object import GameObject


class Collider(Component):
    def __init__(self, go: GameObject, width: float, height: float, drag: float):
        super().__init__(go)
        self._width = width
        self._height = height
        self._drag = drag

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def drag(self):
        return self._drag
