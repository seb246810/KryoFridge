import random
import sqlite3
import hashlib
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox, QDialog
from PyQt5 import uic,QtGui
from Roleselection import *
from driverLogin import *


class driverRegister(QWidget):
    registration_success = pyqtSignal()
    def __init__(self, parent=None):
        super(driverRegister,self).__init__(parent)
        uic.loadUi("../UI/driverRegister.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show()

        self.database()

        self.BackButton.clicked.connect(self.back)
        self.registerbutton.clicked.connect(self.registerFunction)

    def database(self):
        self.conn = sqlite3.connect('deliveryusers.db')
        self.cursor = self.conn.cursor()

    def registerFunction(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()
        confirm = self.confirmfield.text()

        if len(user)==0 or len(password)==0 or len(confirm)==0:
            QMessageBox.warning("Please fill in all inputs.")

        elif password != confirm:
            QMessageBox.warning("Passwords do not match.")
        else:
            self.registerDriver(user,password)

    def registerDriver(self,user,password):
        driverId = self.generateId()
        salt = os.urandom(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        try:
            self.cursor.execute('INSERT INTO deliverydriver(username, password, salt, driverId) VALUES (?, ?, ?, ?)',
                                (user, password_hash.hex(), salt.hex(), driverId))
            self.conn.commit()
            QMessageBox.information(self,"Success", f"Registration Successful. Your DriverID is {driverId}.")
            self.registration_success.emit()
            self.gotoLogin()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", f"Username {user} is already taken, please choose another.")
        except sqlite3.Error as e:
            QMessageBox.warning(self,"Error", f"An error occurred: {e.args[0]}")
            return
        finally:
            self.conn.close()

    def generateId(self):
        return random.randint(1000,9999)

    def gotoLogin(self):
        from driverLogin import driverLogin
        self.close()
        login_window = driverLogin()
        login_window.show()

    def back(self):
        self.close()