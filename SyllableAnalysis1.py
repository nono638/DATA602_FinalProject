import pandas as pd



def makeSyllableStenoDF(df, verbose = False):
    """This function will make a dataframe that contains how a syllable is written from English syllable to Steno.
    It expects a dataframe that has been through the MakeColumns for Analysis functions.
    It expects a 'EqualStructureWithSyllables' column.  It will use that subset of data to map Strokes to syllables"""
    if verbose:
        print("Starting makeSyllableStenoDF...")
    if 'EqualStructureWithSyllables' not in df.columns.tolist():
        if verbose:
            print("Expected a 'EqualStructureWithSyllables' column to perform makeSyllableStenoDF.  Returning df as is....")
        return df
    dfSameLengthStrokesAndSyllables = df[df['EqualStructureWithSyllables'] == True]
    dfDifferentLengthStrokesAndSyllables = df[df['EqualStructureWithSyllables'] != True]

    syllablesList =[]
    strokesList = []
    wordList =[]

    for i in range(len(dfSameLengthStrokesAndSyllables)):
        syllables = dfSameLengthStrokesAndSyllables.iloc[i]['syllables']
        strokes = dfSameLengthStrokesAndSyllables.iloc[i]['Strokes']
        word = dfSameLengthStrokesAndSyllables.iloc[i]['Word']
        for syllable in syllables:
            syllablesList.append(syllable) #expects python 3.8 or greater, ordered dictionaries
        for stroke in strokes:
            strokesList.append(stroke)
        for j in range(len(strokes)):
            wordList.append(word)
    return pd.DataFrame({"stroke": strokesList,
                         "syllable":syllablesList,
                         'word':wordList})

class StenoSyllableMapping:
    """This class is going to be the keys for a dictionary that's a list of English syllables and how they're written in Steno"""
    def __int__(self, syllable, stenoList):
        self.stenoList = stenoList
        self.words = words #should be the list of words
        self.syllable = syllable



    def __repr__(self):  #??possibly right??
        return self.syllable

# def flipKeysAndValues(dictParam):
#     returningDict = {}
#     for item in dictParam.items():
#         returningDict



def getNthSyllableResult(targetSyllable : str, syllableDict : dict, rank = 1, returnWords = False,  verbose = False):
    """This function is to be used right after makeSyllableStenoDF.  It will get all the instances of the target syllable
    and return the nth ranked one.  Default is rank 1 which means the most common Steno outline denoting that
    syllable.  If you enter a rank greater than the number of possible options, it returns  the lowest rank one now.  I might
    consider changing that to a paramater to return None instead..."""

    #validation:
    if type(targetSyllable) is str:
        targetSyllable = targetSyllable.lower()
    else:
        if verbose:
            print('targetSyllable, {}, isn\'t a string.  Returning None...'.format(targetSyllable))
        return None
    workingDF = syllableDict.get(targetSyllable, None)  # expecting a dataframe as key if it's in the dict
    if workingDF is None:
        if verbose:
            print("Unable to find {} in the syllableDict, returning None...".format(targetSyllable))
        return None
    elif (type(workingDF) is not pd.DataFrame):
        if verbose:
            print("Expected the return value of syllabledict[{}] to be a dataframe..  Instead it's a {}.  Returning None...".format(
                targetSyllable, str(type(workingDF))
            ))
        return None
    elif "stroke" not in workingDF.columns.tolist():
        if verbose:
            print("Expected 'stroke' column in the syllableDict value(), returning none..." )
        return None

    # meat and potatoes:
    possibleStrokes = set(workingDF['stroke'])

    StrokesCountsDict = {}
    for i in range(len(workingDF)):
        CountingDict.CountingDictAdd(StrokesCountsDict,
                                     workingDF.iloc[i]['stroke'])

    workingDF['count'] = workingDF['stroke'].apply(lambda x: StrokesCountsDict[x])


    #workingDF['count'] = workingDF.apply(lambda x: len(x[x['stroke'] == ])) #I think this makes a count column that should be the count of the instances of that stroke in the dataframe

    possibleCounts = sorted(set(workingDF['count'])) #sorted in ascending order by default, lowest to highest


    if (rank > len(possibleStrokes)):
        if verbose:
            print("The rank you entered, {}, is greater than the amount of possibilities.  There are {} possible options for {}.".format(
              rank, len(possibleStrokes), targetSyllable))
            print("Therefore, we're returning the last choice for {} which is {}".
                  format(targetSyllable,
                         list(set(workingDF[workingDF['count'] == possibleCounts[0] ]['stroke']) )[0] )  )
            #TODO consider returning false here or making it a param option
        return list(set(workingDF[workingDF['count']==possibleCounts[0] ] ['stroke']) )[0]

    elif (rank <= len(possibleCounts) and rank >=1):
        return list(set(workingDF[workingDF['count'] == possibleCounts[rank*-1] ] ['stroke'] ))[0] #fix

    elif rank <1:
        if verbose:
            print("Invalid rank entered, {}.  Enter a rank 1 or higher.  Returning None...".format(rank))
        return None


if __name__ == '__main__':
    import NoahAndChrisTesting, MakeColumnsForAnalysis, BigOuterMerge, FilterBeforeLogic, CountingDict
    testDF = NoahAndChrisTesting.ChrisDF
    testDF = FilterBeforeLogic.filter1(
        BigOuterMerge.BigOuterMerge(testDF), verbose= True )
    testDF = MakeColumnsForAnalysis.doAll(testDF, verbose= True)


    syllableToStenoResultDF = makeSyllableStenoDF(testDF, verbose=True)

    SyllableMappings = {}
    for syllable in set(syllableToStenoResultDF['syllable']):
        SyllableMappings[syllable] = syllableToStenoResultDF[syllableToStenoResultDF['syllable'] == syllable]

    #
    # testCal = getNthSyllableResult('cal', SyllableMappings, verbose=True )
    # print('--------------------')
    # testCal2 = getNthSyllableResult('cal', SyllableMappings, rank=2, verbose=True)
    #
    # print('--------------------')
    # print('--------------------')
    #
    testSyllable = 'est'.lower()
    testal = getNthSyllableResult(testSyllable, SyllableMappings, verbose=True)
    print("{} primarily written as {}".format(testSyllable, testal))
    print('--------------------')
    testal2 = getNthSyllableResult(testSyllable, SyllableMappings, rank=2, verbose=True)
    print("{} secondarily written as {}.".format(testSyllable, testal2))

    quit()