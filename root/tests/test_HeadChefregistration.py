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

import HeadchefRegistration

@pytest.fixture

def register(qtbot):
    windowtotest = HeadchefRegistration.Headchefregister()
    qtbot.addWidget(windowtotest)
    return windowtotest


def test_accountregister_test(register,qtbot):
        register.usernamefield.setText("seb")
        register.passwordfield.setText("hello")
        register.confirmfield.setText("hello")
        username = register.usernamefield.text()
        register.registerFunction()



        

   

   

        def database(register):
            register.conn = sqlite3.connect('headchefuser.db')
            register.cursor = register.conn.cursor()

    
        database(register)
   
        def accountexists(username):
    

            query = 'SELECT * FROM user WHERE username=?'
            register.cursor.execute(query, (username,))
            row = register.cursor.fetchone()

            return row is not None
    

        def Idcreated(username):
             query ="SELECT headchefID FROM user WHERE username =?"
             register.cursor.execute(query,(username,))
             ID = register.cursor.fetchone()

             return ID is not None
    
   

    
   
    

        assert Idcreated(username)
        assert accountexists(username)


def test_morethanonechef_(register):
        
        def database(register):
                register.conn = sqlite3.connect('headchefuser.db')
                register.cursor = register.conn.cursor()

    
        database(register)
     
     
     
     
          

        user_count_query = 'SELECT COUNT(*) FROM user'
        register.cursor.execute(user_count_query)
        user_count = register.cursor.fetchone()[0]


    



        assert user_count <= 1



def test_registerfunction_differentconfirmedpassword_test(register,qtbot):

    register.usernamefield.setText("barry")
    register.passwordfield.setText("alan")
    register.confirmfield.setText("ala")

    register.registerFunction()

    assert register.error.text()=="Passwords do not match."


def test_registerfunction_nullvalue_test(register,qtbot):

    register.usernamefield.setText("")
    register.passwordfield.setText("")
    register.confirmfield.setText("")

    register.registerFunction()

    assert register.error.text()=="Please fill in all inputs."

     







