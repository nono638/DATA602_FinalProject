import numpy as np

import ConsonantVowelStructure
import pandas as pd
import PhoneticStructure
import CountingDict

def NumStrokesColumn(df, verbose=False):  #not yet used
    if "Strokes" in df.columns.tolist():
        dfWithoutStrokes = df[df['Strokes'].isnull()].copy(deep = True)
        dfWithoutStrokes['NumStrokes'] = np.NaN #Set it to NaN because the others will be numbers.  Don't use None
        df = df[df['Strokes'].notnull()].copy(deep = True)
        df["NumStrokes"] = df["Strokes"].apply(lambda x: len(x) if type(x) == list else None)
        if verbose:
            print("The average number of strokes per entry is {}.".format( round(np.mean(np.array(df['NumStrokes'])),1) ) )
            print("The median number of strokes per entry is {}.".format( round(np.mean(np.median(df['NumStrokes']))) ))
        df = pd.concat([df, dfWithoutStrokes], sort= False)
    elif verbose:
        print("No steno column, unable to make NoStrokes Column...")
    return df

def addStructureCols(df, verbose = False):
    """This function adds Structure Columns to an existing dataframe that has been filterred1 already.
    It takes a dataframe as input and returns the same dataframe as output """
    if "Strokes" in df.columns.tolist():
        df["StenoCVCStructure"] = df['Strokes'].apply(lambda x: ConsonantVowelStructure.MakeStenoCVCs(x))

        if "syllables" in df.columns.tolist(): # syllables and strokes, notice indentation
            df["WordCVCStructure"] = df["syllables"].apply(lambda x: ConsonantVowelStructure.MakeWordCVCs(x) if x is not None else None)

            df["EqualStructureWithSyllables"] = df.apply(
                lambda x: True if x["WordCVCStructure"] == x["StenoCVCStructure"] else False,
                axis=1)  # TODO handle consonants... what does this TODO mean again?
            #break up the df into two parts and then recombine...

            dfWithStrokesAndSyllables = df[df['Strokes'].notnull() & df['syllables'].notnull() ].copy()
            dfWithStrokesAndSyllables['SameLengthStrokesAndSyllables'] = dfWithStrokesAndSyllables.apply(lambda x: len(x['Strokes']) == len(x['syllables']) , axis=1)

            dfWithoutStrokesAndSyllables = df[df['Strokes'].isnull() | df['syllables'].isnull()].copy()
            dfWithoutStrokesAndSyllables['SameLengthStrokesAndSyllables'] = None

            df = pd.concat([dfWithStrokesAndSyllables, dfWithoutStrokesAndSyllables], sort = False)
        elif(verbose):
            print("Expected syllables column in addStructureCols.")
    elif(verbose):
        print("Expected Strokes Column in addStructureCols.")

    if "Phonetics" in df.columns.tolist():
        df = PhoneticStructure.AddPhoneticStructureColumn(df, verbose= verbose)
    elif(verbose):
        print("Expected Phonetics Column in addStructureCols.")
    return df

def firstAndLastSyllablesColumn(df, verbose = False):
    """Adds a first and last
    syllable column to a dataframe and identical first stroke which sees if the first stoke is identical. """
    if verbose:
        print("Starting firstAndLastSyllablesColumn...")
    if "syllables" in df.columns.tolist() and "Strokes" in df.columns.tolist():

        dfWithSyllables = df[df['syllables'].notnull()].copy()
        if len(dfWithSyllables) >0 :

            dfWithSyllables['firstSyllable'] = dfWithSyllables.loc[: , 'syllables'].apply(lambda x: x[0])
            dfWithSyllables['lastSyllable'] = dfWithSyllables.loc[: , 'syllables'].apply(lambda x: x[-1])

            dfWithSyllablesAndStrokes = dfWithSyllables[dfWithSyllables['Strokes'].notnull()].copy()
            dfWithSyllablesButWithoutStrokes = dfWithSyllables[dfWithSyllables['Strokes'].isnull()].copy()

            dfWithSyllablesAndStrokes['identicalFirstStroke'] = dfWithSyllablesAndStrokes.apply(
                lambda x: True if x["Strokes"][0].lower() == x["firstSyllable"].lower() else False, axis=1)
            dfWithSyllablesAndStrokes['identicalLastStroke'] = dfWithSyllablesAndStrokes.apply(
                lambda x: True if x["Strokes"][-1].lower() == x["lastSyllable"].lower() else False, axis=1)

            dfWithSyllables = pd.concat([dfWithSyllablesAndStrokes, dfWithSyllablesButWithoutStrokes ])

            dfWithoutSyllables = df[df['syllables'].isnull()].copy()

            df= pd.concat([dfWithoutSyllables, dfWithSyllables], sort=False)

    elif(verbose):
        print("Expected syllables and Strokes Column in firstSyllablesColumn.")
    return  df


def syllablesPerStrokeColumn(df, verbose = False):
    """adds both a syllable per stroke Column and a syllableStrokeDifference to a dataframe that has a syllables column.
    Expects a dataframe as input and outputs a dataframe."""
    if verbose:
        print("Starting syllablesPerStrokeColumn...")
        print("first row of paramater entered:")
        print(str(df.iloc[0]))
    if "syllables" in df.columns.tolist() and "Strokes" in df.columns.tolist():
        dfWithSyllablesAndStrokes = df[np.logical_and(df["syllables"].notnull() , df['Strokes'].notnull() )].copy()

        if len(dfWithSyllablesAndStrokes) > 0:
            dfWithSyllablesAndStrokes['syllablesPerStroke'] = dfWithSyllablesAndStrokes.apply(lambda x: round(len(x['syllables']) / len(x['Strokes']),2), axis=1)
            dfWithSyllablesAndStrokes['syllableStrokeDifference'] = dfWithSyllablesAndStrokes.apply(lambda x: round(len(x['Strokes']) - len(x['syllables']),2), axis=1)

            dfWithoutSyllablesOrStrokes = df[np.logical_or(df["syllables"].isnull() , df['Strokes'].isnull() )].copy()

            df = pd.concat([dfWithSyllablesAndStrokes, dfWithoutSyllablesOrStrokes], sort= False)
    elif verbose:
        print("No 'syllables' and/or 'Strokes' column, not able to add 'syllablesPerStroke' Column.")
        print("returning the dataframe as is....")
    return df

def doAll(df, verbose = False):
    if verbose:
        print("Starting MakeColumnsForAnalysis.doall ...")
    df = syllablesPerStrokeColumn( NumStrokesColumn(df, verbose= verbose), verbose=verbose)
    df = firstAndLastSyllablesColumn(df, verbose= verbose)
    df = addStructureCols(df, verbose= verbose)
    df = NumStrokesColumn(df, verbose=True)
    return df

if __name__ == '__main__':
    import NoahAndChrisTesting, BigOuterMerge, FilterBeforeLogic, SplitPhoneticsAndSyllables

    TestDF = NoahAndChrisTesting.NoahDF
    TestDF = FilterBeforeLogic.filter1(BigOuterMerge.BigOuterMerge(TestDF), verbose= True)

    print("first break point...")
    #ChrisBoth, ChrisSyllablesOnly, ChrisPhoneticsOnly = SplitPhoneticsAndSyllables.SplitDF(ChrisDF)
    #ChrisBoth = TestDF.copy(deep=True)
    TestDF = NumStrokesColumn(
        syllablesPerStrokeColumn(
            firstAndLastSyllablesColumn(
                addStructureCols(TestDF)
            )
        )
    )


    print("about to close...")
    quit()