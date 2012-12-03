#####
# Feature.py
# @Kobey Shwayder
# Contains Phoneme class
#####

import re
import Util

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
        
        
def FeatureRepr(dict):
    '''Takes dictionary of feature:value and returns a human readable version'''
    toReturn = ""
    keys = dict.keys()
    keys.sort()
    for f in keys:
        if(dict[f] == Feature.Plus):
            toReturn += "+%s, "%f
        elif(dict[f] == Feature.Minus):
            toReturn += "-%s, "%f
        elif(dict[f] == Feature.Needs):
            toReturn += "?%s, "%f
        elif(dict[f] == Feature.Marked):
            toReturn += "m%s, "%f
        elif(dict[f] == Feature.Unmarked):
            toReturn += "u%s, "%f 
        elif(dict[f] == Feature.Any):
            toReturn += "@%s, "%f  
        elif(dict[f] == Feature.NotSpecified):
            toReturn += "0%s, "%f 
        else: 
           raise ValueError("No such feature or value: " + f)
    return toReturn[:-2]

class Phoneme:
    def __init__(self, quick = None,
                 syll = Feature.NotSpecified,
                 cons = Feature.NotSpecified,
                 son = Feature.NotSpecified,
                 cont = Feature.NotSpecified,
                 del_rel = Feature.NotSpecified,
                 flap = Feature.NotSpecified,
                 trill = Feature.NotSpecified,
                 nas = Feature.NotSpecified,
                 voice = Feature.NotSpecified,
                 spread_gl = Feature.NotSpecified,
                 constr_gl = Feature.NotSpecified,
                 lab = Feature.NotSpecified,
                 round = Feature.NotSpecified,
                 labiodent = Feature.NotSpecified,
                 cor = Feature.NotSpecified,
                 ant = Feature.NotSpecified,
                 dist = Feature.NotSpecified,
                 strid = Feature.NotSpecified,
                 lat = Feature.NotSpecified,
                 dors = Feature.NotSpecified,
                 high = Feature.NotSpecified,
                 low = Feature.NotSpecified,
                 front = Feature.NotSpecified,
                 back = Feature.NotSpecified,
                 tense = Feature.NotSpecified, 
                 lar = Feature.NotSpecified, 
                 TR = Feature.NotSpecified,
                 rhotic = Feature.NotSpecified,
                 tap = Feature.NotSpecified):
        self._features = {}
        self._features['syll'] = syll
        self._features['cons'] = cons
        self._features['son'] = son
        self._features['cont'] = cont
        self._features['del_rel'] = del_rel
        self._features['flap'] = flap
        self._features['trill'] = trill
        self._features['nas'] = nas
        self._features['voice'] = voice
        self._features['spread_gl'] = spread_gl
        self._features['constr_gl'] = constr_gl
        self._features['lab'] = lab
        self._features['round'] = round
        self._features['labiodent'] = labiodent
        self._features['cor'] = cor
        self._features['ant'] = ant
        self._features['dist'] = dist
        self._features['strid'] = strid
        self._features['lat'] = lat
        self._features['dors'] = dors
        self._features['high'] = high
        self._features['low'] = low
        self._features['front'] = front
        self._features['back'] = back
        self._features['tense'] = tense
        self._features['lar'] = lar
        self._features['TR'] = TR
        self._features['rhotic'] = rhotic
        self._features['tap'] = tap
        if quick:
            for key in self._features.keys():
                self._features[key] = Feature.Minus
            self._quickparse(quick)
    def _quickparse(self, quick):
        ''' Parses a string of "+feat, -feat" etc.
        Assume default minus unless marked otherwise.
        Assumes -cor -> 0ant, 0dist, 0strid
        Assimes -dors -> 0high, 0back, 0low, 0front, 0tense '''
        features = quick.split(", ")
        for feat in features:
            arg = feat[1:]
            if feat[0] == '+':
                self._features[arg] = Feature.Plus
            elif feat[0] == '-':
                self._features[arg] = Feature.Minus
            elif feat[0] == '0':
                self._features[arg] = Feature.NotSpecified
            elif feat[0] == '?':
                self._features[arg] = Feature.Needs
            elif feat[0] == 'm':
                self._features[arg] = Feature.Marked
            elif feat[0] == 'u':
                self._features[arg] = Feature.Unmarked
            elif feat[0] == '@':
                self._features[arg] = Feature.Any
            else:
                raise ValueError("No such feature value: " + feat[0])
        if self._features['cor'] == Feature.Minus:
            self._features['ant'] = Feature.NotSpecified
            self._features['dist'] = Feature.NotSpecified
            self._features['strid'] = Feature.NotSpecified
        if self._features['dors'] == Feature.Minus:
            self._features['high'] = Feature.NotSpecified
            self._features['low'] = Feature.NotSpecified
            self._features['front'] = Feature.NotSpecified
            self._features['back'] = Feature.NotSpecified
            self._features['tense'] = Feature.NotSpecified
    def __repr__(self):
        '''string representation'''
        return '<Phoneme: ' + FeatureRepr(self._features) + ">" #remove last comma and space
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
                
    