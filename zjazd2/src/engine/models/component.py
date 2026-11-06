from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_object import GameObject
    from ..component_executors.physics_context import PhysicsContext
    from ..component_executors.render_context import RenderContext

class Component:
    """Base class for everything attached to a game object."""

    def __init__(self, go: GameObject):
        self._game_object = go
        self.enabled = True

    @property
    def game_object(self) -> GameObject:
        return self._game_object

    def on_physics_update(self, ctx: PhysicsContext, delta: float):
        """Called on every physics step."""
        pass

    def on_interpolate(self, alpha: float):
        """Called before drawing to smooth movement."""
        pass

    def on_render_update(self, ctx: RenderContext, alpha: float, delta: float):
        """Called on every frame to draw."""
        pass

    def on_setup(self):
        """Called once before the game starts."""
        pass
