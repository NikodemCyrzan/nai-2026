import time
from enum import Enum, auto
from engine.component_executors.physics_context import PhysicsContext
from engine.component_executors.render_context import RenderContext
from engine.models.component import Component
from engine.models.game_object import GameObject


class LoopDebugger(Component):
    def __init__(self, go: GameObject, log_types: set[LogType], setup=False, render=False, physics=False):
        super().__init__(go)
        self._last_physics: float | None = None
        self._setup = setup
        self._render = render
        self._physics = physics
        self._log_types = log_types

    def on_setup(self):
        if not self._setup:
            return

        if LogType.DELTA in self._log_types:
            print("[INFO] setup")

    def on_render_update(self, ctx: RenderContext, alpha: float, delta: float):
        if not self._render:
            return

        if LogType.DELTA in self._log_types:
            print(f"[INFO] render alpha={alpha * 100:.2f}% delta={delta * 1000:.4f}ms")

    def on_physics_update(self, ctx: PhysicsContext, delta: float):
        if not self._physics:
            return

        if LogType.DELTA in self._log_types or LogType.DELTA_ERRORS in self._log_types:
            now = time.perf_counter()
            if self._last_physics is not None:
                real = now - self._last_physics
                if LogType.DELTA in self._log_types:
                    print(f"[INFO] physics exptected_dt={delta * 1000:.2f}ms real_dt={real * 1000:.2f}ms")
                if LogType.DELTA_ERRORS in self._log_types:
                    if abs(real - delta) >= 0.0001:
                        print(f"[WARNING] physics exptected_dt={delta * 1000:.2f}ms real_dt={real * 1000:.2f}ms")
            self._last_physics = now


class LogType(Enum):
    DELTA = auto(),
    DELTA_ERRORS = auto(),
    RENDER_CONTEXT = auto(),
    PHYSICS_CONTEXT = auto()
