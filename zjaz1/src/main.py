import sys
from PyQt6.QtWidgets import (
    QApplication,
)

from controller.actions import GameStartAction, PlayerPlacePawnAction, PlayerMovePawnAction, PlayerRemovePawnAction
from controller.game_controller import GameController
from event.bus import GameEvent
from game import Game
from logic.game_logic import GameStartedEvent, GameExceptionEvent
from model.board import BoardStateChangeEvent, Board
from model.player import PlayerTurnChangeEvent
from rounds.game_round_test import game_scenario_1, verify_scenario, game_scenario_2_blocking
from ui.main_window import MainWindow


if __name__ == "__main__":
    print("start")

    verify_scenario(game_scenario_1, expect_mills=True)
    verify_scenario(game_scenario_2_blocking, expect_mills=False)

    game = Game()
    bus = game.bus

    white_controller = game.white_controller
    black_controller = game.black_controller

    bus.subscribe(GameEvent, lambda event: print(f"Event occurred: {type(event)}: {event.__dict__}"))

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
