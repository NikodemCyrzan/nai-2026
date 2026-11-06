from .sensor import Sensor
from ..models.color import Color
from ..models.component import Component
from ..models.game_object import GameObject


class SensorDebugRenderer(Component):
    """Draws the sensors, their rays and hit points."""

    HIT_COLOR = Color(255, 170, 0)
    MISS_COLOR = Color(120, 140, 170, 140)
    MOUNT_COLOR = Color(0, 200, 255)

    def __init__(self, go: GameObject, ray_width: float = 0.04, marker_radius: float = 0.12):
        super().__init__(go)
        self._ray_width = ray_width
        self._marker_radius = marker_radius
        self._sensors: list[Sensor] = []

    def on_setup(self):
        self._sensors = [c for c in self.game_object.components if isinstance(c, Sensor)]

    def on_render_update(self, ctx, alpha: float, delta: float):
        """Draws each sensor ray."""
        go = self.game_object
        r = self._marker_radius

        for sensor in self._sensors:
            origin = sensor.world_origin(go.position, go.rotation)
            direction = sensor.direction
            distance = sensor.distance

            if distance is None:
                end = origin + direction * sensor.max_range
                ctx.renderer.draw_line(origin, end, self.MISS_COLOR, self._ray_width)
            else:
                end = origin + direction * distance
                ctx.renderer.draw_line(origin, end, self.HIT_COLOR, self._ray_width)
                ctx.renderer.draw_circle(end, r, fill=self.HIT_COLOR)

            ctx.renderer.draw_circle(origin, r * 0.7, fill=self.MOUNT_COLOR)
