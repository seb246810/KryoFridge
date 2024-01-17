import sys
import pytest
from PyQt5 import QtCore


sys.path.append('../root/Modules')
@pytest.fixture

def app(qtbot):
    import entry2
    test_hello_app = entry2.MyApp()
    qtbot.addWidget(test_hello_app)
    return test_hello_app


def test_button(app):
    assert app.label.text() == "Username"
