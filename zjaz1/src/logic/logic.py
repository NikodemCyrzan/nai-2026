from controller.action.actions import GameAction
from models.player import Player
from state.state import GameState


class GameLogic:
    def __init__(self, state: GameState):
        pass

    def handle(self, action: GameAction, player: Player) -> None:
        pass