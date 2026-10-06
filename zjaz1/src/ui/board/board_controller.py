from ui.board.board_view import BoardView
from state.player import Player

# TODO: Implement controller 
class BoardController:
    def __init__(self, boardView: BoardView):
        boardView.set_nodes([Player.Node] * 24)
