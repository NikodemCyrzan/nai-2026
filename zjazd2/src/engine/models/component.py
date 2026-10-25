from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_object import GameObject
    from ..component_executors.physics_context import PhysicsContext
    from ..component_executors.render_context import RenderContext

class Component:
    def __init__(self, go: GameObject):
        self._game_object = go

    @property
    def game_object(self) -> GameObject:
        return self._game_object

    def on_physics_update(self, ctx: PhysicsContext, delta: float):
        pass

    def on_interpolate(self, alpha: float):
        pass

    def on_render_update(self, ctx: RenderContext, alpha: float, delta: float):
        pass

    def on_setup(self):
        pass
