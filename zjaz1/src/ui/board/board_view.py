from PyQt6.QtCore import (QPointF, Qt, pyqtSignal)
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import (QWidget)
from state.player import Player

BOARD_BG = "#111827"
LINE_COLOR = "#4b5563"
POINT_COLOR = "#6b7280"
WHITE_PIECE = "#f9fafb"
BLACK_PIECE = "#1f2937"
PIECE_OUTLINE = "#9ca3af"

POINTS: list[tuple[int, int]] = [
    (0, 0), (3, 0), (6, 0), (6, 3), (6, 6), (3, 6), (0, 6), (0, 3),
    (1, 1), (3, 1), (5, 1), (5, 3), (5, 5), (3, 5), (1, 5), (1, 3),
    (2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (2, 3),
]

LINES: list[tuple[int, int]] = (
    [(s + i, s + (i + 1) % 8) for s in (0, 8, 16) for i in range(8)]
    + [(1, 9), (9, 17), (3, 11), (11, 19), (5, 13), (13, 21), (7, 15), (15, 23)]
)

class BoardView(QWidget):
    point_clicked = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background: {BOARD_BG};")
        self._nodes: list[Player] = [Player.Node] * 24

    def set_nodes(self, nodes: list[Player]):
        self._nodes = list(nodes)
        self.update()

    def _geometry(self) -> tuple[float, float, float]:
        side = min(self.width(), self.height())
        margin = side * 0.08
        step = (side - 2 * margin) / 6
        x0 = (self.width() - side) / 2 + margin
        y0 = (self.height() - side) / 2 + margin
        return x0, y0, step

    def _point_pos(self, index: int) -> QPointF:
        x0, y0, step = self._geometry()
        col, row = POINTS[index]
        return QPointF(x0 + col * step, y0 + row * step)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        _, _, step = self._geometry()
 
        p.setPen(QPen(QColor(LINE_COLOR), 3))
        for a, b in LINES:
            p.drawLine(self._point_pos(a), self._point_pos(b))
 
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(POINT_COLOR))
        for i in range(24):
            p.drawEllipse(self._point_pos(i), 6, 6)
 
        radius = step * 0.32
        p.setPen(QPen(QColor(PIECE_OUTLINE), 2))
        for i, piece in enumerate(self._nodes):
            if piece is Player.Node:
                continue
            p.setBrush(QColor(WHITE_PIECE if piece == "white" else BLACK_PIECE))
            p.drawEllipse(self._point_pos(i), radius, radius)

    def mousePressEvent(self, event):
        click = event.position()
        _, _, step = self._geometry()
        for i in range(24):
            delta = self._point_pos(i) - click
            if delta.x() ** 2 + delta.y() ** 2 <= (step * 0.4) ** 2:
                self.point_clicked.emit(i)
                return
