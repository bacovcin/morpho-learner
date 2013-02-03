#######
# Phonology.py
# @ Kobey Shwayder
# Contains class for morphophonological rules and the function to generate them
#######

from Util import *
from Feature import *
from IPA import *
from copy import deepcopy

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
    
    
def SideofDirFeats(side, dir, s, index, debug=False):
    Feats = {}
    
    if side == "left":
        if index < len(s)-1:
        #to left of
            try:
                OnlyPlusMinus = filter(lambda x:s[index+1]._features[x]==1 or s[index+1]._features[x]==2, s[index+1]._features)
                for feat in OnlyPlusMinus:
                    Feats[feat] = s[index+1][feat]
            except AttributeError: 
                pass #s[index+1] == "_"
    elif side == "right":
        if index > 0:
        #to right of
            try:
                OnlyPlusMinus = filter(lambda x:s[index-1]._features[x]==1 or s[index-1]._features[x]==2, s[index-1]._features)
                for feat in OnlyPlusMinus:
                    Feats[feat] = s[index-1][feat]
            except AttributeError: 
                pass #s[index-1] == "_"
    elif side == "none":
        try:
            OnlyPlusMinus = filter(lambda x:s[index]._features[x]==1 or s[index]._features[x]==2, s[index]._features)
            for feat in OnlyPlusMinus:
                Feats[feat] = s[index][feat]
        except AttributeError: 
	    pass #s[index-1] == "_"
    else:
        raise Exception("Side is not left, right, or none: ", side)
    
    if debug: print "Initial Feats", side, dir, Feats
    
    
    if dir == "left":
        for i in range(0, index-2):
            #from left
            try:
                for feature in s[i]._features.keys():
                    if feature in Feats:
                        if s[i][feature] == Feats[feature]:
                            del Feats[feature]
            except AttributeError:
                pass # s[i] == "_"
    elif dir == "right":
        for i in range(len(s)-1, index+2, -1):
            #from right
            try:
                for feature in s[i]._features.keys():
                    if feature in Feats:
                        if s[i][feature] == Feats[feature]:
                            del Feats[feature]
            except AttributeError:
                pass # s[i] == "_"
    else:
        raise Exception("Direction is not left or right: ", dir)
    
    return Feats
   

def findwhereInsDel(s, index, debug = False):
    '''Find where a segment is inserted or deleted'''
    # Where:
    #  N segments from R or L
    #  before/after segment with features [X]
    #  Syll structure?
    #s = filter(lambda x: x!="_", s)
    absPosL = index
    absPosR = len(s) - (index + 1)
    
    #From L, to left or right of first [X]
    #From R, to left or right of first [X]

    
    RightofLeftFeats = SideofDirFeats("right", "left", s, index) #To right of first X from left
    LeftofRightFeats = SideofDirFeats("left", "right", s, index) #To left of first X from right
    RightofRightFeats = SideofDirFeats("right", "right", s, index)
    LeftofLeftFeats = SideofDirFeats("left", "left", s, index)
                       
                    
    
    if debug: print "RL", RightofLeftFeats
    if debug: print "LR", LeftofRightFeats
    if debug: print "LL", LeftofLeftFeats
    if debug: print "RR", RightofRightFeats

    # absolute position L, R
    # R of first [X] from L,  L of first [X] from R
    # R of first [X] from R, L of first [X] from L
    return (absPosL, absPosR, RightofLeftFeats, LeftofRightFeats, RightofRightFeats, LeftofLeftFeats)
        
def findwhereFeatChange(s, index, debug=False):
    '''Find which segment undergoes feature change'''
    #s = filter(lambda x: x!="_", s)
    absPosL = index
    absPosR = len(s) - (index + 1)
    
    Left = SideofDirFeats("none", "left", s, index)
    Right = SideofDirFeats("none", "right", s, index)
    
    return (absPosL, absPosR, Left, Right)
    
        
     
def StrAlign(s1, s2, debug=False):
    '''Optimal String Alignment with dynamic programming'''
    n = len(s1)
    m = len(s2)
    
    D = [range(n+1)] * (m+1)
    for i in range(len(D)):
        D[i] = range(i, n+i+1)
    
    #deletion and addition scores should penalize segment deletion and addition
    # Positive scores will create all deletion/addition solutions
    deletion_weight = -3
    addition_weight = -3
    
    #match weight should boost perfect matches
    #high match_weight will choose more matches (even with feature differences)
    match_weight = 9
    #if match_weight is lower in magnitude than add/del weight, wonky things happen
    
    
    # featurediff_weight should penalize partial matches down 
    #from perfect match boost
    # 0 means everything is a match
    # higher magnitude means feature difference is less likely to match
    # lower magnitude means feature difference is more likely to match 
    # positive is wonky
    featurediff_weight = -2
    
    D[0][0] = 0
    
    #for row in D: print row
    
    for j in range(n+1):
        D[0][j] = addition_weight*j
    for i in range(m+1):
        D[i][0] = deletion_weight*i
        
    #for row in D: print row
    
    for i in range(1,m+1):
        for j in range(1, n+1):
            #match score is function of feature difference
            #match_score = +match_weight
            match_score = \
                featurediff_weight*len(featureDifference(s1[j-1],s2[i-1]))\
                        + match_weight
            
            match = D[i-1][j-1] + match_score
            gap_s1 = D[i][j-1] + addition_weight
            gap_s2 = D[i-1][j] + deletion_weight
            #print j, i
            #print s1[j-1], s2[i-1]
            #print match, gap_s1, gap_s2
            D[i][j] = max(match, gap_s1, gap_s2)
    
    if debug: 
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
     
               
    if debug: print [IPA[c] for c in s1aln]
    if debug: print [IPA[c] for c in s2aln]
    
    return (s1aln, s2aln, D)
    
def generateProcesses(input, output):
    '''Takes two strings and returns possible processes to convert str1 to str2'''
    # What:
    #  Insert X
    #  Delete X
    #  Change X to Y
    # Where:
    #  N segments from R or L
    #  Nth segment with features [X] from R or L
    #  before/after segment with features [X]
    #  Syll structure?
    alignment = StrAlign(input, output, debug=True)
    s1aln = alignment[0]
    s2aln = alignment[1]
    D = alignment[2]
    
    assert len(s1aln) == len(s2aln) #otherwise something is wrong with alignment
    
    changes = []
    
    word = s1aln
    
    
    print "START:", IPAword(filter(lambda x: x!= "_", word))
    #Find optimal processes:
    for i in range(len(s1aln)):
        if s1aln[i] == s2aln[i]:
            pass # it is a match
        elif s1aln[i] == '_':
            #it is an insertion
            where = findwhereInsDel(s2aln, i)
            
                    # absolute position L, R
                    # R of first [X] from L,  L of first [X] from R
                    # R of first [X] from R, L of first [X] from L
    
            print "insert /"+ IPA[s2aln[i]] + "/ :"
            print "   ", where[0], "segs from left"
            print "   ", where[1], "segs from right"
            if where[2] != {}:
                print "    R of first", (where[2]), "from left"
            if where[3] != {}:
                print "    L of first", (where[3]), "from right"
            if where[4] != {}:
                print "    R of first", (where[4]), "from right"
            if where[5] != {}:
                print "    L of first", (where[5]), "from left"
            word[i] = s2aln[i]
            print IPAword(filter(lambda x: x!= "_", word))
        elif s2aln[i] == '_':
            #it is a deletion
            print findwhereInsDel(s1aln, i)
            
            word[i] = s2aln[i]
            print IPAword(filter(lambda x: x!= "_", word))
        else:
            #it is a feature change
          
            #where?
            where = findwhereFeatChange(s1aln, i)
            print "change to ", featureDifference(s1aln[i], s2aln[i], toprint=True),
            print "( /"+ IPA[s1aln[i]]+ "/ > /"+ IPA[s2aln[i]] + "/ )"
            print "   ", where[0], "segs from left"
            print "   ", where[1], "segs from right"
            if where[2] != {}:
                print "    first", (where[2]), "from left"
            if where[3] != {}:
                print "    first", (where[3]), "from right"
                
            word[i] = s2aln[i]
            print IPAword(filter(lambda x: x!= "_", word))
    #Find other processes:
        
    return None
    


if __name__ == "__main__":
    # 4 and 0 and 1 an 13
    #print len(featureDifference(IPA['u'], IPA['P']))
    #print generateProcesses(PhonParse(r'sIN'), PhonParse(r'sUN'))#"sing", "gesang")
    print generateProcesses(PhonParse(r'patreys'), PhonParse(r'pater'))

