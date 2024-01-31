import sys
import pytest
import sqlite3

from PyQt5 import QtCore

sys.path.append('../Modules')



import driverLogin



@pytest.fixture

def app(qtbot):
     
  
    
    test_hello_app = driverLogin.driverLogin()
    qtbot.addWidget(test_hello_app)
    
    return test_hello_app


def test_Incorrectcredentials_test(app,qtbot):
    app.usernamefield.setText("bob") 
    app.passwordfield.setText("123") 



    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert  app.error.text() =="Invalid username or password"
    assert  app.isVisible()


def test_nullcredentials_test(app,qtbot):
    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert app.error.isVisible()
    assert  app.isVisible()


    

def test_onefieldFilled_test(app,qtbot):
    app.usernamefield.text()== "sam"

    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert app.error.isVisible()
    assert  app.isVisible()


def test_correctcredentials_test(app,qtbot):
    app.usernamefield.setText("seb")
    app.passwordfield.setText("hello123")


    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert app.error.text()== "Login Successful"
    assert app.close()
    app.message.done(1)
    
    
    