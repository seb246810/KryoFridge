import sys
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QMessageBox, QLineEdit, QDialog, QWidget
from PyQt5 import uic,QtGui
import sqlite3
from fridge import *
import re

class driverAddWindow(QWidget):
    def __init__(self):
        super(driverAddWindow, self).__init__()
        uic.loadUi("../UI/driverAdd.ui", self)
        self.show()

        self.conn = sqlite3.connect('fridge.db')
        self.cursor = self.conn.cursor()

        self.conn2 = sqlite3.connect('DeliveryLog.db')
        self.cursor2 = self.conn2.cursor()

        self.conn3 = sqlite3.connect('PurchaseOrder.db')
        self.cursor3 = self.conn3.cursor()



        self.submitButton.clicked.connect(self.addingItems)
        # self.checkBoxColorblindMode.stateChanged.connect(self.ToggleColorblindMode)

    def ToggleColorblindMode(self, state):
        if state == 2:
            self.ApplyColorblindPalette()
        else:
            self.ApplyNormalPalette()


    def ApplyColorblindPalette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("blue"))
        palette.setColor(QPalette.WindowText, QColor("red"))
        self.setPalette(palette)

    def ApplyNormalPalette(self):
        self.setPalette(self.style().standardPalette())

    
    def addingItems(self):
        item = self.itemnamefield.toPlainText()
        qty = self.quantityfield.toPlainText()
        weight = self.weightfield.toPlainText()
        expiryDate = self.expiryDate.date().toString("yyyy-MM-dd")
        deliveryid = self.deliveryfield.toPlainText()

        # item name validation (no numbers)
        if re.search(r'\d', item):
            self.error.setText("Item can't contain numbers")
            return

        # quantity validation (only numbers)
        elif qty and not qty.isdigit():
            self.error.setText("Quantity must be a valid number")
            return

        # weight validation (only numbers)
        elif weight and not weight.isdigit():
            self.error.setText("Weight must be a valid number")
            return

        # if all fields are empty
        elif not item and not qty and not weight:
            self.error.setText("Please input all fields")
            return

        elif deliveryid and not deliveryid.isdigit():
            self.error.setText("Order ID must be a valid number")
            return

        # if item field is empty
        elif not item:
            self.error.setText("Enter a food item name")
            return

        # if delivery id is empty
        elif not deliveryid:
            self.error.setText("Enter a OrderID")
            return

        # if quantity field is empty.
        elif not qty:
            self.error.setText("Enter quantity")
            return

        elif not weight:
            self.error.setText("Enter weight")
            return

        self.cursor3.execute("SELECT 1 FROM PurchaseOrder WHERE OrderID = ?", (deliveryid,))
        if not self.cursor3.fetchone():
            QMessageBox.critical(self, "Error", "Order ID inputted does not exist in the Purchase Order database.")
            return



        self.error.clear()


        try:
            query = "INSERT INTO Fridge (Name, Quantity, Expiry_Date, Weight) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (item, qty, expiryDate, weight))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Item added to fridge database.")
        except sqlite3.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
        try:
            query2 = "INSERT INTO DeliveryLog (Name, Quantity, DeliveryID) VALUES (?, ?, ?)"
            self.cursor2.execute(query2, (item, qty, deliveryid))
            self.conn2.commit()
            self.OrderReceived(deliveryid)
            QMessageBox.information(self, "Success", "Delivery Has Been Logged Successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"DeliveryLog database error: {str(e)}")


    def OrderReceived(self, deliveryID):
            self.cursor3.execute("SELECT Name, Quantity FROM PurchaseOrder WHERE OrderID = ?", (deliveryID,))
            Order = self.cursor3.fetchall()

            Ordered = {name: qty for name, qty in Order}

            self.cursor2.execute("SELECT Name, Quantity FROM DeliveryLog WHERE DeliveryID = ?", (deliveryID,))
            Deliveries = self.cursor2.fetchall()

            Delivered = {name: qty for name, qty in Deliveries}


            Inconsistencies = []
            for name, ordered_qty in Ordered.items():
                delivered_qty = Delivered.get(name, 0)
                if ordered_qty != delivered_qty:
                    Inconsistencies.append(f"Item: {name}, Ordered: {ordered_qty}, Delivered: {delivered_qty}")

            if Inconsistencies:
                InconsistenciesMessage = "\n".join(Inconsistencies)
                QMessageBox.warning(self, "Order Discrepancies",
                                    "There are discrepancies in the order:\n" + InconsistenciesMessage)
            else:
                QMessageBox.information(self, "Order Verification", "All items match the order.")




