# These functions should only be used an the equalStructured subset of the data
import Phonetics_Dict


def PhoneticsAnalysis(df, verbose = False):  #maybe discard this
    """This is going to make an answer key of phonetics from a df..."""
    if "Phonetics" in df.columns.tolist():
        if "syllables" in df.columns.tolist():
            def MakeLeftMidRightForPhonemes  (PhoneticsParam):
                """Again, this should only be used on Equal Structured CVC data"""
                left, mid, right = [],[],[]
                inVowels, inConsonants = False, False
                for i in PhoneticsParam:
            df['Phoneticsleftmidright'] =

        else: #TDO, no syllables, phonetics only
            return df
    else: # no Phonetics column, return df as is
        if verbose:
            print ("Nothing happened with PhoneticsAnyalysis because the df didn't have a phonetics column...")
        return df