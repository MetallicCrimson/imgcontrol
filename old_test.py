import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QGridLayout, QLayout, QBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QDrag
from PyQt5.QtCore import pyqtSlot
import tkinter as tk
from tkinter import filedialog

def window():

    app = QApplication(sys.argv)
    win = QWidget()

    #textLabel = QLabel(win)
    #textLabel.setText("Hello World!")
    
    win.setGeometry(-10,0,300,100)
    win.setWindowTitle("PyQt5 Example")

    

    win.im = QPixmap("./cat.jpg")
    win.label = QLabel()
    win.label.setPixmap(win.im)

    win.grid = QGridLayout()
    win.grid.setSpacing(0)
    win.grid.setContentsMargins(0,0,0,0)
    win.grid.addWidget(win.label,0,0)
    win.setLayout(win.grid)

    button1 = QPushButton(win)
    button1.setText("Button1")
    button1.move(64,32)
    button1.clicked.connect(button1_clicked)

    edit = QLineEdit("", win)
    edit.setDragEnabled(True)
    edit.move(30,65)

    win.show()
    sys.exit(app.exec())


def showDialog():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Perhaps")
    msgBox.setWindowTitle("Something is happening")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.buttonClicked.connect(msgButtonClick)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print("Okay then")

def msgButtonClick(i):
    print("Pressed button is", i.text())

def button1_clicked():
    print("hi")

if __name__ == '__main__':
    folder_selected = filedialog.askdirectory()
    window()

