import uuid

from HeadchefRegistration import *
from fridge import *
import sqlite3

class PurchaseOrder(QtWidgets.QWidget):
    def __init__(self):
        super(PurchaseOrder, self).__init__()
        uic.loadUi("../UI/PurchaseOrder.ui", self)

    # creation of the scroll area
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)

        self.MainLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.scrollWidget.setLayout(self.MainLayout)

        self.DynamicGrid = QtWidgets.QGridLayout()
        self.MainLayout.addLayout(self.DynamicGrid)
        self.DynamicGrid.addWidget(QtWidgets.QLabel("Name"), 0, 0)
        self.DynamicGrid.addWidget(QtWidgets.QLabel("Qty"), 0, 1)
        self.DynamicGrid.addWidget(QtWidgets.QLabel("Order Date"), 0, 2)

        self.ButtonLayout = QtWidgets.QHBoxLayout()
        self.MainLayout.addLayout(self.ButtonLayout)

        self.PushBtn = QtWidgets.QPushButton("Add More")
        self.CreateBtn = QtWidgets.QPushButton("Create Button")
        self.ButtonLayout.addWidget(self.PushBtn)
        self.ButtonLayout.addWidget(self.CreateBtn)
        # self.checkBoxColorblindMode.stateChanged.connect(self.ToggleColorblindMode)

        self.PushBtn.clicked.connect(self.addRow)
        self.CreateBtn.clicked.connect(self.MakePurchaseOrder)

        self.MainLayout.addStretch(1)

        self.row_count = 1
        self.addRow()
        self.addRow()

    def GenerateOrderID(self):
        return ''.join(random.choice('0123456789') for _ in range(6))


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

    def database2(self):
        self.conn2 = sqlite3.connect('PurchaseOrder.db')
        self.cursor2 = self.conn2.cursor()



    def database(self):
        self.conn = sqlite3.connect('Fridge.db')
        self.cursor = self.conn.cursor()


    def MakePurchaseOrder(self):
        self.database()
        self.database2()
        OrderID = self.GenerateOrderID()

        self.conn2.execute("BEGIN")
        Ordered = False
        try:
            InsertionQuery = 'INSERT INTO "PurchaseOrder" ("Name", "Quantity", "OrderDate", "OrderID") VALUES (?, ?, ?, ?)'

            for row in range(1, self.row_count):
                name_widget = self.DynamicGrid.itemAtPosition(row, 0).widget()
                qty_widget = self.DynamicGrid.itemAtPosition(row, 1).widget()
                date_widget = self.DynamicGrid.itemAtPosition(row, 2).widget()

                name = name_widget.text() if isinstance(name_widget, QtWidgets.QLineEdit) else None
                QuantityText = qty_widget.text() if isinstance(qty_widget, QtWidgets.QLineEdit) else None
                OrderDate = date_widget.date().toString("yyyy-MM-dd") if isinstance(date_widget,QtWidgets.QDateEdit) else None
                if not name or not QuantityText:
                    continue

                try:
                    quantity = int(QuantityText)
                except ValueError:

                    QMessageBox.warning(self, "Input Error",
                                        f"Invalid quantity '{QuantityText}' on row {row}. Please enter a valid number.")
                    continue

                self.cursor2.execute(InsertionQuery, (name, quantity, OrderDate, OrderID))
                self.cursor.execute("SELECT Ordered FROM Fridge WHERE Name = ?", (name,))
                result = self.cursor.fetchone()

                if result:
                    self.cursor.execute("UPDATE Fridge SET Ordered = Ordered + ? WHERE Name = ?", (quantity, name))
                    self.conn.commit()
                    Ordered = True

            self.conn2.commit()
            if Ordered:
                QMessageBox.information(self, "Sucessful", "Both the Purchase Order and Fridge databases were updated successfully.")
            else:
                QMessageBox.information(self, "Sucessful", "The Purchase Order database was updated successfully.")
        except Exception as e:

            self.conn2.rollback()
            self.conn.rollback()
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")


    def addRow(self):

        NameBox = QtWidgets.QLineEdit()
        QtyBox = QtWidgets.QLineEdit()
        DateComboBox = QtWidgets.QDateEdit()


        self.DynamicGrid.addWidget(NameBox, self.row_count, 0)
        self.DynamicGrid.addWidget(QtyBox, self.row_count, 1)
        self.DynamicGrid.addWidget(DateComboBox, self.row_count, 2)


        self.row_count += 1

