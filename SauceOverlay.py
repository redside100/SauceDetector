from threading import Thread
import lbpcascade_animeface.examples.detect as detector
from win32api import GetSystemMetrics, GetCursorPos, GetAsyncKeyState
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QFont, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
from PIL import Image, ImageGrab
import keyboard
import time
import reverse_search


class SauceOverlay(QMainWindow):
    def __init__(self):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                QtCore.QSize(width, height),
                QtWidgets.qApp.desktop().availableGeometry()
        ))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle('Sauce Overlay')
        self.dimensions = (0, 0, width, height)
        self.active_regions = []
        self.clicking = False
        self.hold_time = None
        self.holding = False

        thread = Thread(target=self.loop)
        thread.start()

    def paintEvent(self, event):

        if keyboard.is_pressed('shift+f') and not self.holding:
            self.holding = True
            self.hold_time = time.time()
        elif not keyboard.is_pressed('shift+f'):
            self.holding = False

        if self.holding and self.hold_time and time.time() - self.hold_time >= 1 and not self.clicking:
            x, y = GetCursorPos()
            for region in self.active_regions:
                if region[0] <= x <= region[0] + region[2] and region[1] <= y <= region[1] + region[3]:
                    self.setVisible(False)
                    face_img = ImageGrab.grab(self.dimensions)
                    self.setVisible(True)

                    Thread(target=reverse_search.crop_and_upload, args=[face_img, region, self]).start()

        qp = QPainter()
        qp.begin(self)
        qp.setFont(QFont('Decorative', 10))
        qp.setPen(QPen(Qt.green, 5, Qt.SolidLine))

        for region in self.active_regions:
            x, y = GetCursorPos()
            if region[0] <= x <= region[0] + region[2] and region[1] <= y <= region[1] + region[3]:
                qp.setPen(QPen(Qt.red, 5, Qt.SolidLine))
                qp.drawRect(region[0], region[1], region[2], region[3])
                qp.setPen(QPen(Qt.green, 5, Qt.SolidLine))
            else:
                qp.drawRect(region[0], region[1], region[2], region[3])

        qp.end()

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions

    def loop(self):
        while True:
            screen_frame = ImageGrab.grab(self.dimensions)
            self.active_regions = detector.detect(screen_frame)
            self.update()
