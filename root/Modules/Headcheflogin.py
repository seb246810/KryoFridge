import sys
import hashlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QLineEdit, QDialog, QWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import uic, QtGui
import sqlite3
import random
from fridge import *


class Headcheflogin(QWidget):

    def __init__(self, colorblind_mode=False, parent=None):
        super(Headcheflogin, self).__init__()
        uic.loadUi("../UI/ChefLogin.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)  # hides user input password
        self.show()

        self.LoginButton.clicked.connect(self.loginFunction)
        self.RegisterButton.clicked.connect(self.registerWindow)
        self.BackButton.clicked.connect(self.back)

        # connect to database
        self.conn = sqlite3.connect('headchefuser.db')
        self.cursor = self.conn.cursor()

        self.fridge = None

        self.colorblind_mode = colorblind_mode
        if self.colorblind_mode:
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

    def gotofridge(self):
        from fridge import fridgeWindow
        self.fridge = fridgeWindow(role='HeadChef', colorblind_mode=self.colorblind_mode)
        self.hide()
        self.fridge.show()

    def registerWindow(self):
        from HeadchefRegistration import Headchefregister

        # checks number of users
        user_count_query = 'SELECT COUNT(*) FROM user'
        self.cursor.execute(user_count_query)
        user_count = self.cursor.fetchone()[0]

        # denies any head chef registers because there can only be one
        # speech mark it out if not needed

        if user_count > 0:
            QMessageBox.warning(self, "Access Denied",
                                "Oops there can only be one head chef.", QMessageBox.Ok)
        else:
            self.register = Headchefregister(colorblind_mode=self.colorblind_mode)
            self.register.show()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def loginFunction(self):
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(username) == 0 or len(password) == 0:  # error message if there's no input
            self.error.setText("Please input all fields.")
            return

        hashed_password = self.hash_password(password)

        query = 'SELECT * FROM user WHERE username=?'
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchone()

        if user and user[2] == hashed_password:
            self.error.setText("Login Successful")
            self.gotofridge()
        else:
            self.error.setText("Invalid username or password")

    def update_chef_password(self, username, new_password):

        update_query = 'UPDATE user SET password=? WHERE username=?'
        self.cursor.execute(update_query, (new_password, username))
        self.conn.commit()

    def update_chef_role(self, username):
        update_query = 'UPDATE user SET role=? WHERE username=?'
        self.cursor.execute(update_query, ('HeadChef', username))
        self.conn.commit()

    def back(self):
        # import entry2
        # self.window = entry2.entrypoint()
        self.close()
        # self.window.show()
