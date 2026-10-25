import time
from .component_executor import ComponentExecutor
from .physics_context import PhysicsContext
from .render_context import RenderContext
from ..models.game_object import GameObject


class GameLoop:
    MAX_FRAME_TIME = 0.25

    def __init__(self, game_objects: list[GameObject], render_context: RenderContext, physics_context: PhysicsContext):
        assert physics_context.delta > 0
        self._component_executor = ComponentExecutor(game_objects)
        self._render_context = render_context
        self._physics_context = physics_context
        self._accumulator = 0.0
        self._previous: float | None = None

    def setup_components(self):
        self._component_executor.execute_setup()

    def tick(self):
        now = time.perf_counter()
        if self._previous is None:
            self._previous = now
        real_frame_time = now - self._previous
        self._previous = now

        dt = self._physics_context.delta
        self._accumulator += min(real_frame_time, self.MAX_FRAME_TIME)

        while self._accumulator >= dt:
            self._component_executor.execute_physics(self._physics_context, dt)
            self._accumulator -= dt

        alpha = self._accumulator / dt
        self._component_executor.execute_interpolate(alpha)
        self._component_executor.execute_render(self._render_context, alpha, real_frame_time)
