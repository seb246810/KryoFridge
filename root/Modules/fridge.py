from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QDialog, QWidget
from PyQt5 import uic, QtGui
from Roleselection import *
from Headcheflogin import *
from HeadchefRegistration import *


class fridgeWindow(QMainWindow):
    def __init__(self):
        super(fridgeWindow, self).__init__()
        uic.loadUi("../UI/fridge.ui", self)
        self.show()
        conn = sqlite3.connect('Fridge.db')
        cur = conn.cursor()

        conn.commit()
        conn.close()
        self.ExitButton.clicked.connect(self.back)
        self.AddButton.clicked.connect(self.AddItemsToFridge)
        self.RemoveButton.clicked.connect(self.RemoveItemsFromFridge)
        self.ExitButton.clicked.connect(self.Exit)

    def back(self):
        self.close()

    def LoadFridgeContents(self):
        pass

    def AddItemsToFridge(self):
        pass

    def RemoveItemsFromFridge(self):
        pass

    def WritePurchaseOrder(self):
        pass













       
            
        
        


        
