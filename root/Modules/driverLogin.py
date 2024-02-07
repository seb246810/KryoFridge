import sys
import hashlib
import os
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QLineEdit, QDialog, \
    QInputDialog
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer
import sqlite3
import math, random
from fridge import *


class driverLogin(QWidget):

    def __init__(self, parent=None):
        super(driverLogin, self).__init__()
        uic.loadUi("../UI/driverLogin.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)  # hides user input password
        self.show()

        self.LoginButton.clicked.connect(self.driverLoginFunction)
        self.RegisterButton.clicked.connect(self.driverRegisterWindow)
        self.BackBtn.clicked.connect(self.back)

        # connect to database
        self.conn = sqlite3.connect('deliveryusers.db')
        self.cursor = self.conn.cursor()

        self.fridge = None

    def gotofridge(self):
        from fridge import fridgeWindow
        if not self.fridge:
            self.fridge = fridgeWindow("DeliveryDriver")
            self.fridge.show()
            self.close()

    # generates random 4 digit number
    def getOTP(self):
        return ''.join(random.choice('0123456789') for _ in range(4))

    def welcomeDriver(self, username):
        welcome = QMessageBox(self)
        welcome.setWindowTitle("Access Granted.")
        welcome.setText(f"Welcome, {username}!")
        welcome.show()

        timer = QTimer(welcome)
        timer.timeout.connect(welcome.accept)
        timer.start(1500)

        timer.timeout.connect(self.gotofridge)

    def driverRegisterWindow(self):
        from driverRegistration import driverRegister
        self.register = driverRegister()

    def driverLoginFunction(self):
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(username) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")
        else:
            self.validateCredentials(username, password)

    def validateCredentials(self, username, password):
        query = 'SELECT password, salt, driverId FROM deliverydriver WHERE username=?'
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchone()

        if user:
            stored_password_hash, stored_salt, stored_driverId = user
            stored_salt = bytes.fromhex(stored_salt)
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), stored_salt, 100000)
            if password_hash.hex() == stored_password_hash:
                self.verifyDriverID(user, username)
            else:
                self.error.setText("Invalid username or password")
        else:
            self.error.setText("Invalid username or password")

    def verifyDriverID(self, user, username):
        dialog = DriverIDDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            self.error.setText("Driver ID verification cancelled")
            return
        try:
            entered_driverId = int(dialog.getDriverId())
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Driver ID must be a number.")
            return
        stored_driverId = int(user[2])  # Assuming the driver ID is the third item
        if entered_driverId == stored_driverId:
            self.displayOTP(username)
        else:
            QMessageBox.critical(self, "Access Denied", "Invalid DriverID")

    def displayOTP(self, username):
        otp = self.getOTP()
        QMessageBox.warning(self, "One Time Password!", otp, QMessageBox.Ok)

        otp_input, ok = QInputDialog.getText(self, "OTP Verification", "Enter the OTP:")
        if ok and otp_input == otp:
            self.welcomeDriver(username)
        else:
            QMessageBox.critical(self, "Access Denied", "Incorrect OTP. Back to main menu.")
            self.close()

    def update_user_password(self, username, new_password):

        update_query = 'UPDATE deliverydriver SET password=? WHERE username=?'
        self.cursor.execute(update_query, (new_password, username))
        self.conn.commit()

    def back(self):
        # import entry2
        # self.window = entry2.entrypoint()
        self.close()
        # self.window.show()

class DriverIDDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Driver ID Verification")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter your 4-digit Driver ID:", self)
        self.layout.addWidget(self.label)

        self.driverIdInput = QLineEdit(self)
        self.layout.addWidget(self.driverIdInput)

        self.verifyButton = QPushButton("Verify", self)
        self.verifyButton.clicked.connect(self.accept)
        self.layout.addWidget(self.verifyButton)

    def getDriverId(self):
        return self.driverIdInput.text()

