# Here will be the underlying logic of the states
import os
import filetype
import math
import random

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
            try:
                newArray = buildDirStructure(rawTempPath)
            except:
                newArray = []
            filesArray += newArray

    
    if filesArray:
        return filesArray
    else:
        return False
    
def getNextImg(tc):
        if tc.parentItem().randomState:
            tempList = list(set(tc.parentItem().images) - set(tc.parentItem().imgHistory))
            if len(tempList) == 0:
                # with this, it will choose from the last 25% of the imgHistory (rounded up)
                t = math.ceil(len(tc.parentItem().imgHistory) * .25)
                print(t)
                t2 = random.randint(1,t)

                tempImg = tc.parentItem().imgHistory[-t2]
                tempId = tc.parentItem().images.index(tempImg)
                tc.parentItem().imgId = tempId
            else:
                tempId = random.randint(0,len(tempList)-1)
                tc.parentItem().imgId = tc.parentItem().images.index(tempList[tempId])
        else:
            print(tc.parentItem().imgId)
            tc.parentItem().imgId += 1
            if tc.parentItem().imgId >= len(tc.parentItem().images):
                tc.parentItem().imgId = 0
        imgName = tc.parentItem().images[tc.parentItem().imgId]
        return imgName