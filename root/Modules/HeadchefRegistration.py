import re
import sqlite3
import hashlib
import random
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QWidget
from PyQt5.QtGui import QColor
from PyQt5 import uic, QtWidgets
from fridge import *
from Headcheflogin import *

class Headchefregister(QMainWindow):
    def __init__(self,parent = None):
        super(Headchefregister,self).__init__()
        uic.loadUi("../UI/HeadChefRegistration.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show()

        self.BackButton.clicked.connect(self.back)
        self.registerbutton.clicked.connect(self.registerFunction)

        # self.checkBoxColorblindMode.stateChanged.connect(self.ToggleColorblindMode)

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

    def generate_unique_headchefID(self):
        conn = sqlite3.connect('headchefuser.db')
        cur = conn.cursor()
        
        while True:
            headchefID = random.randint(1000, 9999)
            
            # Check if the generated headchefID already exists in the database
            cur.execute('SELECT headchefID FROM user WHERE headchefID=?', (headchefID,))
            existing_id = cur.fetchone()
            
            if not existing_id:
                conn.close()
                return headchefID

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self, password):
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        if not re.search(r'\d', password):
            return "Password must include at least one number."
        return None

    def registerFunction(self):
        user, password, confirm = self.user_input()
        if self.validate_input(user, password, confirm):
            self.registration(user, password)

    def user_input(self):
        return (self.usernamefield.text(),
                self.passwordfield.text(),
                self.confirmfield.text())

    def validate_input(self, user, password, confirm):
        if not user or not password or not confirm:
            QMessageBox.warning(self, "Input Error", "Please fill in all inputs.")
            return False

        if self.validate_password(password):
            QMessageBox.warning(self, "Input Error", self.validate_password(password))
            return False

        if password != confirm:
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return False

        return True

    def registration(self, user, password):
        try:
            conn = sqlite3.connect('headchefuser.db')
            cur = conn.cursor()
            headchefID = self.generate_unique_headchefID()
            hashed_password = self.hash_password(password)
            cur.execute('INSERT INTO user (headchefID, username, password) VALUES (?, ?, ?)',
                        (headchefID, user, hashed_password))
            conn.commit()
            QMessageBox.information(self, "Success", "Head Chef registered successfully.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def back(self):
        self.close()