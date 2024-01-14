import pillow_avif
from PIL import Image
from PyQt6.QtCore import QSize

from quickMenu import *

class ImgFrame(QGraphicsView):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.myScene = QGraphicsScene()
        self.setScene(self.myScene)
        self.myScene.setSceneRect(0,0,width,height)
        self.myScene.setBackgroundBrush(QColor(200,220,200))
        self.backgroundPixmap = None
        self.move(x,y)
        
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

        # without this, the window can't be bigger than a specific size at starting up...?
        self.resize(QSize(width, height))

        self.setWindowTitle("ImgControl")
        self.setWindowIcon(QIcon("icon.png"))

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        if self.fullPixmap == None:
            if self.imgName[-4:] == "avif":
                print("it's an avif")
                pixmap = QPixmap(os.getcwd() + "/temp.jpg")
            else:
                pixmap = QPixmap(self.imgName)

            self.fullPixmap = pixmap

        size = event.size()
        self.setSceneRect(0,0,size.width(),size.height())
        self.breakMask.setRect(0,0,size.width(),size.height())
        self.pixmap2.setPixmap(self.fullPixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio))
        self.pixmap2.setPos((size.width()-self.pixmap2.boundingRect().width()) / 2, (size.height() - self.pixmap2.boundingRect().height()) / 2)

        self.quickMenu.reposition()

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
                self.quickMenu.buttonRandom.pressed()
            case Qt.Key.Key_T:
                self.quickMenu.buttonRestart.pressed()
            case Qt.Key.Key_Left:
                self.quickMenu.buttonLeft.pressed()
            case Qt.Key.Key_Right:
                self.quickMenu.buttonRight.pressed()
            case Qt.Key.Key_F:
                self.quickMenu.buttonDirectory.pressed()
            case Qt.Key.Key_S:
                self.quickMenu.buttonSettings.pressed()
        return super().keyReleaseEvent(event)

    def changeBackground(self,img):
        self.imgName = img
        if os.path.exists(os.getcwd() + "/temp.jpg"):
            os.remove(os.getcwd() + "/temp.jpg")

        if img[-4:] == "avif":
            print("it's an avif")
            self.fullPixmap = self.handleAvif(img)
        else:
            self.fullPixmap = QPixmap(img)

        self.pixmap2.setPixmap(self.fullPixmap.scaled(self.width(),
                                self.height(),
                                Qt.AspectRatioMode.KeepAspectRatio))
        
        (temp_x, temp_y) = self.pixmap2.boundingRect().width(), self.pixmap2.boundingRect().height()
        print(temp_x, temp_y)
        self.pixmap2.setPos((self.width()-temp_x) / 2, (self.height()-temp_y) / 2)

    def handleAvif(self, img):
        imgname = img[:-5]
        tempImgName = os.getcwd() + "/temp.jpg"
        temp = Image.open(img)
        temp.save(tempImgName)
        print("Saved to " + tempImgName)
        pixmap = QPixmap(tempImgName)
        return pixmap
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.quickMenu.settingsWindow.isVisible:
            self.quickMenu.settingsWindow.close()

        if os.path.exists(os.getcwd() + "/temp.jpg"):
            os.remove(os.getcwd() + "/temp.jpg")

        # writing config.txt
        if self.quickMenu.directory != None:
            tempConfig = ""
            tempConfig += str(self.width()) + "\n" + str(self.height()) + "\n" + str(self.pos().x()) + "\n" + str(self.pos().y()) + "\n" + str(int(self.quickMenu.pos().x())) + "\n" + str(int(self.quickMenu.pos().y())) + "\n" + str(int(self.quickMenu.timerCircle.sessionTime/1000)) + "\n" + str(int(self.quickMenu.timerCircle.breakTime/1000)) + "\n" + str(len(self.quickMenu.imgHistory)) + "\n" + str(self.quickMenu.randomState) + "\n" + self.quickMenu.directory
            for item in self.quickMenu.imgHistory:
                tempConfig += "\n" + str(item)

            with open("config.txt", "w") as file:
                file.write(tempConfig)

        return super().closeEvent(a0)