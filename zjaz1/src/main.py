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
from rounds.game_round_test import game_scenario_1
from ui.main_window import MainWindow

if __name__ == "__main__":
    print("start")

    game = Game()
    bus = game.bus

    white_controller = game.white_controller
    black_controller = game.black_controller

    bus.subscribe(GameEvent, lambda event: print(f"Event occurred: {type(event)}: {event.__dict__}"))

    game_scenario_1(white_controller, black_controller)

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
