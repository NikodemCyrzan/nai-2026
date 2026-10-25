import time
from engine.component_executors.physics_context import PhysicsContext
from engine.component_executors.render_context import RenderContext
from engine.models.component import Component
from engine.models.game_object import GameObject


class LoopDebugger(Component):
    def __init__(self, go: GameObject, setup=False, render=False, physics=False):
        super().__init__(go)
        self._last_physics: float | None = None
        self._setup = setup
        self._render = render
        self._physics = physics

    def on_setup(self):
        if not self._setup:
            return

        print("== setup")

    def on_render_update(self, ctx: RenderContext, alpha: float, delta: float):
        if not self._render:
            return

        print(f"== render alpha={alpha * 100:.2f}% delta={delta * 1000:.4f}ms")

    def on_physics_update(self, ctx: PhysicsContext, delta: float):
        if not self._physics:
            return

        now = time.perf_counter()
        if self._last_physics is not None:
            real = now - self._last_physics
            print(f"== physics exptected_dt={delta * 1000:.2f}ms real_dt={real * 1000:.2f}ms")
        self._last_physics = now
