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

import Headcheflogin
import fridge



@pytest.fixture

def register(qtbot):
    windowtotest = Headcheflogin.Headcheflogin()
    qtbot.addWidget(windowtotest)
    return windowtotest

@pytest.fixture

def regwindow(qtbot):
    import HeadchefRegistration
    window =  HeadchefRegistration.Headchefregister()
    qtbot.addWidget(window)
    return window





def test_cantregister_test(register,regwindow):
    regwindow.usernamefield.setText("seb")
    regwindow.passwordfield.setText("hello")
    regwindow.confirmfield.setText("hello")
    username = regwindow.usernamefield.text()

    regwindow.registerFunction()


    def database(register):
            regwindow.conn = sqlite3.connect('headchefuser.db')
            regwindow.cursor = regwindow.conn.cursor()

    
    database(register)
   
    def accountexists(username):
    

            query = 'SELECT * FROM user WHERE username=?'
            regwindow.cursor.execute(query, (username,))
            row = regwindow.cursor.fetchone()

            return row is not None
   


    assert accountexists(username)


    

    with patch.object(QMessageBox, 'warning') as mock_warning:
        register.registerWindow()

        # Check if QMessageBox.warning() was called
        mock_warning.assert_called_once_with(register,  "Access Denied",
                                "Oops there can only be one head chef.",QMessageBox.Ok)
        


def test_userRole_test(register):

    username="seb"
     

    register.update_user_role(username)


    query = 'SELECT role FROM user WHERE username = ?'
    register.cursor.execute(query,(username,))
    ID = register.cursor.fetchone()

    assert ID[0] == "HeadChef"



def test_loginfunction_(register):
       register.usernamefield.setText("seb")
       register.passwordfield.setText("hello")


       register.loginFunction()

       window=register.gotofridge()

       assert window.isVisible()


def test_loginfunctioninvalid_test(register):
     register.usernamefield.setText("he")
     register.passwordfield.setText("hey")


     register.loginFunction()

     assert register.error.text()== "Invalid username or password"



def test_colorblindmode_test(register):
     state=2 #simulate state that checkbutton is clicked

     colorblindmode=register.ToggleColorblindMode(state) #pass into argument


     assert colorblindmode == True #if colorblindmode has switched on returns true


def test_nocolorblindmode_test(register):
     state=1

     standardmode = register.ToggleColorblindMode(state)

     assert standardmode == False





     










