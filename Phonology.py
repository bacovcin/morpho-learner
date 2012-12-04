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
        raise TypeError(x + " is not a Phoneme")
    if not isinstance(y, Phoneme):
        raise TypeError(y + " is not a Phoneme")
    diff = {}
    for feature in x._features.keys():
        if x[feature] != y[feature]:
            diff[feature] = y[feature]
    if toprint:
        return FeatureRepr(diff)
    return diff
    
   
     
def StrAlign(s1, s2):
    '''Optimal String Alignment with dynamic programming'''
    n = len(s1)
    m = len(s2)
    
    D = [range(n+1)] * (m+1)
    for i in range(len(D)):
        D[i] = range(i, n+i+1)
    
    #gap score should penalize gap creation
    # Positive gap score will create all addition/deletion solutions
    gap_score = -2
    
    #match weight should boost perfect matches
    match_weight = 4
    #if match_weight is lower magnitude than gap score wonky things happen
    
    # featurediff_weight should penalize partial matches down 
    #from perfect match boost
    # 0 means everything is a match
    # higher magnitude means feature difference is less likely to match
    # lower magnitude means feature difference is more likely to match 
    # positive is wonky
    featurediff_weight = -1
    
    D[0][0] = 0
    
    #for row in D: print row
    
    for j in range(n+1):
        D[0][j] = gap_score*j
    for i in range(m+1):
        D[i][0] = gap_score*i
        
    #for row in D: print row
    
    for i in range(1,m+1):
        for j in range(1, n+1):
            #match score is function of feature difference
            #match_score = +match_weight
            match_score = \
                featurediff_weight*len(featureDifference(s1[j-1],s2[i-1]))\
                        + match_weight
            
            match = D[i-1][j-1] + match_score
            gap_s1 = D[i][j-1] + gap_score
            gap_s2 = D[i-1][j] + gap_score
            #print j, i
            #print s1[j-1], s2[i-1]
            #print match, gap_s1, gap_s2
            D[i][j] = max(match, gap_s1, gap_s2)
    
    for row in D: print row
    
    score = D[m][n]
    
    #print score
    
    i = m
    j = n
    
    s1aln = []
    s2aln = []
    

    while i>0 and j>0:
        match = abs(D[i][j] - D[i-1][j-1])
        gap1 = abs(D[i][j] - D[i][j-1] )
        gap2 = abs(D[i][j] - D[i-1][j])
        #print i,j
        #print match, gap1, gap2
        if min(match, gap1, gap2) == match:
            s1aln.insert(0,s1[j-1])
            s2aln.insert(0,s2[i-1])
            i = i-1
            j= j-1
            #print "match", [IPA[c] for c in s1aln], [IPA[c] for c in s2aln]
        elif min(match, gap1, gap2) == gap1:
            s1aln.insert(0,s1[j-1])
            s2aln.insert(0,"_")
            j = j-1
            #print "not match", [IPA[c] for c in s1aln], [IPA[c] for c in s2aln]
        elif min(match, gap1, gap2) == gap2:
            s2aln.insert(0,s2[i-1])
            s1aln.insert(0,"_")
            i = i-1
            #print "not match", [IPA[c] for c in s1aln], [IPA[c] for c in s2aln]
        else:
            raise Error("Should not happen")
    if j>0:
        while j > 0:
            s1aln.insert(0,s1[j-1])
            s2aln.insert(0,"_")
            j = j-1
    elif i > 0:
        while i > 0 :
            s1aln.insert(0,"_")
            s2aln.insert(0,s2[i-1])
            i = i-1
     
               
    print [IPA[c] for c in s1aln]
    print [IPA[c] for c in s2aln]
    
    
    

if __name__ == "__main__":
    # 4 and 0 and 1 an 13
    #print len(featureDifference(IPA['u'], IPA['P']))
    print StrAlign(PhonParse(r'v{\ae}tu'), PhonParse(r'p{\ae}TP'))#"sing", "gesang")

