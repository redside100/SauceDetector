from PyQt5.QtWidgets import QApplication
import sys
from SauceOverlay import SauceOverlay


def start_overlay():
    app = QApplication(sys.argv)
    overlay_window = SauceOverlay()
    overlay_window.show()
    app.exec_()


if __name__ == '__main__':
    start_overlay()
