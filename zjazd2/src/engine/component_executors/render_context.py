from PySide6.QtGui import QPainter, QTransform

from ..models.vector2 import Vector2
from ..render_pipeline.renderer import Renderer

class RenderContext:
    def __init__(self):
        self.renderer = Renderer()
        self.view_left = 0.0
        self.view_right = 0.0
        self._painter: QPainter | None = None
        self._width = 0
        self._height = 0

    def begin_frame(self, painter: QPainter, width: int, height: int) -> None:
        self._painter = painter
        self._width = width
        self._height = height
        self.renderer.begin(painter)

    def end_frame(self) -> None:
        self.renderer.end()
        self._painter = None

    def set_view(self, center: Vector2, pixels_per_unit: float) -> None:
        assert self._painter is not None

        t = QTransform()
        t.translate(self._width / 2.0, self._height / 2.0)
        t.scale(pixels_per_unit, -pixels_per_unit)
        t.translate(-center.x, -center.y)
        self._painter.setTransform(t)

        half_w = self._width / 2.0 / pixels_per_unit
        self.view_left = center.x - half_w
        self.view_right = center.x + half_w
