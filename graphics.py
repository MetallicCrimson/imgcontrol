from imgFrame import *

def renderImgFrame(x,y,width,height):
    tempImgFrame = ImgFrame(x,y,width,height)

    return tempImgFrame

def renderQuickMenu(window_width, window_height, menu_position_x, menu_position_y, session_length, break_length, history_size, random_state, directory, history, frame):
    tempMenu = QuickMenu(window_width, window_height, menu_position_x, menu_position_y, session_length, break_length, history_size, random_state, directory, history, frame)

    return tempMenu