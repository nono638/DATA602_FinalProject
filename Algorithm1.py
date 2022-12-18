import pandas as pd
import Phonetics_Dict

def SyllableGuess(x, verbose = False):
    """This function will make a column to guess at the number of syllables in a word, which would be the amount of steno strokes.
    My initial idea is to look at vowel patches, then, with the exception of the first and final group of sylables,
    divide the in-between syllables by 2 and assign them to the prveious or following syllable accordingly.

    NOTE:  I Never got this completely working, I think it's borderline impossible to get it to 100%
    Reread code and use with caution..."""


    inVowelPatch = False
    VowelPatches = [] # perhaps key will be vowel patch and value will be index in string, TODO
    ConsanantPatches = []
    syllables = []

    consonantPatch = ''
    currentVowelPatch = ''
    for i in x:
        if (i in Phonetics_Dict.toRemove): # 'ˌ' whatever that is?? TODO

            continue #this skips nonsense phonemes
        if ((i in Phonetics_Dict.phoneticVowels) and (inVowelPatch == False) ): #new vowel patch
            inVowelPatch = True
            if (consonantPatch != ''):
                ConsanantPatches.append(consonantPatch)
                syllables.append(ConsanantPatches[-1])
                consonantPatch = ""
            currentVowelPatch += i
        elif (i in Phonetics_Dict.phoneticVowels and inVowelPatch == True): #continuing vowel patch
            currentVowelPatch += i
        else: #consanants
            consonantPatch+= i
            inVowelPatch = False
            if currentVowelPatch != "":
                VowelPatches.append(currentVowelPatch)
                syllables.append( VowelPatches[-1] )
                currentVowelPatch = ""



    #final append, get the last bunch appended to sylablles:
    if (currentVowelPatch != ""):
        syllables.append(currentVowelPatch)
    elif (consonantPatch != ""):
        syllables.append(consonantPatch)

    for i in range(len(syllables)):
        if syllables[i][0] in Phonetics_Dict.phoneticVowels: #vowel
            pass #TODO
        else: #consanant
            pass #TODO




    return syllables

    # vowelHit = False
    # leftSide = True
    # leftConsanantCount = 0
    # rightConsanantCount = 0
    # vowelCount = 0
    # syllableCount = 0
    # syllables = {'syllables': [], 'leftSides': [], 'rightSides': []}
    # vowelPatches = 0


    # for i in x:
    #     if i in Phonetics_Dict.phoneticVowels and leftSide == True:
    #         leftSide = False
    #         vowelHit = True
    #         vowelCount +=1
    #     elif i in Phonetics_Dict.phoneticVowels and leftSide == False and vowelHit == True:
    #         leftSide = True
    #         vowelCount += 1
    #     elif (leftSide):
    #         leftConsanantCount += 1
    #         syllables["leftSides"].append(i)
    #     else: #right side
    #         rightConsanantCount +=1




if __name__ == '__main__':
    import NoahAndChrisTesting
    import Phonetics_Dict
    import FilterBeforeLogic

    # print(Phonetics_Dict.phoneticSymbolSet)
    # print()
    # print(Phonetics_Dict.phoneticVowels)
    #
    # print(NoahAndChrisTesting.NoahDF.iloc[4444:4455, :3])

    df1 = (NoahAndChrisTesting.NoahDF)
    #df = Phonetics_Dict.MakePhoneticsDF(df)
    import StenoPhoneticsDF
    df1 = StenoPhoneticsDF.makeDF(df1)
    df1 = FilterBeforeLogic.filter1(df1, verbose=True)
    df1.dropna(subset = ['Phonetics'], inplace=True)
    print(df1.columns.tolist())
    print("Phonetics" in df1.columns.tolist())

    df1['syllable_parts'] = df1['Phonetics'].apply(lambda x: SyllableGuess(x))
    import SylllableAlgorithm
    df1['syllable_Guess']  = df1['syllable_parts'].apply(lambda x : SylllableAlgorithm.makeSyllablesFromBatches(x))
    print(df1.head())
    ThreeOrFewerSyllablesDF = df1[df1['syllable_parts'].apply(lambda x: len(x)) <= 3]
    print()
    print(ThreeOrFewerSyllablesDF.head())
    print(len(ThreeOrFewerSyllablesDF))



    #wrongGuesses = df1[df1['syllable_Guess'] != ]
    print()
