from __future__ import annotations
from typing import TYPE_CHECKING

from .vector2 import Vector2

if TYPE_CHECKING:
    from .component import Component


class GameObject:
    """Object in the game world with a position, rotation and components."""

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

    def get_component[T: Component](self, component_type: type[T]) -> T | None:
        """First component of the given type, or None."""
        for comp in self._components:
            if isinstance(comp, component_type):
                return comp
        return None
