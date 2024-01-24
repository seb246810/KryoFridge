import sys
import os
import pytest

from PyQt5 import QtCore

#print('original sys.path:', sys.path)

sys.path.append('../Modules')

#os.chdir(r,'\root\Modules')


import Roleselection


@pytest.fixture

def app(qtbot):
  
    
    test_hello_app = Roleselection.entrypoint()
    qtbot.addWidget(test_hello_app)
    
    return test_hello_app





def test_Headchefwindowlogin_open(app,qtbot):
    qtbot.mouseClick(app.Headchef,QtCore.Qt.LeftButton)
    assert   app.isVisible()

def test_Driverloginwindow_opens(app,qtbot):
    qtbot.mouseClick(app.Delivery,QtCore.Qt.LeftButton)
    assert app.isVisible()

def test_Label_correct(app):
    assert app.label.text() == "Kryo Fridge Application"



