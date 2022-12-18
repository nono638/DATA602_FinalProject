import Phonetics_Dict
import re
def MakeWordCVCs(x, verbose = False):
    """This function expects a list of English syllables (from the syllables column) and returns a list ran through a vcv
        algorithm and returns a string such as _vc meaning vowel-consonant"""
    if type(x) != list:
        if verbose:
            print("Expected a list here in MakeWordCVCs, got {}  Returning None".format(str(x)))
        return None

    def getConsonantVowelStringStructure(stringParam, verbose = False):
        """This function takes an English syllable (expects 1 string as input) and
        returns its consonant-vowel structure.
        For example, input of 'bots' would return 'cvc'."""
        if type(stringParam) != str:
            print("a string wasn't entered for {}.".format(stringParam))
        stringParam = stringParam.lower()
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"

        cvc = "^[{}]+[{}]+[{}]+$".format( consonants, vowels, consonants)
        cv_ = "^[{}]+[{}]+$".format(consonants, vowels)
        _vc = "^[{}]+[{}]+$".format(vowels, consonants)
        c_c = "^[{}][{}]+$".format(consonants, consonants)  ##?? is this valid?? TODO
        c__ = "^[{}]+$".format(consonants)
        _v_ = "^[{}]+$".format(vowels)

        #the following are basterdization patterns, possibly to discard
        cvcv = "^[{}]+[{}]+[{}]+[{}]+$".format(consonants, vowels, consonants, vowels)
        #possible oversimplifcation here ^, TODO
        vcv = "^[{}]+[{}]+[{}]+$".format(vowels, consonants, vowels)
        # possible oversimplifcation here ^, TODO...
        #  assuming ette or inge are VCs
        cvcvc = "^[{}]+[{}]+[{}]+[{}]+[{}]+$".format(consonants, vowels, consonants, vowels, consonants)
        # nounced, priced, marked, dered, billed --  ends in ed, er
        vcvc = "^[{}]+[{}]+[{}]+[{}]+$".format( vowels, consonants, vowels, consonants)

        if (len(stringParam) >1):
            if re.match(cvc, stringParam) is not None:
                return "cvc"
            elif re.match(cv_, stringParam) is not None:
                return "cv_"
            elif(re.match(_vc, stringParam) is not None):
                return "_vc"
            elif re.match(c_c, stringParam) is not None:
                return "c_c"
            elif re.match(c__, stringParam) is not None: #TODO
                return "c/c" #it can't exactly be known which side the consonant is on in English, TODO
            elif re.match(_v_, stringParam) is not None:
                return "_v_"
            elif re.match(cvcv, stringParam) is not None: # possible oversimplifcation here, fix TODO
                return "cvc"
            elif (re.match(vcv, stringParam) is not None):
                return ("_vc")
            elif (re.match(cvcvc, stringParam) is not None):
                if stringParam[-2:] not in ['er','ed', 'es']:
                    if verbose:
                        print ("something weird happening with {} in getConsonantVowelStringStructure.".format(stringParam))
                return "cvc" #er, ed endings, steno specific
            # elif (re.match(vcvc, stringParam) != None):
            #     return "_vc" #ized
            else:
                if verbose:
                    print('something wrong with "'+ stringParam +'" in getConsonantVowelStringStructure.')
                return None
        else:
            if stringParam in consonants:
                return "c/c" #TODO, rectify with steno consonants
            else:
                return "_v_"

    returningList = []
    for i in x:
        returningList.append(getConsonantVowelStringStructure(i)
        )
    if len(returningList) >= 1:
        return returningList
    else:
        if verbose:
            print("Something went wrong with {} in MakeWordCVCs".format(x))
        return None

def CVCEqualityCheck(stenoCVCOutput, syllablesCVCoutput, verbose = False):
    """This function returns True if the syllable Structure of Steno
    and strings are equal, otherwise it returns false.  It mostly exists
    because some consonant syllables will return 'c/'c' since it's not
    possible to tell where, positionwise relative to the steno keyboard, the consonants
    are.

    This function expects intputs like :

    'cv_' and 'cv_'  returns True

     'cvc' and '_vc' returns False

     'c__' and 'c/c' returns True          <--this is the reason for this function's existence
     '"""

    #Validation:
    if (stenoCVCOutput is None) or syllablesCVCoutput is None:
        if verbose:
            print ("None passed to CVCEqaulityCheck with {} {}, returning None...".format(stenoCVCOutput,syllablesCVCoutput) )
            return None


    if stenoCVCOutput == syllablesCVCoutput:
        return True
    elif ((stenoCVCOutput == "c__") or (stenoCVCOutput == "__c") and syllablesCVCoutput=="c/c"):
        return True
    else:
        return False

# def getConsonantVowelStringStructure(x):
#     """This function takes an English syllable (expects a string as input) and
#     returns its consonant-vowel structure.
#     For example, input of 'bots' would return 'cvc'."""
#     if type(x) != str:
#         print("a string wasn't entered for {}.".format(x))
#     x = x.lower()
#     consonants = "bcdfghjklmnpqrstvwxyz"
#     vowels = "aeiou"
#
#     cvc = "^[{}]+[{}]+[{}]+$".format( consonants, vowels, consonants)
#     cv_ = "^[{}]+[{}]+$".format(consonants, vowels)
#     _vc = "^[{}]+[{}]+$".format(vowels, consonants)
#     c_c = "^[{}][{}]+$".format(consonants, consonants)
#     c__ = "^[{}]+$".format(consonants)
#     _v_ = "^[{}]+$".format(vowels)
#
#     #the following are basterdization patterns, possibly to discard
#     cvcv = "^[{}]+[{}]+[{}]+[{}]+$".format(consonants, vowels, consonants, vowels)
#     #possible oversimplifcation here ^, TODO
#     vcv = "^[{}]+[{}]+[{}]+$".format(vowels, consonants, vowels)
#     # possible oversimplifcation here ^, TODO...
#     #  assuming ette or inge are VCs
#     cvcvc = "^[{}]+[{}]+[{}]+[{}]+[{}]+$".format(consonants, vowels, consonants, vowels, consonants)
#     # nounced, priced, marked, dered, billed --  ends in ed, er
#     vcvc = "^[{}]+[{}]+[{}]+[{}]+$".format( vowels, consonants, vowels, consonants)
#
#     if (len(x) >1):
#         if re.match(cvc, x) is not None:
#             return "cvc"
#         elif re.match(cv_, x) is not None:
#             return "cv_"
#         elif(re.match(_vc, x) is not None):
#             return "_vc"
#         elif re.match(c_c, x) is not None:
#             return "c_c"
#         elif re.match(c__, x) is not None: #TODO
#             return "c/c" #it can't exactly be known which side the consonant is on in English, TODO
#         elif re.match(_v_, x) is not None:
#             return "_v_"
#         elif re.match(cvcv, x) is not None: # possible oversimplifcation here, fix TODO
#             return "cvc"
#         elif (re.match(vcv, x) is not None):
#             return ("_vc")
#         elif (re.match(cvcvc, x) is not None):
#             if x[-2:] not in ['er','ed', 'es']:
#                 print ("something weird happening with {} in getConsonantVowelStringStructure.".format(x))
#             return "cvc" #er, ed endings, steno specific
#         # elif (re.match(vcvc, x) != None):
#         #     return "_vc" #ized
#         else:
#             print('something wrong with "'+ x +'" in getConsonantVowelStringStructure.')
#             return None
#     else:
#         if x in consonants:
#             return "c/c" #TODO, rectify with steno consonants
#         else:
#             return "_v_"

def MakeStenoCVCs(strokeListParam, verbose=False):
    """This function expects a list (of strokes) as input
    and returns a list of equal length with the ouput of the CVC algorithm.

    For example, ['STEpB', 'OE'] would oupt ['cvc','_v_'] ."""
    if type(strokeListParam) != list:
        if verbose:
            print("Expected a list here, got {}.  Returning None...".format(str(strokeListParam)))
        return None

    def getConsonantVowelStenoStructure(stenoParam, verbose = False):
        """This function expects one stroke string as an input
        and returns a single string like cvc for consonant-vowel-consonant.
        It's meant to be used on individual strokes .
        For example, it receives 'STORpL' and returns 'cvc' ."""

        #This first part of the function handles problemKeys on the Steno Keyboard...
        # as well as validates input otherwise making sure entries are permissible
        cleanedStenoParam = ""
        problemKeys = "1234567890*#"
        for char in stenoParam:
            if char not in "#1234567890STKPWHRAO*EUFRrPpBLGTtSsDZ":
                if verbose:
                    print(char, "isn't a steno key, probably calling the wrong function...")
                    print("Returning None from getConsonantVowelStenoStructure ")
                return None
            if char not in problemKeys:
                cleanedStenoParam += str(char)


        #if (len(cleanedStenoParam)>1):
        cvc = "^[STKPWHR]+[AOEU]+[FRrPpBLGTtSsDZ]+$"
        _vc  = "^[AOEU]+[FRrPpBLGTtSsDZ]+$"
        c_c = "^[STKPWHR]+[FRrPpBLGTtSsDZ]+$" #TODO, imporve
        cv_ =  "^[STKPWHR]+[AOEU]+$"
        c__ = "^[STKPWHR]+$"
        _v_ = "^[AOEU]+$"
        __c = "^[FRrPpBLGTtSsDZ]+$"
        if (re.match(cvc, cleanedStenoParam) != None):
            return "cvc"
        elif (re.match(_vc, cleanedStenoParam) != None):
            return "_vc"
        elif (re.match(c_c, cleanedStenoParam) != None):
            return 'c_c'
        elif (re.match(cv_, cleanedStenoParam) != None):
            return 'cv_'
        elif (re.match(c__, cleanedStenoParam) != None):
            return 'c__'
        elif (re.match(_v_, cleanedStenoParam) != None):
            return '_v_'
        elif (re.match(__c, cleanedStenoParam) != None):
            return '__c'

        else:
            if verbose:
                print ("Something went wrong with " + str(stenoParam) + " in ConsonantVowelStructure.py ." )
            return None

    returningList = []
    for i in strokeListParam:
        if (getConsonantVowelStenoStructure(i) is None) and verbose:
            print("Error evaluating {} in MakeStenoCVCs.".format(strokeListParam))
        returningList.append(getConsonantVowelStenoStructure(i))
    if len(returningList) >= 1:
        return returningList
    else:
        if verbose:
            print("There's no list return regarding {} in MakeStenoCVCs... returning None".format(strokeListParam))
        return None



if __name__ == '__main__':

    #I've seemingly broken the testing here, interesting... TODO possibly,
    testStrings = ['SPOs', 'TOLt', 'E', "OELD", "SAOEU", 'hello']

    for i in testStrings:
        print(i,MakeStenoCVCs([i]))

    print('_______________')

    testStrings2 = ['yin', 'HEl', 'ops', 'stu', 'd']
    for i in testStrings2:
        print(i, MakeWordCVCs([i]))

