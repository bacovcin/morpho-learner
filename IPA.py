#######
# IPA.py
# @ Kobey Shwayder
# implementation of TIPA as double dict
# Feature values taken from Bruce Hayes "Introductory Phonology" 2001
# if they were in their, otherwise intuited by Kobey
#######

from Util import *


def ParseTIPA(string):
    '''Given an input raw string (in TIPA) output a list of phonemes. 
        Backslashes should automatically be doubled by python.
        NB supersegmentals, clicks, and diacritics not implemented'''
    output = []
    string = list(string.encode("string-escape")) # make list and unescape characters
    while len(string) > 0:
        rawchar = string.pop(0)
    #for each character, if not brackets or \, return phoneme
        if rawchar == "\\":
        #if \\ get one of following 
        #1. A-z until bracket or space
        #2. not A-z (punctuation) plus following character
        #3. \c{c}
            tipachar = rawchar
            rawchar = string.pop(0)
            while rawchar == "\\":
                rawchar = string.pop(0) #delete multiple escapes
            if rawchar == 'c' and string[0:3] == '{c}':
                tipachar = tipachar + "c{c}"
                output.append(tipachar)
                tipachar = ''
                string = string[3:]
            elif rawchar in '!*:;': #punct
                tipachar = tipachar + rawchar + string.pop(0)
                output.append(tipachar)
                tipachar = ''
            elif re.match("[A-z]", rawchar):
                while rawchar not in "{} " and re.match("[A-z]", rawchar):
                    tipachar = tipachar + rawchar
                    if len(string) > 0:
                        rawchar = string.pop(0)
                    else:
                        break
                output.append(tipachar)
        elif re.match("[A-z0-9@]", rawchar):
            output.append(rawchar)
        #if brackets ignore
        else: #some other character, should be { or }
            #print rawchar
            pass
    return output


def PhonParse(string):
    '''Input a string (in TIPA), returns a list of Phonemes'''
    characterlist = ParseTIPA(string)
    return [IPA[c] for c in characterlist]


IPA = doubleDict()


IPA['a'] = Phoneme(quick="+syll, +approx, +son, +cont, +del_rel, +voice, " +
                    "+dors, +low, 0tense")

IPA['5'] = Phoneme(quick="+syll, +approx, +son, +cont, +del_rel, +voice, " +
                    "+dors, +low, 0tense")

IPA['A'] = Phoneme(quick="+syll, +approx, +son, +cont, +del_rel, +voice, " +
                    "+dors, +low, +back, 0tense")



#currently no duplicates allowed due to double dictionary
# is this necessary?
#IPA['\textscripta'] = IPA['A']
                    

print PhonParse('aA')