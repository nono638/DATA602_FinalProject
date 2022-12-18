import Phonetics_Dict
import pandas as pd
def AddPhoneticStructureColumn(df, verbose = False):
    """    adds a phoneticStructure column to a dataframe that has a phonetics column.
    returns pd.DataFrame
    """
    if "Phonetics" not in df.columns.tolist():
        if verbose:
            print ("There's no phonetics column, returning the df entered...")
        return df
    else:
        def getPhoneticStructure(x):
            result = ""
            inVowelPatch = False
            inConsonantPatch = False
            #print(x)###
            for i in x:
                if i in Phonetics_Dict.phoneticVowels:
                    if (not inVowelPatch):
                        result += "v"
                    inVowelPatch = True
                    inConsonantPatch = False
                elif i in Phonetics_Dict.phoneticConsanants:
                    if (not inConsonantPatch):
                        result += "c"
                    inConsonantPatch = True
                    inVowelPatch = False
            return result

        dfWithPhonetics = df[df["Phonetics"].notnull()].copy()
        dfWithPhonetics['PhoneticsStructure'] = dfWithPhonetics["Phonetics"].apply(lambda x: getPhoneticStructure(x) )

        dfWithoutPhonetics = df[df["Phonetics"].isnull()].copy()
        df = pd.concat([dfWithPhonetics, dfWithoutPhonetics], sort= False)
        return df





if __name__ == '__main__':
    import NoahAndChrisTesting
    NoahDF = NoahAndChrisTesting.NoahDF

    import BigOuterMerge, FilterBeforeLogic, MakeColumnsForAnalysis, SplitPhoneticsAndSyllables

    NoahDF = FilterBeforeLogic.filter1(BigOuterMerge.BigOuterMerge(NoahDF))

    #NoahBothDF, NoahSyllablesOnly, NoahPhoneticsOnly = SplitPhoneticsAndSyllables.SplitDF(NoahDF)
    #del NoahDF

    NoahBothDF = AddPhoneticStructureColumn(NoahDF)

    print()