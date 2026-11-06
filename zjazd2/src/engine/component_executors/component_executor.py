from .physics_context import PhysicsContext
from .render_context import RenderContext
from ..models.game_object import GameObject


class ComponentExecutor:
    """Runs component callbacks for all game objects."""

    def __init__(self, game_objects: list[GameObject]):
        self._game_objects = game_objects

    def execute_setup(self):
        """Calls setup on every component."""
        for go in self._game_objects:
            for comp in go.components:
                comp.on_setup()

    def execute_physics(self, ctx: PhysicsContext, delta: float):
        """Runs one physics step on every enabled component."""
        for go in self._game_objects:
            for comp in go.components:
                if comp.enabled:
                    comp.on_physics_update(ctx, delta)

    def execute_interpolate(self, alpha: float):
        """Smooths positions between physics steps."""
        for go in self._game_objects:
            for comp in go.components:
                comp.on_interpolate(alpha)

    def execute_render(self, ctx: RenderContext, alpha: float, delta: float):
        """Draws every enabled component."""
        for go in self._game_objects:
            for comp in go.components:
                if comp.enabled:
                    comp.on_render_update(ctx, alpha, delta)
