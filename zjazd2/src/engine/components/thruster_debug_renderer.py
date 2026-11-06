from .thrusters import ThrusterController
from ..models.color import Color
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.vector2 import Vector2


class ThrusterDebugRenderer(Component):
    """Draws engine flames sized by the current thrust."""

    COLOR = Color(255, 120, 30)
    CORE_COLOR = Color(255, 230, 120)

    def __init__(self, go: GameObject, max_length: float = 3.0, width: float = 0.25):
        super().__init__(go)
        self._max_length = max_length
        self._width = width
        self._controller: ThrusterController | None = None

    def on_setup(self):
        self._controller = self.game_object.get_component(ThrusterController)
        if self._controller is None:
            raise RuntimeError("ThrusterDebugRenderer requires a ThrusterController on the same GameObject")

    def on_render_update(self, ctx, alpha: float, delta: float):
        """Draws a flame for each working engine."""
        go = self.game_object
        for i, thruster in enumerate(self._controller.thrusters):
            share = self._controller.current_force(i) / thruster.max_force
            if share <= 0.01:
                continue
            origin = go.position + thruster.position.rotated(go.rotation)
            backward = -thruster.direction.rotated(go.rotation)
            side = Vector2(-backward.y, backward.x) * (self._width / 2)
            tip = origin + backward * (self._max_length * share)
            ctx.renderer.draw_polygon([origin + side, tip, origin - side], fill=self.COLOR)
            ctx.renderer.draw_line(origin, origin + backward * (self._max_length * share * 0.6),
                                   self.CORE_COLOR, self._width * 0.3)
