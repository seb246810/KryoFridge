from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QDialog, QWidget, \
    QDialogButtonBox, QVBoxLayout, QFormLayout, QCheckBox, QTableWidgetItem
from PyQt5 import uic, QtGui
from Roleselection import *
from Headcheflogin import *
from driverRegistration import *
from HeadchefRegistration import *
from fridge import *

class UserMenu(QMainWindow):
    def __init__(self, username=None, role=None):
        super(UserMenu, self).__init__()

        uic.loadUi("../UI/UserMenu.ui", self)

        if role:
            self.RoleLabel.setText(role)
8
       # self.NotificationBtn.clicked()
      #  self.PurchaseOrderBtn.clicked()

if __name__ == '__main__':
    app = QApplication([])
    window = UserMenu()
    window.show()
    app.exec_()