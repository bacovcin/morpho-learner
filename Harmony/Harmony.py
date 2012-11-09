# -*- coding: utf-8 -*-
from Feature import *
from Languages import *
from copy import deepcopy


def getSonority(phoneme):
    '''Returns the sonority of a phoneme.
       if a phoneme is unspecified for a sonority-relevant
       feature, it is assumed to be the higher value'''
    #Currently not handling glides
    sonority = 0
    if phoneme['voc'] == Feature.Plus: 
        sonority += 3
        if phoneme['low'] == Feature.Plus or \
           phoneme['low'] == Feature.NotSpecified:
            sonority += 2
        if phoneme['high'] == Feature.Minus or \
           phoneme['high'] == Feature.NotSpecified:
            sonority += 2
        if phoneme['ATR'] == Feature.Minus or \
           phoneme['ATR'] == Feature.NotSpecified:
            sonority += 1
    if phoneme['sonorant'] == Feature.Plus: sonority += 1
    return sonority
            

def CompareLeftandRight(language, word, P, tau, F, debug = False):
    '''Completes a bidirectional harmony search'''
    if debug:
        print "Looking Left"
    wordLeft = Harmony(language, deepcopy(word), P, tau, -1, F, debug)
    #deepcopy creates a new word
    if debug:
        print "Looking Right"
    wordRight = Harmony(language, deepcopy(word), P, tau, 1, F, debug)
    if wordLeft == wordRight:
        return wordLeft
    else:
        return False

def IsOpaque(language, R, phoneme):
    '''returns true if Phoneme contains features in R'''
    for k in R.keys():
        if phoneme[k] != R[k]:
            return False
        else:
            return True

def IsGloballyMarked(language, feature, phoneme):
    '''returns true if phoneme is globally marked for feat in language'''
    if not language.GlobalMarkedness.has_key(feature):
        return True
    if phoneme[feature] == language.GlobalMarkedness[feature]:
        return True
    else:
        return False
    
def IsContextuallyMarked(language, feature, phoneme):
    '''returns true if phoneme is contextually marked for feat in language'''
    #ContextSensitiveMarkedness is a dictionary of the form
    #  ("feature", Feature.Value) -->  [("feature", Feature.Value)...]
    if not (language.ContextSensitiveMarkedness.has_key((feature, phoneme[feature]))):
        return True
    contexts = language.ContextSensitiveMarkedness[(feature, phoneme[feature])]
    for context in contexts:
        if phoneme[context[0]] == context[1]:
            return True
    return False

def IsContrastive(language, feature, phoneme):
    '''returns true if phoneme is contrastive for feature in language'''
    value = phoneme[feature]
    ContrastingPhoneme = deepcopy(phoneme)
    if value == Feature.Plus:
        ContrastingPhoneme[feature] = Feature.Minus
    elif value == Feature.Minus:
        ContrastingPhoneme[feature] = Feature.Plus
    elif value == Feature.Marked:
        ContrastingPhoneme[feature] = Feature.Unmarked
    elif value == Feature.Unmarked:
        ContrastingPhoneme[feature] = Feature.Marked        
    else: #feature is not Plus or Minus nor Marked/Unmarked and therefore not contrastive
        return False
    return language.hasPhoneme(ContrastingPhoneme)

def IsPositionallyContrastive(language, feature, word, P, debug = False):
    '''Checks position of P in word and returns true if that phoneme is 
        positionally contrastive in language'''
    value = word[P][feature]
    ContrastingPhoneme = deepcopy(word[P])
    if debug:
        print "\n\t\t\t^^ %d is marked: %s \t\t\t" \
                           %(P, language.MarkedPosition(word, P)),
    if (word[P]["markedposition"] != Feature.NotSpecified and \
        word[P]["unmarkedposition"] != Feature.NotSpecified):
        if language.MarkedPosition(word, P):
           ContrastingPhoneme["markedposition"] = Feature.Plus
           ContrastingPhoneme["unmarkedposition"] = Feature.Any
        else:
            ContrastingPhoneme["markedposition"] = Feature.Any
            ContrastingPhoneme["unmarkedposition"] = Feature.Plus
    if value == Feature.Plus:
        ContrastingPhoneme[feature] = Feature.Minus
    elif value == Feature.Minus:
        ContrastingPhoneme[feature] = Feature.Plus
    elif value == Feature.Marked:
        ContrastingPhoneme[feature] = Feature.Unmarked
    elif value == Feature.Unmarked:
        ContrastingPhoneme[feature] = Feature.Marked        
    else: #feature is not Plus or Minus nor Marked/Unmarked and therefore not contrastive
        return False
    return language.hasPhoneme(ContrastingPhoneme)
            
            
def Harmony(language, word, P, tau, delta, F, beta, gamma, sigma, debug = False):
    '''An implementation of Andrew's algorithm'''
    myValue = word[P]
    mySegsTraversed = 0
    mySyllsTraversed = 0    
    if debug:
        print "Phoneme at index %d: %s" % (P, myValue)
        print "                   needs features", F
    if isinstance(delta, str):
        if delta.lower() == 'l&r' or delta.lower() == 'both':
            return CompareLeftandRight(language, word, P, tau, F, debug)
        elif delta.lower()[0] == 'r':
            delta = 1
        elif delta.lower()[0] == 'l':
            delta = -1
    if abs(delta) != 1:
        raise ValueError("delta must be 1 or -1, delta = %d" % delta)
    found = True
    needsMarked = False
    sonorityBroken = False
    while len(F) > 0:
        P = P + delta
        mySegsTraversed += 1
        if P>=len(word) or P < 0:
            if needsMarked == False:
                found = False
                break
            else:
                break  
        #is past syllable or segment limit?
        if gamma: #gamma is not infinite
            if gamma == 'countSegs' and mySegsTraversed > beta:
                if debug:
                    print "   !past segment limit"
                found = False
                break
            if gamma == 'countSylls' and mySyllsTraversed > beta:
                if debug:
                    print "   !past syllable limit"
                found = False
                break
        #Check if sonority threshold was broken by preceding segment     
        if sonorityBroken: break
        #
        toRemove = []
        validSource = 'Valid'
        for feat in F:
            phoneme = word[P]
            if(phoneme == "."):
                mySyllsTraversed += 1
                mySegsTraversed -= 1 #subtract one, because one was added, 
                                     #but '.' is not a segment
                if debug:
                    print "sg %s, sl %s    looking at %s: syllable break" % \
                    (mySegsTraversed, mySyllsTraversed, P)
                break      
            if debug:
                print "    looking at %s(%s): %s" % (P, feat, phoneme),
            validSource = 'Valid'
            # Check Sonority Tolerance on segment
            if sigma != 0: #if sonority plays a role:
                if debug:
                    print "son:", getSonority(phoneme), ">", sigma,
                if getSonority(phoneme) > sigma:
                    myValue[feat] = phoneme[feat]
                    if debug: print "* >Sonority Thresh., copying value"
                    sonorityBroken = True
                    break
            #     
            for f in [k for k in tau.keys() if k != 'tauType' and k != 'R']:
                if phoneme[f] != tau[f]:
                    validSource = 'Invalid: %s' % f
            if validSource == 'Valid':
                types = [t for t in tau['tauType']]
                if types == ['All']: validity = "Valid"
                else: validity = False
                invalidity = []
                if types and "contrastive" in types:
                    if not IsContrastive(language, feat, phoneme):
                        invalidity.append("Contrastive")
                    else:
                        validity = 'Valid: Contrastive for %s' % feat
                    types.remove('contrastive')
                if types and "positionally_contrastive" in types:
                    if not IsPositionallyContrastive(language, feat, word, P):
                        invalidity.append("Pos.Cntr.")
                    else:
                        validity = 'Valid: Pos. Contr for %s' % feat
                    types.remove('positionally_contrastive')
                if types and 'marked' in types:
                    if not IsContextuallyMarked(language, feat, phoneme):
                        needsMarked = True
                        invalidity.append("Cntx.Sens")
                        #put in default value now, so it will be there if no marked value is found
                        myValue[feat] = FeatureOpposite(phoneme[feat]) 
                    elif not IsGloballyMarked(language, feat, phoneme):
                        needsMarked = True
                        invalidity.append("Marked")
                        #put in default value now, so it will be there if no marked value is found
                        myValue[feat] = FeatureOpposite(phoneme[feat])
                    else:
                        validity = 'Valid: Marked for %s' % feat
                if validity: validSource = validity
                else: 
                    reasons = ''
                    for reason in invalidity: reasons += reason + '/'
                    validSource = 'Invalid: Not %s for %s' % (reasons[:-1], feat)
            if validSource.startswith('Valid') and tau.has_key('R'):
                if IsOpaque(language, tau['R'], phoneme):
                    validSource = 'Opaque: Blocked!'
            if debug:
                print validSource
            if validSource.startswith('Valid') and \
               (phoneme[feat] == Feature.Plus or \
                phoneme[feat] == Feature.Minus or \
                phoneme[feat] == Feature.Marked or \
                phoneme[feat] == Feature.Unmarked):
                if debug:
                    print "  * match \'%s\' on %s" % (feat, phoneme)
                myValue[feat] = phoneme[feat] 
                toRemove.append(feat)
        if validSource == 'Opaque: Blocked!':
            found = False
            break
        F = list(set(F) - set(toRemove))
    if debug:
        print "  * myValue set to", myValue
    if found:
        return word
    else:
        return False

def Harmonize(language, root, prefixes = [], suffixes = [], debug = False):
    '''takes a root + morpheme and a language and runs Harmony'''
    word = root
    needylist = []
    #membership is the list of what phoneme belongs to what morpheme
    membership = ['root' for i in range(len(root))]
    for i in range(len(prefixes)-1, -1, -1): #Goes in reverse for prefixes
        (word, needylist) = AddAffix(needylist, word,
                                     language.getMorpheme(prefixes[i]),
                                     'pre', debug)
        membership[0:0] = [prefix[i] for x in
                      range(len(language.getMorpheme(prefixes[i]).form))]
    for i in range(len(suffixes)):
        (word, needylist) = AddAffix(needylist, word,
                                     language.getMorpheme(suffixes[i]),
                                     'post', debug)
        membership += [suffixes[i] for x in
              range(len(language.getMorpheme(suffixes[i]).form))]
    if debug:
        print "word:", word
        print "needy:", needylist
        print "membership:", membership
    for needy in needylist:
        buildword = Harmony(language, word, needy[0], needy[1],
                            needy[2], needy[3], needy[4], needy[5], needy[6], debug)
        if buildword == False:
            #then a search failed
            #or no contrastive value donor found
            #revert to default morpheme
            thisMorpheme = membership[needy[0]] #needy[0] is index of phoneme
            (start, end) = getRange(membership, thisMorpheme)
            defaultMorpheme = needy[7]  #needy[7] is default morpheme value
            if debug:
                print "search failure: replacing morpheme in range %s:%s with default:" % (start, end)
                try:
                    print "               %s <--" % str([language[l] for l in defaultMorpheme]), defaultMorpheme
                except TypeError:
                    raise LookupError('No Default Morpheme')
            buildword = word
            buildword[start:end] = defaultMorpheme
        word = buildword
    s = ''
    for letter in word:
        #print letter
        s += language[letter]
    return s

def getRange(l, x):
    '''gets the range of an item x in a list l'''
    start = l.index(x)
    end = len(l)
    for i in range(start, len(l), 1):
            if l[i] != x:
                    end = i
                    break
    return (start, end)
    
def AddAffix(needylist, root, affix, side, debug = False):
    word = root
    if side == 'pre' or side == 'left':
        word = affix.form + word
    elif side == 'post' or side == 'right':
        word += affix.form
    else:
        raise ValueError("Side " + side)
    word = ResolveSyllables(word)
    if debug:
        print "resolved", word
    needy = [(index, word[index].needy()) 
         for index in range(len(word)) if isinstance(word[index], Phoneme) and
             word[index].needy() and [n[0] for n in needylist].count(index) == 0]
    for needyletter in needy:
        needylist.append((needyletter[0], affix.tau,
                       affix.delta, needyletter[1], 
                       affix.beta, affix.gamma, affix.sigma, affix.default))
    return (word, needylist)
    
def ResolveSyllables(word):
    for index in range(len(word) - 1):
        if word[index:index+2] == ['.', '.']:
            word[index:index+2] = ['*', '*']
            for j in range(len(word[:index]), 0, -1):
                if word[j] == '*':
                    word[j] = '.'
                    break
    return [w for w in word if w != '*']
                            

if __name__ == '__main__':

    currLang = Jingulu
    
    root = currLang.Parse('')
                         
    suffix = []
    prefix = ['sibling']
    
    #set debug to False if you just want the answer
    #set debug to True if you want to see the trace
    answer = Harmonize(currLang, root, prefixes = prefix, suffixes = suffix,
                       debug = True)

    print "answer= %s" % answer


    
