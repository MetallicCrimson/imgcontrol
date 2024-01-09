import sys
import typing
from PyQt6 import QtGui
from PyQt6.QtGui import QActionEvent, QCloseEvent, QEnterEvent, QFocusEvent, QKeyEvent, QPainter, QShowEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QRectF, pyqtSlot, Qt, QPointF
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent
from logic import * # ?
import math
import random
import pillow_avif
from PIL import Image
import math

# ⭝ ⭜ 
# This is just a check

# some constants
menu_width = 200
menu_height = 50
outlinePen = QPen()
outlinePen.setWidth(3)
circlePen = QPen()
circlePen.setWidth(0)
# this solution is fucking cursed. setting a color as a brush?
# then what is the point of a brush object?
menuBrush = QColor(0,0,0)

class QuickMenu(QGraphicsItemGroup):
    def __init__(self,x,y,win_width,win_height,frame): # possibly more...?
        super().__init__()
        #self.setPos(x,y)

        # what
        self.frame = frame
        self.currentState = "session"
        self.randomState = True

        # is there a way to check if the menu has been moved?
        # most likely yes. oh whatever
        self.freshlyPressed = False

        # Drawing the background
        tempRect1 = QGraphicsRectItem(x,y+20,17,17) # left square
        tempRect1.setBrush(menuBrush)
        tempRect2 = QGraphicsRectItem(x+18,y+10,214,37) # middle rect
        tempRect2.setBrush(menuBrush)
        tempRect3 = QGraphicsRectItem(x+230,y+20,7,7) # right square
        tempRect3.setBrush(menuBrush)
        tempCircle1 = QGraphicsEllipseItem(0,10,37,37)
        tempCircle1.setBrush(menuBrush)
        tempCircle2 = QGraphicsEllipseItem(0,10,20,20)
        tempCircle2.setBrush(menuBrush)
        tempCircle3 = QGraphicsEllipseItem(212,10,37,37)
        tempCircle3.setBrush(menuBrush)
        tempCircle4 = QGraphicsEllipseItem(207,10,20,20)
        tempCircle4.setBrush(menuBrush)
        #self.addToGroup(tempRect1)
        self.addToGroup(tempRect2)
        #self.addToGroup(tempRect3)
        self.addToGroup(tempCircle1)
        #self.addToGroup(tempCircle2)
        self.addToGroup(tempCircle3)
        #self.addToGroup(tempCircle4)

        # !!!
        self.images = buildDirStructure("C:/Users/tamer/Documents/programming/python/ImgControl_py/testFolder")
        self.imgId = random.randint(0,len(self.images)-1)
        imgName = self.images[self.imgId]
        self.frame.imgName = imgName
        self.frame.changeBackground(imgName)

        self.historySize = 50
        self.resetHistory()
        self.imgHistory[0] = self.frame.imgName

        # Elements of UI: four buttons and the timer circle
        # positions: hardcode? menu size is going to be fixed anyways
        buttonRandom = TestButton(7,15,27,27, "random", self.randomState)
        buttonRestart = TestButton(39,15,27,27, "restart", None)
        buttonLeft = TestButton(71,15,16,27,"left", None)
        buttonRight = TestButton(160,15,16,27, "right", None)
        buttonDirectory = TestButton(181,15,27,27, "directory", None)
        buttonSettings = TestButton(213,15,27,27, "settings", None)
        timerCircle = TimerCircle(x+88, y-6,72)

        self.buttonRandom = buttonRandom
        self.buttonRestart = buttonRestart
        self.buttonLeft = buttonLeft
        self.buttonRight = buttonRight
        self.buttonDirectory = buttonDirectory
        self.buttonSettings = buttonSettings
        self.timerCircle = timerCircle
        self.buttonArray = [buttonRandom, buttonRestart, buttonLeft, timerCircle, buttonRight, buttonDirectory, buttonSettings]
        self.addToGroup(buttonRandom)
        self.addToGroup(buttonRestart)
        self.addToGroup(buttonLeft)
        self.addToGroup(buttonRight)
        self.addToGroup(buttonDirectory)
        self.addToGroup(buttonSettings)
        self.addToGroup(timerCircle)

        self.setAcceptHoverEvents(True)
        self.win_width = win_width
        self.win_height = win_height


        # here? is it a good solution?
        self.settingsWindow = SettingsWindow(self)

        debugState = QGraphicsSimpleTextItem(self.currentState)
        debugState.setBrush(QColorConstants.White)
        self.addToGroup(debugState)
        self.debugState = debugState
        debugState.setPos(20,100)


    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print("Hovered")
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverLeaveEvent(event)
    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.freshlyPressed = True

        pass
    
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.freshlyPressed = False
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()
    
        # check for out of bounds here?
        updated_pos_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_pos_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        # or maybe here
        self.setPos(QPointF(updated_pos_x, updated_pos_y))

        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # ...or here...?
        self.reposition()
        if self.freshlyPressed:
            if (self.buttonRandom.buttonRect.contains(event.pos())):
                self.buttonRandom.testFunct()
            elif (self.buttonRestart.buttonRect.contains(event.pos())):
                self.buttonRestart.testFunct()
            elif (self.buttonLeft.buttonRect.contains(event.pos())):
                self.buttonLeft.testFunct()
            elif (self.buttonRight.buttonRect.contains(event.pos())):
                self.buttonRight.testFunct()
            elif (self.buttonDirectory.buttonRect.contains(event.pos())):
                self.buttonDirectory.testFunct()
            elif (self.buttonSettings.buttonRect.contains(event.pos())):
                self.buttonSettings.testFunct()
            elif (self.timerCircle.boundingRect().contains(event.pos())):
                # checks if the cursor is really in the circle. totally worth it
                if self.timerCircle.radius >= math.sqrt(abs((self.timerCircle.center[0] - event.pos().x())**2 + abs((self.timerCircle.center[1] - event.pos().y())**2))):
                    self.timerCircle.testFunct()

        return super().mouseReleaseEvent(event)
    
    def reposition(self):
        if (self.pos().x() < 0):
            self.setX(0)
        if (self.pos().y() < 0):
            self.setY(0)
        if (self.pos().x() > self.win_width-menu_width):
            print(self.win_width)
            self.setX(self.win_width-menu_width)
        if (self.pos().y() > self.win_height-menu_height):
            print(self.win_height)
            self.setY(self.win_height-menu_height)

    def addToHistory(self, new):
        self.imgHistory.insert(0,new)
        self.imgHistory.pop()

    def resetHistory(self):
        tempArray = []

        tempSize = min(self.historySize, len(self.images))
        for i in range(tempSize): # how much, exactly?
            tempArray.append(False)

        self.imgHistory = tempArray
        self.historyIndex = 0


class ImgFrame(QGraphicsView):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.myScene = QGraphicsScene()
        self.myScene.setSceneRect(0,0,width,height)
        self.myScene.setBackgroundBrush(QColor(200,220,200))


        self.setScene(self.myScene)

        x = 0
        y = 0
        w = 80
        h = 45

        pen = QColor(100,100,100)
        brush = QColor(150,150,150)

        pixmap = QPixmap("cat.jpg")
        pixmap2 = QGraphicsPixmapItem()
        pixmap = pixmap.scaled(int(width),
                               int(height),
                               Qt.AspectRatioMode.KeepAspectRatio)
        pixmap2.setPixmap(pixmap)
        self.pixmap2 = pixmap2
        self.scene().addItem(pixmap2)
        self.scene().setBackgroundBrush(0)
        self.imgName = ""

        self.itemGroup = QGraphicsItemGroup


    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        size = event.size()
        target_size = min(size.width(), size.height()) - 1
        x = (size.width() - target_size) // 2
        y = (size.height() - target_size) // 2
        #self.circle.setRect(x,y,target_size,target_size)
        self.setSceneRect(0,0,size.width(),size.height())
        #self.item.win_width = size.width() !!!
        #self.item.win_height = size.height() !!!

        #self.changeBackground(self.scene().
        
        if self.imgName[-4:] == "avif":
            print("it's an avif")
            #self.imgName = tempImgName

            # phew, almost done it VERY suboptimally
            pixmap = QPixmap(os.getcwd() + "/temp.jpg")
        else:
            pixmap = QPixmap(self.imgName)
        pixmap = pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio)
        self.pixmap2.setPixmap(pixmap)
        self.pixmap2.setPos((size.width()-self.pixmap2.boundingRect().width()) / 2, (size.height() - self.pixmap2.boundingRect().height()) / 2)

# img is a string?
    def changeBackground(self,img):
        #print(img)
        self.imgName = img # maybe not needed?
        print("test", img)
        if os.path.exists(os.getcwd() + "/temp.jpg"):
            os.remove(os.getcwd() + "/temp.jpg")

        if img[-4:] == "avif":
            print("it's an avif")
            #self.imgName = tempImgName

            pixmap = self.handleAvif(img)
        else:
            pixmap = QPixmap(img)
        pixmap = pixmap.scaled(self.width(),
                                self.height(),
                                Qt.AspectRatioMode.KeepAspectRatio)
        self.pixmap2.setPixmap(pixmap)
        print(self.pixmap2.boundingRect().width())
        self.pixmap2.setPos((self.width()-self.pixmap2.boundingRect().width()) / 2, (self.height()-self.pixmap2.boundingRect().height()) / 2)

    def handleAvif(self, img):
        imgname = img[:-5]
        tempImgName = os.getcwd() + "/temp.jpg"
        temp = Image.open(img)
        temp.save(tempImgName)
        print("Saved to " + tempImgName)
        #self.imgName = tempImgName
        pixmap = QPixmap(tempImgName)
        return pixmap

    def handleSettings(self):
        return
        # if self.settingsRect in self.scene().items():
        #     self.scene().removeItem(self.settingsRect)
        # else:
        #     self.scene().addItem(self.settingsRect)
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.quickMenu.settingsWindow.isVisible:
            self.quickMenu.settingsWindow.close()

        return super().closeEvent(a0)


def renderImgFrame(x,y,width,height):
    tempImgFrame = ImgFrame(x,y,width,height)

    return tempImgFrame


def renderQuickMenu(x,y,win_width,win_height,frame):
    tempMenu = QuickMenu(x,y,win_width,win_height,frame)

    return tempMenu

class TestButton(QGraphicsItemGroup):
    def __init__(self,x,y,w,h,purpose, flag):
        super().__init__()
        self.purpose = purpose
        tempRect = QGraphicsRectItem(x,y,w,h)
        tempRect.setBrush(QColorConstants.DarkMagenta)
        innerText = QGraphicsSimpleTextItem()
        innerText.setFont(QFont("TypeWriter", 20,800, False))
        innerText.setPen(QColorConstants.Gray)
        innerText.setBrush(QColorConstants.Gray)
        self.innerText = innerText
        
        # that's important to initializing!
        if self.purpose == "random" and not flag:
            innerText.setPen(QColorConstants.Black)
            innerText.setBrush(QColorConstants.Black)

        self.buttonRect = tempRect.boundingRect()

        match purpose:
            case "random":
                innerText.setText("R")
            case "restart":
                innerText.setText("T")
            case "directory":
                innerText.setText("F")
            case "settings":
                innerText.setText("S")
            case "left":
                innerText.setText("⏴")
            case "right":
                innerText.setText("⏵")    
            case _:
                print("What the fuck")

        self.addToGroup(tempRect)
        self.addToGroup(innerText)
        
        innerText.setY(tempRect.boundingRect().center().y() - innerText.boundingRect().height()/2)
        innerText.setX(tempRect.boundingRect().center().x() - innerText.boundingRect().width()/2)


    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:

        print("Button pressed")
        return super().mouseReleaseEvent(event)
    

    def testFunct(self):
        print(self.purpose, "has been pressed")
        if self.purpose == "directory":
            self.parentItem().timerCircle.timer.stop()
            testName = QFileDialog.getExistingDirectory()
            # this is supposed to return an array, with all the items?
            filesArray = buildDirStructure(testName)
            if filesArray:
                self.parentItem().images = filesArray
                # for name in filesArray:
                #         print(name)
                #         print(os.path.isfile(name))
                print("new dir: " + testName)
                #self.parentItem().timerCircle.restart_time()
                self.parentItem().currentState = "break"
                self.parentItem().timerCircle.currentTime = 0
                self.parentItem().resetHistory()
                self.parentItem().timerCircle.timer.start()
            else:
                self.parentItem().timerCircle.timer.start()
        elif self.purpose == "right":
            self.parentItem().currentState = "break"
            self.parentItem().timerCircle.currentTime = 0
            self.parentItem().timerCircle.timer.start()
        elif self.purpose == "left":
            #print(self.parentItem().historyIndex)
            #print(self.parentItem().imgHistory)
            if self.parentItem().historyIndex < len(self.parentItem().imgHistory) - 1:
                temp = self.parentItem().imgHistory[self.parentItem().historyIndex+1]
                if temp:
                    self.parentItem().historyIndex += 1
                    self.parentItem().currentState = "session"
                    self.parentItem().timerCircle.currentTime = self.parentItem().timerCircle.sessionTime
                    self.parentItem().frame.changeBackground(temp)
                    print("History:", self.parentItem().imgHistory)
                # else:
                #     print("what")
                #     self.parentItem().historyIndex += 1
                #     self.parentItem().currentState = "session"
                #     self.parentItem().timerCircle.currentTime = self.parentItem().timerCircle.sessionTime
                #     nextImg = self.parentItem().timerCircle.getNextImg()
                #     self.parentItem().imgHistory[self.parentItem().historyIndex] = nextImg
                #     self.parentItem().frame.changeBackground(nextImg)
                self.parentItem().timerCircle.timer.start()
            # else:
                # self.parentItem().currentState = "session"
                # self.parentItem().timerCircle.currentTime = self.parentItem().timerCircle.sessionTime
                # nextImg = self.parentItem().timerCircle.getNextImg()
                # self.parentItem().imgHistory.pop(0)
                # self.parentItem().imgHistory.append(nextImg)
                # self.parentItem().frame.changeBackground(nextImg)
                # self.parentItem().timerCircle.timer.start()
        elif self.purpose == "random":
            if self.parentItem().randomState:
                self.parentItem().randomState = False
                self.innerText.setBrush(QColorConstants.Black)
                self.innerText.setPen(QColorConstants.Black)
            else:
                self.parentItem().randomState = True
                self.innerText.setBrush(QColorConstants.Gray)
                self.innerText.setPen(QColorConstants.Gray)
        elif self.purpose == "restart":
            self.parentItem().currentState = "session"
            self.parentItem().timerCircle.currentTime = self.parentItem().timerCircle.sessionTime
            self.parentItem().timerCircle.timer.start()
        elif self.purpose == "settings":
            self.parentItem().frame.handleSettings()
            #self.parentItem().frame.deleteItem(self.parentItem().frame.settingsRect)
            self.parentItem().timerCircle.timer.stop()
            self.parentItem().settingsWindow.show()

            
    
class TimerCircle(QGraphicsItemGroup):
    def __init__(self,x,y,r):
        super().__init__()
        outlineCircle = QGraphicsEllipseItem(x,y,r,r)
        outlineCircle.setPen(outlinePen)
        greenCircle = QGraphicsEllipseItem(x,y,r,r)
        greenCircle.setBrush(QColorConstants.DarkGreen)
        greenCircle.setPen(circlePen)
        redCircle = QGraphicsEllipseItem(x,y,r,r)
        redCircle.setBrush(QColorConstants.Red)
        redCircle.setPen(circlePen)

        tempText1 = QGraphicsSimpleTextItem("2:34")
        tempText1.setFont(QFont("TypeWriter", 15, 0, False))
        tempText1.setY(greenCircle.boundingRect().center().y() - tempText1.boundingRect().height()/2)
        tempText1.setX(greenCircle.boundingRect().center().x() - tempText1.boundingRect().width()/2)

        self.addToGroup(outlineCircle)
        self.addToGroup(greenCircle)
        self.addToGroup(redCircle)
        self.addToGroup(tempText1)
        self.tempText1 = tempText1

        self.greenCircle = greenCircle
        self.redCircle = redCircle
        self.center = (outlineCircle.boundingRect().x()+outlineCircle.boundingRect().width()/2, outlineCircle.boundingRect().y()+outlineCircle.boundingRect().height()/2)
        self.radius = outlineCircle.boundingRect().width()/2


        self.sessionTime = 3000
        self.breakTime = 1000
        self.currentTime = self.sessionTime
        self.interval = 50

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def restart_time(self):
        self.currentTime = self.sessionTime
        self.parentItem().currentState = "session"
        self.parentItem().debugState.setText("session")
        self.timer.start()
        self.repaint()

    def update_time(self):
        if self.currentTime >= self.interval:
            self.currentTime -= self.interval
            self.repaint()
        else:
            # changes of state here?
            match self.parentItem().currentState:
                case "session":
                    if self.breakTime > 0:
                        self.currentTime = self.breakTime
                        self.parentItem().currentState = "break"
                        self.parentItem().debugState.setText("break")
                    else:
                        self.currentTime = self.sessionTime
                        imgName = self.getNextImg()
                        #print(imgName)
                        self.parentItem().frame.imgName = imgName
                        self.parentItem().frame.changeBackground(imgName)
                        self.parentItem().addToHistory(imgName)
                        print("a", self.parentItem().images[self.parentItem().imgId])

                        # self.currentTime = self.sessionTime
                        # newImg = self.images[random.randint(0,len(self.parentItem().images)-1)]
                        # self.parentItem().addToHistory(self.parentItem().frame.imgName)
                        # self.parentItem().frame.changeBackground(newImg)

                        #self.parentItem().imgId = random.randint(0,len(self.parentItem().images)-1)
                        
                case "break":
                    self.currentTime = self.sessionTime
                    self.parentItem().currentState = "session"
                    self.parentItem().debugState.setText("session")

                    #self.parentItem().imgId = random.randint(0,len(self.parentItem().images)-1)
                    if self.parentItem().historyIndex == 0:
                        #print("a", self.parentItem().frame.imgName)
                        
                        #print(self.parentItem().imgHistory)
                        imgName = self.getNextImg()
                        #print(imgName)
                        self.parentItem().frame.imgName = imgName
                        self.parentItem().frame.changeBackground(imgName)
                        self.parentItem().addToHistory(imgName)
                        print("a", self.parentItem().images[self.parentItem().imgId])
                    else:
                        self.parentItem().historyIndex -= 1
                        imgName = self.parentItem().imgHistory[self.parentItem().historyIndex]
                        self.parentItem().frame.imgName = imgName
                        self.parentItem().frame.changeBackground(imgName)
                        


                    

                    


    def testFunct(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def repaint(self):
        #print(int(time*1000))
        time = self.currentTime
        if self.parentItem().currentState == "session":
            fullTime = self.sessionTime
        else:
            fullTime = self.breakTime
        
        angle = int(5760 * (self.currentTime/fullTime))

        self.greenCircle.setStartAngle(1440)
        self.greenCircle.setSpanAngle(angle)

        self.redCircle.setStartAngle(1440)
        self.redCircle.setSpanAngle(-5760+angle)

        remaining = int(time/1000)
        (minutes, seconds) = (math.floor(remaining/60), (remaining % 60))
        if len(str(seconds)) == 1:
            seconds = "0" + str(seconds)
        clockText = str(minutes) + ":" + str(seconds)

        self.tempText1.setText(clockText)
        # self.greenCircle.setSpanAngle(int(time))
        # self.redCircle.setStartAngle(int(time))
        # self.redCircle.setSpanAngle(5760 - int(time))

    def getNextImg(self):
        print("H", self.parentItem().imgHistory)
        if self.parentItem().randomState:
            tempList = list(set(self.parentItem().images) - set(self.parentItem().imgHistory))
            if len(tempList) == 0:
                # with this, it will choose from the last 25% of the imgHistory (rounded up)
                t = math.ceil(len(self.parentItem().imgHistory) * .25)
                print(t)
                t2 = random.randint(1,t)

                tempImg = self.parentItem().imgHistory[-t2]
                tempId = self.parentItem().images.index(tempImg)
                self.parentItem().imgId = tempId
            else:
                tempId = random.randint(0,len(tempList)-1)
                self.parentItem().imgId = self.parentItem().images.index(tempList[tempId])
        else:
            self.parentItem().imgId += 1
            if self.parentItem().imgId >= len(self.parentItem().images):
                self.parentItem().imgId = 0
        imgName = self.parentItem().images[self.parentItem().imgId]
        return imgName

        
    #def __init__(self, x, y, r):
    #    super().__init__(x, y, r, r)
    #    self.setBrush(QColorConstants.DarkGreen)
    #    tempPen = QPen()
    #    tempPen.setWidth(8)
    #    self.setPen(tempPen)

    #def paint(self, painter=None, style=None, widget=None):
    #    painter.fillRect(self, menuBrush.color())


    #tempCircle = QGraphicsEllipseItem(x+((menu_width-66)/2), y-((66-menu_height)/2), 66, 66)

class SettingsWindow(QWidget):
    def __init__(self, qm):
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

        self.qm = qm

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.sessionTimeInput.setText(str(int(self.qm.timerCircle.sessionTime/1000)))
        self.breakTimeInput.setText(str(int(self.qm.timerCircle.breakTime/1000)))
        self.historyInput.setText(str(len(self.qm.imgHistory)))
        
        self.saveButton.setText("Saved ✓")


        return super().showEvent(a0)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.qm.timerCircle.timer.start()

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
            if self.sw.sessionTimeInput.text().isdigit():
                tempSession = int(self.sw.sessionTimeInput.text())
            else:
                return
            if self.sw.breakTimeInput.text().isdigit():
                tempBreak = int(self.sw.breakTimeInput.text())
            else:
                return
            if self.sw.historyInput.text().isdigit():
                tempHistory = int(self.sw.historyInput.text())
            else:
                return
            if tempSession > 0 and tempBreak > 0 and tempHistory >= 0:
                self.qm.timerCircle.sessionTime = tempSession * 1000
                self.qm.timerCircle.breakTime = tempBreak * 1000
                self.qm.historySize = tempHistory
                self.qm.resetHistory()
                self.qm.timerCircle.currentState = "session"
                self.qm.timerCircle.currentTime = self.qm.timerCircle.sessionTime
                self.sw.saveButton.setText("Saved ✓")
        elif a0.key() == Qt.Key.Key_Escape:
            self.sw.close()


        # match self.purpose:
        #     case "sessionTime":
        #         if a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter:
        #             if self.text().isdigit():
        #                 temp = int(self.text())
        #                 if temp > 0:
        #                     print("changing sessionTime")
        #                     self.qm.timerCircle.sessionTime = temp * 1000
        #                     self.qm.timerCircle.currentState = "session"
        #                     self.qm.timerCircle.currentTime = temp * 1000
        #     case "breakTime":
        #         if a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter:
        #             if self.text().isdigit():
        #                 temp = int(self.text())
        #                 if temp >= 0:
        #                     print("changing breakTime")
        #                     self.qm.timerCircle.breakTime = temp * 1000
        #                     self.qm.timerCircle.currentState = "session"
        #                     self.qm.timerCircle.currentTime = self.qm.timerCircle.sessionTime
        #     case "history":
        #         if a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter:
        #             if self.text().isdigit():
        #                 temp = int(self.text())
        #                 if temp > 0:
        #                     print("changing history. nice")
        #                     self.qm.historySize = temp
        #                     self.qm.resetHistory()
        return super().keyReleaseEvent(a0)
    
    def checkInputs(self):
        #print(self.sw.historyInput.text() == str(len(self.qm.imgHistory)))
        return self.sw.sessionTimeInput.text() == str(int(self.qm.timerCircle.sessionTime/1000)) and self.sw.breakTimeInput.text() == str(int(self.qm.timerCircle.breakTime/1000)) and self.sw.historyInput.text() == str(len(self.qm.imgHistory))
    
class SettingsButton(QPushButton):
    def __init__(self, purpose, sw, qm):
        self.sw = sw
        self.purpose = purpose
        self.qm = qm
        super().__init__(str.capitalize(purpose))