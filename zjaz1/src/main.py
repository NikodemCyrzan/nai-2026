import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from ui.main_window import MainWindow

if __name__ == "__main__":
    print("start")
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
