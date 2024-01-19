#import sys
import os
import pytest

from PyQt5 import QtCore

#print('original sys.path:', sys.path)

#sys.path.append('\\root\\Modules')

#os.chdir(r,'\root\Modules')



from ..Modules import Headcheflogin


@pytest.fixture

def app(qtbot):
    
    test_hello_app = Headcheflogin.MyGui()
    qtbot.addWidget(test_hello_app)
    return test_hello_app





def test_window_close(app,qtbot):
    qtbot.mouseClick(app.BackButton,QtCore.Qt.LeftButton)
    assert not  app.isVisible()
    
