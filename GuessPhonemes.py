import numpy as np
import pandas as pd

import Phonetics_Dict
import MakeColumnsForAnalysis
import ConsonantVowelStructure

def PhoneticsFirstPass(df : pd.DataFrame):
    """ This function gets the basic phonetic information from a dataframe that already has a left, mid, and right column.
    This function returns leftPhonemeMapping, midPhonemeMapping, rightPhonemeMapping, which are dataframes that have how
    each phoneme is written on the left, middle, or right.

    Expects Equal Structure to be true."""
    if "Phonetics" not in df.columns.tolist() or "syllables" not in df.columns.tolist(): #basic validation
        print("Expected both a 'Phonetics' and 'syllables' column, returning df...")
        return df
    else:
        dfWithoutPhonetics = df[df['Phonetics'].isnull()]
        df = df[df["Phonetics"].notnull()]

        leftPhonemesList = []
        midPhonemesList = []
        rightPhonemesList = []

        dfNullSyllablesOrNullWordCVCStructure= df[df['syllables'].isnull() | df['WordCVCStructure'].isnull()]
        df = df[np.logical_and( df['syllables'].notnull() , df['WordCVCStructure'].notnull() ) ]
        df = df[ df['WordCVCStructure'] != None] #doesn't seem to do anything for some reson
        df = df[df['syllables'].map(len) ==1] #work with just 1 syllable words, TODO work with multi stroke words

        for row in range(len(df)):
            leftDone, midDone, rightDone = False, False, False
            leftPhonemes, midPhonemes, rightPhonemes = "", "", ""
            if df.iloc[row]['WordCVCStructure'] is None:
                continue
            elif df.iloc[row]['WordCVCStructure'][0][0] == '_': #starts either with a vowel or on the right side
                leftDone = True
                if df.iloc[row]['WordCVCStructure'][0][1] == '_':  # starts on the right side, nested if here
                    midDone = True
            for phoneticSymbol in df.iloc[row]['Phonetics']:
                if phoneticSymbol in Phonetics_Dict.phoneticVowels: #vowel
                    midPhonemes += phoneticSymbol
                    if leftDone == False:
                        leftDone = True
                elif phoneticSymbol in Phonetics_Dict.phoneticConsanants: #consonant
                    if midPhonemes != "":
                        leftDone = True
                    if midDone or leftDone: #right side
                        rightPhonemes+= phoneticSymbol
                    else: #left side
                        leftPhonemes += phoneticSymbol
            if leftPhonemes == "":
                leftPhonemes = "_"
            if midPhonemes == "":
                midPhonemes = "_"
            if rightPhonemes == "":
                rightPhonemes = "_"
            leftPhonemesList.append(leftPhonemes)
            midPhonemesList.append(midPhonemes)
            rightPhonemesList.append(rightPhonemes)
        leftPhonemeMapping = pd.DataFrame({"leftStroke": list(df['lefts']),
                                           "leftPhoneme":leftPhonemesList, "side":"left", "word":list(df['Word'])
                                           })
        midPhonemeMapping = pd.DataFrame({"midStroke": list(df['mids']),
                                          "midPhoneme":midPhonemesList, "side":"mid", "word":list(df['Word'])
                                          })
        rightPhonemeMapping = pd.DataFrame({"rightStroke": list(df['rights']),
                                            "rightPhoneme": rightPhonemesList, "side": "right", "word": list(df['Word'])
                                            })

        return leftPhonemeMapping, midPhonemeMapping, rightPhonemeMapping




def MakeStenoAnswers(leftPhoneticDict, midPhoneticDict, rightPhoneticDict):
    """ This function figures out the maximum occurrence of a phonetic combination corresponding to a
    steno outline and returns a simplified "answer" dictionary that just has the most common occurrence
    and discards other lesser possible steno outlines for a given steno combination.  I eventually want to get rid of
    this.

    ̶T̶h̶i̶s̶ ̶f̶u̶n̶c̶t̶i̶o̶n̶ ̶i̶s̶ ̶s̶u̶p̶p̶o̶s̶e̶d̶ ̶t̶o̶ ̶b̶e̶ ̶p̶a̶s̶s̶e̶d̶ ̶s̶o̶m̶e̶t̶h̶i̶n̶g̶ ̶l̶i̶k̶e̶ ̶W̶o̶r̶d̶s̶T̶o̶G̶u̶e̶s̶s̶B̶o̶t̶h̶
̶ ̶ ̶ ̶ ̶a̶n̶d̶ ̶a̶d̶d̶s̶ ̶a̶ ̶g̶u̶e̶s̶s̶ ̶c̶o̶l̶u̶m̶n̶ ̶b̶a̶s̶e̶d̶ ̶u̶p̶o̶n̶ ̶t̶h̶e̶ ̶p̶h̶o̶n̶e̶t̶i̶c̶ ̶d̶i̶c̶t̶i̶o̶n̶a̶r̶y̶ ̶p̶a̶s̶s̶e̶d̶ ̶a̶s̶ ̶w̶e̶l̶l̶

"""
    leftAnswers = {}
    for phoneme in leftPhoneticDict:
        highScore = 0
        highSteno = ""
        for stenoPossibility in list(leftPhoneticDict[phoneme].keys()):
            if leftPhoneticDict[phoneme][stenoPossibility] > highScore:
                highScore = leftPhoneticDict[phoneme][stenoPossibility]
                highSteno = str(stenoPossibility)
        leftAnswers[phoneme] = highSteno

    midAnswers = {}
    for phoneme in midPhoneticDict:
        highScore = 0
        highSteno = ""
        for stenoPossibility in list(midPhoneticDict[phoneme].keys()):
            if midPhoneticDict[phoneme][stenoPossibility] > highScore:
                highScore = midPhoneticDict[phoneme][stenoPossibility]
                highSteno = str(stenoPossibility)
        midAnswers[phoneme] = highSteno

        rightAnswers = {}
        for phoneme in rightPhoneticDict:
            highScore = 0
            highSteno = ""
            for stenoPossibility in list(rightPhoneticDict[phoneme].keys()):
                if rightPhoneticDict[phoneme][stenoPossibility] > highScore:
                    highScore = rightPhoneticDict[phoneme][stenoPossibility]
                    highSteno = str(stenoPossibility)
            rightAnswers[phoneme] = highSteno

    return leftAnswers, midAnswers, rightAnswers



def MakePhoneticBatches(df, leftAnswerDict, midAnswerDict, rightAnswerDict, verbose = False):
    """This function will actually guess the steno outlines...
    This function uses the left, mid, and right answers generated previously, and 
    applies it to a df.  It will return the dataframe with a new column.
    
    For now, use this on both where you have both the syllable and phonetic data of what needs to be guessed"""
    phoneticBatchList =[]
    for row in range(len(df)):
        phonetics = df.iloc[row]["Phonetics"]
        syllables = df.iloc[row]["syllables"]
        if verbose:
            print("row {}, phonetics: {}     syllables {}".format(row, phonetics, syllables))

        currentlyVowel = False
        currentlyConsonant = False
        currentPhoneticBunch = ""
        phoneticBatches = []
        for i in range(len(phonetics)):
            if phonetics[i] in Phonetics_Dict.phoneticConsanants:
                if currentlyConsonant:
                    currentPhoneticBunch += phonetics[i]
                else:
                    currentlyConsonant = True
                    currentlyVowel = False
                    if currentPhoneticBunch != "":
                        phoneticBatches.append(currentPhoneticBunch)
                    currentPhoneticBunch = phonetics[i]
            elif phonetics[i] in Phonetics_Dict.phoneticVowels: #vowel
                if currentlyVowel:
                    currentPhoneticBunch += phonetics[i]
                else:
                    currentlyVowel =True
                    currentlyConsonant = False
                    if currentPhoneticBunch != "":
                        phoneticBatches.append(currentPhoneticBunch)
                    currentPhoneticBunch = phonetics[i]

        if currentPhoneticBunch != "": #final one
            phoneticBatches.append(currentPhoneticBunch)
        phoneticBatchList.append(phoneticBatches)
        # if verbose:
        #     print(phoneticBatches)
        #     print("-------------")
    return phoneticBatchList

def GuessPhonemesStep2(listParam : list, leftAnswerDict, midAnswerDict, rightAnswerDict, verbose = False):
    """Rename this ridiculous thing.  I'm just breaking this up to troubleshoot"""
    problems = []
    returnList = []
    for phonemes in listParam:
        result = ""
        position = 'left'
        if (len(phonemes) %3) ==0:
            if verbose:
                print("{} has an appropriate length....".format(phonemes))
            try:
                position = 'left'
                for bunch in phonemes:
                    if position == 'left':
                        try:
                            result += leftAnswerDict[bunch]
                        except:
                            if verbose:
                                print ("{} not in left dict".format(bunch) )
                                problems.append(bunch)
                            result += "_"
                        position = 'mid'
                    elif position == 'mid':
                        result += midAnswerDict[bunch]
                        position = 'right'
                    elif position == 'right':
                        result += rightAnswerDict[bunch]
                        position = 'left'
                if verbose:
                    ("phonemes: {}\tresult: {}".format(phonemes, result))
                returnList.append(result)
            except:
                # if verbose:
                #     print('could not find something in', phonemes)
                returnList.append("@@")
        else:
            returnList.append(None)

    return returnList, problems


def PhoneticsAnalysis(df, verbose = False):  #maybe discard this
    """This is going to make an answer key of phonetics from a df..."""
    if "Phonetics" in df.columns.tolist():
        if "syllables" in df.columns.tolist():

            def CountingDictAdd(dictParam, toAdd, verbose = False):
                if type(dictParam)!= dict:
                    if verbose:
                        print("A non-dictionary object was passed to CountingDictAdd... returning None")
                    return None
                if toAdd in dictParam:
                    dictParam[toAdd] +=1
                else:
                    dictParam[toAdd] = 1
                return dictParam




            lefts = df[['left', 'Phonetics', 'syllables', 'leftmidright']]
            lefts = lefts[lefts['left']!='_']




            for i in range(len(lefts)):
                if len(df.iloc[i]['left']) == 1 : #If the length of the list is one
                    CountingDictAdd(leftDict, i)


            mids  = df[['mid', 'Phonetics', 'syllables', 'leftmidright']]
            rights = df[['right', 'Phonetics', 'syllables', 'leftmidright']]




        else: #TDO, no syllables, phonetics only
            return df

    else: # no Phonetics column, return df as is
        if verbose:
            print ("Nothing happened with PhoneticsAnyalysis because the df didn't have a phonetics column...")
        return df


def makePhoneticMappingsRedone(df: pd.DataFrame, verbose: bool = False):
    """This function will make mappings of phonetic symbols to their respective Steno.  It will
    output a dataframe that has the phoneme and its steno usage."""
    if verbose:
        print("Starting makePhoneticMappingsRedone...")
    # Validation
    if "Phonetics" not in df.columns.tolist():
        if verbose:
            print("Expected Phonetics Column in makePhoneticMappingRedone.  Returning df as is...")
        return df

    dfWithoutPhonetics = df[ np.logical_or(df['Phonetics']==None, df['Phonetics'].isnull() ) ]
    df = df[df['Phonetics'].notnull()]
    df = df[df['Phonetics']!=None]
    df = df [df['Steno'].notnull()]

    def ThreePhonemes(listParam: list, verbose = False):
        """This inner function is used just to make a mask for
        threePhoenemes or less from the phonetics column of the passed in DF"""
        mask = []
        for item in listParam:
            phonemeCount = 0
            for char in item:
                if char in Phonetics_Dict.phoneticVowels or char in Phonetics_Dict.phoneticConsanants:
                    phonemeCount +=1
            if phonemeCount==3:
                mask.append(True)
            else:
                mask.append(False)
        return mask

    mask = ThreePhonemes(list(df['Phonetics'] ))

    #dfThreePhonemesOrLess = df[df['Phonetics'].map(lambda x: len(x) <=3) ]
    dfThreePhonemesOrLess = df[mask]
    if verbose:
        print("The type of 'Strokes' is {}".
              format(type(dfThreePhonemesOrLess.iloc[1]['Strokes']) ))
    if type(dfThreePhonemesOrLess.iloc[1]['Strokes'])== str:
        dfThreePhonemesOrLess = dfThreePhonemesOrLess[dfThreePhonemesOrLess['Strokes'].apply(lambda x: len([i for i in x if  i ==','])<1)]
    elif type(dfThreePhonemesOrLess.iloc[1]['Strokes'] == list):
        dfThreePhonemesOrLess = dfThreePhonemesOrLess[dfThreePhonemesOrLess["Strokes"].map(len) <=1]
    else:
        print("The 'strokes' column is typed {}.  It must be a list or a string".format(type(dfThreePhonemesOrLess.iloc[1]['Strokes'])) )
        print("Returning None...")
        return None

    stenoList = []
    phoneticsList = []
    for i in range(len(dfThreePhonemesOrLess)):
        #steno
        leftSten, midSten, rightSten = [],[],[]
        leftStenString, midStenString, rightStenString = '','',"",
        leftKeys, midKeys = "STKPWHR",  "AO*EU"
        for stenoKey in dfThreePhonemesOrLess.iloc[i]['Strokes'][0]:  #Assume one-storke entries.  THis was filterd for earlier.
            typeOf_stenoKey = type(stenoKey)
            if stenoKey not in '[\']': #problemStrokes
                if stenoKey in leftKeys:
                    leftStenString+= stenoKey#leftSten.append(stenoKey)
                elif stenoKey in midKeys:
                    midStenString += stenoKey#midSten.append(stenoKey)
                else:
                    rightStenString += stenoKey#.append(stenoKey)
        leftSten.append(leftStenString)
        midSten.append(midStenString)
        rightSten.append(rightStenString)
        #phonetics
        leftPhonemes, midPhonemes, rightPhonemes = [],[],[]
        leftPhonemeString, midPhonemeString, rightPhonemeString = "","",""
        vowelPhonemeDone = False
        for phoneme in dfThreePhonemesOrLess.iloc[i]['Phonetics']:
            if phoneme in Phonetics_Dict.phoneticVowels or phoneme in Phonetics_Dict.phoneticConsanants:
                if phoneme not in Phonetics_Dict.phoneticVowels and vowelPhonemeDone is False:
                    leftPhonemeString += phoneme #leftPhonemes.append( phoneme)
                elif phoneme in Phonetics_Dict.phoneticVowels:
                    vowelPhonemeDone = True
                    midPhonemeString += phoneme #midPhonemes.append(phoneme)
                elif phoneme not in Phonetics_Dict.phoneticVowels and vowelPhonemeDone:
                    rightPhonemeString += phoneme #rightPhonemes.append(phoneme)
        leftPhonemes.append(leftPhonemeString)
        midPhonemes.append(midPhonemeString)
        rightPhonemes.append(rightPhonemeString)
            #fix empty lists:
        for keyBunches in [leftSten, midSten, rightSten]:
            if len(keyBunches)==0:
                keyBunches.append(None)
        for phonemeBunches in [leftPhonemes, midPhonemes, rightPhonemes]:
            if len(phonemeBunches)==0:
                phonemeBunches.append(None)

        stenoList.append([leftSten, midSten, rightSten])
        phoneticsList.append([leftPhonemes, midPhonemes, rightPhonemes])

    PhoneticsDictDF = pd.DataFrame(
        {"Phonetics":phoneticsList,
          "Steno":stenoList,
         'Word':list(dfThreePhonemesOrLess['Word'])}
    )
    PhoneticsDictDF['leftSteno']= [i[0][0]  if i[0][0] !="" else None for i in
                                   list(PhoneticsDictDF['Steno'])]
    PhoneticsDictDF['leftPhonetics'] = [i[0][0]  if i[0][0] !="" else None for i in
                                        list(PhoneticsDictDF['Phonetics'])]
    PhoneticsDictDF['midSteno'] = [i[1][0] if i[1][0] != "" else None for i in
                                   list(PhoneticsDictDF['Steno'])]
    PhoneticsDictDF['midPhonetics'] = [i[1][0] if i[1][0] != "" else None for i in
                                         list(PhoneticsDictDF['Phonetics'])]
    PhoneticsDictDF['rightSteno'] = [i[2][0] if i[2][0] != "" else None for i in
                                        list(PhoneticsDictDF['Steno'])]
    PhoneticsDictDF['rightPhonetics'] = [i[2][0] if i[2][0] != "" else None for i in
                                        list(PhoneticsDictDF['Phonetics'])]


    return PhoneticsDictDF


if __name__ == '__main__':
    import BigOuterMerge
    import NoahAndChrisTesting
    import SplitPhoneticsAndSyllables
    import FilterBeforeLogic

    #NoahDF = NoahAndChrisTesting.NoahDF
    testDF = NoahAndChrisTesting.ChrisDF
    print("Length before filtering: {:,}".format(len(testDF)))

    testDF = FilterBeforeLogic.filter1(BigOuterMerge.BigOuterMerge(testDF) , verbose=True)
    # NoahBoth, NoahSyllablesOnly, NoahPhoneticsOnly = SplitPhoneticsAndSyllables.SplitDF(NoahDF)
    testDF = MakeColumnsForAnalysis.doAll(testDF, verbose=True)

    NoahDF2 = NoahAndChrisTesting.NoahReady1

    # if len(list(NoahDF.columns)) > len(list(NoahDF2.columns)):
    #     print("There are more columns in NoahDF")
    # else:
    #     print("There are more columns in NoahDF2.")
    #
    # for col in list(NoahDF2.columns):
    #     if col not in list(NoahDF.columns):
    #         print("{} is in DF2 but not df".format(col))

    # if (NoahDf == NoahDf2):
    #     print("NoahDF2 is working...")
    # else:
    #     print("NoahDF2 is NOT working...")

    #leftPhonemeMapping, midPhonemeMapping, rightPhonemeMapping = PhoneticsFirstPass(NoahDf)

    #something = makePhoneticMappingsRedone(NoahDf, verbose = True)
    phoneticsBasicDF = makePhoneticMappingsRedone(testDF, verbose=True)

    print('The type of the the phoneticsBasicDF steno column is {} '.format(\
        type(phoneticsBasicDF.iloc[1]['Steno'])) )

    print('The type of the the elements in the phoneticsBasicDF steno column is {} '.format(\
        type(phoneticsBasicDF.iloc[1]['Steno'][0])))


    #midAE_contains = phoneticsBasicDF['æ' in phoneticsBasicDF['Phonetics'][1]]
    # print(phoneticsBasicDF.iloc[6])
    # print(phoneticsBasicDF.iloc[6]['Phonetics'])
    # print(phoneticsBasicDF.iloc[6]['Phonetics'][1])
    # print(phoneticsBasicDF.iloc[6]['Phonetics'][1][0])
    #
    # print()
    # for item in list(phoneticsBasicDF.loc[:,'Phonetics'].values):
    #     print(item[1][0])



    phoneticsBasicDF_MIDɛ = phoneticsBasicDF[phoneticsBasicDF['midPhonetics'] == 'ɛ']

    phoneticsBasicDF_RIGHTɹ = phoneticsBasicDF[phoneticsBasicDF['rightPhonetics'] == 'ɹ']

    phoneticsBasicDF_RIGHTʃ = phoneticsBasicDF[phoneticsBasicDF['rightPhonetics'] == 'ʃ']

    phoneticsBasicDF_LEFTtɹ = phoneticsBasicDF[phoneticsBasicDF['leftPhonetics'] == 'tɹ']
    #midAE_is = phoneticsBasicDF[phoneticsBasicDF.loc[:,'Phonetics'][1][0] == 'æ']


    #[[None], ['æ'], ['p', 't']]

    quit()

