from controller.actions import GameAction
from logic.game_logic import GameLogic
from model.player import Player


class GameController:
    def __init__(self,
        logic: GameLogic,
        player: Player,
    ):
        self._player: Player = player
        self._logic: GameLogic = logic

    def perform(self, action: GameAction,) -> None:
        self._logic.handle(action, self._player)
