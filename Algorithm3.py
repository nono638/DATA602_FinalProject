import pandas as pd
import MakeColumnsForAnalysis

import BigOuterMerge
import FilterBeforeLogic
import Phonetics_Dict
import SplitPhoneticsAndSyllables
import WordFrequency
import PhoneticStructure
import StenoSides

if __name__ == '__main__':
    import NoahAndChrisTesting

    Sourcedf = NoahAndChrisTesting.FranceneDF

    Sourcedf = BigOuterMerge.BigOuterMerge(Sourcedf)
    WordsToGuess = Sourcedf.copy(deep=True)

    Sourcedf = FilterBeforeLogic.filter1(Sourcedf, verbose = True)
    SourceBoth, SourceSyllablesOnly, SourcePhoneticsOnly = SplitPhoneticsAndSyllables.SplitDF(Sourcedf)
    SourceBoth = PhoneticStructure.AddPhoneticStructureColumn(SourceBoth)
    SourceBoth = MakeColumnsForAnalysis.addStructureCols(SourceBoth)
    SourcePhoneticsOnly = PhoneticStructure.AddPhoneticStructureColumn(SourcePhoneticsOnly) #lol why are the different functions here
    SourcePhoneticsOnly = MakeColumnsForAnalysis.addStructureCols(SourcePhoneticsOnly)

    WordsToGuess = WordsToGuess.drop(Sourcedf.index)


    #WordsToGuess = WordsToGuess.drop(WordsToGuess[~WordsToGuess.Steno.isnull()].index)
    WordsToGuess = WordsToGuess.drop(WordsToGuess[WordsToGuess.Steno.notnull()].index)

    WordsToGuess.drop(["Steno", "Translation", "Strokes"], axis = 1, inplace=True)
    WordsToGuess = pd.merge(WordsToGuess, WordFrequency.WordFreq, how ='left', on ='Word')
    WordsToGuess.drop_duplicates(subset='Word', inplace = True)

    WordsToGuessBoth, WordsToGuessSyllablesOnly, WordsToGuessPhoneticsOnly = SplitPhoneticsAndSyllables.SplitDF(WordsToGuess)

    EqualSidesBoth = SourceBoth[SourceBoth["EqualStructureWithSyllables"] == True]
    #EqualSides.drop(["Special"], inplace=True)

    vowelsPhonemesDict = {}
    for i in  Phonetics_Dict.phoneticVowels:
        vowelsPhonemesDict[i] = 0

    for i in range(len(EqualSidesBoth)):
        for j in EqualSidesBoth.iloc[i]["Phonetics"]:
            if j in vowelsPhonemesDict:
                vowelsPhonemesDict[j] +=1

    import StenoSides
    EqualSidesBoth['left'] = EqualSidesBoth["Strokes"].apply(lambda x: StenoSides.getLeftKeys(x) )
    EqualSidesBoth['mid'] = EqualSidesBoth["Strokes"].apply(lambda x: StenoSides.getVowelKeys(x))
    EqualSidesBoth['right'] = EqualSidesBoth["Strokes"].apply(lambda x: StenoSides.getRighttKeys(x))
    EqualSidesBoth['leftmidright'] = EqualSidesBoth.apply(lambda x : [[i for i in x['left'] ],[i for i in x['mid']],[i for i in x['right']]], axis = 1)

    #EqualSidesBoth["PhoneticsGuess"] = EqualSidesBoth.apply(lambda x: blah if len(x['Syllables'])==1 else None)
    import GuessPhonemes

    leftMapping1, midMapping1, rightMapping1 = GuessPhonemes.PhoneticsFirstPass(EqualSidesBoth)
    #leftMapping1.drop("side", axis = 1, inplace=True)
    #leftGrouped = leftMapping1.groupby('leftPhoneme')
    #leftGroupedCount = leftGrouped.value_counts()
    # print()
    # print(leftGrouped.size().unstack(fill_value=0) )

    leftPhoneticResults ={}
    midPhoneticResults ={}
    rightPhoneticResults = {}
    import CountingDict
    for i in range (len (leftMapping1)):
        phoneme = leftMapping1.iloc[i]["leftPhoneme"]
        stroke = leftMapping1.iloc[i]['leftStroke'][0]
        if (phoneme == "_"):
            continue
        if phoneme not in leftPhoneticResults:
            leftPhoneticResults[phoneme] = {}
        CountingDict.CountingDictAdd(leftPhoneticResults[phoneme], stroke)
    print('left done...')

    for i in range(len(midMapping1)):
        phoneme = midMapping1.iloc[i]["midPhoneme"]
        stroke = midMapping1.iloc[i]['midStroke'][0]
        if (phoneme == "_"):
            continue
        if phoneme not in midPhoneticResults:
            midPhoneticResults[phoneme] = {}
        CountingDict.CountingDictAdd(midPhoneticResults[phoneme], stroke)
    print('mid done...')


    for i in range (len (rightMapping1)):
        phoneme = rightMapping1.iloc[i]["rightPhoneme"]
        stroke = rightMapping1.iloc[i]['rightStroke'][0]
        if (phoneme == "_"):
            continue
        if phoneme not in rightPhoneticResults:
            rightPhoneticResults[phoneme] = {}
        CountingDict.CountingDictAdd(rightPhoneticResults[phoneme], stroke)

    leftAnswers, midAnswers, rightAnswers = GuessPhonemes.MakeStenoAnswers(leftPhoneticResults, midPhoneticResults, rightPhoneticResults)

    guessesPhoneticsBoth = SourceBoth.copy(deep = True)
    PhoneticBatches = GuessPhonemes.MakePhoneticBatches(guessesPhoneticsBoth,
                                                             leftAnswers, midAnswers, rightAnswers, verbose= True)

    guessesPhoneticsBoth['phoneticBatces'] = PhoneticBatches
    Phonetic_Guesses, problems = GuessPhonemes.GuessPhonemesStep2(PhoneticBatches,
                                                             leftAnswers, midAnswers, rightAnswers, verbose= True)


    guessesPhoneticsBoth['guess'] = [i.upper() if type(i)==str else None for i in Phonetic_Guesses]

    guessesPhoneticsBoth["is_correct"] = guessesPhoneticsBoth.apply(lambda x : x["guess"] == x["Steno"], axis = 1)

    guessesPhoneticsBoth = guessesPhoneticsBoth[guessesPhoneticsBoth['guess'].notnull()]
    guessesPhoneticsBoth = guessesPhoneticsBoth[guessesPhoneticsBoth['guess'] != "@@"]


    actualGuesses = WordsToGuessBoth.copy(deep = True)
    PhoneticBatchesActual = GuessPhonemes.MakePhoneticBatches(actualGuesses,
                                                              leftAnswers, midAnswers, rightAnswers)

    ActualGuesses , problemsActual = GuessPhonemes.GuessPhonemesStep2(PhoneticBatchesActual,
                                                                      leftAnswers, midAnswers, rightAnswers)
    actualGuesses['guess'] = ActualGuesses

    actualGuesses = actualGuesses[ actualGuesses['guess'].notnull() ]
    actualGuesses = actualGuesses[actualGuesses['guess'] != "@@"]


    print("The percent guessed correctly was {}.".format(
        len(guessesPhoneticsBoth[guessesPhoneticsBoth['is_correct'] == True])
        / len (guessesPhoneticsBoth)))

    print()
