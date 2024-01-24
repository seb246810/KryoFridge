from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox, QDialog, QWidget
from PyQt5 import uic,QtGui
from Roleselection import *
#from Headcheflogin import *
#from HeadchefRegistration import *


class fridgeWindow(QMainWindow):
    def __init__(self):
        super(fridgeWindow,self).__init__()
        uic.loadUi("../UI/fridge.ui",self)
        self.show()

        self.ExitButton.clicked.connect(self.back)

        

    def back(self):
       
        
        self.close()
       
        
       
            
        
        


        
