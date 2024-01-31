import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox, QLineEdit, QDialog, QInputDialog
from PyQt5 import uic,QtGui
from PyQt5.QtCore import QTimer
import sqlite3
import math, random
from fridge import *




class driverLogin(QWidget):

    def __init__(self, parent=None):
        super(driverLogin, self).__init__()
        uic.loadUi("../UI/driverLogin.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password) #hides user input password
        self.show()

        self.LoginButton.clicked.connect(self.driverLoginFunction)
        self.RegisterButton.clicked.connect(self.driverRegisterWindow)
        self.BackButton.clicked.connect(self.back)

        # connect to database
        self.conn = sqlite3.connect('deliveryusers.db')
        self.cursor = self.conn.cursor()

        self.fridge = None

    def gotofridge(self):
        from fridge import fridgeWindow
        if not self.fridge:
            self.fridge = fridgeWindow()

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

        self.fridge = fridgeWindow()
        self.fridge.show()



    def driverRegisterWindow(self):
        from driverRegistration import driverRegister
        self.register = driverRegister()

    def driverLoginFunction(self):
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(username)==0 or len(password)==0: # error message if there's no input
            self.error.setText("Please input all fields.")

        else:
            query = 'SELECT * FROM deliverydriver WHERE username=? AND password=?'
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()

            if user:
                self.error.setText("Login Successful")

                new_password = password
                self.update_user_password(username, new_password)
                self.close()
                
                # display one time password
                otp = self.getOTP()
                QMessageBox.warning(self, "One Time Password!", otp, QMessageBox.Ok)

                # prompt for OTP verification
                otp_input, ok = QInputDialog.getText(self, "OTP Verification", "Enter one time password: ")

                if ok and otp_input == otp:
                    self.welcomeDriver(username)
                    self.fridge = fridgeWindow()
                    self.fridge.show()

                    
                else:
                    QMessageBox.critical(self, "Access Denied!", "Incorrect One Time Password. Back to main menu.")
                    self.close()
                
                     
                
            else:
                self.error.setText("Invalid username or password")

    def update_user_password(self, username, new_password):

        update_query = 'UPDATE deliverydriver SET password=? WHERE username=?'
        self.cursor.execute(update_query, (new_password, username))
        self.conn.commit()
        
    def back(self):
        #import entry2
        #self.window = entry2.entrypoint()
        self.close()
        #self.window.show()
    

if __name__ == '__main__':
    app = QApplication([])
    window = driverLogin()
    window.show()
    app.exec_()


