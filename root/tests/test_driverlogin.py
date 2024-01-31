import sys
import pytest
import sqlite3

from PyQt5 import QtCore

sys.path.append('../Modules')







@pytest.fixture

def app(qtbot):
     
    import driverLogin
    
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
    app.passwordfield.setText("don1")


    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert app.error.text()== "Login Successful"
    assert app.close()

def test_otp_test(app,qtbot):

    otp =app.getOTP()

    assert len(otp) ==4


def test_updatepassword__(app,qtbot):
    username = "seb"
    password = "don1"

    app.update_user_password(username,password)

    query = 'SELECT password FROM deliverydriver WHERE username= ?'
    app.cursor.execute(query, (username,))
    user = app.cursor.fetchone()

    assert user[0] == password


   
  
    
    
    