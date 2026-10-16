from game import Game
from model.player import PlayerTurnChangeEvent, PlayerStateChangeEvent
from controller.actions import PlayerPlacePawnAction
from model.board import BoardStateChangeEvent
from model.player import Player, PlayerPhase

from PyQt6.QtCore import QTimer

class AiController:
    def __init__(self, game: Game):
        self._bus = game._bus
        self._controller = game._black_controller

        self._bus.subscribe(PlayerTurnChangeEvent, self._on_turn_change)
        self._bus.subscribe(BoardStateChangeEvent, self._on_board_change)
        self._bus.subscribe(PlayerStateChangeEvent, self._on_player_state_change)
        self._index = 0
        self._board = None
        self._phase = None

    def _on_turn_change(self, event: PlayerTurnChangeEvent) -> None:
        if event.player != Player.Black:
            return

        QTimer.singleShot(500, lambda: self._perform(self._controller, event))

    def _on_player_state_change(self, event: PlayerStateChangeEvent):
        if event.player != Player.Black:
            return
        
        self._phase = event.state.phase

    def _on_board_change(self, event: BoardStateChangeEvent):
        self._board = event.board

    def _perform(self, controller, event):
        weights = [0] * self._board.length

        match self._phase:
            case PlayerPhase.Placing:
                self._count_weights_placing(weights)
            case PlayerPhase.Moving:
                self._count_weights_moving(weights)
            case PlayerPhase.Flying:
                self._count_weights_flying(weights)


        # TODO: DO AI STUFF
        # controller.perform(PlayerPlacePawnAction(self._index))        

    def _count_weights_placing(self, weights):
        nodes = self._board.get_all_nodes()
        for i, node in enumerate(nodes):
            weight = 0
            for mill_row in self._board.get_mill_rows(i):
                weight += mill_row

    def _count_weights_moving(self, weights):
        pass

    def _count_weights_flaying(self, weights):
        pass