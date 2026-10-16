from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget
)
from game import Game
from ui.top_bar.top_bar_view import TopBarView
from ui.board.board_view import BoardView
from ui.window_controller import WindowController

class MainWindow(QMainWindow):
    def __init__(self, game: Game):
        super().__init__()
        self.setWindowTitle("NAI - Nine Men's Morris - s30161, s30291")

        self.topBar = TopBarView()
        self.board = BoardView()

        layout = QVBoxLayout()
        layout.addWidget(self.topBar)
        layout.addWidget(self.board, stretch=1)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(700, 500)

        self._window_controller = WindowController(self, game)
