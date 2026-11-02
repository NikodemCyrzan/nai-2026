from PySide6.QtCore import QPoint
from PySide6.QtGui import QPolygon, QPen, QBrush, QColor

from ..models.component import Component
from ..models.game_object import GameObject
from ..models.terrain import Terrain


class TerrainRenderer(Component):
    def __init__(self, go: GameObject, terrain: Terrain):
        super().__init__(go)
        self._terrain = terrain

    def on_render_update(self, ctx, alpha: float, delta: float):
        left = int(ctx.view_left - 100)
        right = int(ctx.view_right + 100)

        arr = [QPoint(x, int(self._terrain.height_at(x))) for x in range(left, right)]
        arr.insert(0, QPoint(left, -1000))
        arr.append(QPoint(right, -1000))
        p = QPolygon(arr)

        pen = QPen(QColor(160,160,160))
        pen.setWidth(0.9)

        brush = QBrush(QColor(190,190,190))

        ctx.renderer.draw_polygon(p, pen, brush)
