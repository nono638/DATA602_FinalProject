import pandas as pd
import re

# see https://pandas.pydata.org/docs/reference/api/pandas.Series.str.count.html
def filter1(df, verbose = False): #2 Rs are deliberate, so it doesn't overwrite something else
    """This filterr function, deliberatly mispelledd, runs several functions to clean up a given dictionary before
    analysis.  It's meant to grow to handle unusual entries."""

    def dropNulls(df):
        beforeLen = len(df)
        df = df[(df['Translation'].notnull()) & (df['Translation'].notna())].copy()
        df = df[~df['Translation'].str.isspace()].copy()
        df = df[df['Steno'].notna()].copy()
        if verbose:
            print('{:,} rows dropped from dropNulls.'.format(beforeLen - len(df)))
        return df


    def dropMultiWord(df): #Maybe could do something here....
        beforeLen = len(df)
        df["Translation"] = df['Translation'].str.strip()
        df = df[df['Translation'].str.count(' ') < 1].copy() # <=?
        if verbose:
            print('{} rows dropped from DropMultiWord.'.format(beforeLen - len(df)))
        return df

    def dropNumbers(df, comprehensive = True):
        """This will drop numbers from both the translation and the steno.
        The "comprehensive" parameter, default = True, discards any steno or translation
        with a number in it."""
        beforeLen = len(df)

        if comprehensive:
            df = df[~df['Translation'].str.contains('[0-9]')]
            df = df[~df['Steno'].str.contains('[0-9]')]

        else:
            df = df[~df['Translation'].str.isnumeric()] #tilde means bitwise not
            df = df[~df['Steno'].str.isnumeric()]  # tilde means bitwise not

        if verbose:
            print('{} rows dropped from dropNumbers.'.format(beforeLen - len(df)))
        return df

    def dropUpper(df):
        beforeLen = len(df)
        df = df[~df['Translation'].str.isupper()]  #https://pandas.pydata.org/docs/reference/api/pandas.Series.str.isupper.html
        if verbose:
            print('{} rows dropped from dropUpper.'.format(beforeLen - len(df)))
        return df

    def dropSpecialChars(df, specialChars = '[\^\{\}\|\()#"\.,&]'):
        beforeLen = len(df)
        df = df[~df['Translation'].str.contains(specialChars)]  # https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html
        if verbose:
            print('{} rows dropped from dropSpecialChars.'.format(beforeLen - len(df)))
        return df

    def dropImproperSteno(df, stenoKeyboardString ='[STKPWHRAO\*EUFRBLGDZ]'):  #\ needed for regex
        beforeLen = len(df)
        df = df[~df['Steno'].str.islower()]  # https://pandas.pydata.org/docs/reference/api/pandas.Series.str.islower.html
        df = df[df['Steno'].str.contains(stenoKeyboardString)] #Steno Entries Should only have these symbols, nothing else
        if verbose:
            print('{} rows dropped from dropImproperSteno.'.format(beforeLen - len(df)))
        return df

    def dropDuplicateWords(df):
        """This has been used to  drop Word Duplicates and  is now being used for Steno Duplicates"""
        if "Word" in df.columns.tolist():
            beforeLen = len(df)
            df = df.drop_duplicates(subset="Word") #subset might need to be a list if python version <=3.7
            afterLen = len(df)
            if verbose:
                print("{:,} words were dropped due to duplicate words (usually from multiple definitions.)".format(beforeLen-afterLen))
            return df
        else:
            if verbose:
                print("Expexted 'Word' Column, couldn't drop duplicate words!")
            pass

    def dropShortForms(df):
        if "Steno" in df.columns.tolist():
            beforeLen = len(df)
            df = df[df['Steno'].map(len) > 1]
            if verbose:
                print("{:,} dropped from dropShortForms.".format(beforeLen - len(df)))

        #TODO
            #drop short forms that don't have any vowels.  It's a convention that English words have vowels.
           # df = df.drop( df['stroke']  )

        elif verbose:
            print("Expected a steno column, returning df as is...")

        return df




    #back to filterr function
    df = dropShortForms(
        dropDuplicateWords(
            dropImproperSteno(
                dropMultiWord(
                    dropUpper(
                        dropSpecialChars(
                            dropNumbers (
                                dropNulls(df)
                                                        )
                                                        )
                                            )
        )
        )
        )
    )
    if verbose:
        print()
    return df





if __name__ == '__main__':
    import  NoahAndChrisTesting



    a = filter1(NoahAndChrisTesting.ChrisDF, verbose= True)

    print("A:",len(a) )

    from Phonetics_Dict import phoneticsDF
    print('phoneticsDF:', len(phoneticsDF))

    a['word_lowered'] = a["Translation"].str.lower()
    #print(a[a['Translation'].str.istitle()].head())
    b = phoneticsDF
    b['word_lowered'] = b['Word'].str.lower()

    c = pd.merge(a, b, on= 'Word', how= 'inner')
    print('There are {:,} viable entries in the stenodict and the phoneticsDF.'.
          format(len(c)))
    d = c[c['Word'].str.istitle()]
    print(d.head(22))
    #print(phoneticsDF[phoneticsDF['word'].str.istitle()].head(22))
    print(a[a['Translation'].str.istitle()].head(3))