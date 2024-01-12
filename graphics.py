import sys
import typing
from PyQt6 import QtGui
from PyQt6.QtGui import QActionEvent, QCloseEvent, QEnterEvent, QFocusEvent, QKeyEvent, QMouseEvent, QPainter, QShowEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QRectF, pyqtSlot, Qt, QPointF, QSize
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget
from logic import * # ?
import math
import random
import pillow_avif
from PIL import Image
import math

# ⭝ ⭜ 

# some constants
menu_width = 252
menu_height = 77
outlinePen = QPen()
outlinePen.setWidth(3)
circlePen = QPen()
circlePen.setWidth(0)
# this solution is fucking cursed. setting a color as a brush?
# then what is the point of a brush object?
menuBrush = QColor(0,0,0)
randomOffColor = QColor(60,60,60)
randomOnHoverColor = QColor(50,50,50)

class QuickMenu(QGraphicsItemGroup):
    def __init__(self,window_width, window_height, x, y, session_length, break_length, history_size, random_state, directory, history, frame): # possibly more...?
        super().__init__()
        #self.setPos(x,y)

        # what
        self.frame = frame
        self.currentState = "session"
        if random_state == "True":
            self.randomState = True
        else:
            self.randomState = False

        # is there another way to check if the menu has been moved?
        # most likely yes. oh whatever
        self.freshlyPressed = False

        # Drawing the background
        backgroundRect = QGraphicsRectItem(0,0,249,74)
        backgroundRect.setVisible(False)
        tempRect1 = QGraphicsRectItem(0,20,17,17) # left square
        tempRect1.setBrush(menuBrush)
        tempRect2 = QGraphicsRectItem(18,10,214,37) # middle rect
        tempRect2.setBrush(menuBrush)
        tempRect3 = QGraphicsRectItem(230,20,7,7) # right square
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
        #self.addToGroup(tempRect2)
        self.addToGroup(backgroundRect)
        #self.addToGroup(tempRect3)
        #self.addToGroup(tempCircle1)
        #self.addToGroup(tempCircle2)
        #self.addToGroup(tempCircle3)
        #self.addToGroup(tempCircle4)

        # !!!
        self.images = False
        self.historySize = history_size
        self.historyIndex = 0


        self.painter = QPainter()

        if directory != None:
            self.directory = directory
            self.images = buildDirStructure(directory)
            #print(self.images)
            #self.imgId = random.randint(0,len(self.images)-1) # !!! fix

            if history:
                #print(history)
                self.imgHistory = history
                imgName = history[0]
                self.frame.imgName = imgName
                self.frame.changeBackground(imgName)
                self.imgId = self.images.index(imgName)

            else:
                self.imgId = -1
                self.resetHistory()
                # if self.randomState:
                #     self.imgId = random.randint(0,len(self.images)-1)
                # else:
                #     print("Setting imgId to 0")
                #     self.imgId = 0
                imgName = self.images[self.imgId]

                self.frame.imgName = imgName
                self.frame.changeBackground(imgName)
                self.imgHistory[0] = self.frame.imgName
        else:
            # guess it wasn't that bad of a todo after all
            self.directory = None
            self.images = None
            self.imgId = -1


        # Elements of UI: four buttons and the timer circle
        # positions: hardcode? menu size is going to be fixed anyways
        buttonRandom = TestButton(7,23,27,27, "random", self.randomState)
        buttonRestart = TestButton(39,23,27,27, "restart", None)
        buttonLeft = TestButton(71,23,16,27,"left", None)
        buttonRight = TestButton(162,23,16,27, "right", None)
        buttonDirectory = TestButton(183,23,27,27, "directory", None)
        buttonSettings = TestButton(215,23,27,27, "settings", None)
        timerCircle = TimerCircle(88,0,74, session_length, break_length, self)

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
        self.win_width = window_width
        self.win_height = window_height
        self.x_pos = x
        self.y_pos = y

        self.moveBy(x,y)


        # here? is it a good solution?
        self.settingsWindow = SettingsWindow(self)


    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        #print(event.pos())
        return
        if (self.buttonRandom.buttonRect.contains(event.pos())):
            self.buttonRandom.hoverOn()
        elif (self.buttonRestart.buttonRect.contains(event.pos())):
            self.buttonRestart.hoverOn()
        elif (self.buttonLeft.buttonRect.contains(event.pos())):
            self.buttonLeft.hoverOn()
        elif (self.buttonRight.buttonRect.contains(event.pos())):
            self.buttonRight.hoverOn()
        elif (self.buttonDirectory.buttonRect.contains(event.pos())):
            self.buttonDirectory.hoverOn()
        elif (self.buttonSettings.buttonRect.contains(event.pos())):
            self.buttonSettings.hoverOn()
        return super().hoverEnterEvent(event)
    
    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        if (self.buttonRandom.buttonRect.contains(event.pos())):
            self.buttonRandom.hoverFunct()
        elif (self.buttonRestart.buttonRect.contains(event.pos())):
            self.buttonRestart.hoverFunct()
        elif (self.buttonLeft.buttonRect.contains(event.pos())):
            self.buttonLeft.hoverFunct()
        elif (self.buttonRight.buttonRect.contains(event.pos())):
            self.buttonRight.hoverFunct()
        elif (self.buttonDirectory.buttonRect.contains(event.pos())):
            self.buttonDirectory.hoverFunct()
        elif (self.buttonSettings.buttonRect.contains(event.pos())):
            self.buttonSettings.hoverFunct()
        else:
            self.buttonRandom.hoverOff()
            self.buttonRestart.hoverOff()
            self.buttonLeft.hoverOff()
            self.buttonRight.hoverOff()
            self.buttonDirectory.hoverOff()
            self.buttonSettings.hoverOff()

        return super().hoverMoveEvent(event)
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if (self.buttonRandom.buttonRect.contains(event.pos())):
            self.buttonRandom.hoverOff()
        elif (self.buttonRestart.buttonRect.contains(event.pos())):
            self.buttonRestart.hoverOff()
        elif (self.buttonLeft.buttonRect.contains(event.pos())):
            self.buttonLeft.hoverOff()
        elif (self.buttonRight.buttonRect.contains(event.pos())):
            self.buttonRight.hoverOff()
        elif (self.buttonDirectory.buttonRect.contains(event.pos())):
            self.buttonDirectory.hoverOff()
        elif (self.buttonSettings.buttonRect.contains(event.pos())):
            self.buttonSettings.hoverOff()
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

        self.x_pos = updated_pos_x
        self.y_pos = updated_pos_y
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
        if (self.pos().x() > self.frame.width()-menu_width):
            self.setX(self.frame.width()-menu_width)
        if (self.pos().y() > self.frame.height()-menu_height):
            self.setY(self.frame.height()-menu_height)

    def addToHistory(self, new):
        self.imgHistory.insert(0,new)
        self.imgHistory.pop()

    def resetHistory(self):
        tempArray = []

        tempSize = min(self.historySize, len(self.images))
        for i in range(tempSize): # how much, exactly?
            tempArray.append(False)
        print(self.frame.imgName)
        tempArray[0] = self.frame.imgName

        self.imgHistory = tempArray
        self.historyIndex = 0

    # maybe not needed
    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColorConstants.Black)
        painter.setPen(QColorConstants.Gray)
        painter.drawEllipse(0,18,38,38)
        painter.drawEllipse(212,18,38,38)

        painter.setPen(QColorConstants.Black)
        painter.drawRect(20,18,212,38)

        painter.setPen(QColorConstants.Gray)
        painter.drawLine(20,18,232,18)
        painter.drawLine(20,56,232,56)

        
        
        return super().paint(painter, option, widget)


class ImgFrame(QGraphicsView):
    def __init__(self, x, y, width, height):
        super().__init__()

        
        self.myScene = QGraphicsScene()
        self.setScene(self.myScene)
        self.myScene.setSceneRect(0,0,width,height)
        self.myScene.setBackgroundBrush(QColor(200,220,200))
        self.backgroundPixmap = None
        self.move(x,y)

        pen = QColor(100,100,100)
        brush = QColor(150,150,150)

        pixmap = QPixmap()
        pixmap2 = QGraphicsPixmapItem()
        pixmap = pixmap.scaled(width,
                               height,
                               Qt.AspectRatioMode.KeepAspectRatio)
        pixmap2.setPixmap(pixmap)
        self.pixmap2 = pixmap2
        self.fullPixmap = None
        self.scene().addItem(pixmap2)

        breakMask = QGraphicsRectItem(0,0,width,height)
        breakMask.setPen(QColor(0,0,0,0))
        breakMask.setBrush(QColor(0,0,0,150))
        
        self.breakMask = breakMask
        self.scene().setBackgroundBrush(0)
        self.imgName = ""

        self.itemGroup = QGraphicsItemGroup
        self.scene().addItem(breakMask)

        # why even
        if width > 1706 or height > 720:
            print("but whyyyy")
            # why. why even does it fix the issue. what the absolute fuck
            
        self.resize(QSize(width, height))


    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        if self.fullPixmap == None:
            if self.imgName[-4:] == "avif":
                print("it's an avif")
                #self.imgName = tempImgName

                # phew, almost done it VERY suboptimally
                pixmap = QPixmap(os.getcwd() + "/temp.jpg")
            else:
                pixmap = QPixmap(self.imgName)

            self.fullPixmap = pixmap

        #print(event.size())
        size = event.size()
        

        #target_size = min(size.width(), size.height()) - 1
        #x = (size.width() - target_size) // 2
        #y = (size.height() - target_size) // 2
        #self.circle.setRect(x,y,target_size,target_size)
        #print("S", size.width(), size.height())
        self.setSceneRect(0,0,size.width(),size.height())
        self.breakMask.setRect(0,0,size.width(),size.height())
        self.quickMenu.reposition()
        #self.quickMenu.moveBy(tempXmove, tempYmove)
        #self.item.win_width = size.width() !!!
        #self.item.win_height = size.height() !!!

        #self.changeBackground(self.scene().
        
        # if self.imgName[-4:] == "avif":
        #     print("it's an avif")
        #     #self.imgName = tempImgName

        #     # phew, almost done it VERY suboptimally
        #     pixmap = QPixmap(os.getcwd() + "/temp.jpg")
        # else:
        #     pixmap = QPixmap(self.imgName)

        #print(pixmap.width(), pixmap.height())
        #pixmap = pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio)
        #print(self.pixmap2.scale())
        self.pixmap2.setPixmap(self.fullPixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))
        self.pixmap2.setPos((size.width()-self.pixmap2.boundingRect().width()) / 2, (size.height() - self.pixmap2.boundingRect().height()) / 2)

    def keyReleaseEvent(self, event: QKeyEvent | None) -> None:
        if self.quickMenu.directory == None and (event.key() in [Qt.Key.Key_Space, Qt.Key.Key_T, Qt.Key.Key_Left, Qt.Key.Key_Right]):
            return

        match event.key():
            case Qt.Key.Key_Space:
                if self.quickMenu.currentState == "session" and self.quickMenu.frame.breakMask.isVisible():
                    self.quickMenu.frame.breakMask.setVisible(False)

                if self.quickMenu.timerCircle.timer.isActive():
                    self.quickMenu.timerCircle.timer.stop()
                else:
                    self.quickMenu.timerCircle.timer.start()

            case Qt.Key.Key_R:
                self.quickMenu.buttonRandom.testFunct()
            case Qt.Key.Key_T:
                self.quickMenu.buttonRestart.testFunct()
            case Qt.Key.Key_Left:
                self.quickMenu.buttonLeft.testFunct()
            case Qt.Key.Key_Right:
                self.quickMenu.buttonRight.testFunct()
            case Qt.Key.Key_F:
                self.quickMenu.buttonDirectory.testFunct()
            case Qt.Key.Key_S:
                self.quickMenu.buttonSettings.testFunct()
        return super().keyReleaseEvent(event)

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
        #self.backgroundPixmap = pixmap
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
        
        print(self.quickMenu.historyIndex)

        if os.path.exists(os.getcwd() + "/temp.jpg"):
            os.remove(os.getcwd() + "/temp.jpg")

        # write config.txt
        tempConfig = ""
        tempConfig += str(self.width()) + "\n" + str(self.height()) + "\n" + str(self.pos().x()) + "\n" + str(self.pos().y()) + "\n" + str(int(self.quickMenu.pos().x())) + "\n" + str(int(self.quickMenu.pos().y())) + "\n" + str(int(self.quickMenu.timerCircle.sessionTime/1000)) + "\n" + str(int(self.quickMenu.timerCircle.breakTime/1000)) + "\n" + str(len(self.quickMenu.imgHistory)) + "\n" + str(self.quickMenu.randomState) + "\n" + self.quickMenu.directory
        for item in self.quickMenu.imgHistory:
            tempConfig += "\n" + str(item)

        #print(tempConfig)
        with open("config.txt", "w") as file:
            file.write(tempConfig)

        return super().closeEvent(a0)


def renderImgFrame(x,y,width,height):
    tempImgFrame = ImgFrame(x,y,width,height)

    return tempImgFrame


def renderQuickMenu(window_width, window_height, menu_position_x, menu_position_y, session_length, break_length, history_size, random_state, directory, history, frame):
    tempMenu = QuickMenu(window_width, window_height, menu_position_x, menu_position_y, session_length, break_length, history_size, random_state, directory, history, frame)

    return tempMenu

class TestButton(QGraphicsItemGroup):
    def __init__(self,x,y,w,h,purpose, flag):
        super().__init__()
        self.purpose = purpose
        tempRect = QGraphicsRectItem(x,y,w,h)
        tempRect.setBrush(QColorConstants.Black)
        innerText = QGraphicsSimpleTextItem()
        innerText.setFont(QFont("TypeWriter", 20,800, False))
        innerText.setPen(QColorConstants.Gray)
        innerText.setBrush(QColorConstants.Gray)
        self.innerText = innerText

        if purpose == "directory":
            self.fresh_change = False
        
        # that's important to initializing! ...?
        if self.purpose == "random" and not flag:
            innerText.setPen(randomOffColor)
            innerText.setBrush(randomOffColor)

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
        
        # hmmm
        innerText.setY(tempRect.boundingRect().center().y() - innerText.boundingRect().height()/2)
        innerText.setX(tempRect.boundingRect().center().x() - innerText.boundingRect().width()/2)
        if purpose == "left":
            innerText.setY(innerText.y() - 2)
            innerText.setX(innerText.x() + 3)
        if purpose == "right":
            innerText.setY(innerText.y() - 2)
            innerText.setX(innerText.x() + 1)
    
    def hoverFunct(self):
        if not (self.purpose == "random" and not self.parentItem().randomState):
            self.innerText.setPen(QColorConstants.DarkGray)
            self.innerText.setBrush(QColorConstants.DarkGray)
        else:
            self.innerText.setPen(randomOnHoverColor)
            self.innerText.setBrush(randomOnHoverColor)
        if self.purpose == "directory" and self.fresh_change:
            self.innerText.setPen(QColorConstants.Gray)
            self.innerText.setBrush(QColorConstants.Gray)
            self.fresh_change = False

    def hoverOff(self):
        #print(self.purpose, "2")
        if self.purpose == "random":
            if self.parentItem().randomState:
                self.innerText.setPen(QColorConstants.Gray)
                self.innerText.setBrush(QColorConstants.Gray)
            else:
                self.innerText.setPen(randomOffColor)
                self.innerText.setBrush(randomOffColor)
        else:
            self.innerText.setPen(QColorConstants.Gray)
            self.innerText.setBrush(QColorConstants.Gray)
        if self.purpose == "directory":
            self.innerText.setPen(QColorConstants.Gray)
            self.innerText.setBrush(QColorConstants.Gray)


    def testFunct(self):
        if (self.parentItem().directory == None and not (self.purpose == "directory" or self.purpose == "settings" or self.purpose == "random")):
            print("What")
            return
        print(self.purpose, "has been pressed")
        if self.purpose == "directory":
            self.fresh_change = True
            self.parentItem().timerCircle.timer.stop()
            testName = QFileDialog.getExistingDirectory()
            # Why the hell was the line below there?
            #self.parentItem().timerCircle.timer.start()
            # this is supposed to return an array, with all the items?
            filesArray = buildDirStructure(testName)
            if filesArray:
                self.parentItem().directory = testName
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
                self.innerText.setPen(QColorConstants.Gray)
                self.innerText.setBrush(QColorConstants.Gray)
                #self.hoverOff()
            else:
                print("Dir:", self.parentItem().directory)
                if self.parentItem().directory != None:
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
                self.innerText.setBrush(randomOffColor)
                self.innerText.setPen(randomOffColor)
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
    def __init__(self,x,y,r, session_length, break_length, qm):
        super().__init__()
        self.setParentItem(qm)
        # for some reason, using QPen width as a border is kind of janky
        backgroundRect = QGraphicsRectItem(x,y,r,r)
        backgroundRect.setVisible(False)

        borderCircle = QGraphicsEllipseItem(x-1,y-1,r+2,r+2)
        borderCircle.setPen(0)
        borderCircle.setBrush(0)
        outlineCircle = QGraphicsEllipseItem(x,y,r,r)
        outlineCircle.setPen(0)
        outlineCircle.setBrush(QColorConstants.LightGray)
        # greenCircle = QGraphicsEllipseItem(x,y,r,r)
        # greenCircle.setBrush(QColorConstants.DarkGreen)
        # greenCircle.setPen(circlePen)
        # redCircle = QGraphicsEllipseItem(x,y,r,r)
        # redCircle.setBrush(QColorConstants.Red)
        # redCircle.setPen(circlePen)
        outerCircle = QGraphicsEllipseItem(x+4,y+4,r-8,r-8)
        outerCircle.setBrush(0)
        innerCircle = QGraphicsEllipseItem(x+8,y+8,r-16,r-16)
        innerCircle.setBrush(QColorConstants.LightGray)
        innerCircle.setPen(QColorConstants.LightGray)
        self.x_pos = x
        self.y_pos = y
        self.r = r


        tempText1 = QGraphicsSimpleTextItem("2:34") # !!! fix
        tempText1.setFont(QFont("TypeWriter", 15, 0, False))
        tempText1.setY(outlineCircle.boundingRect().center().y() - tempText1.boundingRect().height()/2)
        tempText1.setX(outlineCircle.boundingRect().center().x() - tempText1.boundingRect().width()/2)

        #self.addToGroup(borderCircle)
        #self.addToGroup(outlineCircle)
        #self.addToGroup(outerCircle)
        #self.addToGroup(innerCircle)
        self.addToGroup(tempText1)
        self.addToGroup(backgroundRect)
        self.tempText1 = tempText1

        self.outlineCircle = outlineCircle
        self.outerCircle = outerCircle
        self.innerCircle = innerCircle
        self.outerCircle.setStartAngle(1440)
        self.center = (outlineCircle.boundingRect().x()+outlineCircle.boundingRect().width()/2, outlineCircle.boundingRect().y()+outlineCircle.boundingRect().height()/2)
        self.radius = outlineCircle.boundingRect().width()/2

        self.sessionTime = session_length * 1000
        self.breakTime = break_length * 1000
        self.currentTime = self.sessionTime - 50
        self.interval = 50

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_time)

        self.repaint()
        #if self.parentItem().images:
        #    self.timer.start()

    def restart_time(self):
        self.currentTime = self.sessionTime
        self.parentItem().currentState = "session"
        self.timer.start()
        #self.repaint()

    def update_time(self):
        if self.currentTime >= self.interval:
            self.currentTime -= self.interval
            self.repaint()
            self.update()
        else:
            # changes of state here?
            match self.parentItem().currentState:
                case "session":
                    if self.breakTime > 0:
                        self.currentTime = self.breakTime
                        self.parentItem().currentState = "break"
                        self.parentItem().frame.breakMask.setVisible(True)
                    else:
                        #print("No break, restarting session")
                        self.currentTime = self.sessionTime
                        imgName = self.getNextImg()
                        #print(imgName)
                        self.parentItem().frame.imgName = imgName
                        
                        # what
                        self.parentItem().frame.fullPixmap = QPixmap(imgName)


                        self.parentItem().frame.changeBackground(imgName)
                        self.parentItem().addToHistory(imgName)
                        #print("a", self.parentItem().images[self.parentItem().imgId])

                        # self.currentTime = self.sessionTime
                        # newImg = self.images[random.randint(0,len(self.parentItem().images)-1)]
                        # self.parentItem().addToHistory(self.parentItem().frame.imgName)
                        # self.parentItem().frame.changeBackground(newImg)

                        #self.parentItem().imgId = random.randint(0,len(self.parentItem().images)-1)
                        
                case "break":
                    self.parentItem().frame.breakMask.setVisible(False)
                    self.currentTime = self.sessionTime
                    self.parentItem().currentState = "session"


                    #self.parentItem().imgId = random.randint(0,len(self.parentItem().images)-1)
                    if self.parentItem().historyIndex == 0:
                        #print("a", self.parentItem().frame.imgName)
                        
                        #print(self.parentItem().imgHistory)
                        imgName = self.getNextImg()
                        print(imgName)
                        self.parentItem().frame.imgName = imgName
                        self.parentItem().frame.changeBackground(imgName)
                        self.parentItem().addToHistory(imgName)
                        
                        #print("a", self.parentItem().images[self.parentItem().imgId])
                    else:
                        self.parentItem().historyIndex -= 1
                        imgName = self.parentItem().imgHistory[self.parentItem().historyIndex]
                        self.parentItem().frame.imgName = imgName
                        
                        self.parentItem().frame.changeBackground(imgName)
                    self.parentItem().frame.fullPixmap = QPixmap(imgName)
                        
                        


                    

                    


    def testFunct(self):
        if self.parentItem().currentState == "break":
            self.parentItem().frame.breakMask.setVisible(True)
        else:
            self.parentItem().frame.breakMask.setVisible(False)
            print("Hola")
    
        # well, more shit to refactor
        if self.parentItem().directory == None:
            return

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

        self.outerCircle.setSpanAngle(angle)

        remaining = int(time/1000) + 1
        (minutes, seconds) = (math.floor(remaining/60), (remaining % 60))
        if len(str(seconds)) == 1:
            seconds = "0" + str(seconds)
        clockText = str(minutes) + ":" + str(seconds)

        self.tempText1.setText(clockText)
        self.tempText1.setY(self.outlineCircle.boundingRect().center().y() - self.tempText1.boundingRect().height()/2)
        self.tempText1.setX(self.outlineCircle.boundingRect().center().x() - self.tempText1.boundingRect().width()/2)
        # self.greenCircle.setSpanAngle(int(time))
        # self.redCircle.setStartAngle(int(time))
        # self.redCircle.setSpanAngle(5760 - int(time))

    def getNextImg(self):
        #print("H", self.parentItem().imgHistory)
        #print("R", self.parentItem().images)
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
                # what the fuck
                tempId = random.randint(0,len(tempList)-1)
                self.parentItem().imgId = self.parentItem().images.index(tempList[tempId])
        else:
            print(self.parentItem().imgId)
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


    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        if self.parentItem().currentState == "session":
            fullTime = self.sessionTime
        else:
            fullTime = self.breakTime
        
        angle = int(5760 * (self.currentTime/fullTime)) - 100

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColorConstants.Black)
        painter.drawEllipse(self.x_pos,self.y_pos,self.r,self.r) # border circle

        # maybe here?
        if self.parentItem().currentState == "session":
            painter.setBrush(QColorConstants.LightGray)
        else:
            painter.setBrush(QColor(250,215,160))
        painter.drawEllipse(self.x_pos+1,self.y_pos+1,self.r-2,self.r-2) # outer circle
        tempPen = QPen(QColorConstants.Black)
        tempPen.setWidth(5)
        painter.setPen(tempPen)
        # (x+4,y+4,r-8,r-8)
        if angle < 50 :
            tempAngle = 50
        else:
            tempAngle = angle
        painter.drawArc(self.x_pos+6,self.y_pos+6,self.r-12,self.r-12, 1440,tempAngle-50)

        painter.setPen(QColorConstants.Black)
        painter.setBrush(QColorConstants.Black)
        painter.drawEllipse(self.x_pos + int(self.r / 2), self.y_pos + 4,4,4)
        origin_x = self.x_pos + self.r/2 - 2
        origin_y = self.y_pos + self.r/2 - 2

        theta = angle / 5760 * 2 * math.pi + (math.pi / 2)
        
        #theta -= math.pi/4
        painter.setBrush(QColorConstants.Black)
        #print(math.cos(theta), math.sin(theta))
        painter.drawEllipse(int(origin_x + math.cos(theta) * (self.r/2-6)), int(origin_y - math.sin(theta) * (self.r/2-6)), 5, 5)

        return super().paint(painter, option, widget)

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
        if self.qm.directory != None:
            self.historyInput.setText(str(len(self.qm.imgHistory)))
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)
        
        self.saveButton.setText("Saved ✓")


        return super().showEvent(a0)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.qm.directory != None:
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
            if self.qm.directory == None:
                return

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
            if tempSession > 0 and tempBreak >= 0 and tempHistory > 0:
                self.qm.timerCircle.currentTime = tempSession * 1000
                self.qm.timerCircle.sessionTime = tempSession * 1000
                self.qm.timerCircle.breakTime = tempBreak * 1000
                self.qm.historySize = tempHistory
                if len(self.qm.imgHistory) != tempHistory:
                    self.qm.resetHistory()
                self.qm.timerCircle.parentItem().currentState = "session"
                self.sw.saveButton.setText("Saved ✓")

                # why
        elif a0.key() == Qt.Key.Key_Escape:
            self.sw.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        #self.qm.timerCircle.update()

        return super().closeEvent(a0)


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
        if self.qm.directory == None:
            return self.sw.sessionTimeInput.text() == str(int(self.qm.timerCircle.sessionTime/1000)) and self.sw.breakTimeInput.text() == str(int(self.qm.timerCircle.breakTime/1000))
        else:
            #print(self.sw.historyInput.text() == str(len(self.qm.imgHistory)))
            return self.sw.sessionTimeInput.text() == str(int(self.qm.timerCircle.sessionTime/1000)) and self.sw.breakTimeInput.text() == str(int(self.qm.timerCircle.breakTime/1000)) and self.sw.historyInput.text() == str(len(self.qm.imgHistory))
    
class SettingsButton(QPushButton):
    def __init__(self, purpose, sw, qm):
        self.sw = sw
        self.purpose = purpose
        self.qm = qm
        super().__init__(str.capitalize(purpose))

    def mouseReleaseEvent(self, e: QMouseEvent | None) -> None:
        # for a bit later
        print(self.purpose)
        return super().mouseReleaseEvent(e)