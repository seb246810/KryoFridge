import sys
import pytest
import sqlite3

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QApplication, QMessageBox, QLineEdit, QDialog, \
    QInputDialog
from unittest.mock import patch

sys.path.append('../Modules')


import driverLogin






    
    








@pytest.fixture

def app(qtbot):
     
    
    
    test_hello_app = driverLogin.driverLogin()
    qtbot.addWidget(test_hello_app)
    
    return test_hello_app

@pytest.fixture

def registeraccounts(qtbot):
    import driverRegistration
  
    

    register = driverRegistration.driverRegister()
    qtbot.addWidget(register)

    return register


@pytest.fixture

def driverid(qtbot):
    
  
    

    iddialog = driverLogin.DriverIDDialog()
    qtbot.addWidget(iddialog)

    return iddialog



def test_Incorrectcredentials_test(app,qtbot):
    app.usernamefield.setText("bob") 
    app.passwordfield.setText("123") #set up test



    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton) #execute test
    
    assert  app.error.text() =="Invalid username or password"  #assert error message is correct
    assert  app.isVisible()





def test_nullcredentials_test(app,qtbot):
    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert app.error.text()=="Please input all fields."
    assert  app.isVisible()


    

def test_onefieldFilled_test(app,qtbot):
    app.usernamefield.text()== "sam"

    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert app.error.text()=="Please input all fields."
    assert  app.isVisible()






   


def test_correctcredentials_test(app,qtbot,registeraccounts):

    def accountdelete(username):

        query = 'DELETE FROM deliverydriver WHERE username=?'
        app.cursor.execute(query,(username,))
        app.conn.commit()
        row = app.cursor.fetchone()

        return row is None


   
    assert app.isVisible()
   
    app.usernamefield.setText("seb")
    app.passwordfield.setText("don")      #setuptest
    username="seb"
    password="don"
    storedId = 7966

    registeraccounts.registerDriver(username,password)

    def accountexists(username):
    

        query = 'SELECT * FROM deliverydriver WHERE username=?' 
        app.cursor.execute(query, (username,))
        row = app.cursor.fetchone()

        return row is not None

    print("After creating DriverIDDialog:", app.isVisible())


    

   


    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton) #execute test


    

    


    assert accountexists(username) #assert account exists in database

   

    assert accountdelete(username)
    

   

    


    



    




    

def test_otp_test(app,qtbot):

    otp =app.getOTP()

    assert len(otp) ==4
    assert type(otp) == str

def test_gotofridge(app,qtbot):
    from fridge import fridgeWindow

    app.fridge = None  # Reset fridge instance
    app.close = lambda: None 

    app.gotofridge()

    assert app.fridge.isVisible()
    app.close()

def test_showdriverreigster_test(app):
   from driverRegistration import driverRegister
   app.driverRegisterWindow()

    
   assert app.register.isVisible()


def test_getuserid_test(app,driverid,qtbot):
    username = "cat"

    password = "pat"

    #app.validateCredentials(user,password)

    

    #app.dialog = None

    driverid.driverIdInput.setText("7966") 

    #qtbot.mouseClick(driverid.verifybutton,QtCore.Qt.LeftButton)

    ID= driverid.getDriverId()

    assert ID == "7966"

    
    #assert driverid.isVisible()



    #app.verifyDriverID( user, username)




def test_updatepassword__(app,qtbot,registeraccounts):
    username = "seb"
    password = "don1"
    newpassword = "hello"

    def accountdelete(username):

        query = 'DELETE FROM deliverydriver WHERE username=?'
        app.cursor.execute(query,(username,))
        app.conn.commit()
        row = app.cursor.fetchone()

        return row is None

    def database(app):
        app.conn = sqlite3.connect('deliveryusers.db')
        app.cursor = app.conn.cursor()


  


    registeraccounts.registerDriver(username,password)

    
    
    
    app.update_driver_password(username,newpassword)


    query = 'SELECT password FROM deliverydriver WHERE username= ?'
    app.cursor.execute(query, (username,))
    user = app.cursor.fetchone()

    

    assert user[0] == newpassword

    assert accountdelete(username)





   
  
    
    
    