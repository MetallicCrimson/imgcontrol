## just playing with libraries
import time
from graphics import *

if (__name__ == '__main__'):
    

    # todo: initialize these from config.txt
    timer_length = 300
    break_length = 0
    window_width = 800
    window_height = 600
    window_position_x = 0
    window_position_y = 0
    menu_position_x = 0
    menu_position_y = 0

    app = QApplication(sys.argv)
    frame = renderImgFrame(window_position_x, window_position_y, window_width, window_height)
    quick_menu = renderQuickMenu(menu_position_x, menu_position_y, window_width, window_height, frame)
    #bg_img = BackgroundImg(window_width, window_height)
    #print(quick_menu)
    #timer = Timer(quick_menu.timerCircle)
    #timer.start()

    ## testing file stuff!
    #newButton = TestButton()
    #newButton.move(200,200)
    #frame.scene().addWidget(newButton)
    
    #frame.scene().addItem(bg_img)☻
    frame.scene().addItem(quick_menu)
    frame.quickMenu = quick_menu
    frame.setWindowTitle("ImgControl")
    frame.move(50,50) # this is interesting. lucky guess 4ever
    #print(frame.scene().items()[0])

    frame.show()
    app.exec()
    
    sys.exit()
