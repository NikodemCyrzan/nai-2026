from .physics_context import PhysicsContext
from .render_context import RenderContext
from ..models.game_object import GameObject


class ComponentExecutor:
    def __init__(self, game_objects: list[GameObject]):
        self._game_objects = game_objects

    def execute_setup(self):
        for go in self._game_objects:
            for comp in go.components:
                comp.on_setup()

    def execute_physics(self, ctx: PhysicsContext, delta: float):
        for go in self._game_objects:
            for comp in go.components:
                comp.on_physics_update(ctx, delta)

    def execute_render(self, ctx: RenderContext, alpha: float, delta: float):
        for go in self._game_objects:
            for comp in go.components:
                comp.on_render_update(ctx, alpha, delta)
