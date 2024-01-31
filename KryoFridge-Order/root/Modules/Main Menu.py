from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QDialog, QWidget, \
    QDialogButtonBox, QVBoxLayout, QFormLayout, QCheckBox, QTableWidgetItem
from PyQt5 import uic, QtGui
from Roleselection import *
from Headcheflogin import *
from driverRegistration import *
from HeadchefRegistration import *

class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()

        uic.loadUi("../UI/MainMenu2.ui", self)




        self.Driver_Login_Window = driverLogin(self)
        self.Driver_Register_Window = driverRegister(self)
        self.HChef_Register_Window = Headchefregister(self)
        self.HChef_Login_Window = Headcheflogin(self)

        self.stackedWidget.addWidget(self.Driver_Register_Window)
        self.stackedWidget.addWidget(self.Driver_Login_Window)
        self.stackedWidget.addWidget(self.HChef_Register_Window)
        self.stackedWidget.addWidget(self.HChef_Login_Window)

        self.DriverRegBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.DriverLogBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.HChefRegBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.HChefLogBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

if __name__ == '__main__':
    app = QApplication([])
    window = MainMenu()
    window.show()
    app.exec_()