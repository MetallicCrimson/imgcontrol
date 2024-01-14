from PyQt6.QtCore import QTimer
from logic import * # ?
from settingsWindow import *

class TimerCircle(QGraphicsItemGroup):
    def __init__(self,x,y,r, session_length, break_length, qm):
        super().__init__()
        self.setParentItem(qm)
        backgroundRect = QGraphicsRectItem(x,y,r,r)
        backgroundRect.setVisible(False)

        outlineCircle = QGraphicsEllipseItem(x,y,r,r)
        outlineCircle.setVisible(False)
        self.outlineCircle = outlineCircle
        self.x_pos = x
        self.y_pos = y
        self.r = r


        tempText1 = QGraphicsSimpleTextItem("2:34") # !!! fix
        tempText1.setFont(QFont("TypeWriter", 15, 0, False))
        tempText1.setY(y - tempText1.boundingRect().height()/2)
        tempText1.setX(x - tempText1.boundingRect().width()/2)

        self.addToGroup(tempText1)
        self.addToGroup(backgroundRect)
        self.tempText1 = tempText1

        self.center = (outlineCircle.boundingRect().x()+outlineCircle.boundingRect().width()/2, outlineCircle.boundingRect().y()+outlineCircle.boundingRect().height()/2)
        self.radius = outlineCircle.boundingRect().width()/2

        self.sessionTime = session_length * 1000
        self.breakTime = break_length * 1000
        self.interval = 33
        self.currentTime = self.sessionTime - self.interval
        
        self.timer = QTimer()
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.update_time)

        self.repaint()

    def restart_time(self):
        self.currentTime = self.sessionTime
        self.parentItem().currentState = "session"
        self.timer.start()

    def update_time(self):
        if self.currentTime > self.interval:
            self.currentTime -= self.interval
            self.repaint()
            self.update()
        else:
            match self.parentItem().currentState:
                case "session":
                    if self.breakTime > 0:
                        self.parentItem().frame.breakMask.setVisible(True)
                        self.currentTime = self.breakTime
                        self.parentItem().currentState = "break"
                    else:
                        self.currentTime = self.sessionTime
                        imgName = self.getNextImg()
                        self.parentItem().frame.imgName = imgName
                        self.parentItem().frame.changeBackground(imgName)
                        self.parentItem().addToHistory(imgName)
                        
                case "break":
                    self.parentItem().frame.breakMask.setVisible(False)
                    self.currentTime = self.sessionTime
                    self.parentItem().currentState = "session"
                    if self.parentItem().historyIndex == 0:
                        imgName = self.getNextImg()
                        self.parentItem().frame.imgName = imgName
                        self.parentItem().frame.changeBackground(imgName)
                        self.parentItem().addToHistory(imgName)
                    else:
                        self.parentItem().historyIndex -= 1
                        imgName = self.parentItem().imgHistory[self.parentItem().historyIndex]
                        self.parentItem().frame.imgName = imgName
                        self.parentItem().frame.changeBackground(imgName)

    def timerPressed(self):
        if self.parentItem().currentState == "break":
            self.parentItem().frame.breakMask.setVisible(True)
        else:
            self.parentItem().frame.breakMask.setVisible(False)
    
        # well, more shit to refactor
        if self.parentItem().directory == None:
            return

        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def getNextImg(self):
        return self.parentItem().getNextImg()

    def repaint(self):
        time = self.currentTime

        remaining = int(time/1000) + 1
        (minutes, seconds) = (math.floor(remaining/60), (remaining % 60))
        if len(str(seconds)) == 1:
            seconds = "0" + str(seconds)
        clockText = str(minutes) + ":" + str(seconds)

        self.tempText1.setText(clockText)
        self.tempText1.setY(self.outlineCircle.boundingRect().center().y() - self.tempText1.boundingRect().height()/2)
        self.tempText1.setX(self.outlineCircle.boundingRect().center().x() - self.tempText1.boundingRect().width()/2)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        if self.parentItem().currentState == "session":
            fullTime = self.sessionTime
        else:
            fullTime = self.breakTime
        
        angle = int(5760 * (self.currentTime/fullTime)) - 100

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(0)
        painter.drawEllipse(self.x_pos,self.y_pos,self.r,self.r) # border circle

        if self.parentItem().currentState == "session":
            painter.setBrush(QColorConstants.LightGray)
        else:
            painter.setBrush(QColor(250,215,160))
        painter.drawEllipse(self.x_pos+1,self.y_pos+1,self.r-2,self.r-2) # outer circle
        tempPen = QPen(0)
        tempPen.setWidth(5)
        painter.setPen(tempPen)
        if angle < 50 :
            tempAngle = 50
        else:
            tempAngle = angle
        painter.drawArc(self.x_pos+6,self.y_pos+6,self.r-12,self.r-12, 1440,tempAngle-50)

        painter.setPen(0)
        painter.setBrush(0)
        painter.drawEllipse(self.x_pos + int(self.r / 2), self.y_pos + 4,4,4)
        origin_x = self.x_pos + self.r/2 - 2
        origin_y = self.y_pos + self.r/2 - 2

        theta = angle / 5760 * 2 * math.pi + (math.pi / 2)
        painter.drawEllipse(int(origin_x + math.cos(theta) * (self.r/2-6)), int(origin_y - math.sin(theta) * (self.r/2-6)), 5, 5)

        return super().paint(painter, option, widget)