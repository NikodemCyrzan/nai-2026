from ..models.color import Color
from ..models.component import Component
from ..models.game_object import GameObject
from ..models.terrain import Terrain
from ..models.vector2 import Vector2


class TerrainRenderer(Component):
    """Draws the terrain."""

    MARGIN = 100.0
    SAMPLE_SPACING = 1.0
    BOTTOM = -1000.0

    def __init__(self, go: GameObject, terrain: Terrain,
                 fill: Color = Color(190, 190, 190), stroke: Color = Color(160, 160, 160)):
        super().__init__(go)
        self._terrain = terrain
        self._fill = fill
        self._stroke = stroke

    def on_render_update(self, ctx, alpha: float, delta: float):
        """Draws the visible part of the terrain."""
        left = ctx.view_left - self.MARGIN
        right = ctx.view_right + self.MARGIN
        count = int((right - left) / self.SAMPLE_SPACING) + 1

        points = [Vector2(left, self.BOTTOM)]
        for i in range(count + 1):
            x = left + i * self.SAMPLE_SPACING
            points.append(Vector2(x, self._terrain.height_at(x)))
        points.append(Vector2(points[-1].x, self.BOTTOM))

        ctx.renderer.draw_polygon(points, fill=self._fill, stroke=self._stroke)
