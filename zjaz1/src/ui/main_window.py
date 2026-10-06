from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget
)
from ui.top_bar.top_bar_view import TopBarView
from ui.board.board_view import BoardView
from ui.window_controller import WindowController

class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Nine Men's Morris")

        self.topBar = TopBarView()
        self.board = BoardView()

        layout = QVBoxLayout()
        layout.addWidget(self.topBar)
        layout.addWidget(self.board, stretch=1)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(700, 500)

        WindowController(self)
