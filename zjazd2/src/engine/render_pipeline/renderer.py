import math

from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QPainter, QPainterPath, QPen, QPixmap, QPolygonF
from PySide6.QtSvg import QSvgRenderer

from ..models.vector2 import Vector2


def prepare_painter(p: QPainter, pos: Vector2, rotation: float):
    p.save()
    p.translate(pos.x, pos.y)
    p.rotate(math.degrees(rotation))


class Renderer:
    def __init__(self):
        self._painter: QPainter | None = None

    def begin(self, painter: QPainter) -> None:
        self._painter = painter

    def end(self) -> None:
        self._painter = None

    def draw_path(self, path: QPainterPath, pos: Vector2, rotation: float, pen: QPen, brush: QBrush) -> None:
        p = self._painter
        assert p is not None

        prepare_painter(p, pos, rotation)
        p.setPen(pen)
        p.setBrush(brush)
        p.drawPath(path)
        p.restore()

    def draw_pixmap(self, pixmap: QPixmap, target: QRectF, pos: Vector2, rotation: float) -> None:
        p = self._painter
        assert p is not None

        prepare_painter(p, pos, rotation)
        p.scale(1, -1)
        p.drawPixmap(target, pixmap, QRectF(pixmap.rect()))
        p.restore()

    def draw_polygon(self, polygon: QPolygonF, pen: QPen, brush: QBrush) -> None:
        p = self._painter
        assert p is not None

        p.setPen(pen)
        p.setBrush(brush)
        p.drawPolygon(polygon)

    def draw_svg(self, svg: QSvgRenderer, target: QRectF, pos: Vector2, rotation: float) -> None:
        p = self._painter
        assert p is not None

        prepare_painter(p, pos, rotation)
        p.scale(1, -1)
        svg.render(p, target)
        p.restore()
