
from timerCircle import *

menu_width = 252
menu_height = 77
randomOffColor = QColor(60,60,60)
randomOnHoverColor = QColor(50,50,50)

class QuickMenu(QGraphicsItemGroup):
    def __init__(self,window_width, window_height, x, y, session_length, break_length, history_size, random_state, directory, history, frame):
        super().__init__()

        # what
        self.frame = frame
        self.currentState = "session"
        if random_state == "True":
            self.randomState = True
        else:
            self.randomState = False

        self.freshlyPressed = False

        # Drawing the background
        backgroundRect = QGraphicsRectItem(0,0,249,74)
        backgroundRect.setVisible(False)
        tempRect1 = QGraphicsRectItem(0,20,17,17) # left square
        tempRect1.setBrush(0)
        tempRect2 = QGraphicsRectItem(18,10,214,37) # middle rect
        tempRect2.setBrush(0)
        tempRect3 = QGraphicsRectItem(230,20,7,7) # right square
        tempRect3.setBrush(0)
        tempCircle1 = QGraphicsEllipseItem(0,10,37,37)
        tempCircle1.setBrush(0)
        tempCircle2 = QGraphicsEllipseItem(0,10,20,20)
        tempCircle2.setBrush(0)
        tempCircle3 = QGraphicsEllipseItem(212,10,37,37)
        tempCircle3.setBrush(0)
        tempCircle4 = QGraphicsEllipseItem(207,10,20,20)
        tempCircle4.setBrush(0)
        self.addToGroup(backgroundRect)
        
        self.images = False
        self.historySize = history_size
        self.historyIndex = 0

        self.painter = QPainter()

        if directory != None and os.path.exists(directory):
            self.directory = directory
            self.images = buildDirStructure(directory)

            if history:
                self.imgHistory = history
                imgName = history[0]
                self.frame.imgName = imgName
                self.frame.changeBackground(imgName)
                self.imgId = self.images.index(imgName)

            else:
                self.imgId = -1
                self.resetHistory()
                imgName = self.images[self.imgId]

                self.frame.imgName = imgName
                self.frame.changeBackground(imgName)
                self.imgHistory[0] = self.frame.imgName
        else:
            self.directory = None
            self.images = None
            self.imgId = -1

        print(self.images)

        # Elements of UI: six buttons and the timer circle
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

        self.settingsWindow = SettingsWindow(self, self.frame.x(), self.frame.y())
    
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
    
        updated_pos_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_pos_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        self.x_pos = updated_pos_x
        self.y_pos = updated_pos_y
        self.setX(updated_pos_x)
        self.setY(updated_pos_y)

        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.reposition()
        if self.freshlyPressed:
            if (self.buttonRandom.buttonRect.contains(event.pos())):
                self.buttonRandom.pressed()
            elif (self.buttonRestart.buttonRect.contains(event.pos())):
                self.buttonRestart.pressed()
            elif (self.buttonLeft.buttonRect.contains(event.pos())):
                self.buttonLeft.pressed()
            elif (self.buttonRight.buttonRect.contains(event.pos())):
                self.buttonRight.pressed()
            elif (self.buttonDirectory.buttonRect.contains(event.pos())):
                self.buttonDirectory.pressed()
            elif (self.buttonSettings.buttonRect.contains(event.pos())):
                self.buttonSettings.pressed()
            elif (self.timerCircle.boundingRect().contains(event.pos())):
                # checks if the cursor is really in the circle. totally worth it
                if self.timerCircle.radius >= math.sqrt(abs((self.timerCircle.center[0] - event.pos().x())**2 + abs((self.timerCircle.center[1] - event.pos().y())**2))):
                    self.timerCircle.timerPressed()
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
        for i in range(tempSize):
            tempArray.append(False)
        print(self.frame.imgName)
        tempArray[0] = self.frame.imgName

        self.imgHistory = tempArray
        self.historyIndex = 0

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


    def pressed(self):
        if (self.parentItem().directory == None and not (self.purpose == "directory" or self.purpose == "settings" or self.purpose == "random")):
            print("What")
            return
        print(self.purpose, "has been pressed")
        if self.purpose == "directory":
            self.fresh_change = True
            self.parentItem().timerCircle.timer.stop()
            testName = QFileDialog.getExistingDirectory()
            print("Test name: " + testName)
            filesArray = buildDirStructure(testName)
            if filesArray:
                self.parentItem().directory = testName
                self.parentItem().images = filesArray
                print("new dir: " + testName)
                self.parentItem().currentState = "break"
                self.parentItem().timerCircle.currentTime = 0
                self.parentItem().resetHistory()
                if self.parentItem().randomState == True:
                    self.parentItem().imgId = random.randint(0,len(filesArray))
                else:                
                    self.parentItem().imgId = -1
                self.parentItem().timerCircle.timer.start()
                self.innerText.setPen(QColorConstants.Gray)
                self.innerText.setBrush(QColorConstants.Gray)
            else:
                print("Dir:", self.parentItem().directory)
                if self.parentItem().directory != None:
                    self.parentItem().timerCircle.timer.start()
        elif self.purpose == "right":
            self.parentItem().currentState = "break"
            self.parentItem().timerCircle.currentTime = 0
            self.parentItem().timerCircle.timer.start()
        elif self.purpose == "left":
            if self.parentItem().historyIndex < len(self.parentItem().imgHistory) - 1:
                temp = self.parentItem().imgHistory[self.parentItem().historyIndex+1]
                if temp:
                    self.parentItem().historyIndex += 1
                    self.parentItem().currentState = "session"
                    self.parentItem().timerCircle.currentTime = self.parentItem().timerCircle.sessionTime
                    self.parentItem().frame.changeBackground(temp)
                    print("History:", self.parentItem().imgHistory)
                self.parentItem().timerCircle.timer.start()
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
            self.parentItem().timerCircle.timer.stop()
            self.parentItem().settingsWindow.show()