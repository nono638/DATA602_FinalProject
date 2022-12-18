def getLeftKeys(x):
    """Returns only the right steno keys from a string.  Assumes Standardized Stroke input."""
    leftKeys = "STKPWHR"

    if(type(x) == list):
        returnList = []
        for i in x:
            leftString = ""
            for j in i:
                if j in leftKeys:
                    leftString += j
            if (leftString is None) or (leftString ==""):
                leftString = "_"
            returnList.append(leftString)
        return returnList
    else:  #param isn't a list
        returnString = ""

        for i in x:
            if i in leftKeys:
                returnString += i
        if (len(returnString) > 0):
            return returnString
        else:
            return None


def getRighttKeys(x):
    """Returns only the left steno keys from a string.  Assumes Standardized Stroke"""
    rightKeys = "FrpBLGtsDZ"
    if type(x) == list:
        returnList = []
        for i in x:
            rightString = ""
            for j in i:
                if j in rightKeys:
                    rightString += j
            if (rightString is None) or (rightString == ""):
                rightString = "_"
            returnList.append(rightString)
        return returnList
    else:
        returnString = ""

        for i in x:
            if i in rightKeys:
                returnString += i
        if (len(returnString) > 0):
            return returnString
        else:
            return None


def getVowelKeys(x):
    """Returns only the mid steno keys from a string.  Assumes Standardized Stroke"""
    midKeys = "AO*EU"

    if type(x) == list:
        returnList = []
        for i in x:
            midString = ""
            for j in i:
                if j in midKeys:
                    midString += j
            if (midString is None) or (midString == ""):
                midString = "_"
            returnList.append(midString)
        return returnList
    else:
        returnString = ""
        for i in x:
            if i in midKeys:
                returnString += i
        if (len(returnString) > 0):
            return returnString
        else:
            return None