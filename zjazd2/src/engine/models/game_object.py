from typing import TYPE_CHECKING
from .vector2 import Vector2

if TYPE_CHECKING:
    from .component import Component


class GameObject:
    def __init__(
        self,
        components: list[Component],
        pos: Vector2 | None = None,
        rotation: float = 0.0,
    ):
        self._components = components
        self.position = pos or Vector2(0.0, 0.0)
        self.rotation = rotation

    @property
    def components(self):
        return self._components
