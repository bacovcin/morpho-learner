#######
# Phonology.py
# @ Kobey Shwayder
# Contains class for morphophonological rules and the function to generate them
#######

from Util import *
from Feature import *
from IPA import *

class MPrule:
    def __init__(self):
        self._data = {} #_data has pairs of X:Y where MP rule changes X to Y
        self._rule = None #_rule will be active rule
        self._possiblerules = []  #possible rules consistent with data
        
        
def featureDifference(x,y, toprint = False):
    '''Takes two phonemes and returns difference in features to change X into Y'''
    if not isinstance(x, Phoneme):
        raise TypeException(x + "is not a Phoneme")
    if not isinstance(y, Phoneme):
        raise TypeException(y + "is not a Phoneme")
    diff = {}
    for feature in x._features.keys():
        if x[feature] != y[feature]:
            diff[feature] = y[feature]
    if toprint:
        return FeatureRepr(diff)
    return diff
    
   
     
def LDdist(s1, s2):
    '''Optimal String Alignment Metric through Levenshtein-Damerau distance'''
    if len(s1) < len(s2):
        return LDdist(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

if __name__ == "__main__":
    print LDdist("bb", "aa")
