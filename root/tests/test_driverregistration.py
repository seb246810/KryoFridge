import sys
import pytest
import sqlite3

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QSignalSpy
from unittest.mock import patch
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QApplication, QMessageBox, QLineEdit, QDialog, \
    QInputDialog

sys.path.append('../Modules')

import driverRegistration 

@pytest.fixture

def register(qtbot):
    windowtotest = driverRegistration.driverRegister()
    qtbot.addWidget(windowtotest)
    return windowtotest


def test_registerfunction_differentconfirmedpassword_test(register,qtbot):

    register.usernamefield.setText("barry")
    register.passwordfield.setText("alan")
    register.confirmfield.setText("ala")

   

    #register.registerFunction()

    with patch.object(QMessageBox, 'warning') as mock_warning:
        register.registerFunction()

        # Check if QMessageBox.warning() was called
        mock_warning.assert_called_once_with(register,  "Passwords do not match.")


def test_registerfunction_notextinput_test(register,qtbot):
    register.usernamefield.setText("")
    register.passwordfield.setText("")
    register.confirmfield.setText("")



    with patch.object(QMessageBox, 'warning') as mock_warning:
        register.registerFunction()

        # Check if QMessageBox.warning() was called
        mock_warning.assert_called_once_with(register,  "Please fill in all inputs.")



def test_registerfunction_Onefieldnull_test(register,qtbot):

    register.usernamefield.setText("barry")
    register.passwordfield.setText("alan")
    register.confirmfield.setText("")

   

    #register.registerFunction()

    with patch.object(QMessageBox, 'warning') as mock_warning:
        register.registerFunction()

        # Check if QMessageBox.warning() was called
        mock_warning.assert_called_once_with(register,  "Please fill in all inputs.")



def test_registerfunction_Correctfields_test(register,qtbot):

    register.usernamefield.setText("barry")
    register.passwordfield.setText("alan")
    register.confirmfield.setText("alan")

    username=register.usernamefield.text()
    

    

   

    register.registerFunction()

    def database(register):
        register.conn = sqlite3.connect('deliveryusers.db')
        register.cursor = register.conn.cursor()

    
    database(register)
   
    def accountexists(username):
    

        query = 'SELECT * FROM  WHERE username=?'
        register.cursor.execute(query, (username,))
        row = register.cursor.fetchone()

        return row is not None
    

    

   

    
   
    


    assert accountexists(username)

    def accountdelete(username):

        query = 'DELETE FROM deliverydriver WHERE username=?'
        register.cursor.execute(query,(username,))
        register.conn.commit()
        row = register.cursor.fetchone()

        return row is None
    
    assert accountdelete(username)


def test_useralreadyexists_test(register,qtbot):
    user = "cat"

    password= "don1"



    with patch.object(QMessageBox, 'warning') as mock_warning:
        register.registerDriver(user,password)

        # Check if QMessageBox.warning() was called
        mock_warning.assert_called_once_with(register,  "Error", f"Username {user} is already taken, please choose another.")







    


