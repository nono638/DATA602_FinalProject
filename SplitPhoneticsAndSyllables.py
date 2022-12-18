import numpy as np



def SplitDF(dfParam, verbose = False ):
    """This function will take a dataframe from FilterBeforeLogic and
    split it into a syllable based section and a syllable based section.
    This function will drop steno outlines for which there's neither phonetics nor syllabic information.

    This function outputs THREE dataframes:

    The first is Both syllables and Phonetics

    The second in the ONLY syllablesDF (no phonetic information).

    The third  is the only  PhoneticsDF (no syllable information)"""

    # Basic validation:
    if "Steno" not in dfParam.columns.tolist() and verbose:
        print("Expected Steno Column")
        try:
            return None, None, None
        except:
            return None
    elif "syllables" not in dfParam.columns.tolist() and verbose:
        print("Expected syllables column...")
        try:
            return None, None, None
        except:
            return None
    elif  "Phonetics" not in dfParam.columns.tolist() and verbose:
        print("Expected Phonetics Column...")
        try:
            return None, None, None
        except:
            return None
    else:
        #dfParam.dropna(subset= ["Steno", "Translation"], inplace=True) #this should have been done in FiterBeforeLogic, duplicative,. possibly erase.

        BothDF =  dfParam[np.logical_and (dfParam['syllables'].notnull() , dfParam["Phonetics"].notnull() )]

        syllableOnlyDF = dfParam[np.logical_and (dfParam['syllables'].notnull() , dfParam["Phonetics"].isnull() )]

        phoneticsOnlyDF = dfParam[np.logical_and (dfParam['syllables'].isnull() , dfParam["Phonetics"].notnull() )]

        phoneticsOnlyDF.drop(labels = ["syllables", "syllablesRaw", "definition"], axis = 1, inplace= True)
        syllableOnlyDF.drop('Phonetics', axis=1, inplace=True)


        if verbose:
            AnalysisTotalString = \
                "There are {both:,} entries that have both phonetic and syllable information and  {either:,} entries that have either only one or the other, which means there are  {total:,} total entries for analyis.".format(
                both = len(BothDF), either =(len(syllableOnlyDF) + len(phoneticsOnlyDF)),
                total = (len(syllableOnlyDF) + len(phoneticsOnlyDF) + len(BothDF))
            )
            print(AnalysisTotalString)

        return BothDF, syllableOnlyDF, phoneticsOnlyDF


if __name__ == '__main__':
    import NoahAndChrisTesting
    NoahDF = NoahAndChrisTesting.NoahDF
    import BigOuterMerge
    NoahDF = BigOuterMerge.BigOuterMerge(NoahDF)

    import FilterBeforeLogic
    NoahDF = FilterBeforeLogic.filter1(NoahDF, verbose= True)

    NoahBoth, NoahSyllablesOnly, NoahPhoneticsOnly = SplitDF(NoahDF, verbose= True)


    #Note, using this leftovers, I've found that the function is dropping words for which there's neither syllabic nor phonetic information
    leftovers = NoahDF.drop(NoahBoth.index)
    leftovers = leftovers.drop(NoahPhoneticsOnly.index)
    leftovers = leftovers.drop(NoahSyllablesOnly.index)

    print(NoahBoth.head())