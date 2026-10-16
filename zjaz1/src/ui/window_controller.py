from game import Game
from ui.top_bar.top_bar_controller import TopBarController
from ui.board.board_controller import BoardController

class WindowController:
    def __init__(self, window, game: Game):
        self._top_bar_controller = TopBarController(window.topBar, game.bus)
        self._board_controller = BoardController(window.board, game.bus, game.white_controller)
