from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QWidget
from PyQt5 import uic,QtGui
from fridge import *


class Headchefregister(QWidget):
    def __init__(self,parent = None):
        super(Headchefregister,self).__init__()
        uic.loadUi("../UI/HeadChefRegistration.ui",self)
        self.show()

        #self.Username.clicked.connect(self)
        #self.Password.clicked.connect(self)
        #self.Confirm.clicked.connect(self)
        #self.BackButton.clicked.connect(self)
        


        
