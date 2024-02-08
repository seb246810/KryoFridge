import sqlite3

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QWidget
from PyQt5 import uic,QtGui
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

    def registerFunction(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()
        confirm = self.confirmfield.text()
        headchefID = random.randint(1000, 9999)

        if len(user)==0 or len(password)==0 or len(confirm)==0:
            self.error.setText("Please fill in all inputs.")

        elif password != confirm:
            self.error.setText("Passwords do not match.")

        else:
            conn = sqlite3.connect('headchefuser.db')
            cur = conn.cursor()

            # Generate a unique headchefID
            headchefID = self.generate_unique_headchefID()

            headchef_info = [headchefID, user, password]
            cur.execute('INSERT INTO user(headchefID, username, password) VALUES (?,?,?)', headchef_info)

            conn.commit()
            conn.close()
            self.close()
            

    def back(self):
        self.close()