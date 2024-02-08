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

def driverid(qtbot):
  
    

    idtag = driverLogin.DriverIDDialog()
    qtbot.addWidget(idtag)

    return idtag




def test_Incorrectcredentials_test(app,qtbot):
    app.usernamefield.setText("bob") 
    app.passwordfield.setText("123") 



    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)
    assert  app.error.text() =="Invalid username or password"
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






   


def test_correctcredentials_test(app,qtbot,driverid):

   # monkeypatch.setattr(driverLogin, 'DriverIDDialog', MockDriverIDDialog)
    assert app.isVisible()
   
    app.usernamefield.setText("seb")
    app.passwordfield.setText("don1")
    username="seb"
    storedId = 7966

    print("After creating DriverIDDialog:", app.isVisible())


    

   


    qtbot.mouseClick(app.LoginButton,QtCore.Qt.LeftButton)


    def accountexists(username):
    

        query = 'SELECT * FROM deliverydriver WHERE username=?'
        app.cursor.execute(query, (username,))
        row = app.cursor.fetchone()

        return row is not None

    #print("is visible", MockDriverIDDialog.isVisible())

    #settingtext=driverid.mockDriverInputId.setText(str(storedId))


    #assert mock_dialog is not None, "Mocked dialog not found in top-level widgets"

    # Perform assertions related to the mock dialog
    


   




    #dialog = qtbot.waitExposed(driverLogin.DriverIDDialog)
    #dialog = qtbot.waitUntil(lambda: any(isinstance(widget, driverLogin.DriverIDDialog) for widget in QApplication.topLevelWidgets()))
    #with qtbot.waitExposed(driverLogin.DriverIDDialog) as dialog:
        # Check if the dialog is visible
    #dialog.show()
    assert accountexists(username)

    #assert dialog.isVisible()
    
    #assert dialog.isVisible()
    #assert dialog.isVisible()
    #with qtbot.waitExposed(driverid):
        # Perform assertions or inspection
        #assert driverid.isVisible()  # Assuming driverid is the instance of DriverIDDialog
        #assert app.error.text() == "Login Successful"

    #driverid.setFocus()
    #assert driverid.isVisible()
    #assert settingtext == "7966"

    
    #mock_dialog = app.findChild(MockDriverIDDialog)
    

    #QTest.qWaitForWindowExposed(driverid)

    
    #print("Dialog isVisible:", mock_dialog.isVisible())
    #print("Dialog isActiveWindow:", driverid.isActiveWindow())
    #print("Dialog isTopLevel:", driverid.isTopLevel())
    #print("Dialog windowState:", driverid.windowState())

    
    #qtbot.wait(100)

    #print("Dialog geometry:", driverid.geometry())

    #assert mock_dialog.isVisible()

    #app.close()



    #driverid.driverIdInput.setFocus()
    #driverid.show()

    #driver_id_input = driverid.findChild(QLineEdit, "driverInputId")

    #assert driver_id_input is not None


    

   

    


    



    #qtbot.waitUntil(lambda: idtag.isVisible())

    #print("After creating DriverIDDialog:", driverid.isVisible())

    #print("Before setting text:", driverid.driverIdInput.isVisible(), driverid.driverIdInput.text())
    
    #print("Is modal:", driverid.isModal())

    # Now that the dialog is shown, you can interact with it
    #dialog = qtbot.findObject(DriverIDDialog)
    
    # Set the driverId in the DriverIDDialog using setText
    #idwindow.driverIdInput.setText(str(storedId))
  
    #QTimer.singleShot(500, idtag)
    #QTest.keyClicks(driverid.driverIdInput, str(storedId))
    #driver_id_input.setText(str(storedId))
    #dialog.findChild(QLineEdit, "driverIdInput").setText(str(app.storedId))
    #print("After setting text:", driverid.driverIdInput.isVisible(), driverid.driverIdInput.text())

    # Accept the QDialog
    #qtbot.mouseClick(driverid.verifyButton, QtCore.Qt.LeftButton)

    #driver_id_from_dialog = idtag.getDriverId()
    #assert app.error.text()== "Login Successful"
    
    #assert app.close()





    

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




def test_updatepassword__(app,qtbot):
    username = "seb"
    password = "don1"

    app.update_user_password(username,password)

    query = 'SELECT password FROM deliverydriver WHERE username= ?'
    app.cursor.execute(query, (username,))
    user = app.cursor.fetchone()

    assert user[0] == password


   
  
    
    
    