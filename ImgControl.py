import sys
from imgFrame import *


if (__name__ == '__main__'):
    
    tempDirTest = os.getcwd() + "/testFolder"

    if not os.path.exists(os.getcwd() + "/config.txt"): #os♣.path.exists(os.getcwd() + "/config.txt"):
        tempConfig = """800
600
50
50
200
100
60
10
20
False
None
"""

        f = open("config.txt", "w")
        f.write(tempConfig)
        f.close()

    with open("config.txt") as configFile:
        configLines = [line.strip() for line in configFile]

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
    if directory == "None":
        directory = None
    history = configLines[11:]
    for i in range(len(history)):
        if history[i] == "False":
            history[i] = False

    app = QApplication(sys.argv)
    frame = ImgFrame(window_position_x, window_position_y, window_width, window_height)
    quick_menu = QuickMenu(window_width, window_height, menu_position_x, menu_position_y, session_length, break_length, history_size, random_state, directory, history, frame)

    frame.scene().addItem(quick_menu)
    frame.quickMenu = quick_menu

    frame.setWindowTitle("ImgControl")

    frame.show()
    app.exec()
    
    sys.exit() 