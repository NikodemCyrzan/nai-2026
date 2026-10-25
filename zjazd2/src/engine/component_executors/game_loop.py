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
        self._running = False
        self._render_context = render_context
        self._physics_context = physics_context

    def setup_components(self):
        self._component_executor.execute_setup()

    def start_loop(self):
        self._running = True
        dt = self._physics_context.delta
        accumulator = 0.0
        previous = time.perf_counter()

        while self._running:
            now = time.perf_counter()
            frame_time = min(now - previous, self.MAX_FRAME_TIME)
            previous = now
            accumulator += frame_time

            while accumulator >= dt:
                self._component_executor.execute_physics(self._physics_context, self._physics_context.delta)
                accumulator -= dt

            alpha = accumulator / dt
            self._component_executor.execute_render(self._render_context, alpha)

    def stop_loop(self):
        self._running = False
