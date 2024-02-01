from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QWidget
from PyQt5 import uic,QtGui
from fridge import *

class Headchefregister(QMainWindow):
    def __init__(self,parent = None):
        super(Headchefregister,self).__init__()
        uic.loadUi("../UI/HeadChefRegistration.ui",self)
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
            conn = sqlite3.connect('headchefuser.db')
            cur = conn.cursor()


            headchef_info = [user, password]
            cur.execute('INSERT INTO users(username, password) VALUES (?,?)', headchef_info)

            conn.commit()
            conn.close()
            self.close()
            

    def back(self):
        self.close()