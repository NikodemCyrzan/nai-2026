from controller.actions import PlayerPlacePawnAction, PlayerMovePawnAction, PlayerRemovePawnAction
from controller.game_controller import GameController
from event.bus import GameEventBus
from logic.game_logic import GameEndedEvent
from model.board import BoardStateChangeEvent
from model.player import Player, PlayerPhase, PlayerStateChangeEvent, PlayerTurnChangeEvent
from ui.board.board_view import BoardView


class BoardController:
    def __init__(self, view: BoardView, bus: GameEventBus, controller: GameController):
        self._view = view
        self._controller = controller

        self._turn: Player = Player.Empty
        self._phase: PlayerPhase = PlayerPhase.Placing
        self._nodes: list[Player] = [Player.Empty] * 24
        self._selected: int | None = None
        self._ended: bool = False

        view.set_nodes(self._nodes)
        view.point_clicked.connect(self._on_click)

        bus.subscribe(BoardStateChangeEvent, self._on_board_change)
        bus.subscribe(PlayerTurnChangeEvent, self._on_turn_change)
        bus.subscribe(PlayerStateChangeEvent, self._on_player_state_change)
        bus.subscribe(GameEndedEvent, self._on_game_ended)

    def _on_board_change(self, event: BoardStateChangeEvent) -> None:
        self._nodes = event.board.get_all_nodes()
        self._view.set_nodes(self._nodes)

    def _on_turn_change(self, event: PlayerTurnChangeEvent) -> None:
        self._turn = event.player
        self._select(None)

    def _on_player_state_change(self, event: PlayerStateChangeEvent) -> None:
        if event.player == Player.White:
            self._phase = event.state.phase

    def _on_game_ended(self, event: GameEndedEvent) -> None:
        self._ended = True
        self._select(None)

    def _on_click(self, index: int) -> None:
        if self._ended or self._turn != Player.White:
            return

        if self._phase == PlayerPhase.Placing:
            self._controller.perform(PlayerPlacePawnAction(at_index=index))

        elif self._phase == PlayerPhase.Removing:
            self._controller.perform(PlayerRemovePawnAction(at_index=index))

        elif self._nodes[index] == Player.White:
            self._select(index)

        elif self._selected is not None:
            from_index = self._selected
            self._select(None)
            self._controller.perform(PlayerMovePawnAction(from_index=from_index, to_index=index))

    def _select(self, index: int | None) -> None:
        self._selected = index
        self._view.set_selected(index)
