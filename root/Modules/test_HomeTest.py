import sys
import pytest
from log  import MyGui
from PyQt5 import QtCore


@pytest.fixture

def app(qtbot):
    
    test_hello_app = MyGui()
    qtbot.addWidget(test_hello_app)
    return test_hello_app


def test_button(app):
    assert app.label.text() == "Username"

def test_label(app):
    assert app.label_2.text()== "Password"


def test_window_close(app,qtbot):
    qtbot.mouseClick(app.return_2,QtCore.Qt.LeftButton)
    assert not  app.isVisible()
