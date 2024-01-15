# Here will be the underlying logic of the states
import os
import filetype

def buildDirStructure(start_dir):
    tempNames = []
    # I don't like try-except in production code, but os.listdir()
    # will literally terminate the code if the user clicks on "cancel"
    try:
        tempNames = os.listdir(start_dir)
    except:
        return False
    filesArray = []
    for tempName in tempNames:
        tempPath = os.path.join(start_dir, tempName).replace("\\", "/")
        print(tempPath)
        rawTempPath = r'{}'.format(tempPath)
        if os.path.exists(rawTempPath) and os.path.isfile(rawTempPath):
            if filetype.is_image(rawTempPath):
                filesArray.append(rawTempPath)
        else:
            newArray = buildDirStructure(rawTempPath)

            if newArray:
                filesArray += newArray

    if filesArray:
        return filesArray
    else:
        return False