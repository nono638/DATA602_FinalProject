import pandas as pd
import re
def HandleRTF(rtfFile):
    """This handles Case Cat RTFs obviously..."""
    try:
        #ChrisDictFileString = "Data Sources/Personal Dictionary_D_1.rtf"
        with open(rtfFile, 'r') as file:  # with statement automatically closes
            dictFile = file.read()
        file.close()

        stenoDcit = dictFile.splitlines()
        #[print(i) for i in stenoDcit[:24]]
    except:
        print('Cound\'t open {}....'.format(rtfFile))
        stenoDcit = None

    return stenoDcit

def MakeStenoDf(stringParam, verbose = False):
    """This makes a DataFrame where the steno strokes have spaces
    instead of slashes and a special column from Case Cat."""
    entries = []
    for line in stringParam:
        if r"\*\cxs " in line:
            entries.append(line[8:]) #get rid of first 8 characters of valid strokes
    if verbose:
        print("There are {:,} entries in the CaseCat dictionary.".format(len(entries)))
    #[print(i) for i in entries[:3]]

    entriesDict = {}
    for entry in entries:
        # print(entry)
        # print(re.findall("(.+)}", entry)) #Steno
        # print(re.findall("}(.+)",entry)) #Translation
        try:
            entriesDict[re.findall("(.+?)}", entry)[0]] = re.findall("}(.+)", entry)[0]
            # print("adding {} as {}...".format([re.findall("(.+?)}", entry)[0]], re.findall("}(.+)", entry)[0]))
        except:
            if verbose:
                print('couldn\'t process {}  continuing...'.format(entry))
            ## With Chris's dictionary, there's two entries that didn't work...
            continue
    stenoDf = pd.DataFrame({"Steno": entriesDict.keys(), \
                            "Translation": entriesDict.values()})
    #import re

    ## Create Special column to Case Cat's special translation junk
    stenoDf["Special"] = stenoDf["Translation"].apply(\
        lambda x: re.findall('(s[123457890]{.*}|s[123457890])', x)[0] if len(re.findall('(s[123457890])', x)) > 0 else None)


    #Change the Translation column to use spaces instead of slashes for multiple stokes


    stenoDf["Steno"] = stenoDf["Steno"].apply(lambda  x: x.replace('/', ' ') ) # replace all of chris's slashes with spaces

    #Standardize the strokes column:
    try:
        import Standardize_Stokes
        stenoDf = Standardize_Stokes.AddStrokesColumn(stenoDf)
        stenoDf['Strokes'] = stenoDf['Strokes'].apply(lambda x: Standardize_Stokes.StandardizeStrokes(x))

    except:
        print("  Couldn't import Standardize_Strokes.py ...")



    stenoDf['Word'] = stenoDf['Translation'].apply(lambda x: x.lower()) # for standardization, merging

    return stenoDf






if (__name__ == '__main__'):
    import re
    import pandas as pd

    ChrisDict = HandleRTF("Data Sources/Personal Dictionary_D_1.rtf")
    df = MakeStenoDf(ChrisDict)
    print(df.head() )

    print()
