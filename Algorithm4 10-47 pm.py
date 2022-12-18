import numpy as np
import pandas as pd

import CountingDict
import MakeColumnsForAnalysis
import GuessPhonemes
import BigOuterMerge
import FilterBeforeLogic
import Phonetics_Dict
import WordFrequency
import PhoneticStructure
import StenoSides
import SyllableAnalysis1

import sklearn
import copy
if __name__ == '__main__':
    import NoahAndChrisTesting

    Sourcedf = NoahAndChrisTesting.NoahDF
    Stenographer = "Noah"

    #First the WordsToGuess is set as a copy of the BigOuterMerge Result
    df = BigOuterMerge.BigOuterMerge(Sourcedf)
    WordsToGuess = df.copy(deep=True)
    #Then filter the df
    df = FilterBeforeLogic.filter1(df, verbose = True)
    df = MakeColumnsForAnalysis.doAll(df)
    #then set the WordstoGuess as the ones that are left over
    WordsToGuess = WordsToGuess.drop(df.index)
    WordsToGuess = WordsToGuess[WordsToGuess["Word"].notnull()]
    WordsToGuess = WordsToGuess[WordsToGuess["Steno"].isnull()]
    #WordsToGuess = WordsToGuess[WordsToGuess['Word'].apply(lambda x: True if " " not in x else False)] #drop multi-word
    #WordsToGuess = MakeColumnsForAnalysis.doAll(WordsToGuess, verbose= True)

    WordsToGuess.drop(["Steno", "Translation", "Strokes"], axis = 1, inplace=True)
    WordsToGuess = pd.merge(WordsToGuess, WordFrequency.WordFreq, how ='left', on ='Word')
    WordsToGuess.drop_duplicates(subset='Word', inplace = True)
    if "NumStrokes" in WordsToGuess.columns.tolist() and "syllablesPerStroke" in WordsToGuess.columns.tolist() and \
        "syllableStrokeDifference" in WordsToGuess.columns.tolist():
        WordsToGuess.drop(["NumStrokes", "syllablesPerStroke", "syllableStrokeDifference"], axis=1, inplace=True)
    WordsToGuess = WordsToGuess[WordsToGuess['Word'].apply(lambda x: len(x)>2)] # to eliminate 1 and 2-char "Words"
    if "Special" in WordsToGuess.columns.tolist():
        WordsToGuess = WordsToGuess[WordsToGuess['Special'].isnull()] #drop any special columns, relevant for Case Cat #TODO possibly
        WordsToGuess.drop("Special", axis=1, inplace=True)

    print("making EqualStructure...")
    EqualBothSides = df[df["EqualStructureWithSyllables"]==True].copy(deep= True)
    EqualBothSides['lefts'] = EqualBothSides.loc[:,"Strokes"].apply(lambda x: StenoSides.getLeftKeys(x))
    EqualBothSides['mids'] = EqualBothSides.loc[:,"Strokes"].apply(lambda x: StenoSides.getVowelKeys(x))
    EqualBothSides['rights'] = EqualBothSides.loc[:,"Strokes"].apply(lambda x: StenoSides.getRighttKeys(x))
    EqualBothSides['leftmidrights'] = EqualBothSides.apply(
        lambda x: [[i for i in x['lefts']], [i for i in x['mids']], [i for i in x['rights']]], axis=1)



    leftMapping1, midMapping1, rightMapping1 = GuessPhonemes.PhoneticsFirstPass(EqualBothSides)
    #this makes the mappingDF, which has the sides and steno and phonemes and the word it came from
    if len(leftMapping1.columns.tolist()) == len(midMapping1.columns.tolist()) and len(leftMapping1.columns.tolist()) == len(rightMapping1.columns.tolist()):
        mappingsDict ={"Stroke": [], "Phoneme":[], "side":[], "word":[] }
        for mapping in [leftMapping1, midMapping1, rightMapping1]:
            for stroke in list(mapping.iloc[:,0]) :
                mappingsDict["Stroke"].append(stroke)
            for phoneme in list(mapping.iloc[:,1]) :
                mappingsDict['Phoneme'].append(phoneme)
            for side in  list(mapping.iloc[:,2]):
                mappingsDict['side'].append(side)
            for word in list(mapping.iloc[:,3]):
                mappingsDict['word'].append(word)

    PhoneticsFirstPassMappingsDF = pd.DataFrame(mappingsDict)
    del mappingsDict


    testPhoneme, testSide = 'ɫ', 'left'.lower()
    test1 = PhoneticsFirstPassMappingsDF[np.logical_and( PhoneticsFirstPassMappingsDF['side'] == testSide, PhoneticsFirstPassMappingsDF['Phoneme'] == testPhoneme)]



    leftMappingGrouped = leftMapping1.groupby('leftPhoneme').count().sort_values(by='side')
    midMappingGrouped = midMapping1.groupby('midPhoneme').count().sort_values(by ='side')
    rightMappingGrouped = rightMapping1.groupby('rightPhoneme').count().sort_values(by ='side')

    del leftMapping1, midMapping1, rightMapping1

    makePhoneticMappingsRedoneDF = GuessPhonemes.makePhoneticMappingsRedone(df, verbose=True)


    makePlots = False
    if makePlots:
        import seaborn as sns
        import datetime as dt
        import matplotlib.pyplot as plt
        import os
        print("Making plots...")
        try:
            os.mkdir("Outputs/{}".format(Stenographer))
            print("Directories made.")
        except OSError as error:
            if Stenographer not in list(os.listdir("Outputs")):
                print(error)
                print("Couldn't make directory {}.  continuing...".format(Stenographer))
        #try:
        plt.figure(figsize=(25, 8))
                                                #x = "indexx", y = "countt"
        ax = sns.barplot(data = leftMappingGrouped, x = leftMappingGrouped.index, y ="side").\
            set(
            title = "Initial Data Availablity\nleft Phoneme counts, {:,} datapoints from dictionary size of {:,} ({}'s dictionary)".
            format(len(EqualBothSides), len(Sourcedf), Stenographer)
            , xlabel = "Left Phonemes", ylabel = "count")
        plt.savefig("Outputs/{}/leftMapping-{}.png".format(
            Stenographer,
            str(dt.datetime.now())).replace(":", "-")
                    )
        ax = None
        plt.figure(figsize=(25, 8))

        ax = sns.barplot(data=midMappingGrouped, x=midMappingGrouped.index, y="side"). \
            set(
            title="Initial Data Availablity\nmid (vowel) Phoneme counts, {:,} datapoints from dictionary size of {:,} ({}'s dictionary)".
            format(len(EqualBothSides), len(Sourcedf), Stenographer)
            , xlabel="mid Phonemes", ylabel="count")
        plt.savefig("Outputs/{}/MidMapping-{}.png".format(
            Stenographer,
            str(dt.datetime.now())).replace(":", "-")
                    )

        ax = None
        plt.figure(figsize=(25, 8))

        ax = sns.barplot(data=rightMappingGrouped, x=rightMappingGrouped.index, y="side"). \
            set(
            title="Initial Data Availablity\nright Phoneme counts, {:,} datapoints from dictionary size of {:,} ({}'s dictionary)".
            format(len(EqualBothSides), len(Sourcedf), Stenographer)
            , xlabel="right Phonemes", ylabel="count")
        plt.savefig("Outputs/{}/RightMapping-{}.png".format(\
            Stenographer,
            str(dt.datetime.now())).replace(":", "-")
                    )


    # except:
    #     print("Couldn't make plots... continuing...")



    del Sourcedf, leftMappingGrouped, midMappingGrouped, rightMappingGrouped


    SyllableDictDF = SyllableAnalysis1.makeSyllableStenoDF(df, verbose=True)

    def SyllableGuess(df: pd.DataFrame, SyllableDF :pd.DataFrame = SyllableDictDF, verbose = False):
        """This takes the main dataframe or words to guess and uses the second param, SyllableDF, which is made
        with SyllableAnalysis.1 to look up and how syllables are written and try to guess words."""
        if verbose:
            print("Starting SyllableGuess")
        dfWithSyllables = df[df["syllables"].notnull()].copy()
        dfWithoutSyllables = df[df["syllables"].isnull()].copy()
        SyllableGuessColumnList = []
        for i in range(len(dfWithSyllables)):
            runningSteno, syllLookup = "", ""
            for syll in dfWithSyllables.iloc[i]['syllables']:
                try:
                    workingDF = SyllableDF[SyllableDF['syllable'] == syll]
                    if len(workingDF) > 0:
                        if len(set(workingDF["stroke"])) ==1:
                             syllLookup = list(workingDF["stroke"])[0]
                        else: #more than one way to write the syllable in dictionary:
                            tempDict = {}
                            for item in list(workingDF['stroke']):
                                CountingDict.CountingDictAdd(tempDict, item)

                            highScore = 0
                            highScorer = None
                            for item in tempDict:
                                if tempDict[item] > highScore:
                                    highScorer = item
                                    highScore = tempDict[item]

                            syllLookup = str(highScorer)
                    else:
                        syllLookup = None
                except:
                    syllLookup = None

                if syllLookup is not None and runningSteno is not None:
                    if len(runningSteno) >=1: #add space first for subsequent strokes
                        runningSteno += " " + syllLookup
                    else:
                        runningSteno += syllLookup
                else:
                    syllLookup = None
                    runningSteno = None
            SyllableGuessColumnList.append(runningSteno)
        SyllableGuessColumnList = [i.upper().strip() if type(i)==str else None for i in SyllableGuessColumnList]
        if verbose:
            print()
            print("{}% of words were able to be guessed at syllablically in {}"
                  "'s dictionary.".format(\
                round( ( (len([i for i in SyllableGuessColumnList if i is None]) / len(SyllableGuessColumnList)) *100),1),
                Stenographer
            )
            )


        dfWithSyllables['SyllableGuess'] = SyllableGuessColumnList

        dfWithoutSyllables['SyllableGuess'] = None

        df  = pd.concat([dfWithSyllables, dfWithoutSyllables], sort=False )
        return df


    df = SyllableGuess(df, verbose=True)

    df["SyllableGuessCorrect"] = df.apply(lambda x: x['Steno'] == x['SyllableGuess'], axis=1)
    print("{}%  of syllables guesses were correct for {}'s dictionary.".format( \
        round((len(df[df['SyllableGuessCorrect']==True]) / len(df[df['SyllableGuess'].notnull()]))*100,1), Stenographer
        ))

    def PhonemeGuess(df : pd.DataFrame, phoneticsDF : pd.DataFrame = makePhoneticMappingsRedoneDF, verbose = False):
        """This will guess the steno for given phonemes and return the same df with a PhonemeGuess Column.
        The first df param is the dataframe that has the user data, the second param is the phoneticsDF lookup df
        which came from makePhoneticMappingsRedone.  This function will return the same dataframe entered with new column."""
        if verbose:
            print("\nStarting PhonemeGuess...")

        dfWithPhonmes = df[df["Phonetics"].notnull()].copy()
        if verbose:
            print("There are {:,} entries with phonemes in {}'s dictionary to \"learn\" phonetics from.".format(len(dfWithPhonmes), Stenographer) )
        dfWithoutPhonemes = df[df["Phonetics"].isnull()].copy()

        PhoneticGuesses = []
        for i in range(len(dfWithPhonmes)):
            #First make phonetic Bataches
            phonetics = dfWithPhonmes.iloc[i]['Phonetics']
            currentlyConsonant, currentlyVowel = False, False
            phoneticBatches = []
            currentBatch = ""
            for phoneme in phonetics:
                if phoneme in Phonetics_Dict.phoneticConsanants:
                    if currentlyVowel:
                    # if currentlyVowel:
                        currentlyVowel = False
                        if len(currentBatch)>=1:
                            phoneticBatches.append(currentBatch) #append previous vowel batch, if any
                            currentBatch = ""
                    currentBatch+= phoneme
                    currentlyConsonant = True
                elif phoneme in Phonetics_Dict.phoneticVowels:
                    if currentlyConsonant:
                        currentlyConsonant = False
                        if len(currentBatch)>=1:
                            phoneticBatches.append(currentBatch) #append previous consonants batch, if any
                            currentBatch =""
                    currentBatch += phoneme
                    currentlyVowel = True
            if len(currentBatch) >=1:
                phoneticBatches.append(currentBatch)

            if phoneticBatches[0][0] in Phonetics_Dict.phoneticConsanants:
                wordStartsWithConsonant = True
                currentlyLeftPhoneticBatch = True
            else:
                wordStartsWithConsonant = False
                currentlyLeftPhoneticBatch = False

            #Then try to translate batches
            runningSteno = ""
            for batchNum in range(len(phoneticBatches)):
                stenoBatchToAdd = ""
                side = None
                tempBatches = None
                if batchNum==0 and phoneticBatches[batchNum][0] in Phonetics_Dict.phoneticConsanants:
                    side = 'left'
                elif batchNum == len(phoneticBatches)-1 and phoneticBatches[batchNum][0] in Phonetics_Dict.phoneticConsanants:
                    side = 'right'
                elif phoneticBatches[batchNum][0] in Phonetics_Dict.phoneticVowels:
                    side = 'mid'
                    currentlyLeftPhoneticBatch = False
                elif phoneticBatches[batchNum][0] in Phonetics_Dict.phoneticConsanants: #consonants

                    if len(phoneticBatches[batchNum]) % 2 == 0: #even num of consonants, usually 2
                        tempBatches =[]
                        tempBatches.append(phoneticBatches[batchNum][: (len(phoneticBatches[batchNum]) // 2) ])
                        tempBatches.append(phoneticBatches[batchNum][(len(phoneticBatches[batchNum]) // 2) :])
                    elif (len(phoneticBatches[batchNum]) ==3):
                        tempBatches = []
                        tempBatches.append(phoneticBatches[batchNum][0])
                        tempBatches.append(phoneticBatches[batchNum][1:])
                    elif (len(phoneticBatches[batchNum]) == 1 ):
                        #Short  vowels in the IPA are / ɪ / -pit, / e / -pet, / æ / -pat, / ʌ / -cut, / ʊ / -put, / ɒ / -dog, / ə / -about.
                        # Long vowels in the IPA # are / i: / -week, / ɑ: / -hard, / ɔ: / -fork, / ɜ: / -heard, / u: / -boot.
                        #Long vowels vs short vowels here.
                        if batchNum > 0 and  phoneticBatches[batchNum-1]  in ['ɪ','e', 'æ ', 'ʌ'  , 'ʊ' ,' ɒ', ' ə']:
                            side = 'right'
                        else:
                            side = 'left'
                            addNewStrokeSpace = True

#TODO loop through temp dicts if applicable, has to deal with breaking up consonant batches.

                if tempBatches is None: #no tempBatches, or splitting of batches, happened previously.
                    # So we'll take the one batch and put it in a list:
                    tempBatches = [phoneticBatches[batchNum]]
                # elif len(tempBatches)>1:
                #     if verbose:
                #         print("temp batches:\t{}".format(tempBatches))
                # else:
                #     if verbose:
                #         print("Shouldn't be here....") #This would mean temp batches is screwed up.
                previousSide = None
                for tempBatch in tempBatches:
                    if len(tempBatches) <= 1:
                        try:
                            workingDF = phoneticsDF[phoneticsDF[side + "Phonetics"] == phoneticBatches[batchNum]].copy()
                        except:
                            workingDF = None
                    elif(len(tempBatches) ==2):
                        if tempBatch == tempBatches[0]:
                            side = 'right'
                        elif tempBatch == tempBatches[1]:
                            side = 'left'
                            currentlyLeftPhoneticBatch = True
                        workingDF = phoneticsDF[phoneticsDF[side + "Phonetics"] == tempBatch].copy()
                    if workingDF is None or len(workingDF) <=0:
                        runningSteno = None
                    else:
                        tempDict = {}
                        for sten in list(workingDF[side+"Steno"]):
                            CountingDict.CountingDictAdd(tempDict, sten)
                        highScore = 0
                        highScorer = None
                        for steno in tempDict:
                            if tempDict[steno] > highScore:
                                highScorer = steno
                                highScore = tempDict[steno]
                    if runningSteno != None:
                        if highScorer != None:
                            #
                            if currentlyLeftPhoneticBatch == False and side == 'right': #This is my terrible attempt at multi-stroke steno
                                runningSteno += highScorer+ " "
                                currentlyLeftPhoneticBatch = True
                            elif batchNum > 0 and currentlyLeftPhoneticBatch and side == 'left':
                                runningSteno +=  " " + highScorer
                            elif previousSide != 'right' and side == 'mid'  and previousSide != None:
                                runningSteno += " " + highScorer
                            else:
                                runningSteno += highScorer


                            previousSide = copy.copy(side)
                        else:
                            runningSteno = None
                            previousSide = None
            PhoneticGuesses.append(runningSteno)

        fixedPhoneticGuesses = []
        for guess in PhoneticGuesses:
            if guess is None:
                fixedPhoneticGuesses.append(None)
            elif type(guess) is str:
                if guess[-1] == '\n':
                    guess = guess[:-1]
                guess = guess.replace("  ", " ")
                fixedPhoneticGuesses.append(guess)
            else:
                fixedPhoneticGuesses.append(guess)


        dfWithPhonmes['PhoneticGuesses'] = [i.upper().strip() if type(i) is str else None for i in fixedPhoneticGuesses]
        dfWithoutPhonemes['PhoneticGuesses'] = None

        df = pd.concat([dfWithPhonmes, dfWithPhonmes], sort = False )

        #for debugging:

        return df

    df = PhonemeGuess(df, makePhoneticMappingsRedoneDF, verbose = True)



    df['PhoneticGuessCorrect'] = df.apply(lambda x: x['Steno'] == x['PhoneticGuesses'], axis = 1)

    print("{:,} phonetic guesses were made and of those  {:,}  were correct  for {}'s dictionary.\n"
          "Only {}% of entries were able to to have a  phonetic guess made\n,"
          "and of those, {}% were correct.".format(
        len(df[df['PhoneticGuesses'].notnull() ].copy()),
        len(df[df['PhoneticGuessCorrect']==True].copy() ),
        Stenographer,
                round( (len(df[df['PhoneticGuesses'].notnull() ] ) / len(df) *100), 1),
                 round( ( len(df[df['PhoneticGuesses'].notnull() & df['Steno'].notnull()  &  df['PhoneticGuessCorrect'] ==True]) / len(df[df['PhoneticGuesses'].notnull() & df['Steno'].notnull() ].copy() ) ) *100 ,1 )
    ) )
    print("(Some guess were made even where phonetic information wasn't available from the phonetics dataset.\nThat's why these number might look a bit odd.)")

    # print("np.logical_and(df['NumStrokes'].notnull(), df['PhoneticGuesses'].notnull())")
    # print(np.logical_and(df['NumStrokes'].notnull(), df['PhoneticGuesses'].notnull()))
    # print()


    dfValidStrokesAndPhonetics = df[np.logical_and(df['NumStrokes'].notnull(), df['PhoneticGuesses'].notnull())].copy()
    dfValidStrokesAndPhonetics['NumStrokesPerPhonetics'] = dfValidStrokesAndPhonetics['PhoneticGuesses'].apply(lambda x: len([i for i in x if i == " "])+1 if x is not None else None )
    dfValidStrokesAndPhonetics['NumStrokesCorrect'] = dfValidStrokesAndPhonetics.apply(lambda x: x['NumStrokesPerPhonetics'] == x['NumStrokes'], axis = 1)

    dfInvalidStrokesOrPhonetics = df[np.logical_or(df['NumStrokes'].isnull(), df['PhoneticGuesses'].isnull())].copy()
    dfInvalidStrokesOrPhonetics['NumStrokesPerPhonetics'] = None
    dfInvalidStrokesOrPhonetics['NumStrokesCorrect'] = None



    if len(dfValidStrokesAndPhonetics)>1:
        # dfEqualStrokesAndPhonetics = dfEqualStrokesAndPhonetics[dfEqualStrokesAndPhonetics['NumStrokes'] == dfEqualStrokesAndPhonetics["PhoneticGuesses"].apply(lambda x: [i for i in x if i ==" "])]
        print("Of entries where the number of strokes (a proxy for syllables) was correct, {}% of guess were made correctly.".format( \
            round((len(
                dfValidStrokesAndPhonetics[ \
                    dfValidStrokesAndPhonetics['NumStrokesPerPhonetics']==True]) /
                   len(dfValidStrokesAndPhonetics) ) * 100, 1)
            )
        )
    else:
        print("Something wrong with dfEqualStrokesAndPhonetics, length is 0...")


    df = pd.concat([dfValidStrokesAndPhonetics, dfInvalidStrokesOrPhonetics], sort = False)

    quit()
