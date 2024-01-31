import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox, QDialog
from PyQt5 import uic,QtGui
from PyQt5 import QtWidgets
from HeadchefRegistration import Headchefregister
from Headcheflogin import Headcheflogin
from driverLogin import driverLogin
import sqlite3




class entrypoint(QMainWindow):
    
    def __init__(self):
        super(entrypoint,self).__init__()
        uic.loadUi("../UI/entrypoint.ui",self)
        self.show()

        self.Headchef.clicked.connect(self.loginScreen)
        self.Delivery.clicked.connect(self.driverLoginWindow)
        self.staff.clicked.connect(self.signup)

    def loginScreen(self):
        self.login =Headcheflogin()

    def signup(self):
        
        self.window = Headchefregister()
        #self.close()
        self.window.show()

    def driverLoginWindow(self):
        self.login = driverLogin()




       
        



    
          
            
            
        
 

    
