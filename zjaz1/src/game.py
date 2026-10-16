from constants import PLAYER_INITIAL_PAWNS_COUNT
from controller.game_controller import GameController
from event.bus import GameEventBus
from logic.game_logic import GameLogic
from model.board import Board
from model.player import Player
from state.game_state import GameState, GameStateInitializer


class Game:
    def __init__(self):
        initializer = GameStateInitializer(
            player_white_initial_pawns=PLAYER_INITIAL_PAWNS_COUNT,
            player_black_initial_pawns=PLAYER_INITIAL_PAWNS_COUNT,
        )

        self._board = Board()
        self._bus = GameEventBus()
        self._state = GameState(bus=self._bus, board=self._board, initializer=initializer)
        self._logic = GameLogic(self._state, self._bus)
        self._white_controller = GameController(self._logic, Player.White)
        self._black_controller = GameController(self._logic, Player.Black)

    @property
    def white_controller(self) -> GameController:
        return self._white_controller

    @property
    def black_controller(self) -> GameController:
        return self._black_controller

    @property
    def bus(self) -> GameEventBus:
        return self._bus
