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
    def __init__(self, data = {}, possiblerules = []):
        self._data = data #_data has pairs of X:Y:D where MP rule changes X to Y with D as Levenshtein matrix
        self._possiblerules = possiblerules  #possible rules consistent with data
        '''a rule is a list of processes (so multiple changes in one rule can happen), 
        each item in the list is a tuple (T,C,L) where T is type of change (ins, del, featch)
        C is the affected change and L is the location.
        L is list of possible tuple (type,side,dir,feats)
        In cases where multiple rules apply, the list is critically ordered'''
    def applyrule(self, rule, form):
#        for process in rule:
#            if rule[0] == 'ins':
#                #find place L and insert segment in C
#            elif rule[0] == 'del':
#                #find segment C or place L and delete it
#            elif rule[0] == 'featch':
#                #find segment and affect change
            
        pass

        
            
    def checkadd(self, newdata):
        '''newdata formatted (x,y) where x -> y
        checks all possible rules in this MP, winnows down to possible rules that fit this data as well
        or returns False if not possible'''
        # Need to have the ability to change restrictions on features if they match
        # note that the place restrictions are supersets?? of possible restrictions
        testingrules = self._possiblerules
        for rule in testingrules:
            if applyrule(rule, newdata[0]) != newdata[1]:
                testingrules.remove(rule)
        if len(testingrules) > 0:
            self._possiblerules = testingrules
            return True
        else:
            return False
                
def interpretrule(ruleset):
    for i, rule in enumerate(ruleset):
        humanreadable = str(i) + ") "
        if rule[0] == "ins": humanreadable += "insert "
        elif rule[0] == "del": humanreadable += "delete "
        elif rule[0] == "featch": humanreadable += "change to "
        else: raise TypeError("Rule type not ins, del, or featch: ", rule)
        
        if rule[0] == "ins": 
            rule[1] = "/" + IPA[rule[1]] + "/"
            
        humanreadable += str(rule[1]) + "\n"
        
        #where
        i = 0
        for location in rule[2]:
            i += 1
            humanreadable += "   " + chr(i+96) + ". "
            if location[0] == 'abs':
                humanreadable += str(location[3]) + " segs"
            elif location[0] == 'rel':
                if location[1] != 'none':
                    humanreadable += location[1] + " of "
                humanreadable += "first {" + FeatureRepr(location[3]) + "}" + " from " + location[2]    + "\n"
                humanreadable += "       = first " + str(subset(FeatureRepr(location[3])))
            else: raise TypeError("Location type not abs or rel: ", location)
            humanreadable += " from " + location[2]    + "\n"
        print humanreadable            
        
def featureDifference(x,y, raw = False, toprint = False, list = False, debug=False):
    '''Takes two phonemes and returns difference in features to change X into Y
    If list = True, it returns the list of changed features, otherwise it returns a number
    If raw == True, it return all changed features, otherwise it returns a modified
    set taking into consideration Feature geometry.'''
    if not isinstance(x, Phoneme):
        raise TypeError(x + " is not a Phoneme")
    if not isinstance(y, Phoneme):
        raise TypeError(y + " is not a Phoneme")
    diff = {}
    for feature in x._features.keys():
        if x[feature] != y[feature]:
            diff[feature] = y[feature]
    if raw and list:
        if toprint:
            return FeatureRepr(diff)
        return diff
    elif raw:
        return len(diff)
    else:
        #Skeletal features (syll) are hardest to change
        #Root node features (cons, son) are hard to change
        #Major articulators (lab, cor, dors, TR) are next
        # Where should manner features go?
        #Minor place features laryngeal features are easiest
        
        skel_weight = 1000
        root_weight = 100
        major_weight = 10
        minor_weight = 1
        
        skel = ['syll']
        root = ['cons', 'son']
        major = ['lab', 'cor', 'dors', 'TR']
        
        manner = ['cont', 'lat', 'nas', 'strid', 'del_rel']
        major.extend(manner)
        
        
#        '''Assumes -cor -> 0ant, 0dist
#        Assumes -dors -> 0high, 0back, 0low, 0front, 0tense 
#        Assumes -lab -> 0round'''
#        placenodes = {'lab':['round'], 'dors':['high', 'back', 'low', 'front', 'tense'],
#                      'cor':['ant', 'dist']}
#        for feat in placenodes.keys():
#            if feat in diff.keys() and diff[feat] in [Feature.Minus, Feature.NotSpecified, Feature.Any]:
#                for subfeat in placenodes[feat]:
#                    del diff[subfeat]


        # Changes:  changing to or from nasal shouldn't count as +/- sonorant as well, since sonorant has a high weight
        #            but the change from stop to nasal is pretty natural
        
        n = 0
        for feat in diff.keys():
            # Special Cases:  
            #1) changing to or from nasal shouldn't count as +/- sonorant as well, since sonorant has a high weight
            #but the change from stop to nasal is pretty natural
            if feat == 'son' and 'nas' in diff.keys():
                n = n
            # Normal Cases:
            elif feat in skel: n = n + skel_weight
            elif feat in root: n = n + root_weight
            elif feat in major: n = n + major_weight
            else: n = n + minor_weight
                    
        if debug: print IPA[x], ">", IPA[y], "=>", FeatureRepr(diff), "::", n
        
        return n
                
    
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
            pass #?? s[index] == "_"
    else:
        raise Exception("Side is not left, right, or none: ", side)
    
    if debug: print "Initial Feats", side, dir, Feats
    
    if dir == "left":
        for i in range(index-1, -1, -1):
            #from left
            #print "L>>>", i, IPA[s[i]]
            try:
                for feature in s[i]._features.keys():
                    if feature in Feats:
                        if s[i][feature] == Feats[feature]:
                            del Feats[feature]
            except AttributeError:
                pass # s[i] == "_"
    elif dir == "right":
        for i in range(index+1, len(s)):
            #from right
            #print "R>>>", i, IPA[s[i]]
            try:
                for feature in s[i]._features.keys():
                    if feature in Feats:
                        #print feature, Feats[feature], s[i][feature]
                        if s[i][feature] == Feats[feature]:
                            del Feats[feature]
            except AttributeError:
                pass # s[i] == "_"
            #print Feats
    else:
        raise Exception("Direction is not left or right: ", dir)
    
    return Feats
   
def findwhereDel(s, index, debug=False):
    '''Find where/what segment is deleted'''


    # Where:
    #  N segments from R or L
    #  before/after segment with features [X]
    #  First segment of type [X] fron R or L 

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
    
    firstR = SideofDirFeats("none", "right", s, index)
    firstL = SideofDirFeats("none", "left", s, index)
    
    # absolute position L, R
    # R of first [X] from L,  L of first [X] from R
    # R of first [X] from R, L of first [X] from L
    return (absPosL, absPosR, RightofLeftFeats, LeftofRightFeats, RightofRightFeats, LeftofLeftFeats, firstL, firstR)

def findwhereIns(s, index, debug = False):
    '''Find where a segment is inserted'''
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
    deletion_weight = -10
    addition_weight = -10
    
    #match weight should boost perfect matches
    #high match_weight will choose more matches (even with feature differences)
    match_weight = 70
    #if match_weight is lower in magnitude than add/del weight, wonky things happen
    
    
    # featurediff_weight should penalize partial matches down 
    #from perfect match boost
    # 0 means everything is a match
    # higher magnitude means feature difference is less likely to match
    # lower magnitude means feature difference is more likely to match 
    # positive is wonky
    featurediff_weight = -30
    
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
                featurediff_weight*featureDifference(s1[j-1],s2[i-1], debug=debug)\
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
    
def generateProcesses(input, output, debug=False):
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
    alignment = StrAlign(input, output, debug=debug)
    s1aln = alignment[0]
    s2aln = alignment[1]
    D = alignment[2]
    
    assert len(s1aln) == len(s2aln) #otherwise something is wrong with alignment
    
    word = s1aln
    
    
    processes = []
    
    if debug: print "START:", IPAword(filter(lambda x: x!= "_", word))
    #Find optimal processes:
    for i in range(len(s1aln)):
        '''a rule is a list of processes (so multiple changes in one rule can happen), 
        each item in the list is a tuple (T,C,L) where T is type of change (ins, del, featch)
        C is the affected change and L is the location.
        L is list of possible tuple (type,side,dir,feats)  type is 'abs' or 'rel'
        In cases where multiple rules apply, the list is critically ordered'''
        thisprocess = [None, None, None]
        if s1aln[i] == s2aln[i]:
            pass # it is a match
        elif s1aln[i] == '_':
            thisprocess[0] = 'ins'
            thisprocess[1] = s2aln[i]
            locations = []
            #it is an insertion
            where = findwhereIns(s2aln, i)
            
                    # absolute position L, R
                    # R of first [X] from L,  L of first [X] from R
                    # R of first [X] from R, L of first [X] from L
    
            if debug: print "insert /"+ IPA[s2aln[i]] + "/ :"
            if debug: print "   ", where[0], "segs from left"
            locations.append(['abs', 'none', 'left', where[0]])
            if debug: print "   ", where[1], "segs from right"
            locations.append(['abs', 'none', 'right', where[1]])
            if where[2] != {}:
                if debug: print "    R of first", (where[2]), "from left"
                locations.append(['rel', 'right', 'left', where[2]])
            if where[3] != {}:
                if debug: print "    L of first", (where[3]), "from right"
                locations.append(['rel', 'left', 'right', where[3]])
            if where[4] != {}:
                if debug: print "    R of first", (where[4]), "from right"
                locations.append(['rel', 'right', 'left', where[4]])
            if where[5] != {}:
                if debug: print "    L of first", (where[5]), "from left"
                locations.append(['rel', 'left', 'left', where[5]])
            word[i] = s2aln[i]
            if debug: print IPAword(filter(lambda x: x!= "_", word))
            thisprocess[2] = locations
            processes.append(thisprocess)
        elif s2aln[i] == '_':
            #it is a deletion
            thisprocess[0] = 'del'
            thisprocess[1] = '' # you don't know what to delete!
            locations = []
            
            where = findwhereDel(s1aln, i)
            
            if debug: print "Delete /"+ IPA[s1aln[i]] + "/ :"
            if debug: print "   ", where[0], "segs from left"
            locations.append(['abs', 'none', 'left', where[0]])
            if debug: print "   ", where[1], "segs from right"
            locations.append(['abs', 'none', 'right', where[1]])
            if where[2] != {}:
                if debug: print "    R of first", (where[2]), "from left"
                locations.append(['rel', 'right', 'left', where[2]])
            if where[3] != {}:
                if debug: print "    L of first", (where[3]), "from right"
                locations.append(['rel', 'left', 'right', where[3]])
            if where[4] != {}:
                if debug: print "    R of first", (where[4]), "from right"
                locations.append(['rel', 'right', 'right', where[4]])
            if where[5] != {}:
                if debug: print "    L of first", (where[5]), "from left"
                locations.append(['rel', 'left', 'left', where[5]])
            if where[6] != {}:
                if debug: print "    first", (where[6]), "from left"
                locations.append(['rel', 'none', 'left', where[6]])
            if where[7] != {}:
                if debug: print "    first", (where[7]), "from right"
                locations.append(['rel', 'none', 'right', where[7]])
            
            word[i] = s2aln[i]
            if debug: print IPAword(filter(lambda x: x!= "_", word))
            
            thisprocess[2] = locations
            processes.append(thisprocess)
            
        else:
            #it is a feature change
            thisprocess[0] = 'featch'
            thisprocess[1] = featureDifference(s1aln[i], s2aln[i], raw = True, list = True, toprint=True)
            locations = []
            #where?
            where = findwhereFeatChange(s1aln, i)
            if debug: print "change to ", featureDifference(s1aln[i], s2aln[i], raw = True, list = True, toprint=True),
            if debug: print "( /"+ IPA[s1aln[i]]+ "/ > /"+ IPA[s2aln[i]] + "/ )"
            if debug: print "   ", where[0], "segs from left"
            locations.append(['abs', 'none', 'left', where[0]])
            if debug: print "   ", where[1], "segs from right"
            locations.append(['abs', 'none', 'right', where[1]])
            if where[2] != {}:
                if debug: print "    first", (where[2]), "from left"
                locations.append(['rel', 'none', 'left', where[2]])
            if where[3] != {}:
                if debug: print "    first", (where[3]), "from right"
                locations.append(['rel', 'none', 'right', where[3]])
                
            word[i] = s2aln[i]
            if debug:  print IPAword(filter(lambda x: x!= "_", word))
            
            thisprocess[2] = locations
            processes.append(thisprocess)
    #Find other processes:
        
    return processes
    
def MultiplePairTest(list):
    '''test multiple pairs of strings.  list should be list of tuples a>b.  a and b need to be r'strings' '''
    for (a,b) in list:
        print a, " > ", b
        interpretrule(generateProcesses(PhonParse(a), PhonParse(b)))
    return None
    
if __name__ == "__main__":
    #print len(featureDifference(IPA['u'], IPA['P']))
    MultiplePairTest([(r'pater',r'patr'), (r'iken', r'ikn'), (r'wOk', r'wOkt'), 
                      (r'fil', r'felt'), (r'oae', r'oe')])
    #generateProcesses(PhonParse(r'oae'), PhonParse(r'oe'), debug=True)

