import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication,QMessageBox,QWidget
from PyQt5 import uic,QtGui

from Roleselection import entrypoint



class mainentry(QWidget):
    

    def main():
        
        app= QApplication([])
        window = entrypoint()
        app.exec_()
    

    if __name__ == '__main__':
        main()
