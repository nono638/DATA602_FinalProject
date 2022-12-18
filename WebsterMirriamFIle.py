import re
import pandas as pd
import io
_SyllableDictFile = open("Data Sources/dictionaryWithSyllables.txt", "r", encoding= "utf_8_sig") # this encoding seems to fix read issues as in anime which has an accent sign over the e
SyllableDict =  _SyllableDictFile.read()

#original data source : https://www.gutenberg.org/ebooks/29765

#print(SyllableDict)
SyllableDictLines = SyllableDict.splitlines()
SyllableDictLines = SyllableDictLines[27:] # Drop first 28 lines, TODO for end of file...


class WordsDictEntry:
    def __init__(self, word, syllablesRaw, definition, verbose = False):
        self.word = word
        self.syllablesRaw = syllablesRaw
        self.definition = definition
        if verbose:
            print('created new WordsDictEntry: \n{} \n{} \n{}'.format(
                self.word,
                self.syllablesRaw,
                self.definition
        )
            )
            print("___")
    def __repr__(self):
        return str(self.word) + " " + str(self.syllablesRaw)  +" : " +str (self.definition)


WordsDict = []
def makeWordsDict():
    wordPreviousLine = False
    capturingDefinition = False
    definition = ""
    syllablesRaw = None
    word = ""

    counter = 0
    verbose = False
    for line in SyllableDictLines:
        counter +=1
        if (verbose):
            print()
            print("@@",line)
        if (
                (line.isupper() ) and
                ( (" " not in line) and ("[" not in line) and ("]" not in line) ) and
                (wordPreviousLine == False) and
                (line !="") and
                ( (line != "III.") and (line != "I.") and (line != "II.") and
                  (line != "C6H5.C2H2.CHO.") and (line != "C2H5.O.CH3.") )

        ):
            if (capturingDefinition): #This portion sees that a new word has begun and therefore appends the newly made entry
                if definition[:5] == "Defn:":
                    definition = definition[5:]
                entry = WordsDictEntry(word, syllablesRaw, definition)
                #print(entry)
                WordsDict.append(entry)
                del entry

            word = line #sets the new isupper() word as the line
            if(verbose):
                print("^New Word: ", line)
            wordPreviousLine = True
            capturingDefinition = False
            definition = ""
        elif wordPreviousLine: #look for syllables
            if (line !=""):
                try:
                    pattern = "^[^,\s]+"
                    syllablesRaw = line[re.match(pattern, line).span()[0]:re.match(pattern, line).span()[1]]
                    if syllablesRaw[-1] == ",":
                        syllablesRaw = syllablesRaw[:-1]

                    if(verbose):
                        print("syllablesRaw:",syllablesRaw)
                        if re.match("[()#@`/\.&<>|]", syllablesRaw) != None:
                            print('something wrong here: ', syllablesRaw, line, word, 'discarded')
                    if re.match("[()#@`/\.&<>|]", syllablesRaw) != None:
                        syllablesRaw = "NO SYLLABLES"
                    #TODO Pos
                except:
                    print("couldnt handle {}".format(line))
                    syllablesRaw = "NO SYLLABLES"

            else:
                syllablesRaw = "NO SYLLABLES"
            wordPreviousLine = False
        elif ( (len(line)>=6 and (line[:5] == "Defn:" ) ) or (line[:2] == '1. ') or (capturingDefinition ) ):

            capturingDefinition = True
            definition += line
            if (verbose):
                print(definition)
        if (line == "End of Project Gutenberg's Webster's Unabridged Dictionary, by Various"):
            if verbose:
                print("DONE!!!!", counter)
            break

makeWordsDict() #call above function, puts variables in function scope


def MakeDF():
    count = 0
    wordz = []
    syllablez = []
    definitionz = []
    print()  # "NO SYLLABLES
    for i in WordsDict:
        wordz.append(i.word)
        i.syllablesRaw = i.syllablesRaw.lower()
        sylls = []
        runningSyllable = ""
        for j in i.syllablesRaw:
            if j not in "\"*`":
                runningSyllable += j
            else:
                sylls.append(runningSyllable)
                runningSyllable = ""

        if(len(runningSyllable)>1 and (runningSyllable[-1]=='.' or runningSyllable[-1]==';') ): #This takes care of a few weird ones where it's ending in a period or semicolon for some reason
            runningSyllable = runningSyllable[:-1]
        if (runningSyllable not in "\"';."):
            if runningSyllable != "" and len(runningSyllable)>=1:
                sylls.append(runningSyllable)

        syllablez.append(sylls)
        definitionz.append(i.definition)
        if i.syllablesRaw == 'NO SYLLABLES':
            count += 1
    print("There are {} entries where the syllables couldn't be parsed.".format(count))

    df = pd.DataFrame({
        "Word": [i.lower() for i in wordz],
        "syllablesRaw": [i.syllablesRaw for i in WordsDict],
        "syllables": syllablez,
        "definition": definitionz
    })

    df = df[df['Word'].apply(lambda x: len(x) > 1)]
    return df

WebstersDF = MakeDF()


if __name__ == '__main__':
    for i in WordsDict[41131:41132]:
        print (i)
        print('---------------')

    print('{:,} entries.'.format(len(WordsDict)))



    print(WebstersDF.head())
    print()