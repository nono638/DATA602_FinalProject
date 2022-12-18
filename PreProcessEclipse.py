import pandas as pd
import numpy as np
import re

def ProcessTextFile(path): #TXT expected
    """Expects .txt file, returns splitlines() of text file.
    Output to be passed to MakeBasicStenoDataFrame"""
    try:
        with open(path, 'r') as file:  # with statement automatically closes
            DictFile = file.read()
    except:
        print("Couldn't open file: {}".format(path))
        return None
    try:
        file.close()
    except:
        print('Could not close file: ', path)
        pass
    mydict = DictFile.splitlines()
    return mydict


def MakeBasicStenoDataFrame(StenoDictParam):
    """Returns a dataframe with Steno and Translation.
    Expects preprocessed file as input."""
    stenoDict= {}
    for i in StenoDictParam:
        #print(i)
        stenoDict[i[:i.find("=")].strip() ] = \
            i[i.find("=")+1:].strip()
    StenoDictDF = pd.DataFrame({"Steno":list(stenoDict.keys()),
                   "Translation": list(stenoDict.values())})

    def AddStrokesColumn(df):
        try:
            import Standardize_Stokes
        except:
            print('Couldn\'t import Standardize Stokes, returning none.')
            return None
        df = Standardize_Stokes.AddStrokesColumn(df)  # Strange call, the function just adds the column

        df['Strokes'] = df['Strokes'].apply(lambda x: Standardize_Stokes.StandardizeStrokes(x))
        return df

    StenoDictDF['Word'] = StenoDictDF['Translation'].apply(lambda x: x.lower()) # for standardization, merging
    #StenoDictDF["Word"] = stenoDict['word']

    StenoDictDF = AddStrokesColumn(StenoDictDF)

    return StenoDictDF


def ResolveEclipseConflicts(df, conflictSymbol = '\\', verbose = False):
    """I hate backslashes in python, ahhh!!!  TODO"""

    #Note: Do not touch the backslashes here!!! It works, I have no idea why.  Don't touch it!

    specialDelination = "|_|_"
    df2= df[df["Translation"].str.contains('\\\\')]
    print("There are {} conflicts in the entered dictionary.".format(len(df2)))
    Translations = list(df2['Translation'])
    #print(Translations[:7])
    TranslationsFixed = [i.replace('\\', specialDelination) for i in Translations]
    if verbose:
        print("TranslationsFixed:")
        print()
        print(TranslationsFixed[:5])

    TuplesList =[]
    for i in TranslationsFixed:
        #print(i)
        try:
            tranA = re.findall("[^_|]+", i)[0]
            #print(tranA)
            tranB = re.findall("[^_|]+", i)[1] #i[i.find(specialDelination) + len(specialDelination) + 1:]
            #print(tranB)
            TuplesList.append ( (tranA, tranB))
        except:
            if verbose:
                print("{} Didn't work!!".format(i))
            TuplesList.append((None, None) )

    if verbose:
        print()
        print("TuplesList:")
        print(TuplesList[:5])
    cols = list(df2.columns)
    if len(TuplesList) == len(df2):
        print("Length Check passed!")
    else:
        print("Length Check failed!")

    df3ListList = []

    for i in range(len(df2)):
        df3ListItem=[]
        for j in range(len(cols)):
            df3ListItem.append(df2.iloc[i,j])
        df3ListItem.append(TuplesList[i][0])

        df3ListList.append(df3ListItem)

        df3ListItem = []
        for j in range(len(cols)):
            df3ListItem.append(df2.iloc[i,j])
        df3ListItem.append(TuplesList[i][1]) #second tuple item this time
        df3ListList.append(df3ListItem)


    if verbose:
        if len(df3ListList) == len(df2) *2:
            print("df3ListList length passed!")
        else:
            print("df3ListList length failed!")

    df3 = pd.DataFrame()
    for i in range(len(cols)):
        df3[cols[i]] = [j[i] for j in df3ListList]

    #df3['Fixed'] = [i[-1] for i in df3ListList]
    df3['Translation'] = [i[-1] for i in df3ListList]


    #Almost there, fix this!
    df3.dropna(subset=['Translation'], inplace=True)
    df3['Word'] = [i.lower() for i in list(df3['Translation']) ]


    if verbose:
        print('df3ListList[:4] :')
        print(df3ListList[:4])

    if verbose:
        if len(df3) / 2 == len(df2):
            print("Final Length Check passed!")
        else:
            print("Final Length Check failed!")


    # df4 = pd.merge(df3, df[~df["Translation"].str.contains('\\\\') ], how = "outer", on ="Steno")
    # # df2= df[df["Translation"].str.contains('\\\\')]

    df4 = pd.concat([df3, df[~df["Translation"].str.contains('\\\\') ] ])



    return df4


    # #for now, only handle the first two conflicts, possibly to do increase to 3:
    # Translations = list(df2['Translation'])
    # for i in range(len(Translations)):
    #  #   if Translations[i][0] == conflictSymbol:
    #     #print(Translations[i])
    #     #print(Translations[i][0:2])
    #     if Translations[0] == conflictSymbol[0]:
    #         Translations[i] = Translations[i][1:]
    # ConflictTuples = []
    # for i in Translations:
    #     Tran1 = i[:i.find(conflictSymbol[0])].strip()
    #     Tran2 = i[i.find(conflictSymbol[0])+1:].strip()
    #     ConflictTuples.append( (Tran1, Tran2))
    #
    # if (len(ConflictTuples) == len(Translations) and verbose):
    #     print("Lengths are right...")
    #
    # results = []
    # Stenos = list(df2["Steno"])
    # for i in range(len(Stenos)):
    #     results.append( (Stenos[i], ConflictTuples[i][0]))
    #     results.append((Stenos[i], ConflictTuples[i][1])) #assuming only 2 conflicts each for now... TODO
    #
    # df3 = pd.DataFrame({
    #     "Steno": [i[0] for i in results] ,
    #     "Translation": [i[1] for i in results]
    # })
    # return df3

if __name__ == '__main__':
    import pandas as pd

    NoahDictFile = "Data Sources/NCollinDict1.txt"
    # put any another = separated dictionary here

    #[print(i) for i in mydict[:5]]
    df = MakeBasicStenoDataFrame(ProcessTextFile(NoahDictFile))
    #print(df.head())
    print(df.head())
    #print('ok')



#This portion tests that the StenoDictionary and Phonetics Dictioary can be compared and eventually merged.
    df2 = ResolveEclipseConflicts(df)
    quit()