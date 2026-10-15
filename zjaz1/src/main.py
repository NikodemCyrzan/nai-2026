import sys
from PyQt6.QtWidgets import (
    QApplication,
)

from controller.controller import GameController
from game import Game
from ui.main_window import MainWindow

if __name__ == "__main__":
    print("start")

    game = Game()

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())