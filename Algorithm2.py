from typing import Union, Any

import pandas as pd
import BigOuterMerge
import FilterBeforeLogic
import WebsterMirriamFIle
import re
import ConsonantVowelStructure
import WordFrequency
import SplitPhoneticsAndSyllables

# def MakeStenoCVCs(strokeListParam, verbose = False):
#     """This function expects a list (of strokes) and returns a list
# 	of equal length with the ouput of the CVC algorithm."""
#     if type(strokeListParam) != list:
#         print("Expected a list here, got {}.  Rerturning None...".format(str(strokeListParam)))
#         return None
#     returningList = []
#     for i in strokeListParam:
#         if (ConsonantVowelStructure.getConsonantVowelStenoStructure(i) is None) and verbose:
#             print("Error evaluating {} in MakeStenoCVCs.".format(strokeListParam))
#         returningList.append(\
#             ConsonantVowelStructure.getConsonantVowelStenoStructure(i) )
#     if (len(returningList) >=1):
#         return returningList
#     else:
#         if verbose:
#             print ("There's no list return regarding {} in MakeStenoCVCs... returning None".format(strokeListParam))
#         return None
# def MakeStenoCVCs(x, verbose = False):
#     """This expects a list (of strokes) and returns a list ran through a cvc
#     algorithm, return the consonant-vowel structure of the Steno."""
#     if type(x) != list:
#         print("Expected a list here, got {}".format(str(x)))
#         return None
#     returningList = []
#     for i in x:
#         if (ConsonantVowelStructure.getConsonantVowelStenoStructure(i) is None) and verbose:
#             print("Error evaluating {}".format(x))
#         returningList.append(\
#             ConsonantVowelStructure.getConsonantVowelStenoStructure(i) )
#     if (len(returningList) >=1):
#         return returningList
#     else:
#         if verbose:
#             print ("Something went wrong with {} ...".format(x))
#         return None

# def MakeWordCVCs(x, verbose = False):
#     """This function expects a list of English syllables (from the syllables column) and returns a list ran through a vcv
#         algorithm and returns a string such as _vc meaning vowel-consonant"""
#     if type(x) != list:
#         if verbose:
#             print("Expected a list here in MakeWordCVCs, got {}  Returning None".format(str(x)))
#         return None
#     returningList = []
#     for i in x:
#         returningList.append(\
#             ConsonantVowelStructure.getConsonantVowelStringStructure(i)
#             )
#     if len(returningList) >=1:
#         return returningList
#     else:
#         if verbose:
#             print ("Something went wrong with {} in MakeWordCVCs".format(x))
#         return None
def MakeNestedStenoDict(SameLengthAndStructure, verbose = False):
    """Makes a nested dictionary with the outer dictionary as syllables
    and their keys as dictionaries with those keys being a possible
    way of writing it and  those values being the frequency of that particular
    writing..."""
    testy = {}  # this will be a nested dictionary
    syllablesList = list(SameLengthAndStructure['syllables'])
    strokesList = list(SameLengthAndStructure['Strokes'])
    wordsList = list(SameLengthAndStructure['Word'])
    if (len(syllablesList) == (len(strokesList))):
        for i in range(len(syllablesList)):  # go through each element in column
            for j in range(len(syllablesList[i])):  # go throug each syllable in syllables value
                if syllablesList[i][j] not in testy:
                    testy[syllablesList[i][j]] = {strokesList[i][j]: 1}
                    testy[syllablesList[i][j]]['explanations'] = []
                    testy[syllablesList[i][j]]['explanations'].append(
                        "{} written {}".format(wordsList[i], strokesList[i]))

                elif syllablesList[i][j] in testy:
                    testy[syllablesList[i][j]]['explanations'].append(
                        "{} written {}".format(wordsList[i], strokesList[i]))
                    if strokesList[i][j] not in testy[syllablesList[i][j]]:
                        testy[syllablesList[i][j]][strokesList[i][j]] = 1
                    else:
                        testy[syllablesList[i][j]][strokesList[i][j]] += 1
        return testy
    else:
        if verbose:
            print('these two lists should be the same length...')
            print("Retuning None...")
        return None

def makeResultsFromNestedStenoDict(dictParam):
    """Makes a simple dict with the key as an English Syllable
     and the most likely steno Stroke as the value."""
    results = {}
    for i in dictParam:
        currentMax=0
        currentStroke=""
        for k in dictParam[i]:
            if k !='explanations':
                if (dictParam[i][k] > currentMax):
                    currentMax = dictParam[i][k]
                    currentStroke = k
        results[i] = currentStroke
    return results





#_________________________________________________

if __name__ == '__main__':
    import NoahAndChrisTesting
    import pandas as pd
    Noahdf = NoahAndChrisTesting.NoahDF.copy()
    #noahdf['word'] = noahdf['Translation']
    #Noahdf = pd.merge(noahdf , WebsterMirriamFIle.WebstersDF, how = 'inner', on = 'word')
    Noahdf = BigOuterMerge.BigOuterMerge(Noahdf)
    Noahdf = FilterBeforeLogic.filter1(Noahdf)
    Noahdf, _, __ = SplitPhoneticsAndSyllables.SplitDF(Noahdf)
    del _, __
    #print(Noahdf.head())
    #
    # shortForms = Noahdf[(
    #     (Noahdf['Strokes'].apply(lambda x: len(x) ) <2)
    #     &
    #     (Noahdf['syllables'].apply(lambda x: len(x) ) >=3)
    # )]

    # print(Noahdf.columns)
    # print(type(Noahdf.columns))
    #
    #df.rename(columns= {
    #    i for i in df.columns : i for i in df.columns
    #}, inplace=True)

    print()
    # The following few lines might be superfluous, consider deleting.

    Noahdf.dropna(subset = ['syllables'], inplace = True) #just added

    import MakeColumnsForAnalysis
    Noahdf = MakeColumnsForAnalysis.firstSyllablesColumn(Noahdf)
    # Noahdf['firstSyllable'] = Noahdf['syllables'].apply( lambda  x: x[0].upper())
    # Noahdf['identicalFirstStroke'] = Noahdf.apply(lambda x: True if  x["Strokes"][0] == x["firstSyllable"] else False, axis = 1)

    Noahdf = MakeColumnsForAnalysis.syllablesPerStrokeColumn(Noahdf)

    #Noahdf['syllablesPerStroke'] = Noahdf.apply(lambda x:  len(x['syllables'] )  / len(x['Strokes'] )  , axis = 1)

    identicals = Noahdf[Noahdf['identicalFirstStroke'] == True ]

    #I don't know that the following are ever used?  They're just in __main__:
    cvc = "^[STKPWHR]+[AEOU]+[FRrPpBTLGtSsDZ]+$"
    cv = "^[STKPWHR]+[AEOU]+$"
    vc = "^[AEOU]+[FRrPpBLGTtSsDZ]+$"

    # Noahdf ['firstStrokePattern'] = Noahdf.apply(
    #     lambda x: "cvc" if re.match(cvc, x['Strokes'][0]) != None
    #     else("cv" if re.match(cv, x['Strokes'][0]) != None  else(
    #     ("vc" if re.match(vc, x['Strokes'][0]) != None  else "-") ) )
    #     , axis = 1)
    #import MakeColumnsForAnalysis
    Noahdf = MakeColumnsForAnalysis.addStructureCols(Noahdf)

    # Noahdf["StenoCVCStructure"] = Noahdf['Strokes'].apply(lambda x: ConsonantVowelStructure.MakeStenoCVCs(x))
    # Noahdf["WordCVCStructure"] = Noahdf["syllables"].apply(lambda x: ConsonantVowelStructure.MakeWordCVCs(x))
    # Noahdf['SameLengthStrokesAndSyllables'] = Noahdf.apply(lambda x: len(x['Strokes']) == len(x['syllables']) , axis = 1 )
    Noahdf["EqualStructure"] = Noahdf.apply(lambda x :True if x["WordCVCStructure"] == x["StenoCVCStructure"] else False, axis = 1 ) #TODO handle consonants

    # def duplicateDetectorColumnMaker(x): #Noah's confused himself!  It's super effective!
    #     """I don't remember the purpose of this function.  It seems to make a column that
    #     will subsequently run drop_duplicates on..."""
    #     returnList = []
    #     returnList.append(x['Strokes'])
    #     returnList.append(x['Word'])
    #     return returnList
    #
    # Noahdf['DuplicateDetector'] = Noahdf.apply(lambda x :duplicateDetectorColumnMaker(x), axis = 1)

    SameLengthAndStructure = Noahdf[(Noahdf['EqualStructure']==True ) & (Noahdf['SameLengthStrokesAndSyllables'] ==True) ].reset_index()

    # testy = {}  # this will be a nested dictionary
    # syllablesList = list(SameLengthAndStructure['syllables'])
    # strokesList = list(SameLengthAndStructure['Strokes'])
    # wordsList = list(SameLengthAndStructure['word'])
    # if (len(syllablesList) == (len(strokesList))):
    #     for i in range(len(syllablesList)):  # go through each element in column
    #         for j in range(len(syllablesList[i])):  # go throug each syllable in syllables value
    #             if syllablesList[i][j] not in testy:
    #                 testy[syllablesList[i][j]] = {strokesList[i][j]: 1}
    #                 testy[syllablesList[i][j]]['explanations'] = []
    #                 testy[syllablesList[i][j]]['explanations'].append(
    #                     "{} written {}".format(wordsList[i], strokesList[i]))
    #
    #             elif syllablesList[i][j] in testy:
    #                 testy[syllablesList[i][j]]['explanations'].append(
    #                     "{} written {}".format(wordsList[i], strokesList[i]))
    #                 if strokesList[i][j] not in testy[syllablesList[i][j]]:
    #                     testy[syllablesList[i][j]][strokesList[i][j]] = 1
    #                 else:
    #                     testy[syllablesList[i][j]][strokesList[i][j]] += 1



    NoahNestedStenoDict1 = MakeNestedStenoDict(SameLengthAndStructure)

    #results will store the most common stenographic interpretation of a syllable
    results = makeResultsFromNestedStenoDict(NoahNestedStenoDict1)
    # results = {}
    # for i in NoahNestedStenoDict1:
    #     currentMax=0
    #     currentStroke=""
    #     for k in NoahNestedStenoDict1[i]:
    #         if k !='explanations':
    #             if (NoahNestedStenoDict1[i][k] > currentMax):
    #                 currentMax = NoahNestedStenoDict1[i][k]
    #                 currentStroke = k
    #     results[i] = currentStroke


    ## guessing, to be a seprate class
    wordsToGuess = list(WebsterMirriamFIle.WebstersDF['Word'])
    NoahWords = list(Noahdf['Word'])
    print("Making wordsToGuess... takes a moment...")
    wordsToGuess = [ i for i in wordsToGuess if i not in NoahWords]

    Noahdf['SyllableDifference'] = Noahdf.apply( lambda x:  len(x['Strokes']) - len(x['syllables']) , axis = 1)

    guesses = pd.DataFrame({"Word":wordsToGuess} )
    guesses = pd.merge(guesses, WebsterMirriamFIle.WebstersDF, how = 'left', on = 'Word')

    def Guess(ListOfSyllables, answerKey = results, verbose = False):
        """This function will return a guess when given a list of  syllables and the answerKey.
        The answerKey is supposed to be a dictionary that has keys as the syllable and values
        of the most likely steno translation of that syllable.m"""
        guesses = []
        for i in ListOfSyllables:
            if i in answerKey:
                guesses.append(answerKey[i])
            else:
                if verbose:
                    print("{} from {} not in answerKey, returning None.".format(i, ListOfSyllables))
                    print("Returning None")
                return None #consider returning helper string here...
        return guesses

    guesses['Guess'] = guesses['syllables'].apply(lambda x: Guess(x))
    #
    # this will save the subset of syllables that were not guessed because a syllable was not in the results dict
    unableToGuess = guesses[guesses['Guess'].isnull()]
    unableToGuess = pd.merge(unableToGuess, WordFrequency.WordFreq, how='left', on="Word")

    guesses.dropna(subset= ["Guess"] , inplace=True)

    guesses = guesses.drop_duplicates(subset=["Word"] ).reset_index()


    guesses = pd.merge(guesses, WordFrequency.WordFreq, how = 'left', on = "Word")
    guesses.rename(columns = {"count":"Frequency_Count"})




    print()
    print()