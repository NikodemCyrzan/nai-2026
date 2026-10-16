from constants import PLAYER_INITIAL_PAWNS_COUNT
from event.bus import GameEventBus
from logic.game_logic import GameEndedEvent, GameExceptionEvent
from model.board import BoardStateChangeEvent
from model.player import Player, PlayerPhase, PlayerStateChangeEvent, PlayerTurnChangeEvent
from ui.top_bar.top_bar_view import TopBarView

PHASE_MESSAGES: dict[PlayerPhase, str] = {
    PlayerPhase.Placing: "Twój ruch: postaw pionek",
    PlayerPhase.Moving: "Twój ruch: przesuń pionek",
    PlayerPhase.Flying: "Twój ruch: przeskocz pionkiem",
    PlayerPhase.Removing: "Młynek! Usuń pionek przeciwnika",
}


class TopBarController:
    def __init__(self, view: TopBarView, bus: GameEventBus):
        self._view = view

        self._turn: Player = Player.Empty
        self._phase: PlayerPhase = PlayerPhase.Placing
        self._to_place: dict[Player, int] = {
            Player.White: PLAYER_INITIAL_PAWNS_COUNT,
            Player.Black: PLAYER_INITIAL_PAWNS_COUNT,
        }
        self._on_board: dict[Player, int] = {Player.White: 0, Player.Black: 0}
        self._error: str | None = None
        self._winner: Player | None = None

        bus.subscribe(BoardStateChangeEvent, self._on_board_change)
        bus.subscribe(PlayerTurnChangeEvent, self._on_turn_change)
        bus.subscribe(PlayerStateChangeEvent, self._on_player_state_change)
        bus.subscribe(GameExceptionEvent, self._on_exception)
        bus.subscribe(GameEndedEvent, self._on_game_ended)

        self._render()

    def _on_board_change(self, event: BoardStateChangeEvent) -> None:
        nodes = event.board.get_all_nodes()
        self._on_board = {player: nodes.count(player) for player in self._on_board}
        self._error = None
        self._render()

    def _on_turn_change(self, event: PlayerTurnChangeEvent) -> None:
        self._turn = event.player
        self._error = None
        self._render()

    def _on_player_state_change(self, event: PlayerStateChangeEvent) -> None:
            self._to_place[event.player] = event.state.pawns_left_to_place
            if event.player == Player.White:
                self._phase = event.state.phase
            self._error = None
            self._render()

    def _on_exception(self, event: GameExceptionEvent) -> None:
        if event.player != Player.White:
            return
        self._error = event.message
        self._render()

    def _on_game_ended(self, event: GameEndedEvent) -> None:
        self._winner = event.winner
        self._render()

    def _render(self) -> None:
        self._view.set_state(
            self._pawns_count(Player.White),
            self._pawns_count(Player.Black),
            self._turn == Player.White,
            self._message(),
        )

    def _pawns_count(self, player: Player) -> int:
        return self._to_place[player] + self._on_board[player]

    def _message(self) -> str:
        if self._winner is not None:
            return "Wygrałeś!" if self._winner == Player.White else "Przegrałeś"

        if self._error is not None:
            return self._error

        if self._turn == Player.White:
            return PHASE_MESSAGES[self._phase]

        if self._turn == Player.Black:
            return "Ruch przeciwnika"

        return ""
