import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox, QDialog
from PyQt5 import uic,QtGui
from PyQt5 import QtWidgets
from HeadchefRegistration import *
from Headcheflogin import *
from driverLogin import *
from driverRegistration import *
from fridge import *
import sqlite3




class entrypoint(QMainWindow):
    
    def __init__(self):
        super(entrypoint,self).__init__()
        uic.loadUi("../UI/entrypoint.ui",self)
        self.show()

        self.StaffBtn.clicked.connect(lambda: self.GotoFridge('Staff'))


        self.Driver_Login_Window = driverLogin(self)
        self.HChef_Register_Window = Headchefregister(self)


        self.stackedWidget.addWidget(self.Driver_Login_Window)
        #self.stackedWidget.addWidget(self.Fridge_Window)
        self.stackedWidget.addWidget(self.HChef_Register_Window)


        self.DeliveryBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.HeadchefBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

    def GotoFridge(self, role):

        self.Fridge_Window = fridgeWindow(role = role)
        self.Fridge_Window.show()



    def loginScreen(self):
        self.login = Headcheflogin()

    def signup(self):
        
        self.window = Headchefregister()
        self.close()
        self.window.show()

    def driverLoginWindow(self):
        self.login = driverLogin()


if __name__ == '__main__':
    app = QApplication([])
    window = entrypoint()
    window.show()
    sys.exit(app.exec_())

       
        



    
          
            
            
        
 

    
