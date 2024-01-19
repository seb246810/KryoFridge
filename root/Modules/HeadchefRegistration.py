from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox
from PyQt5 import uic,QtGui


class Headchefregister(QMainWindow):
    def __init__(self):
        super(Headchefregister,self).__init__()
        uic.loadUi("../UI/HeadChefRegistration.ui",self)
        self.show()

        #self.Username.clicked.connect(self)
        #self.Password.clicked.connect(self)
        #self.Confirm.clicked.connect(self)
        #self.BackButton.clicked.connect(self)
        


        
