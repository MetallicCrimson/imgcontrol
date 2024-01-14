# Here will be the underlying logic of the states
import sys
import os
import filetype
import time
import threading
from PyQt6.QtCore import QTimer

def buildDirStructure(start_dir):
    print(start_dir)
    tempNames = []
    # I don't like try-except in production code, but os.listdir()
    # will literally terminate the code if the user clicks on "cancel"
    try:
        tempNames = os.listdir(start_dir)
    except:
        return False
    print(tempNames)
    filesArray = []
    for tempName in tempNames:
        print(tempName)
        tempPath = os.path.join(start_dir, tempName)
        rawTempPath = r'{}'.format(tempPath)
        if os.path.isfile(rawTempPath):
            if filetype.is_image(rawTempPath):
                filesArray.append(rawTempPath)
        else:
            # This is a VERY hacky solution, but I can't do anything against these
            # system protected directories. Oh, do I like working in Windows
            newArray = []
            print(tempName)
            try:
                newArray = buildDirStructure(rawTempPath)
                print("Hola")
                filesArray += newArray
            except:
                newArray = []
            filesArray += newArray

    
    if filesArray:
        return filesArray
    else:
        return False