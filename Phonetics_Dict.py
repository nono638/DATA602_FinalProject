import pandas as pd
_phoneticeDFPath = "Data Sources/en_US_phonetic_dictionary"
phoneticsDF = pd.read_csv(_phoneticeDFPath,
                          names=("Word", "Phonetics") ,
                          delimiter="\t",
                          encoding="utf-8")
#print(phoneticsDF.head())

def slashCount(x):
    """Count the number of slashes, /,  in a string"""
    SlashCount = 0
    for i in x:
        #print(i)
        if i == '/':
            SlashCount +=1
    return SlashCount

def endsInSlash(x):
    """returns true if the string ends in a slash, '/' """
    if (x[-1] == '/'):
        return True
    else:
        return False

phoneticsDF['Slash_Count'] = phoneticsDF.Phonetics.apply(lambda x: slashCount(x))


if __name__ == "__main__":
    print("There are {:,} entries in the phonetics dictionary and {:,} have two or more phonetic interpretations.".format(
            len(phoneticsDF),
            len(phoneticsDF[phoneticsDF['Slash_Count'] > 2])))
    print('For now, for simplicity, drop these.  These could eventually be refactored and then  re-added.  TODO') #TODO

# print(phoneticsDF[phoneticsDF['Slash_Count'] >= 2] )
# For now, for simplicity, drop these.  These could eventually be refactored and then re-added.  TODO
phoneticsDF = phoneticsDF[phoneticsDF['Slash_Count'] <= 2]

# drop Slash_Count Column
phoneticsDF.drop("Slash_Count", axis=1, inplace= True)



def MakePhoneticsDF(df):  #What was the point of this again?? To delete??
    """Seemingly returns a DF with a column that sees if a word i the phoneticsDF is in a user dictionary..."""
    dictWords = set(df['Translation']) #Expecting Translation column
    phoneticsDF['InDict'] = phoneticsDF['Word'].apply(lambda x : x in dictWords)
    return phoneticsDF

phoneticSymbolSet = set()
for i in set(phoneticsDF['Phonetics']):
    for symbol in i:
        if symbol not in phoneticSymbolSet:
            phoneticSymbolSet.add(symbol)
    # TODO take care of slash, make two+ entries possibly

toRemove = [' ', ',', '/', '??', '??']  # TODO: Research what these ticks are.
# The slash is used for two phonetic pronunciations
for i in toRemove:
    try:
        phoneticSymbolSet.remove(i)
    except KeyError:
        #print('couldn\'t remove', i)
        pass
phoneticVowels = {'??' ,'a', '??' ,'o' ,'e' , 'i' , 'u' , '??' , '??' , '??' ,'??' , '??', '?? ',  '??' } # ?? = er
 #['/??f??', '??', 't', '??', '/'] = fluster  :/
# ?? like thought, "open o" , https://en.wikipedia.org/wiki/Open-mid_back_rounded_vowel
# ?? - after
# ?? = oo I'd say
# ?? = short a
#https://en.wikipedia.org/wiki/International_Phonetic_Alphabet_chart
phoneticConsanants = phoneticSymbolSet - phoneticVowels


if __name__ == '__main__':
    print(phoneticsDF.iloc[456:,:].head(20))















    #print(slashCount('/k??z/'))


    #print(phoneticsDF[phoneticsDF['phonetics'].apply()])