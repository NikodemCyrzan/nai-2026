import sys
from PyQt6.QtWidgets import (
    QApplication,
)

from controller.actions import GameStartAction
from event.bus import GameEvent
from game import Game
from rounds.game_round_test import game_scenario_1, verify_scenario, game_scenario_2_blocking
from ui.main_window import MainWindow
from ai.ai_controller import AiController


if __name__ == "__main__":
    verify_scenario(game_scenario_1, expect_mills=True)
    verify_scenario(game_scenario_2_blocking, expect_mills=False)

    game = Game()
    bus = game.bus

    white_controller = game.white_controller
    black_controller = game.black_controller

    bus.subscribe(GameEvent, lambda event: print(f"Event occurred: {type(event)}: {event.__dict__}"))

    app = QApplication(sys.argv)
    main = MainWindow(game)
    main.show()
    ai = AiController(game)
    white_controller.perform(GameStartAction())
    sys.exit(app.exec())
