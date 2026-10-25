import sys
from game import Game

from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import QApplication

def main():
    fmt = QSurfaceFormat()
    fmt.setSamples(4)
    fmt.setSwapInterval(1)
    QSurfaceFormat.setDefaultFormat(fmt)

    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
