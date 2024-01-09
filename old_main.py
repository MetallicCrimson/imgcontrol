import sys
#import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSlot, Qt, QPointF
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent
#from functools import partial

class MyMenu(QGraphicsRectItem):
    def __init__(self,x,y,w,h,p,b,win_width,win_height):
        super().__init__(x,y,w,h)
        self.setPos(x,y)
        self.setPen(p)
        self.setBrush(b)
        self.setAcceptHoverEvents(True)
        self.win_width = win_width
        self.win_height = win_height


    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        print("Hovered")
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return super().hoverLeaveEvent(event)
    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print("Pressed down")
        pass
    
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
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
        if (self.pos().x() < 0):
            self.setX(0)
        if (self.pos().y() < 0):
            self.setY(0)
        if (self.pos().x() > self.win_width-200):
            print(self.win_width)
            self.setX(self.win_width-200)
        if (self.pos().y() > self.win_height-200):
            print(self.win_height)
            self.setY(self.win_height-200)
        

        #print(self.pos().x(), self.pos().y())
        return super().mouseReleaseEvent(event)

class MyFrame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.myScene = QGraphicsScene()
        self.myScene.setSceneRect(0,0,800,600)
        self.myScene.setBackgroundBrush(QColor(100,150,150))

        self.setScene(self.myScene)

        x = 0
        y = 0
        w = 80
        h = 45

        pen = QColor(100,100,100)
        brush = QColor(150,150,150)

        self.itemGroup = QGraphicsItemGroup

        #self.itemGroup.addToGroup(MyMenu(5,5,10,10,10,10,100,80))
        tempItem = MyMenu(5,5,10,10,10,10,100,80)
        print(tempItem)

        self.item = MyMenu(x,y,w,h,pen,brush,self.sceneRect().width, self.sceneRect().height)
        self.scene().addItem(self.item)

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        size = event.size()
        target_size = min(size.width(), size.height()) - 1
        x = (size.width() - target_size) // 2
        y = (size.height() - target_size) // 2
        #self.circle.setRect(x,y,target_size,target_size)
        self.setSceneRect(0,0,size.width(),size.height())
        self.item.win_width = size.width()
        self.item.win_height = size.height()


if (__name__ == '__main__'):
    app = QApplication(sys.argv)
    fr = MyFrame()
    fr.show()
    sys.exit(app.exec())

