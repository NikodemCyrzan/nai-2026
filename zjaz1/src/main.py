import sys
from PyQt6.QtWidgets import (
    QApplication,
)

from controller.actions import GameStartAction, PlayerPlacePawnAction
from controller.game_controller import GameController
from event.bus import GameEvent
from game import Game
from logic.game_logic import GameStartedEvent, GameExceptionEvent
from model.board import BoardStateChangeEvent, Board
from model.player import PlayerTurnChangeEvent
from ui.main_window import MainWindow

if __name__ == "__main__":
    print("start")

    game = Game()
    bus = game.bus

    white_controller = game.white_controller
    black_controller = game.black_controller

    bus.subscribe(GameEvent, lambda event: print(f"Event occurred: {type(event)}: {event.__dict__}"))
    bus.subscribe(GameExceptionEvent, lambda event: print(f"Game exception occurred: {event.message} for player {event.player}"))
    bus.subscribe(GameStartedEvent, lambda event: print("Game started!"))
    bus.subscribe(PlayerTurnChangeEvent, lambda event: print(f"Player turn changed to: {event.player}"))
    bus.subscribe(BoardStateChangeEvent, lambda event: print(f"Board state changed: {event.board.get_all_nodes()}"))


    white_controller.perform(GameStartAction())
    black_controller.perform(PlayerPlacePawnAction(at_index=0))
    white_controller.perform(PlayerPlacePawnAction(at_index=0))
    white_controller.perform(PlayerPlacePawnAction(at_index=0))
    black_controller.perform(PlayerPlacePawnAction(at_index=0))
    white_controller.perform(PlayerPlacePawnAction(at_index=1))
    black_controller.perform(PlayerPlacePawnAction(at_index=1))




    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())