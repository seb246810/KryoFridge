from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QDialog, QWidget, \
    QDialogButtonBox, QVBoxLayout, QFormLayout, QCheckBox, QTableWidgetItem, QDateEdit
from PyQt5 import uic, QtGui
from Roleselection import *
from Headcheflogin import *
from HeadchefRegistration import *
import sqlite3


def user_role():
    return 'HeadChef'


class fridgeWindow(QMainWindow):
    def __init__(self):
        super(fridgeWindow, self).__init__()
        uic.loadUi("../UI/fridge.ui", self)

        self.database()
        self.user_role_access()

        self.ExitButton.clicked.connect(self.back)
        self.AddButton.clicked.connect(self.AddItemsToFridge)
        self.RemoveButton.clicked.connect(self.RemoveItemsFromFridge)
        self.OrderButton.clicked.connect(self.MakePurchaseOrder)
        self.HealthReportButton.clicked.connect(self.HealthReport)

    def database(self):
        self.conn = sqlite3.connect('fridge.db')
        self.cursor = self.conn.cursor()
        self.LoadFridgeContents()

    def LoadFridgeContents(self):
        self.cursor.execute("SELECT Name, Quantity, Expiry_Date, Weight, Ordered FROM Fridge")
        rows = self.cursor.fetchall()
        self.fridgeStorage.setRowCount(len(rows))
        for row_num, row_data in enumerate(rows):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.fridgeStorage.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def AddItemsToFridge(self):
        dialog = AddItemsDialog()
        if dialog.exec_() == QDialog.Accepted:
            item_data = dialog.get_data()
            self.Db_Insertion(item_data)
            self.LoadFridgeContents()

    def Db_Insertion(self, item_data):
        try:
            self.cursor.execute('''INSERT INTO Fridge (Name, Quantity, Expiry_Date, Weight, Ordered) 
            VALUES (?, ?, ?, ?, ?)''',
                                (item_data['name'],
                                 item_data['quantity'],
                                 item_data['expiry_date'],
                                 item_data['weight'],
                                 item_data['ordered']))
            self.conn.commit()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        finally:
            self.LoadFridgeContents()

    def RemoveItemsFromFridge(self):
        dialog = RemoveItemDialog()
        if dialog.exec_() == QDialog.Accepted:
            item_data = dialog.get_data()
            self.Db_Deletion(item_data)
            self.LoadFridgeContents()
    def Db_Deletion(self, item_data):
        try:
            self.cursor.execute("SELECT Quantity FROM Fridge WHERE Name=?", (item_data['name'],))
            result = self.cursor.fetchone()
            if result:
                current_quantity = result[0]
                new_quantity = current_quantity - item_data['quantity']
                if new_quantity > 0:
                    self.cursor.execute("UPDATE Fridge SET Quantity=? WHERE Name=?",
                                        (new_quantity, item_data['name']))
                else:
                    self.cursor.execute("DELETE FROM Fridge WHERE Name=?", (item_data['name'],))
                self.conn.commit()
            else:
                print("Item not found")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        finally:
            self.LoadFridgeContents()

    def MakePurchaseOrder(self):
        if user_role() != 'HeadChef':
            QMessageBox.warning(self, "Access Denied", "You do not have the access to purchase order")
            return
        purchase_order = "Purchase Order\n\n"
        self.cursor.execute("SELECT Name, Quantity FROM Fridge WHERE Ordered=0")
        items = self.cursor.fetchall()

        if not items:
            QMessageBox.information(self, "No Order", "There are no items to order.")
            return
        for item in items:
            name, quantity = item
            purchase_order += f"Item: {name}, Quantity: {quantity}\n"
        QMessageBox.information(self, "Purchase Order", purchase_order)

        self.cursor.execute("UPDATE Fridge SET Ordered=1 WHERE Ordered=0")
        self.conn.commit()
        self.LoadFridgeContents()

    def HealthReport(self):#
        if user_role() != 'HeadChef':
            QMessageBox.warning(self, "Access Denied", "You do not have the access to View the Health Report")
            return

        health_status = "Health Report\n\n"
        self.cursor.execute("SELECT Name,Expiry_Date FROM Fridge ORDER BY Expiry_Date ASC")
        items = self.cursor.fetchall()

        if not items:
            QMessageBox.information(self, "No Items", "There are currently no items in the fridge.")
            return
        for item in items:
            name, expiry_date = item
            health_status += f"Item: {name}, Expiry_Date: {expiry_date}\n"

        QMessageBox.information(self, "Health Report", health_status)


    def user_role_access(self):
        current_role = user_role()
        self.AddButton.setEnabled(current_role in ['HeadChef', 'DeliveryDriver'])
        self.RemoveButton.setEnabled(current_role == 'HeadChef')
        self.OrderButton.setEnabled(current_role == 'HeadChef')
        self.HealthReportButton.setEnabled(current_role == 'HeadChef')

    def back(self):
        self.conn.close()
        self.close()


class AddItemsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Item")
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.name_edit = QLineEdit(self)
        self.quantity_edit = QLineEdit(self)
        self.expiry_date_edit = QDateEdit(self)
        self.expiry_date_edit.setCalendarPopup(True)
        self.expiry_date_edit.setDate(QDate.currentDate())
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
            "expiry_date": self.expiry_date_edit.date().toString("yyyy-MM-dd"),
            "weight": float(self.weight_edit.text()),
            "ordered": int(self.ordered_checkbox.isChecked())
        }

class RemoveItemDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remove Item")

        layout = QVBoxLayout()
        from_layout = QFormLayout()
        self.name_edit = QLineEdit(self)
        self.quantity_edit = QLineEdit(self)

        from_layout.addRow("Name", self.name_edit)
        from_layout.addRow("Quantity", self.quantity_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(from_layout)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "quantity": int(self.quantity_edit.text())
        }

if __name__ == '__main__':
    app = QApplication([])
    window = fridgeWindow()
    window.show()
    app.exec_()