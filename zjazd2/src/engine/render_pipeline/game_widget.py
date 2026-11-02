import traceback
from collections.abc import Callable

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication


class GameWidget(QOpenGLWidget):
    def __init__(
        self,
        game_loop,
        render_context,
        on_drag: Callable[[QPoint, QPoint], None] | None = None,
        on_key: Callable[[int, bool], None] | None = None,
    ):
        super().__init__()
        self._loop = game_loop
        self._ctx = render_context
        self._on_drag = on_drag
        self._on_key = on_key
        self._drag_start: QPoint | None = None
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.frameSwapped.connect(self.update)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setFocus()
            self._drag_start = event.position().toPoint()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            start = self._drag_start
            self._drag_start = None
            if start is not None and self._on_drag is not None:
                self._on_drag(start, event.position().toPoint())
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right):
            if not event.isAutoRepeat() and self._on_key is not None:
                self._on_key(event.key(), True)
            event.accept()
            return
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right):
            if not event.isAutoRepeat() and self._on_key is not None:
                self._on_key(event.key(), False)
            event.accept()
            return
        super().keyReleaseEvent(event)

    def paintGL(self):
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
