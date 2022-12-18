import pandas as pd
import Phonetics_Dict
import WebsterMirriamFIle


def BigOuterMerge(df, inner = False):
    """This function makes a larger df to be subsequently filtered.  It merges a user
    steno dictionary, already preprocessed, with the websters and phonetics dictionary.  This
    function outputs a dataframe which should be passed to the FilterBeforeLogic functions."""
    if 'Word' in df: #word corrected to 'Word'
        df = pd.merge(df, Phonetics_Dict.phoneticsDF, on='Word', how = 'outer')
        df = pd.merge(df, WebsterMirriamFIle.WebstersDF, on = 'Word', how = 'outer')

        if inner:
            df = df.dropna().reset_index()
            df = df.drop('index', axis = 1)

        return df

    else:
        print("Expected 'word' column")
        return None



if __name__ == '__main__':
    import NoahAndChrisTesting

    NoahDF = NoahAndChrisTesting.NoahDF


    NoahDF = BigOuterMerge(NoahDF)
    #df3 = df2.dropna().reset_index()
    ChrisDF = NoahAndChrisTesting.ChrisDF
    ChrisDF = BigOuterMerge(ChrisDF)
    #ChrisDF.dropna(subset = ["Steno", 'syllables'] , inplace= True)

    print()
    print()