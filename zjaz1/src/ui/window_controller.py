from ui.top_bar.top_bar_controller import TopBarController
from ui.board.board_controller import BoardController

class WindowController:
    def __init__(self, window):
        self._top_bar_controller = TopBarController(window.topBar)
        self._board_controller = BoardController(window.board)
