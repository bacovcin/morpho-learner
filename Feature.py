#####
# Feature.py
# @Kobey Shwayder
# Contains Phoneme class and phonparse method
#####

import re

class Feature:
    Plus = 1
    Minus = 2
    Marked = 3
    Unmarked = 4
    NotSpecified = 5
    Needs = 6
    Any = 0
    
def FeatureOpposite(val):
    if val == 1: return 2
    if val == 2: return 1
    if val == 3: return 4
    if val == 4: return 3
    else: return None
        
class Phoneme:
    def __init__(self, voc = Feature.NotSpecified, high = Feature.NotSpecified,
                 back = Feature.NotSpecified, round = Feature.NotSpecified,
                 ATR = Feature.NotSpecified, nasal = Feature.NotSpecified,
                 sonorant = Feature.NotSpecified, labial = Feature.NotSpecified,
                 lateral = Feature.NotSpecified, velar = Feature.NotSpecified,
                 cont = Feature.NotSpecified, coronal = Feature.NotSpecified,
                 voiced = Feature.NotSpecified, low = Feature.NotSpecified,
                 markedposition = Feature.NotSpecified, consonantal = Feature.NotSpecified,
                 unmarkedposition = Feature.NotSpecified):
        self._features = {}
        self._features['voc'] = voc
        self._features['high'] = high
        self._features['back'] = back
        self._features['round'] = round
        self._features['ATR'] = ATR
        self._features['nasal'] = nasal
        self._features['sonorant'] = sonorant
        self._features['lateral'] = lateral
        self._features['velar'] = velar
        self._features['cont'] = cont
        self._features['coronal'] = coronal
        self._features['low'] = low
        self._features['voiced'] = voiced
        self._features['markedposition'] = markedposition
        self._features['unmarkedposition'] = unmarkedposition
        self._features['labial'] = labial
        self._features['consonantal'] = consonantal
    def __repr__(self):
            toReturn = '<Phoneme: '
            keys = self._features.keys()
            keys.sort()
            for f in keys:
                if(self._features[f] == Feature.Plus):
                    toReturn += "+%s, "%f
                elif(self._features[f] == Feature.Minus):
                    toReturn += "-%s, "%f
                elif(self._features[f] == Feature.Needs):
                    toReturn += "?%s, "%f
                elif(self._features[f] == Feature.Marked):
                    toReturn += "m%s, "%f
                elif(self._features[f] == Feature.Unmarked):
                    toReturn += "u%s, "%f 
                elif(self._features[f] == Feature.Any):
                    toReturn += "@%s, "%f  
                else: #Feature.NotSpecified
                   pass
            return toReturn[:-2] + ">" #remove last comma and space
    def needy(self):
        needs = [feat for feat in self._features.keys()
                 if self._features[feat] == Feature.Needs]
        if needs == []:
            return None
        else:
            return needs
    def __getitem__(self, key):
        '''Phoneme[key]'''
        return self._features[key]
    def __setitem__(self, key, value):
        '''Phoneme[key] = value'''
        self._features[key] = value
    def __eq__(self, other):
        '''Phoneme == other'''
        if not isinstance(other, self.__class__):
            return False
        for feat in self._features.keys():
            if self._features[feat] != other._features[feat]:
                return False
        return True
    def __ne__(self, other):
        '''Phoneme != other'''
        return not self.__eq__(other)

def PhonParse(string):
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
                
    