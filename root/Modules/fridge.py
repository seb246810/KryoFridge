from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QDialog, QWidget, \
    QDialogButtonBox, QVBoxLayout, QFormLayout, QCheckBox
from PyQt5 import uic, QtGui
from Roleselection import *
from Headcheflogin import *
from HeadchefRegistration import *


def user_role():
    return 'HeadChef'


class fridgeWindow(QMainWindow):
    def __init__(self):
        super(fridgeWindow, self).__init__()
        uic.loadUi("../UI/fridge.ui", self)
        self.show()
        conn = sqlite3.connect('Fridge.db')
        cur = conn.cursor()

        conn.commit()
        conn.close()

        self.user_role_access()

        self.ExitButton.clicked.connect(self.back)
        self.AddButton.clicked.connect(self.AddItemsToFridge)
        self.RemoveButton.clicked.connect(self.RemoveItemsFromFridge)
        self.ExitButton.clicked.connect(self.back)

    def back(self):
        self.close()

    def LoadFridgeContents(self):
        pass

    def AddItemsToFridge(self):
        dialog = AddItemsToFridge()
        if dialog.exec_() == QDialog.Accepted:
            item_data = dialog.get_data()
            print("Item added:", item_data)

    def RemoveItemsFromFridge(self):
        pass

    def WritePurchaseOrder(self):
        pass

    def user_role_access(self):
        current_role = user_role()
        self.AddButton.setEnabled(current_role in ['HeadChef', 'DeliveryDriver'])
        self.RemoveButton.setEnabled(current_role == 'HeadChef')


class AddItemsToFridge(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Item")
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.name_edit = QLineEdit(self)
        self.quantity_edit = QLineEdit(self)
        self.expiry_date_edit = QLineEdit(self)
        self.weight_edit = QLineEdit(self)
        self.ordered_checkbox = QCheckBox("Ordered", self)
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Quantity:", self.quantity_edit)
        form_layout.addRow("Expiry Date:", self.expiry_date_edit)
        form_layout.addRow("Weight (L):", self.weight_edit)
        form_layout.addRow(self.ordered_checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

        def get_data(self):
            return {
                "name": self.name_edit.text(),
                "quantity": int(self.quantity_edit.text()),
                "expiry_date": self.expiry_date_edit.text(),
                "weight": float(self.weight_edit.text()),
                "ordered": self.ordered_checkbox.isChecked()
            }

    if __name__ == '__main__':
        app = QApplication([])
        window = fridgeWindow()
        app.exec_()
