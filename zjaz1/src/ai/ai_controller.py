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

    def _score_rows(self, nodes, index, black_two, white_two):
        score = 0
        for mill_row in self._board.get_mill_rows(index):
            others = [nodes[j] for j in mill_row if j != index]
            whites = others.count(Player.White)
            blacks = others.count(Player.Black)

            if whites and blacks:
                continue

            if whites == 2:
                score += white_two
            elif blacks == 2:
                score += black_two
            else:
                score += whites + blacks

        return score

    def _count_weights_placing(self, weights):
        nodes = self._board.get_all_nodes()
        for i, node in enumerate(nodes):
            if node != Player.Empty:
                weights[i] = -1
                continue

            weights[i] = self._score_rows(nodes, i, black_two=2, white_two=3)

    def _count_weights_moving(self, weights):
        nodes = self._board.get_all_nodes()
        for i, node in enumerate(nodes):
            weights[i] = -1
            if node != Player.Empty:
                continue

            for neighbour in self._board.get_neighbours(i):
                if nodes[neighbour] != Player.Black:
                    continue

                nodes[neighbour] = Player.Empty
                score = self._score_rows(nodes, i, black_two=4, white_two=3)
                nodes[neighbour] = Player.Black

                weights[i] = max(weights[i], score)

    def _count_weights_flying(self, weights):
        nodes = self._board.get_all_nodes()
        black_pawns = [i for i, node in enumerate(nodes) if node == Player.Black]
        for i, node in enumerate(nodes):
            weights[i] = -1
            if node != Player.Empty:
                continue

            for pawn in black_pawns:
                nodes[pawn] = Player.Empty
                score = self._score_rows(nodes, i, black_two=5, white_two=4)
                nodes[pawn] = Player.Black

                weights[i] = max(weights[i], score)
