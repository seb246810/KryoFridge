import sys
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
        DeliveryID = self.DeliveryIDfield.toPlainText()

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

        # if item field is empty
        elif not item:
            self.error.setText("Enter a food item name")
            return
        elif not DeliveryID:
            self.error.setText("Enter a OrderID")
            return

        # if quantity field is empty.
        elif not qty:
            self.error.setText("Enter quantity")
            return

        elif not weight:
            self.error.setText("Enter weight")
            return

        self.error.clear()

        # Insert data into the fridge database
        try:
            query = "INSERT INTO Fridge (Name, Quantity, Expiry_Date, Weight) VALUES (?, ?, ?, ?)"
            query2 = "INSERT INTO DeliveryLog (Name, Quantity, DeliveryID) VALUES (?, ?, ?)"
            self.cursor.execute(query, (item, qty, expiryDate, weight))
            self.conn.commit()
            self.cursor2.execute((query2,item,qty,DeliveryID))
            self.conn2.commit()
            QMessageBox.information(self, "Success", "Item added to fridge database.")
            QMessageBox.information(self, "Success", "Delivery Has Been Logged Successfully.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def OrderReceived(self):
            # insert code to read database for what the headchef ordered
            pass

        # add functionality if driver input does not match with headchef ordered database
        
            


