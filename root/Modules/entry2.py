import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox
from PyQt5 import uic,QtGui
from log import *




class entrypoint(QMainWindow):
    
    def __init__(self):
        super(entrypoint,self).__init__()
        uic.loadUi("../UI/entrypoint.ui",self)
        self.show()

        self.Headchef.clicked.connect(self.signup)
        self.Delivery.clicked.connect(self.signup)
        self.staff.clicked.connect(self.signup)

    def signup(self):
        
        self.window = MyGui()
        #self.close()
        self.window.show()




       
        



    
          
            
            
        
 

    
