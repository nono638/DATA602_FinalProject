def AddStrokesColumn(df):
    """This function uses an internal function, getStrokes(), to make a column in a
     dataframe for the strokes list column from the steno column.  It returns
     the modified dataframe"""
    def getStrokes(x):
        if " " not in x: #one stroke
            return [x]  # If it's only one stroke, it'll be a list with length 1
        else: # more than one stroke
            strokes = []
            stroke = ""
            for i in x:
                if i != " ":
                    stroke += i
                else:
                    strokes.append(stroke)
                    stroke = ""

            strokes.append(stroke) #append last remaining stroke

            return strokes

    df["Strokes"] = df['Steno'].apply(getStrokes)
    return  df


def StandardizeStrokes(x):
    """
    "Standardized" Strokes will handle the second instance of a duplicative (right) key on the steno keyboard.
    For instance the right T or the final S lowercase, so t or s. It also drops dashes which are used to denote final keys.
    Expects a list as input, returns a list that has been 'standardized'.

    For example:

    'STOPS'  -->  'STOps'
    """
    # Validate input a bit:
    if type(x) != list:
        print("Was expecting a list as input, received {}. Returning None".format(x))
        return None

    tells = '-AO*EUFBLG'  #
    doubles = 'STPR'
    strokes = []
    for stroke in x:  # expecting a list of strokes
        # print("stroke", stroke)
        rightSide = False
        pendingStroke = ""
        count = 0

        for i in stroke:
            if i in tells:
                rightSide = True  # we're already on the right side of the keyboard
            if i != "-":
                if i not in doubles:  # not a key that's doubled, no standardization needed
                    pendingStroke += i
                elif i in doubles:  # doubled keys that potentially need standardization
                    if rightSide:  # We've already established we're on the right side from tells
                        pendingStroke += i.lower()
                    elif ((i == 'S') and (count > 0)):  # if S is anything but the first letter, it's final S
                        pendingStroke += i.lower()
                    elif ((i == 'T') and (("T" in stroke[:count]) or \
                                          ("K" in stroke[:count]) or \
                                          ("P" in stroke[:count]) or \
                                          ("W" in stroke[:count]) or \
                                          ("H" in stroke[:count]) or \
                                          ("R" in stroke[:count]))):
                        pendingStroke += i.lower()
                    elif ((i == 'P') and (("P" in stroke[:count]) or \
                                          ("W" in stroke[:count]) or \
                                          ("H" in stroke[:count]) or \
                                          ("R" in stroke[:count]))):
                        pendingStroke += i.lower()
                    elif ((i == 'R') and (("R" in stroke[:count]))):
                        pendingStroke += i.lower()
                    else:
                        pendingStroke += i
            count += 1

        strokes.append(pendingStroke)

    return strokes