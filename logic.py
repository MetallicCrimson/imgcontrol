# Here will be the underlying logic of the states
import sys
import os
import filetype
import time
import threading
from PyQt6.QtCore import QTimer

def buildDirStructure(start_dir):

    tempNames = []
    # I don't like try-except in production code, but os.listdir()
    # will literally terminate the code if the user clicks on "cancel"
    try:
        tempNames = os.listdir(start_dir)
    except:
        print("Nothing selected")
        return False
    filesArray = []

    for tempName in tempNames:
        tempPath = os.path.join(start_dir, tempName)
        rawTempPath = r'{}'.format(tempPath)
        if os.path.isfile(rawTempPath):
            if filetype.is_image(rawTempPath):
                filesArray.append(rawTempPath)
        else:
            #if os.access(rawTempPath, os.W_OK):
            # This is a VERY hacky solution, but I can't do anything against these
            # system protected directories. Oh, do I like working in Windows
            if tempName != "My Music" and tempName != "My Pictures" and tempName != "My Videos":
                newArray = buildDirStructure(rawTempPath)
            else:
                print(rawTempPath, "is not accessible")
                continue
            filesArray += newArray

    return filesArray

# trying to make it reversed...?
class Timer():
    def __init__(self, menu):
        self._timer = None

        # apparently it can be too fast to render...?
        self.interval = 0.05
        self.is_running = False
        self.next_call = time.time()
        self.menu = menu

        self.max_time = 5 # ?
        self.current_time = self.max_time
        print("Timer init")

    def _run(self):
        self.is_running = False
        self.menu.repaint(self.current_time)
        self.start()

    def start(self):
        #print("starting timer...?")
        if not self.is_running:
            self.next_call += self.interval
            self.current_time -= self.interval
            current_time = self.current_time
            
            print(self.current_time)

            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()

            self.is_running = True

            if self.current_time <= 0:
                self._timer.cancel()
                self.is_running = False

    def stop(self):
        self._timer.cancel()
        self.is_running = False