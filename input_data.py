from Comb import *
from itertools import repeat

class word(object):
    def __init__(self,phon,morph):
        self.phonology = phon           #list of segments with features
        self.morphology = list(morph)   #ordered list of m-feature
                                        #sets  associated with word

class exponent(object):
        def __init__(self,phonology,side):
            self.phon = phonology       #phonology of exponent
            self.side = side            #adfix type (suffix/prefix/?infix) 0 = undefined
            

class vocab_item(object):
    def __init__(self,morph_feature,phonology,side,context):
        self.morph_feature = morph_feature       #m-feature to be spelled out
        self.exponent = exponent(phonology,side) #exponent and adfix status
        self.context = context                   #when to use this item
        
class settings(object):
    def __init__(self, complexity, length, phon):
        self.complexity = complexity #reward for null phonology
        self.length = length         #weight of the list length penalty
        self.phon = phon             #weight of the phonology vs. allomorphy 
                                     #penalty, which can be negative

def Dictionaryify(input):
    lexicon = {} 
    for word in input:
        for morph in word.morphology:
            try:
                lexicon[morph[0]][morph[1]] = word
            except:
                lexicon[morph[0]] = {morph[1]:word}
    return lexicon

def find_common_substring(word_list):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    long_string =""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string

    result = ''
    for j in range(len(long_string)):
        for i in range(len(long_string)-1,-1,-1):
            if len(long_string[j:i]) > len(result):
                if is_common_substr(long_string[j:i],word_list):
                    result = long_string[j:i]
    return result

def create_model_space(lexicon, ordering):
    listOfTypeModels = []
    for type in ordering:
        listOfMorphs = []
        for morph in lexicon[type]:
            setOfTriggers = set((morph, x) for y in set(ordering) - set([type]) 
                                  for x in lexicon[y].keys())
            listOfMorphs.append(product([morph,set_combs(setOfTriggers)]))
        listOfTypeModels.append(product(listOfMorphs))
    return list(product(listOfTypeModels))
