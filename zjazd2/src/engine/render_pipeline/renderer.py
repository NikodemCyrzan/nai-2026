import math
from collections.abc import Sequence

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen, QPixmap, QPolygonF
from PySide6.QtSvg import QSvgRenderer

from ..models.color import Color
from ..models.vector2 import Vector2


def _qcolor(color: Color) -> QColor:
    return QColor(color.r, color.g, color.b, color.a)


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

    def draw_polygon(
        self,
        points: Sequence[Vector2],
        fill: Color | None = None,
        stroke: Color | None = None,
        stroke_width: float = 0.0,
    ) -> None:
        """Draws a polygon in world coordinates. stroke_width is in world units (0 = 1px hairline)."""
        p = self._painter
        assert p is not None

        if stroke is None:
            pen = QPen(Qt.PenStyle.NoPen)
        else:
            pen = QPen(_qcolor(stroke))
            pen.setWidthF(stroke_width)
        brush = QBrush(_qcolor(fill)) if fill is not None else QBrush(Qt.BrushStyle.NoBrush)

        p.setPen(pen)
        p.setBrush(brush)
        p.drawPolygon(QPolygonF([QPointF(v.x, v.y) for v in points]))

    def draw_svg(self, svg: QSvgRenderer, target: QRectF, pos: Vector2, rotation: float) -> None:
        p = self._painter
        assert p is not None

        prepare_painter(p, pos, rotation)
        p.scale(1, -1)
        svg.render(p, target)
        p.restore()
