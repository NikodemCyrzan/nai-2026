from easyAI import Negamax, TwoPlayerGame
from game import Game
from model.player import PlayerTurnChangeEvent, PlayerStateChangeEvent

from controller.actions import PlayerPlacePawnAction, PlayerMovePawnAction, PlayerRemovePawnAction
from model.board import BoardStateChangeEvent
from model.player import Player, PlayerPhase

from PyQt6.QtCore import QTimer


class _NineMensMorrisEasyAI(TwoPlayerGame):

    def __init__(self, board, phases, pawns_left_to_place):
        self.players = [Player.Black, Player.White]
        self.nodes = board.get_all_nodes()
        self.board = board
        self.phases = phases.copy()
        self.pawns_left_to_place = pawns_left_to_place.copy()
        self.nplayer = 1

    @property
    def current_player(self):
        return self.players[self.nplayer - 1]

    def switch_player(self):
        if self.phases[self.current_player] == PlayerPhase.Removing:
            return
        self.nplayer = 3 - self.nplayer

    def possible_moves(self):
        player = self.current_player
        phase = self.phases[player]

        if phase == PlayerPhase.Placing:
            return [("place", index) for index, node in enumerate(self.nodes)
                    if node == Player.Empty]

        if phase == PlayerPhase.Removing:
            opponent = self._opponent(player)
            return [
                ("remove", index)
                for index, node in enumerate(self.nodes)
                if node == opponent and self._can_remove(index, opponent)
            ]

        sources = [
            index for index, node in enumerate(self.nodes)
            if node == player
        ]
        destinations = [
            index for index, node in enumerate(self.nodes)
            if node == Player.Empty
        ]
        if phase == PlayerPhase.Moving:
            return [
                ("move", source, destination)
                for source in sources
                for destination in destinations
                if destination in self.board.get_neighbours(source)
            ]
        return [
            ("move", source, destination)
            for source in sources
            for destination in destinations
        ]

    def make_move(self, move):
        player = self.current_player
        kind = move[0]

        if kind == "place":
            index = move[1]
            self.nodes[index] = player
            self.pawns_left_to_place[player] -= 1
            if self.pawns_left_to_place[player] == 0:
                self.phases[player] = PlayerPhase.Moving
            changed_index = index
        elif kind == "move":
            source, destination = move[1:]
            self.nodes[source] = Player.Empty
            self.nodes[destination] = player
            changed_index = destination
        else:
            self.nodes[move[1]] = Player.Empty
            self._restore_phase(player)
            return

        if self._is_mill(changed_index, player):
            self.phases[player] = PlayerPhase.Removing

    def win(self):
        player = self.current_player
        opponent = self._opponent(player)
        if self.pawns_left_to_place[opponent] > 0:
            return False
        return (
            self.nodes.count(opponent) < 3
            or not self._has_moves(opponent)
        )

    def is_over(self):
        return self.win()

    def scoring(self):
        if self.win():
            return 100
        opponent = self._opponent(self.current_player)
        if self.pawns_left_to_place[opponent] == 0 and (
            self.nodes.count(self.current_player) < 3
            or not self._has_moves(self.current_player)
        ):
            return -100
        return self.nodes.count(self.current_player) - self.nodes.count(opponent)

    def _opponent(self, player):
        return Player.White if player == Player.Black else Player.Black

    def _is_mill(self, index, player):
        return any(
            all(self.nodes[node] == player for node in row)
            for row in self.board.get_mill_rows(index)
        )

    def _can_remove(self, index, opponent):
        if self._is_mill(index, opponent):
            return self._all_pawns_in_mills(opponent)
        return True

    def _all_pawns_in_mills(self, player):
        return all(
            self._is_mill(index, player)
            for index, node in enumerate(self.nodes)
            if node == player
        )

    def _has_moves(self, player):
        if self.phases[player] == PlayerPhase.Flying:
            return any(node == Player.Empty for node in self.nodes)
        return any(
            self.nodes[neighbour] == Player.Empty
            for source, node in enumerate(self.nodes)
            if node == player
            for neighbour in self.board.get_neighbours(source)
        )

    def _restore_phase(self, player):
        if self.pawns_left_to_place[player] > 0:
            self.phases[player] = PlayerPhase.Placing
        elif self.nodes.count(player) <= 3:
            self.phases[player] = PlayerPhase.Flying
        else:
            self.phases[player] = PlayerPhase.Moving


class AiController:
    def __init__(self, game: Game):
        self._bus = game._bus
        self._controller = game._black_controller

        self._bus.subscribe(PlayerTurnChangeEvent, self._on_turn_change)
        self._bus.subscribe(BoardStateChangeEvent, self._on_board_change)
        self._bus.subscribe(PlayerStateChangeEvent, self._on_player_state_change)
        self._board = game._state.board.value
        self._ai = Negamax(3)

    def _on_turn_change(self, event: PlayerTurnChangeEvent) -> None:
        if event.player != Player.Black:
            return

        QTimer.singleShot(2000, lambda: self._perform(self._controller))

    def _on_player_state_change(self, event: PlayerStateChangeEvent):
        if event.player != Player.Black:
            return

        # After a mill the turn doesn't change, so removing has to be triggered here
        if event.state.phase == PlayerPhase.Removing:
            QTimer.singleShot(2000, lambda: self._perform(self._controller))

    def _on_board_change(self, event: BoardStateChangeEvent):
        self._board = event.board

    def _perform(self, controller):
        state = controller._logic._state
        search = _NineMensMorrisEasyAI(
            self._board,
            {
                Player.Black: state.black_player_state.value.phase,
                Player.White: state.white_player_state.value.phase,
            },
            {
                Player.Black: state.black_player_state.value.pawns_left_to_place,
                Player.White: state.white_player_state.value.pawns_left_to_place,
            },
        )
        move = self._ai(search)

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
