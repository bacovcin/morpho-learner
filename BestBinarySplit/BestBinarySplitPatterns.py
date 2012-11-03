#The Best Binary Split Algorithm
# Version 3:Reranking using Natural Class patterning
# MA Thesis, Computational Linguistics, Brandeis University
# @author: Kobey Shwayder

from copy import deepcopy

class Feature:
        '''This is the struct to define what + and - mean for a feature'''
        Plus = 1
        Minus = 2
        NotSpecified = 5

def FeatureOpposite(featval):
        '''This method returns the opposite value of a feature'''
        if featval == 1: return 2
        elif featval == 2: return 1
        else: return featval

GlobalFeats = ['high', 'low', 'front', 'back', 'round', 'ATR']
globalDefaultRanks = {'low' : 0, 'high' : 1, 'back' : 2,
                  'front':3, 'round':4, 'ATR': 5}

class Vowel:
        '''the vowel class'''
        def __init__(self, char, high = Feature.NotSpecified, 
                        low = Feature.NotSpecified,
                        front = Feature.NotSpecified, 
                        back = Feature.NotSpecified,
                        round = Feature.NotSpecified, 
                        ATR = Feature.NotSpecified,
                        long = Feature.Minus):
                self._features = {}
                self._features['high'] = high
                self._features['front'] = front
                self._features['back'] = back
                self._features['low'] = low
                self._features['round'] = round
                self._features['ATR'] = ATR
                self._features['long'] = long
                self.symbol = char

        def __repr__(self):
                '''the string representation of the Vowel'''
                toReturn = '<Vowel-\'%s\': ' % self.symbol.encode('UTF-8')
                keys = self._features.keys()
                keys.sort()
                for f in keys:
                        if(self._features[f] == Feature.Plus):
                                toReturn += "+%s, "%f
                        elif(self._features[f] == Feature.Minus):
                                toReturn += "-%s, "%f
                        else: #Feature.NotSpecified
                           pass
                return toReturn[:-2] + ">" #remove last comma and space
                
        def __getitem__(self, key):
                '''Vowel[key]'''
                return self._features[key]
        def __setitem__(self, key, value):
                '''Vowel[key] = value'''
                self._features[key] = value
        def __eq__(self, other):
                '''Vowel == other'''
                if not isinstance(other, self.__class__):
                        return False
                for feat in self._features.keys():
                        if self._features[feat] != other._features[feat]:
                                return False
                return True
        def __ne__(self, other):
                '''Vowel != other'''
                return not self.__eq__(other)

def rankFeatures(tiedFeatures,
                ranks = globalDefaultRanks):
        '''Given the tied features and a ranking, split the tie'''
        ranked = [(ranks[f],f) for f in tiedFeatures]
        ranked.sort()
        return [p[1] for p in ranked]

def FindBestSingle(matrix, ranking, relevantFeats):
        '''Finds the best feature to split by breaking ties with rankFeatures'''
        splits = {}
        for f in matrix:
                if not splits.has_key(matrix[f]): splits[matrix[f]] = []
                splits[matrix[f]].append(f)
        for k in splits: 
                if len(splits[k]) > 1: splits[k] = rankFeatures(splits[k],
                                                                ranks = ranking)

        splits = [(k, splits[k]) for k in splits]
        splits.sort()
        return splits[0][1][0]

                        
def findBestSplit(sets, ranking, features, relevantFeats):
        '''Finds the best split by scoring each feature and
        passing the scores to FindBestSingle'''
        if len(sets) == 1:
                return FindBestSingle(sets[0], ranking, relevantFeats)
        else:
                scores = {}
                for feature in features:
                        scoreList = []
                        for set in sets:
                                if set.has_key(feature):
                                         scoreList.append(set[feature])
                                else:
                                        scoreList = []
                                        break
                        if scoreList != []: scores[feature] = scoreList
                for key in scores:
                        scores[key] = sum(scores[key])/len(scores[key])
                return FindBestSingle(scores, ranking, relevantFeats)
                                

def splitSet(vowelsets, feature):
        '''splits a vowelset on the feature by dividing each subset into
        two subsets the [+feature] and the [-feature] subset'''
        newVowelSet = []
        for vowels in vowelsets:
                if isinstance(vowels, list):
                        plus = []
                        minus = []
                        for vowel in vowels:
                                if vowel[feature] == Feature.Plus:
                                        plus.append(vowel)
                                if vowel[feature] == Feature.Minus:
                                        minus.append(vowel) 
                        for sign in [plus, minus]:
                                if len(sign) > 1: newVowelSet.append(sign)
        return newVowelSet      
        

def distinguish(vowelsets, ranks = globalDefaultRanks,
                features = GlobalFeats, relevantFeats = []):
        '''the main method for distinguishing a vowel set'''
        results = []    
        for vowels in vowelsets:
                if isinstance(vowels, list):
                        print [v.symbol for v in vowels]
                        matrix = {}
                        for f in features:
                                matrix[f] = [v[f] for v in vowels]
                        for f in matrix:
                                matrix[f] = \
                                 max(float(matrix[f].count(Feature.Plus))/\
                                             len(matrix[f]),
                                     float(matrix[f].count(Feature.Minus))/\
                                             len(matrix[f]))
                        results.append((vowels, matrix))
        if results == []: return relevantFeats
        bestSplitFeat = findBestSplit([pairs[1] for pairs in results],
                                      ranks, features,
                                      relevantFeats)
        features.remove(bestSplitFeat)
        relevantFeats.append(bestSplitFeat)
        print "best split:", bestSplitFeat, "\n###################\n"
        return distinguish(splitSet(vowelsets, bestSplitFeat),
                           ranks = ranks,
                           features = features,
                           relevantFeats = relevantFeats)


def FindContrasts(vowels, feat, featset, trace = 0):
        '''Given the vowels, a featureset, and a feature, finds all the
        pairs of vowels that are contrastive for that feature'''
        pairs = []
        visited = []
        for vowel in [vow for vow in vowels if vow not in visited]:
                partner = deepcopy(vowel)
                partner[feat] = FeatureOpposite(vowel[feat])
                for v in [vow for vow in vowels if vow not in visited]:
                        match = reduce(lambda x,y: x and y,
                                       map(lambda feat:
                                           v[feat] == partner[feat],
                                           featset))
                        if trace > 0:
                                print vowel.symbol, "?=", v.symbol, match
                        if match:
                                pairs.append((vowel, v))
                                visited.append(vowel)
                                visited.append(v)
        return pairs

def FindShared(Class):
        '''Finds the common feature in that divides the class'''
        allshared = []
        for group in Class:
                shared = {}
                for feat in GlobalFeats:
                        if reduce(lambda x,y: x and y,
                            map(lambda p: p[feat] == group[0][feat],
                                group)):
                                shared[feat] = group[0][feat]
                allshared.append(shared)
        assert len(allshared) == 2
        feats = []
        for feat in allshared[0]:
                if allshared[1].has_key(feat) and\
                   allshared[1][feat] == FeatureOpposite(allshared[0][feat]):
                        feats.append(feat)
        return feats

def findfuzzy(candidates, target, immutable, fuzziness):
        '''finds candidate closest to target, making sure immutable feature
        is the same, within fuzziness limit'''
        candidates = [c for c in candidates if
                      c[immutable] == target[immutable]]
        for candidate in candidates:
                fuzzyFactor = sum([1 for feat in target._features
                                   if candidate[feat] != target[feat]])
                if fuzzyFactor <= fuzziness:
                        return candidate
                

def FindPairs(Class, feat):
        '''finds the pairs from each group that contrast by feat
           i.e. ATR(u, lax_u)'''
        pairs = []
        fuzziness = 0
        while len(Class[0]) > 1 and fuzziness < 3:
                #print "fuzzy = ", fuzziness
                for phon in Class[0]:
                        partner = deepcopy(phon)
                        partner[feat] = FeatureOpposite(phon[feat])
                        fuzzymatch = findfuzzy(Class[1], partner,
                                               feat, fuzziness)
                        if fuzzymatch:
                                #fix the symbol on partner (which is currently == phon):
                                partner = Class[1][Class[1].index(fuzzymatch)]
                                pairs.append((phon, partner))
                                Class[1].remove(partner)
                                Class[0].remove(phon)
                        else: fuzziness += 1
        #print feat, pairs
        return pairs
        
        

def FindActive(Classes):
        '''Finds active classes and returns a re-ranking of that language's
                features to reflect those classes'''
        pairs = {}  # feature => list of tuples of phonemes
        ranking = globalDefaultRanks
        bestrank = -1
        for Class in Classes:
                feats = FindShared(Class)
                for feat in feats:
                        pairs[feat] = FindPairs(deepcopy(Class), feat)
                        ranking[feat] = bestrank
                        bestrank = bestrank - 1
        return (ranking, pairs)
                
                


if __name__ == "__main__":
        #defining the vowels
        i = Vowel("i", high = Feature.Plus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)
        y = Vowel("y", high = Feature.Plus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Plus, ATR = Feature.Plus)
        
        e = Vowel("e", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)
        slash_o = Vowel('slsh-o', high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Plus, ATR = Feature.Plus)
        
        epsilon = Vowel("epsil", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Minus)
        oe = Vowel("oe", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Plus, ATR = Feature.Minus)

        ash = Vowel("ae", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Plus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)

        u = Vowel("u", high = Feature.Plus, front = Feature.Minus,
                        low = Feature.Minus, back = Feature.Plus,
                        round = Feature.Plus, ATR = Feature.Plus)
        unround_u = Vowel("unrd-u", high = Feature.Plus, front = Feature.Minus,
                          low = Feature.Minus, back = Feature.Plus,
                          round = Feature.Minus, ATR = Feature.Plus)

        o = Vowel("o", high = Feature.Minus, front = Feature.Minus,
                        low = Feature.Minus, back = Feature.Plus,
                        round = Feature.Plus, ATR = Feature.Plus)
        baby_gamma= Vowel("b-gam", high = Feature.Minus, front = Feature.Minus,
                          low = Feature.Minus, back = Feature.Plus,
                          round = Feature.Minus, ATR = Feature.Plus)

        open_o = Vowel('opn-o', high = Feature.Minus, front = Feature.Minus,
                       low = Feature.Minus, back = Feature.Plus,
                       round = Feature.Plus, ATR = Feature.Minus)
        
        wedge = Vowel("wedge", high = Feature.Minus, front = Feature.Minus,
                             low = Feature.Minus, back = Feature.Plus,
                             round = Feature.Minus, ATR = Feature.Minus)


        schwa = Vowel("schwa", high = Feature.Minus, front = Feature.Minus,
                      low = Feature.Minus,back = Feature.Minus,
                      round = Feature.Minus, ATR = Feature.Plus)
        
        lax_i = Vowel("lax-i", high = Feature.Plus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Minus)
        lax_u = Vowel("lax-u", high = Feature.Plus, front = Feature.Minus,
                        low = Feature.Minus, back = Feature.Plus,
                        round = Feature.Plus, ATR = Feature.Minus)

        a = Vowel("a", high = Feature.Minus, front = Feature.Minus,
                  low = Feature.Plus, back = Feature.Plus,
                  round = Feature.Minus, ATR = Feature.Minus)

        central_a = Vowel("ctr-a", high = Feature.Minus, front = Feature.Minus,
                  low = Feature.Plus, back = Feature.Minus,
                  round = Feature.Minus, ATR = Feature.Minus)

        round_a = Vowel("rnd-a", high = Feature.Minus, front = Feature.Minus,
                  low = Feature.Plus, back = Feature.Plus,
                  round = Feature.Plus, ATR = Feature.Minus)

        barred_i = Vowel("bar-i", high =Feature.Plus, front=Feature.Minus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)
        
        
        vowels = [i, u, schwa, a, open_o, lax_u]


        #Classes is a list of sets of vowels that pattern together
        # so if a~e and i~u then Classes = [[[a,u], [i,e]]]
        Classes = [[[u,schwa],[a,lax_u]],[[a],[open_o]]]

        #Find the new ranking for this language
        ranking = FindActive(Classes) #returns (rankings, pairs)

        #pretty print the rankings
        featureranks = [(ranking[0][feat], feat) for feat in ranking[0]]
        featureranks.sort()
        toprint = "Rankings: "
        for r in featureranks: toprint += r[1] + ' > '
        print toprint[:-3], '\n'
        
        #this distinguishes the vowels
        distinctiveFeats = distinguish([vowels], ranks = ranking[0])

        #pretty print the features
        print "       ",
        for f in distinctiveFeats:
                print f, "\t",
        print ""
        for vowel in vowels:
                print "%(sym)6s " % {'sym': vowel.symbol.encode('UTF-8')},
                for f in distinctiveFeats:
                        if vowel[f] == Feature.Plus: print "+",
                        elif vowel[f] == Feature.Minus: print "-",
                        print "\t",
                print ""
        print "\n"

        #print the contrastive pairs for each feature
        print "Contrasts:"
        for feat in distinctiveFeats:
                print feat,":",
                pairs = FindContrasts(deepcopy(vowels), feat, distinctiveFeats)
                print [(x.symbol, y.symbol) for (x,y) in pairs]

