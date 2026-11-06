import traceback

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication

from ..models.input import Drag, Input
from ..models.vector2 import Vector2


def _to_vector(p: QPointF) -> Vector2:
    return Vector2(p.x(), p.y())


class GameWidget(QOpenGLWidget):
    """Window that shows the game and reads the mouse."""

    def __init__(self, game_loop, render_context, input: Input):
        super().__init__()
        self._loop = game_loop
        self._ctx = render_context
        self._input = input
        self._drag_start: Vector2 | None = None
        self.frameSwapped.connect(self.update)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = _to_vector(event.position())
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._drag_start is not None:
                self._input.push_drag(Drag(self._drag_start, _to_vector(event.position())))
            self._drag_start = None
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def paintGL(self):
        """Runs one game loop tick and draws the frame."""
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.fillRect(self.rect(), QColor(25, 28, 36))

            self._ctx.begin_frame(painter, self.width(), self.height())
            self._loop.tick()
            self._ctx.end_frame()
        except Exception:
            traceback.print_exc()
            self.frameSwapped.disconnect(self.update)
            QApplication.quit()
        finally:
            painter.end()
