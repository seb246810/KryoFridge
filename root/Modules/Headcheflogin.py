import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QLineEdit, QDialog, QWidget
from PyQt5 import uic,QtGui
import sqlite3
from fridge import *




class Headcheflogin(QWidget):

    def __init__(self, parent = None):
        super(Headcheflogin, self).__init__()
        uic.loadUi("../UI/ChefLogin.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password) #hides user input password
        self.show()

        self.LoginButton.clicked.connect(self.loginFunction)
        self.RegisterButton.clicked.connect(self.registerWindow)
        self.BackButton.clicked.connect(self.back)

        # connect to database
        self.conn = sqlite3.connect('headchefuser.db')
        self.cursor = self.conn.cursor()

        # drop the 'users' table if it exists
        self.cursor.execute('DROP TABLE IF EXISTS headchefuser')

        # create table for users if it does not exist yet
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')

        self.fridge = None

    def gotofridge(self):
        if not self.fridge:
            self.fridge = fridgeWindow()
        self.hide()
        self.fridge.show()

    def registerWindow(self):
        from HeadchefRegistration import Headchefregister

        self.window = Headchefregister()
        self.window.show()

        # checks number of users
        user_count_query = 'SELECT COUNT(*) FROM users'
        self.cursor.execute(user_count_query)
        user_count = self.cursor.fetchone()[0]

        # denies any head chef registers because there can only be one
        # speech mark it out if not needed

        if user_count > 0:
            QMessageBox.warning(self, "Access Denied",
                                "Oops there can only be one head chef.", QMessageBox.Ok)
        else:
            self.register = Headchefregister()

    def loginFunction(self):
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(username)==0 or len(password)==0: # error message if there's no input
            self.error.setText("Please input all fields.")

        else:
            query = 'SELECT * FROM users WHERE username=? AND password=?'
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()

            if user:
                self.error.setText("Login Successful")

                new_password = password
                self.update_user_password(username, new_password)
                
                self.gotofridge()

     
                
            else:
                self.error.setText("Invalid username or password")

    def update_user_password(self, username, new_password):

        update_query = 'UPDATE users SET password=? WHERE username=?'
        self.cursor.execute(update_query, (new_password, username))
        self.conn.commit()
        
    def back(self):
        #import entry2
        #self.window = entry2.entrypoint()
        self.close()
        #self.window.show()
    




