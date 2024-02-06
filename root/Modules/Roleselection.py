import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox, QDialog
from PyQt5 import uic,QtGui
from PyQt5 import QtWidgets
from HeadchefRegistration import *
from Headcheflogin import *
from driverLogin import *
import sqlite3




class entrypoint(QMainWindow):
    
    def __init__(self):
        super(entrypoint,self).__init__()
        uic.loadUi("../UI/entrypoint.ui",self)
        self.show()

        self.Headchef.clicked.connect(self.loginScreen)
        self.Delivery.clicked.connect(self.driverLoginWindow)
        self.staff.clicked.connect(self.staffAccess)

    def loginScreen(self):
        self.login = Headcheflogin()

    def staffAccess(self):
        from fridge import fridgeWindow
        self.window = fridgeWindow()
        #self.close()
        self.window.show()

    def driverLoginWindow(self):
        self.login = driverLogin()




       
        



    
          
            
            
        
 

    
