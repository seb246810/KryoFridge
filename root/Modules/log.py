import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox
from PyQt5 import uic,QtGui



class MyGui(QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("../UI/login.ui",self)
        self.show()

        self.pushButton.clicked.connect(self.login)
        self.return_2.clicked.connect(self.home)

    def login(self):
        if self.lineEdit.text()=="seb" and self.lineEdit_2.text()=="password":
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
        else:
            message = QMessageBox()
            message.setText("Invalid Login")
            message.exec_()

    def home(self):
        #import entry2
        #self.window = entry2.entrypoint()
        self.close()
        #self.window.show()
    




