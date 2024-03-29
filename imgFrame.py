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
        self.move(x,y)

        backgroundLabel = QLabel()

        self.backgroundLabel = backgroundLabel
        self.scene().addWidget(backgroundLabel)
        self.tempRatio = 1
        tempFont = QFont()
        tempFont.setPixelSize(22)

        defaultLabel = QLabel()
        self.defaultLabel = defaultLabel
        defaultLabel.setFont(tempFont)
        defaultLabel.setText("""     Please select a folder,
  or check out the settings!  """)
        self.scene().addWidget(defaultLabel)

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

        width = self.width()
        height = self.height()

        if height == 0:
            return

        windowRatio = width / height

        if windowRatio > self.tempRatio:
            newHeight = height
            newWidth = height * self.tempRatio
        else:
            newWidth = width
            newHeight = width * (1 / self.tempRatio)

        self.backgroundLabel.resize(int(newWidth), int(newHeight))
        self.backgroundLabel.move((width - self.backgroundLabel.width())//2, (height - self.backgroundLabel.height())//2)

        if self.defaultLabel.isVisible():
            self.defaultLabel.move((width - self.defaultLabel.width())//2, (height - self.defaultLabel.height())//2)

        size = event.size()
        self.setSceneRect(0,0,size.width(),size.height())
        self.breakMask.setRect(0,0,size.width(),size.height())

        self.quickMenu.reposition()
        return super().resizeEvent(event)

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
        self.defaultLabel.setVisible(False)
        


        if img[-4:] == "avif":
            tempImgName = "temp.jpg"
            temp = Image.open(img)
            temp.save(tempImgName)
            tempPixmap = QPixmap(tempImgName)
            img = tempImgName
        else:
            tempPixmap = QPixmap(img)

        width = self.width()
        height = self.height()
        
        tempRatio = tempPixmap.width() / tempPixmap.height()
        self.tempRatio = tempRatio
        windowRatio = width / height

        if windowRatio > self.tempRatio:
            newHeight = height
            newWidth = height * self.tempRatio
        else:
            newWidth = width
            newHeight = width * (1 / self.tempRatio)

        self.backgroundLabel.setStyleSheet("border-image: url('" + img + "');")
        
        self.backgroundLabel.resize(int(newWidth), int(newHeight))
        self.backgroundLabel.move((width - self.backgroundLabel.width())//2, (height - self.backgroundLabel.height())//2)

        self.imgName = img
        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.quickMenu.settingsWindow.isVisible:
            self.quickMenu.settingsWindow.close()

        # it shouldn't exist at this point, but just to be safe
        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")

        # writing config.txt
        if self.quickMenu.directory != None:
            tempConfig = ""
            tempConfig += str(self.width()) + "\n" + str(self.height()) + "\n" + str(self.pos().x()) + "\n" + str(self.pos().y()) + "\n" + str(int(self.quickMenu.pos().x())) + "\n" + str(int(self.quickMenu.pos().y())) + "\n" + str(int(self.quickMenu.timerCircle.sessionTime/1000)) + "\n" + str(int(self.quickMenu.timerCircle.breakTime/1000)) + "\n" + str(len(self.quickMenu.imgHistory)) + "\n" + str(self.quickMenu.randomState) + "\n" + self.quickMenu.directory
            for item in self.quickMenu.imgHistory:
                tempConfig += "\n" + str(item)

            with open("config.txt", "w") as file:
                file.write(tempConfig)

        return super().closeEvent(a0)