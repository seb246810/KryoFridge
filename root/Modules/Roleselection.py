import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QDialog
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from HeadchefRegistration import *
from driverLogin import *
from fridge import *
import sqlite3


class entrypoint(QMainWindow):

    def __init__(self):
        super(entrypoint, self).__init__()
        uic.loadUi("../UI/entrypoint.ui", self)
        self.show()

        self.Headchef.clicked.connect(self.loginScreen)
        self.Delivery.clicked.connect(self.driverLoginWindow)
        self.staff.clicked.connect(self.staffAccess)

        self.checkBoxColorblindMode.stateChanged.connect(self.ToggleColorblindMode)

    def ToggleColorblindMode(self, state):
        if state == 2:
            self.ApplyColorblindPalette()
        else:
            self.ApplyNormalPalette()

    def ApplyColorblindPalette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("blue"))
        palette.setColor(QPalette.WindowText, QColor("red"))
        self.setPalette(palette)

    def ApplyNormalPalette(self):
        self.setPalette(self.style().standardPalette())

    def loginScreen(self):
        colorblind_mode = self.checkBoxColorblindMode.isChecked()
        self.login = Headcheflogin(colorblind_mode=colorblind_mode)
        self.login.show()

    def staffAccess(self):
        colorblind_mode = self.checkBoxColorblindMode.isChecked()
        self.window = fridgeWindow(colorblind_mode=colorblind_mode)
        self.window.show()

    def driverLoginWindow(self):
        colorblind_mode = self.checkBoxColorblindMode.isChecked()
        self.login = driverLogin(colorblind_mode=colorblind_mode)
        self.login.show()