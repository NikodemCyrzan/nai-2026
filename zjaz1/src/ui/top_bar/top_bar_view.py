from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QWidget,
    QHBoxLayout,
    QLabel
)

BAR_BG = "#111827"
ACTIVE_BG = "#1f2937"
TEXT_ACTIVE = "#f9fafb"
TEXT_INACTIVE = "#6b7280"
MESSAGE_COLOR = "#fbbf24"

class TopBarView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("topBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"#topBar {{ background: {BAR_BG}; }}")
 
        self._white = PlayerPanel("Gracz")
        self._black = PlayerPanel("AI", mirrored=True)
 
        self._message = QLabel("")
        self._message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._message.setStyleSheet(
            f"color: {MESSAGE_COLOR}; font-size: 15px; font-weight: bold;"
        )
 
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(self._white, 0, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self._message, 0, 1)
        layout.addWidget(self._black, 0, 2, Qt.AlignmentFlag.AlignRight)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 1)
 
    def set_state(self, white: int, black: int, white_turn: bool, message: str) -> None:
        self._white.set_count(white)
        self._black.set_count(black)
        self._white.set_active(white_turn)
        self._black.set_active(not white_turn)
        self._message.setText(message)

class PlayerPanel(QWidget):
    def __init__(self, name: str, mirrored: bool = False) -> None:
        super().__init__()
        self.setObjectName("playerPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
 
        self._name = QLabel(name)
        self._count = QLabel("0")
 
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)
 
        if mirrored:
            layout.addWidget(self._count)
            layout.addWidget(self._name)
        else:
            layout.addWidget(self._name)
            layout.addWidget(self._count)
 
        self.set_active(False)
 
    def set_count(self, count: int) -> None:
        self._count.setText(str(count))
 
    def set_active(self, active: bool) -> None:
        bg = ACTIVE_BG if active else "transparent"
        color = TEXT_ACTIVE if active else TEXT_INACTIVE
        self.setStyleSheet(f"""
            #playerPanel {{ background: {bg}; border-radius: 8px; }}
            QLabel {{ color: {color}; font-size: 15px; font-weight: bold; }}
        """)