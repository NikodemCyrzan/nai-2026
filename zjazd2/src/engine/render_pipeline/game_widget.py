import traceback
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication


class GameWidget(QOpenGLWidget):
    def __init__(self, game_loop, render_context):
        super().__init__()
        self._loop = game_loop
        self._ctx = render_context
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.frameSwapped.connect(self.update)

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
