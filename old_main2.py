import sys
#import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSlot, Qt, QPointF
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent
from functools import partial

class FullMenu(QGraphicsItemGroup):
    def __init__(self,win_width,win_height):
        super().__init__()
        self.win_width = win_width()
        self.win_height = win_height()

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
        if (self.pos().x() > self.win_width-100):
            print(self.win_width)
            self.setX(self.win_width-100)
        if (self.pos().y() > self.win_height-50):
            print(self.win_height)
            self.setY(self.win_height-50)
        

        #print(self.pos().x(), self.pos().y())
        return super().mouseReleaseEvent(event)

class MyMenu(QGraphicsRectItem):
    def __init__(self,x,y,w,h,p,b,win_width,win_height):
        super().__init__(x,y,w,h)
        self.setPos(x,y)
        self.setPen(p)
        self.setBrush(b)
        self.setAcceptHoverEvents(True)
        self.win_width = win_width()
        self.win_height = win_height()


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

# note: QSS is also available!

class MyFrame(QGraphicsView):

    def __init__(self):
        super().__init__()

        self.myScene = QGraphicsScene()
        self.myScene.setSceneRect(0,0,1000,600)
        #self.myScene.setBackgroundBrush(QColor(100,150,150))
        
        self.setScene(self.myScene)

        x = 0
        y = 0
        w = 80
        h = 45

        pen = QColor(100,100,100)
        brush = QColor(150,150,150)

        pixmap = QPixmap("cat.jpg")
        pixmap2 = QGraphicsPixmapItem()
        pixmap = pixmap.scaled(int(self.myScene.width()),
                               int(self.myScene.height()),
                               Qt.AspectRatioMode.KeepAspectRatio)
        pixmap2.setPixmap(pixmap)
        
        
        self.scene().addItem(pixmap2)
        self.scene().setBackgroundBrush(0)
        


        self.fullMenu = FullMenu(self.sceneRect().width, self.sceneRect().height)
        self.fullMenu.addToGroup(QGraphicsRectItem(x,y,w,h))
        self.fullMenu.addToGroup(QGraphicsEllipseItem(0,0,30,50))

        self.item = MyMenu(x,y,w,h,pen,brush,self.sceneRect().width, self.sceneRect().height)
        self.scene().addItem(self.fullMenu)

        

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        size = event.size()
        target_size = min(size.width(), size.height()) - 1
        x = (size.width() - target_size) // 2
        y = (size.height() - target_size) // 2
        self.setSceneRect(0,0,size.width(),size.height())
        self.fullMenu.win_width = size.width()
        self.fullMenu.win_height = size.height()

        pixmap = QPixmap("cat.jpg")
        pixmap = pixmap.scaled(self.width(),
                               self.height(),
                               Qt.AspectRatioMode.KeepAspectRatio)
        self.items().__getitem__(3).setPixmap(pixmap)

        # this fuckery is to move the pixmap (background) to the center. have to do some VERY heavy restructuring later
        print(self.width())
        print(self.items().__getitem__(3).pixmap().height())
        self.items().__getitem__(3).setX((self.width() - self.items().__getitem__(3).pixmap().width()) / 2)
        self.items().__getitem__(3).setY((self.height() - self.items().__getitem__(3).pixmap().height()) / 2)
        


if (__name__ == '__main__'):
    app = QApplication(sys.argv)
    fr = MyFrame()
    fr.show()
    sys.exit(app.exec())

