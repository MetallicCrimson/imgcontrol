from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import math


boldFont = QFont()
boldFont.setBold(True)
helpText1 = "Overview:"
helpText2 = """ImgControl is a timed image viewer for artists, who want to practice quick sketches. It takes a directory, gets all its images (even from the subdirectories), and shows them either in a row, or in a random order. The program can be controlled with the (fully movable) UI row and with keyboard input as well.
"""
helpText3 = "The UI bar functions:"
helpText4 = """(the keyboard input is just the same letter, left-right arrow, and space for the timer circle)

R: changes the ordering. If it's light, it displays the images randomly, if it's dark, it walks through them in order.
T: restarts the timer with the current image (basically the same as moving left and then right).
Left arrow: jumps back to the previous image (if it can: check the "Image history" section).
Timer circle: pauses and resumes the timer.
Right arrow: gets the next image (either randomly or not).
F: displays a folder selection dialog. If there is a folder selected, it clears the image history, restarts the timer, and displays either the first image, or a random one.
(Note: the OS can mess up some default folder localization names ("My pictures", etc), so in order to avoid errors, don't choose them.)
S: displays the settings window.
"""
helpText5 = "Inputs in settings:"
helpText6 = """Session seconds: the length of each drawing session. Lower limit is 1, upper limit is technically nonexistent (except the memory limitations), but please try to end it before the heat death of the universe...
Break seconds: the option to include a short (or long, you decide) break between sessions. Lower limit is 0, in which case it will simply goes to the next image without hesitation.
Image history size: the program keeps track of the last x images for two reasons: to enable left scrolling, and to not randomly select the images in it (thus eliminating repetition). A size of 50 should be enough for all purposes, but it can handle larger without a problem. Also, the history size cannot be bigger than the number of images in the directory.


Note: hitting Enter saves the inputs (just like clicking the Save button), hitting Esc closes the settings window (without saving).
Another note: if you want to delete the saved config data, delete config.txt from the folder of the program."""
aboutText = """This app was developed by Daniel Kovacs, as a request of an artist who got salty for not having a timed viewer for her million quintillion bajillion images (shoutout to Lia).

It was made using Python, with PyQt6 as the graphics library.
MIT license applies, so you can do anything you want either with this or with the code itself.

Github page:"""

class SettingsWindow(QWidget):
    def __init__(self, qm, win_x, win_y):
        super().__init__()
        layout = QVBoxLayout()
        
        self.sessionLabel = QLabel("Session seconds:")
        sessionTimeInput = SettingsInput("sessionTime", self, qm)
        self.sessionTimeInput = sessionTimeInput
        self.breakLabel = QLabel("Break seconds:")
        breakTimeInput = SettingsInput("breakTime", self, qm)
        self.breakTimeInput = breakTimeInput
        self.historyLabel = QLabel("Image history size:")
        historyInput = SettingsInput("history", self, qm)
        self.historyInput = historyInput
        saveButton = SettingsButton("save", self, qm)
        self.saveButton = saveButton
        helpButton = SettingsButton("help", self, qm)
        self.helpButton = helpButton
        aboutButton = SettingsButton("about", self, qm)
        self.aboutButton = aboutButton

        layout.addWidget(self.sessionLabel)
        layout.addWidget(self.sessionTimeInput)
        layout.addWidget(self.breakLabel)
        layout.addWidget(self.breakTimeInput)
        layout.addWidget(self.historyLabel)
        layout.addWidget(self.historyInput)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.helpButton)
        layout.addWidget(self.aboutButton)
        self.setLayout(layout)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("icon.png"))

        self.qm = qm

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.move(self.qm.frame.x() + 30, self.qm.frame.y() + 30)

        self.sessionTimeInput.setText(str(int(self.qm.timerCircle.sessionTime/1000)))
        self.breakTimeInput.setText(str(int(self.qm.timerCircle.breakTime/1000)))
        if self.qm.directory != None:
            self.historyInput.setText(str(len(self.qm.imgHistory)))
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)
        
        self.saveButton.setText("Saved ✓")
        return super().showEvent(a0)
    
    def keyReleaseEvent(self, a0: QKeyEvent | None) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()

        return super().keyReleaseEvent(a0)

    def saveInputs(self):
        if self.qm.directory == None:
            return

        if self.sessionTimeInput.text().isdigit():
            tempSession = int(self.sessionTimeInput.text())
        else:
            return
        if self.breakTimeInput.text().isdigit():
            tempBreak = int(self.breakTimeInput.text())
        else:
            return
        if self.historyInput.text().isdigit():
            tempHistory = int(self.historyInput.text())
        else:
            return
        
        if tempSession > 0 and tempBreak >= 0 and tempHistory > 0:
            self.qm.timerCircle.currentTime = tempSession * 1000
            self.qm.timerCircle.sessionTime = tempSession * 1000
            self.qm.timerCircle.breakTime = tempBreak * 1000
            self.qm.historySize = tempHistory
            if len(self.qm.imgHistory) != tempHistory:
                self.qm.resetHistory()
            self.qm.timerCircle.parentItem().currentState = "session"
            self.saveButton.setText("Saved ✓")

            # this is the most important part of the code
            if (tempSession == round(44.81**(3/2) + math.log(57208) ** 2) and tempBreak == round((59392 >> 10) + (math.perm(5,2)) - round(math.pi) ** 2)):
                self.saveButton.setText("Very funny")

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.qm.directory != None:
            self.qm.timerCircle.timer.start()
            self.qm.frame.breakMask.setVisible(False)

        return super().closeEvent(a0)
    
class SettingsInput(QLineEdit):
    def __init__(self, purpose, sw, qm):
        self.sw = sw
        self.purpose = purpose
        self.qm = qm
        super().__init__()

    def keyReleaseEvent(self, a0: QKeyEvent | None) -> None:
        if self.checkInputs():
            self.sw.saveButton.setText("Saved ✓")
        else:
            self.sw.saveButton.setText("Save")

        if a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter:
            self.sw.saveInputs()

        elif a0.key() == Qt.Key.Key_Escape:
            self.sw.close()
    
    def checkInputs(self):
        if self.qm.directory == None:
            return self.sw.sessionTimeInput.text() == str(int(self.qm.timerCircle.sessionTime/1000)) and self.sw.breakTimeInput.text() == str(int(self.qm.timerCircle.breakTime/1000))
        else:
            return self.sw.sessionTimeInput.text() == str(int(self.qm.timerCircle.sessionTime/1000)) and self.sw.breakTimeInput.text() == str(int(self.qm.timerCircle.breakTime/1000)) and self.sw.historyInput.text() == str(len(self.qm.imgHistory))
    
class SettingsButton(QPushButton):
    def __init__(self, purpose, sw, qm):
        self.sw = sw
        self.purpose = purpose
        self.qm = qm

        if purpose in ["help", "about"]:
            tempWindow = SettingsSubWindow(purpose, qm)
            self.subWindow = tempWindow

        super().__init__(str.capitalize(purpose))

    def mouseReleaseEvent(self, e: QMouseEvent | None) -> None:
        match self.purpose:
            case "save":
                self.sw.saveInputs()
            case "help":
                self.subWindow.show()
            case "about":
                self.subWindow.show()

        return super().mouseReleaseEvent(e)
    
class SettingsSubWindow(QWidget):
    def __init__(self, purpose, qm):
        super().__init__()

        tempLayout = QVBoxLayout()
        self.setLayout(tempLayout)
        self.resize(0,0)

        self.purpose = purpose
        self.setFixedWidth(600)
        self.setWindowIcon(QIcon("icon.png"))

        if purpose == "help":
            tempLabel0 = QLabel()
            self.tempLabel0 = tempLabel0
            tempLabel0.setWordWrap(True)
            tempLabel1 = QLabel(helpText1)
            self.tempLabel1 = tempLabel1
            tempLabel1.setFont(boldFont)
            tempLabel1.setWordWrap(True)
            tempLabel2 = QLabel(helpText2)
            tempLabel2.setWordWrap(True)
            tempLabel3 = QLabel(helpText3)
            tempLabel3.setFont(boldFont)
            tempLabel3.setWordWrap(True)
            tempLabel4 = QLabel(helpText4)
            tempLabel4.setWordWrap(True)
            tempLabel5 = QLabel(helpText5)
            tempLabel5.setFont(boldFont)
            tempLabel5.setWordWrap(True)
            tempLabel6 = QLabel(helpText6)
            tempLabel6.setWordWrap(True)

            self.layout().addWidget(tempLabel0)
            self.layout().addWidget(tempLabel1)
            self.layout().addWidget(tempLabel2)
            self.layout().addWidget(tempLabel3)
            self.layout().addWidget(tempLabel4)
            self.layout().addWidget(tempLabel5)
            self.layout().addWidget(tempLabel6)

            self.setWindowTitle("Help")
        else:
            tempLabel1 = QLabel(aboutText)
            tempLabel1.setWordWrap(True)
            tempLabel2 = QLabel("<a href=\"https://github.com/SilverCrimson\">https://github.com/SilverCrimson</a>")
            tempLabel2.setWordWrap(True)
            tempLabel2.setOpenExternalLinks(True)
            self.layout().addWidget(tempLabel1)
            self.layout().addWidget(tempLabel2)

            self.setWindowTitle("About")

        self.qm = qm

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.move(self.qm.frame.x() + 60, self.qm.frame.y() + 60)
        if self.purpose == "help":
            if self.qm.directory == None:
                self.tempLabel0.setText("(If this is your first time opening the app, you have to select a directory to get it running. It can't show images without the images...)\n")
            else:
                self.tempLabel0.setMaximumHeight(0)
                self.tempLabel0.setText("")
        return super().showEvent(a0)

    def keyReleaseEvent(self, a0: QKeyEvent | None) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()

        return super().keyReleaseEvent(a0)