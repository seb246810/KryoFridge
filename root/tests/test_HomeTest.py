#import sys
import os
import pytest

from PyQt5 import QtCore

#print('original sys.path:', sys.path)

#sys.path.append('\\root\\Modules')

#os.chdir(r,'\root\Modules')



from ..Modules import log


@pytest.fixture

def app(qtbot):
    
    test_hello_app = log.MyGui()
    qtbot.addWidget(test_hello_app)
    return test_hello_app


def test_button(app):
    assert app.label.text() == "Username"

def test_label(app):
    assert app.label_2.text()== "Password"


def test_window_close(app,qtbot):
    qtbot.mouseClick(app.return_2,QtCore.Qt.LeftButton)
    assert not  app.isVisible()
    
