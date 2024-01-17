import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox
from PyQt5 import uic,QtGui



class MyGui(QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("../UI/ChefLogin.ui",self)
        self.show()

        self.LoginButton.clicked.connect(self.login)
        self.BackButton.clicked.connect(self.home)

    def login(self):
        if self.UsernameLineEdit.text()=="seb" and self.PasswordLineEdit.text()=="password":

            username = self.UsernameLineEdit.text()
            message = QMessageBox()
            message.setText("Welcome " + username)
            message.exec_()
            
        else:
            message = QMessageBox()
            message.setText("Invalid Login")
            message.exec_()

    def home(self):
        #import entry2
        #self.window = entry2.entrypoint()
        self.close()
        #self.window.show()
    




