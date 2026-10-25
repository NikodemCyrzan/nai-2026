import math
from ..models.component import Component


class Camera(Component):
    def __init__(self, go, target=None, pixels_per_unit: float = 20.0, smoothing: float = 5.0):
        super().__init__(go)
        self.target = target
        self.pixels_per_unit = pixels_per_unit
        self._smoothing = smoothing

    def on_render_update(self, ctx, alpha, delta):
        pos = self.game_object.position
        if self.target:
            goal = self.target.position
            k = 1.0 - math.exp(-self._smoothing * delta)
            pos.x += (goal.x - pos.x) * k
            pos.y += (goal.y - pos.y) * k
        ctx.set_view(pos, self.pixels_per_unit)
