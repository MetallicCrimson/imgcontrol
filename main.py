## just playing with libraries
import time
from graphics import *

if (__name__ == '__main__'):
    
    if not os.path.exists(os.getcwd() + "/config.txt"): #os.path.exists(os.getcwd() + "/config.txt"):
        tempConfig = """800
600
50
50
200
100
10
30
20
True
""" + os.getcwd() + "/testFolder"

        f = open("config.txt", "w")
        f.write(tempConfig)
        f.close()

    with open("config.txt") as configFile:
        configLines = [line.strip() for line in configFile]

    # todo: initialize these from config.txt
    window_width = int(configLines[0])
    window_height = int(configLines[1])
    window_position_x = int(configLines[2])
    window_position_y = int(configLines[3])
    menu_position_x = int(configLines[4])
    menu_position_y = int(configLines[5])
    session_length = int(configLines[6])
    break_length = int(configLines[7])
    history_size = int(configLines[8])
    random_state = configLines[9]
    directory = configLines[10]

    app = QApplication(sys.argv)
    frame = renderImgFrame(window_position_x, window_position_y, window_width, window_height)
    quick_menu = renderQuickMenu(window_width, window_height, menu_position_x, menu_position_y, session_length, break_length, history_size, random_state, directory, frame)
    #bg_img = BackgroundImg(window_width, window_height)
    #print(quick_menu)
    #timer = Timer(quick_menu.timerCircle)
    #timer.start()☻s

    ## testing file stuff!
    #newButton = TestButton()
    #newButton.msove(200,200)
    #frame.scene().addWidget(newButton)
    
    #frame.scene().addItem(bg_img)☻
    frame.scene().addItem(quick_menu)
    frame.quickMenu = quick_menu
    #frame.quickMenu = quick_menu
    frame.setWindowTitle("ImgControl")
    #frame.move(50,50) # this is interesting. lucky guess 4ever
    #print(frame.scene().items()[0])

    frame.show()
    app.exec()
    
    sys.exit()