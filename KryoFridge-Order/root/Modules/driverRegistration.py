from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox, QDialog
from PyQt5 import uic,QtGui
from Roleselection import *
from driverLogin import *
from fridge import *


class driverRegister(QWidget):
    def __init__(self, parent=None):
        super(driverRegister,self).__init__()
        uic.loadUi("../UI/driverRegister.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show()

        self.BackButton.clicked.connect(self.back)
        self.registerbutton.clicked.connect(self.registerFunction)

    def registerFunction(self):
        user = self.usernamefield.text()
        password = self.passwordfield.text()
        confirm = self.confirmfield.text()

        if len(user)==0 or len(password)==0 or len(confirm)==0:
            self.error.setText("Please fill in all inputs.")

        elif password != confirm:
            self.error.setText("Passwords do not match.")

        else:
            conn = sqlite3.connect('deliveryusers.db')
            cur = conn.cursor()


            driver_info = [user, password]
            cur.execute('INSERT INTO deliverydriver(username, password) VALUES (?,?)', driver_info)

            conn.commit()
            conn.close()
            self.close()
            

    def back(self):
        self.close()

    #def home(self):
        #from Roleselection import entrypoint
        #self.back = entrypoint()
        #self.close()
        
            
        
        


        
