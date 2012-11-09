# -*- coding: utf-8 -*-
from Util import doubleDict
from Feature import *
from copy import deepcopy

class Language(object):
    def __init__(self, inventory = doubleDict(), morphemes = None, 
                 MarkedPosition = lambda word, P: False, GlobalMarkedness = None,
                 ContextSensitiveMarkedness = None):
        #because default variables are shared, the above needs to be None, 
        #and the following are the actual defaults
        if morphemes == None: morphemes = {"tauType" : ["All"]}
        if GlobalMarkedness == None: GlobalMarkedness = {}
        if ContextSensitiveMarkedness == None: ContextSensitiveMarkedness = {}
        #
        self._inventory = inventory
        self._morphemes = morphemes
        self.MarkedPosition = MarkedPosition;
        self.GlobalMarkedness = GlobalMarkedness;
        self.ContextSensitiveMarkedness = ContextSensitiveMarkedness
    def __getitem__(self, key):
        '''L[key]'''
        return self._inventory[key]
    def __setitem__(self, key, val):
        '''L[key] = val'''
        self._inventory[key] = val
    def hasPhoneme(self, phoneme):
        return self._inventory.has(phoneme)
    def addMorpheme(self, name, morpheme):
        '''adds morpheme to language'''
        self._morphemes[name] = morpheme
    def getMorpheme(self, name):
        '''gets morpheme from morphemes'''
        return self._morphemes[name]
    def Parse(self, string):
        return [self[c] for c in string]
    def defMarkedPosition(self, lambdaFunction):
        '''Defines what a marked position is in this language'''
        if lambdaFunction.func_code.co_argcount != 2:
            raise TypeError("MarkedPosition function must have two arguments")
        self._MarkedPosition = lambdaFunction
    def defGlobalMarkedness(self, dictionary):
        '''Defines global markedness for this language'''
        self.GlobalMarkedness = dictionary
    def addtoGlobalMarkedness(self, feature, value):
        '''Adds value of feature as Globally Marked in this language'''
        self.GlobalMarkedness[feature] = value
    def defContextSensitiveMarkedness(self, dictionary):
        '''defines context sensitive markedness for this language'''
        self.ContextSensitiveMarkedness = dictionary
    def addtoContextSensitiveMarkedness(self, feature, context):
        '''Adds feature in context to Context Sensitive Markedness'''
        self.ContextSensitiveMarkedness[feature] = context

class Morpheme:
    def __init__(self, morpheme,
                 tau = {'tauType': ['All']}, delta = "left", default = None,
                 beta = False, gamma = False, sigma = 0):
        self.form = morpheme
        if not isinstance(tau['tauType'], list): tau['tauType'] = [tau['tauType']]
        self.tau = tau   #tauType can be All, contrastive, positionally_contrastive, or marked  
        self.delta = delta
        self.beta = beta #beta  -- 1, 2 or False (infinite)
        self.gamma = gamma #gamma -- countSegs or countSylls
        self.default = default
        self.sigma = sigma #sonority tolerance
    def __repr__(self):
        string = self.form, self.delta, self.tau
        return str(string)


#TURKISH
TurkishInv = doubleDict()
TurkishInv['i'] = Phoneme(back = Feature.Minus, high = Feature.Plus,
            round = Feature.Minus, voc = Feature.Plus)

TurkishInv['I'] = Phoneme(back = Feature.Plus, high = Feature.Plus,
            round = Feature.Minus, voc = Feature.Plus)

TurkishInv['u'] = Phoneme(back = Feature.Plus, high = Feature.Plus,
            round = Feature.Plus, voc = Feature.Plus)

TurkishInv['U'] = Phoneme(back = Feature.Minus, high = Feature.Plus,
            round = Feature.Plus, voc = Feature.Plus)

TurkishInv['a'] = Phoneme(back = Feature.Plus, high = Feature.Minus,
            round = Feature.Minus, voc = Feature.Plus)

TurkishInv['e'] = Phoneme(back = Feature.Minus, high = Feature.Minus,
            round = Feature.Minus, voc = Feature.Plus)

TurkishInv['o'] = Phoneme(back = Feature.Plus, high = Feature.Minus,
            round = Feature.Plus, voc = Feature.Plus)

TurkishInv['O'] = Phoneme(back = Feature.Minus, high = Feature.Minus,
            round = Feature.Plus, voc = Feature.Plus)
TurkishInv['C'] = Phoneme(voc = Feature.Minus)
TurkishInv['Y'] = Phoneme(voc = Feature.Minus, high = Feature.Plus,
     back = Feature.Minus, round = Feature.Minus)
TurkishInv['N'] = Phoneme(voc = Feature.Minus, nasal = Feature.Plus)
TurkishInv['r']= Phoneme(voc = Feature.Minus, sonorant = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Minus)
TurkishInv['t'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Minus)
TurkishInv['s'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Plus, voiced = Feature.Minus)
TurkishInv['d'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Plus)
TurkishInv['l'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Plus, back=Feature.Plus)
TurkishInv['k'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Minus, back = Feature.Plus)
TurkishInv['g'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Plus, back = Feature.Plus)
TurkishInv['n'] = Phoneme(voc= Feature.Minus, cont = Feature.Plus, voiced = Feature.Plus,
                          nasal = Feature.Plus, lateral = Feature.Minus)
TurkishInv["K"] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Minus, back= Feature.Minus)
TurkishInv["G"] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Plus, back = Feature.Minus)
TurkishInv["L"] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Plus, back=Feature.Minus)
TurkishInv["p"] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, nasal = Feature.Minus,
                          labial = Feature.Plus)



TurkAcc = Morpheme([Phoneme(back = Feature.Needs, high = Feature.Plus,
                         round = Feature.Needs, voc = Feature.Plus)],
                         tau = {"tauType" : "All", "voc" : Feature.Plus}, delta = 'left')

TurkGen = Morpheme([Phoneme(back = Feature.Needs, high = Feature.Plus,
                                   round = Feature.Needs, voc = Feature.Plus),
                           TurkishInv['n']], tau = {"tauType" : "All", "voc" : Feature.Plus}, 
                           delta = 'left')

TurkPl = Morpheme([TurkishInv['l'], Phoneme(back = Feature.Needs, high = Feature.Minus,
                                   round = Feature.Minus, voc = Feature.Plus),
                           TurkishInv['r']],  
                           tau = {"tauType" : "All", "voc" : Feature.Plus}, 
                           delta = 'left')

TurkNominalize = Morpheme([TurkishInv['g'],TurkishInv['e'],TurkishInv['n']])
TurkProg = Morpheme([Phoneme(voc = Feature.Plus, back = Feature.Needs,
                     high = Feature.Plus, round = Feature.Needs),
             TurkishInv['C'], TurkishInv['o'], TurkishInv['r']], 
             tau = {"tauType" : "All", "voc" : Feature.Plus}, delta = 'left')

TurkMorphemes = {}
TurkMorphemes['acc'] = TurkAcc
TurkMorphemes['gen'] = TurkGen
TurkMorphemes['pl'] = TurkPl
TurkMorphemes['nominal'] = TurkNominalize
TurkMorphemes['prog'] = TurkProg

Turkish = Language(inventory = TurkishInv, morphemes = TurkMorphemes)
#END TURKISH

#AKAN
AkanInv = doubleDict()
AkanInv['o'] = Phoneme(back = Feature.Plus, high = Feature.Minus,
            round = Feature.Plus, voc = Feature.Plus, ATR = Feature.Plus)
AkanInv['O'] = Phoneme(back = Feature.Plus, high = Feature.Minus,
            round = Feature.Plus, voc = Feature.Plus, ATR = Feature.Minus)
AkanInv['u'] = u = Phoneme(back = Feature.Plus, high = Feature.Plus,
            round = Feature.Plus, voc = Feature.Plus, ATR = Feature.Plus)
AkanInv['U'] = u = Phoneme(back = Feature.Plus, high = Feature.Plus,
            round = Feature.Plus, voc = Feature.Plus, ATR = Feature.Minus)
AkanInv['e'] = Phoneme(back = Feature.Minus, high = Feature.Minus,
            round = Feature.Minus, voc = Feature.Plus, ATR = Feature.Plus)
AkanInv['E'] = Phoneme(back = Feature.Minus, high = Feature.Minus,
            round = Feature.Minus, voc = Feature.Plus, ATR = Feature.Minus)
AkanInv['C'] = Phoneme(voc = Feature.Minus)

AkanMorphs = {}
AkanMorphs['future'] = Morpheme([Phoneme(back = Feature.Plus, high = Feature.Minus,
            round = Feature.Plus, voc = Feature.Plus, ATR = Feature.Needs)],
                                 delta = 'right')

Akan = Language(AkanInv, AkanMorphs)
#END AKAN

#WOLEAIAN
WolInv = doubleDict()
WolInv['i'] = Phoneme(back = Feature.Minus, high = Feature.Plus,
            round = Feature.Minus, voc = Feature.Plus, low = Feature.Minus)
WolInv['e'] = Phoneme(back = Feature.Minus, high = Feature.Minus,
            round = Feature.Minus, voc = Feature.Plus, low = Feature.Minus)
WolInv['U'] = u = Phoneme(back = Feature.Minus, high = Feature.Plus,
            round = Feature.Plus, voc = Feature.Plus, low = Feature.Minus)
WolInv['O'] = u = Phoneme(back = Feature.Minus, high = Feature.Minus,
            round = Feature.Plus, voc = Feature.Plus, low = Feature.Minus)
WolInv['a'] = Phoneme(back = Feature.Minus, high = Feature.Minus,
            round = Feature.Minus, voc = Feature.Plus, low = Feature.Plus)
WolInv['u'] = Phoneme(back = Feature.Plus, high = Feature.Plus,
            round = Feature.Plus, voc = Feature.Plus, low = Feature.Minus)
WolInv['o'] = Phoneme(back = Feature.Plus, high = Feature.Minus,
            round = Feature.Plus, voc = Feature.Plus, low = Feature.Minus)
WolInv['0'] = Phoneme(back = Feature.Plus, high = Feature.Minus,
            round = Feature.Minus, voc = Feature.Plus, low = Feature.Plus)

WolInv['C'] = Phoneme(voc = Feature.Minus)
WolInv['l'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Plus)
WolInv['m'] = Phoneme(voc= Feature.Minus, cont = Feature.Plus, voiced = Feature.Plus,
                          nasal = Feature.Plus, lateral = Feature.Minus, labial = Feature.Plus)
WolInv['t'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Minus)


WolMorphs = {}
WolMorphs['theme'] = Morpheme([Phoneme(voc = Feature.Plus, high = Feature.Minus,
                                      round = Feature.Minus, back = Feature.Minus,
                                      low = Feature.Needs)],
                              delta = 'L&R',
                              tau = {"tauType" : "All", "voc" : Feature.Plus},
                              default = [Phoneme(voc = Feature.Plus,
                                                 high = Feature.Minus,
                                                 round = Feature.Minus,
                                                 back = Feature.Minus,
                                                 low = Feature.Plus)])

Woleaian = Language(WolInv, WolMorphs)

Woleaian.addMorpheme('1sg', Morpheme(Woleaian.Parse('Ci')))
Woleaian.addMorpheme('2sg', Morpheme(Woleaian.Parse('mu')))
Woleaian.addMorpheme('3sg', Morpheme(Woleaian.Parse('la')))
#END WOLEAIAN

#FINNISH
FinInv = doubleDict()
FinInv['i'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Plus, low = Feature.Minus)
FinInv['e'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Minus, low = Feature.Minus)
FinInv['A'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Minus, low = Feature.Plus)
FinInv['U'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Plus,
                      high = Feature.Plus, low = Feature.Minus)
FinInv['O'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Plus,
                      high = Feature.Minus, low = Feature.Minus)
FinInv['u'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Plus,
                      high = Feature.Plus, low = Feature.Minus)
FinInv['o'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Plus,
                      high = Feature.Minus, low = Feature.Minus)
FinInv['a'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Minus,
                      high = Feature.Minus, low = Feature.Plus)
FinInv['C'] = Phoneme(voc = Feature.Minus)
FinInv['n'] = Phoneme(voc = Feature.Minus, nasal = Feature.Plus,
                      coronal = Feature.Plus)
                    
Finnish = Language(FinInv)

Finnish.addMorpheme('essive',
                    Morpheme([Phoneme(voc = Feature.Minus, nasal = Feature.Plus,
                                      coronal = Feature.Plus),
                              Phoneme(voc = Feature.Plus, high = Feature.Minus,
                                      low = Feature.Plus, round = Feature.Minus,
                                      back = Feature.Needs)],
                              delta = 'left', default = Finnish.Parse('nA')))
                                                       
                                      

#END FINNISH

#FinnishB
FinnishB = Language(FinInv)
FinnishB.addtoGlobalMarkedness("back", Feature.Plus)
#FinnishB.addtoGlobalMarkedness("back", Feature.Plus)
FinnishB.addMorpheme('partit.sg', Morpheme([Phoneme(voc = Feature.Plus,
                      back = Feature.Needs, round = Feature.Minus,
                      high = Feature.Minus, low = Feature.Plus)],
                      tau = {'tauType' : ['marked'], 'voc' : Feature.Plus},
                      sigma = 7))

#END FINNISH-B

#CLASSICAL MONGOLIAN
CMInv = doubleDict()
CMInv['i'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Plus)
CMInv['e'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Minus)
CMInv['U'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Plus,
                      high = Feature.Plus)
CMInv['O'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Plus,
                      high = Feature.Minus)
CMInv['u'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Plus,
                      high = Feature.Plus)
CMInv['o'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Plus,
                      high = Feature.Minus)
CMInv['a'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Minus,
                      high = Feature.Minus)
CMInv['C'] = Phoneme(voc = Feature.Minus)

ClassicalMongolian = Language(CMInv)

ClassicalMongolian.addMorpheme('abl',
                               Morpheme([Phoneme(voc = Feature.Plus,
                                                 high = Feature.Minus,
                                                 round = Feature.Minus,
                                                 back = Feature.Needs),
                                         Phoneme(voc = Feature.Minus),
                                         Phoneme(voc = Feature.Plus,
                                                 high = Feature.Minus,
                                                 round = Feature.Minus,
                                                 back = Feature.Needs)],
                                        delta = 'left'))

#END CLASSICAL MONGOLIAN

#UYGHUR
UygInv = doubleDict()
UygInv['i'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Plus, low = Feature.Minus)
UygInv['e'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Minus, low = Feature.Minus)
UygInv['A'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus,
                      high = Feature.Minus, low = Feature.Plus)
UygInv['U'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Plus,
                      high = Feature.Plus, low = Feature.Minus)
UygInv['O'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Minus, round = Feature.Plus,
                      high = Feature.Minus, low = Feature.Minus)
UygInv['u'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Plus,
                      high = Feature.Plus, low = Feature.Minus)
UygInv['o'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Plus,
                      high = Feature.Minus, low = Feature.Minus)
UygInv['a'] = Phoneme(voc = Feature.Plus,
                      back = Feature.Plus, round = Feature.Minus,
                      high = Feature.Minus, low = Feature.Plus)
UygInv['C'] = Phoneme(voc = Feature.Minus)
UygInv['n'] = Phoneme(voc = Feature.Minus, nasal = Feature.Plus,
                      coronal = Feature.Plus)
UygInv['y'] = Phoneme(voc = Feature.Minus, high = Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus)
UygInv['l'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Plus)
UygInv['r'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Minus)
UygInv['t'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Minus)
                    
Uyghur = Language(UygInv)

Uyghur.addMorpheme('pl', Morpheme([UygInv['l'],
                            Phoneme(voc = Feature.Plus, high = Feature.Minus,
                             low = Feature.Plus, round = Feature.Minus,
                              back = Feature.Needs), UygInv['r']],
                              tau = {"tauType" : "contrastive", "voc" : Feature.Plus},
                                  delta = 'left',
                                  default = Uyghur.Parse('lar')))

#END UYGHUR

#KARAIM
KaraimInv = doubleDict()
# i U I u
# e O a o
#markedposition is first syllable
#unmarkedposition is non-initial syllable
KaraimInv['i'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         high = Feature.Plus, unmarkedposition = Feature.Plus,
                         markedposition = Feature.Plus)
KaraimInv['U'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         high = Feature.Plus, unmarkedposition = Feature.Plus,
                         markedposition = Feature.Plus)
KaraimInv['u'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         high = Feature.Plus, unmarkedposition = Feature.Plus,
                         markedposition = Feature.Plus)
KaraimInv['I'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         high = Feature.Plus, unmarkedposition = Feature.Minus,
                         markedposition = Feature.Plus)
KaraimInv['a'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         high = Feature.Minus, unmarkedposition = Feature.Plus,
                         markedposition = Feature.Plus)
KaraimInv['e'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         high = Feature.Minus, unmarkedposition = Feature.Minus,
                         markedposition = Feature.Plus)
KaraimInv['o'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         high = Feature.Minus, unmarkedposition = Feature.Plus,
                         markedposition = Feature.Plus)
KaraimInv['O'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         high = Feature.Minus, unmarkedposition = Feature.Minus,
                         markedposition = Feature.Plus)

KaraimInv['F'] = Phoneme(voc = Feature.Minus, back = Feature.Minus)
KaraimInv['B'] = Phoneme(voc = Feature.Minus, back = Feature.Plus)
KaraimInv['j'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, high = Feature.Plus,
     back = Feature.Minus, round = Feature.Minus)

Karaim = Language(KaraimInv)

Karaim.defMarkedPosition(lambda word, P: word[:P].count('.') == 0)

Karaim.addMorpheme('gen',
                   Morpheme([Phoneme(voc = Feature.Minus, back = Feature.Needs),
                             Phoneme(voc = Feature.Plus, back = Feature.Needs,
                                     high = Feature.Plus, round = Feature.Minus,
                                     unmarkedposition = Feature.Any, 
                                     markedposition = Feature.Plus),
                             Phoneme(voc = Feature.Minus, back = Feature.Needs)],
                             delta = 'left'
                             )
                   )

Karaim.addMorpheme('abl',
                  Morpheme([Phoneme(voc = Feature.Minus, back = Feature.Needs),
                             KaraimInv['a'],
                             Phoneme(voc = Feature.Minus, back = Feature.Needs)],
                             delta = 'left', tau = {'tauType': 'positionally_contrastive'},
                             ))

Karaim.addMorpheme('pl',
                  Morpheme([Phoneme(voc = Feature.Minus, back = Feature.Needs),
                             KaraimInv['a'],
                             Phoneme(voc = Feature.Minus, back = Feature.Needs)],
                             delta = 'left', tau = {'tauType': 'positionally_contrastive'}))

#END KARAIM

#SIBE
#U i I u
#O e a o
SibeInv = doubleDict()
SibeInv['U'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         low = Feature.Minus)
SibeInv['i'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Minus)
SibeInv['I'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Minus)
SibeInv['u'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Minus)
SibeInv['O'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         low = Feature.Plus)
SibeInv['e'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Plus)
SibeInv['a'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Plus)
SibeInv['o'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Plus)

SibeInv['C'] = Phoneme(voc = Feature.Minus)
SibeInv['d'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                       cont = Feature.Minus, voiced = Feature.Plus)
SibeInv['l'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Plus)
SibeInv['r'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Minus)
SibeInv['f'] = Phoneme(voc = Feature.Minus, labial = Feature.Plus, 
                          cont = Feature.Plus, voiced = Feature.Minus)
SibeInv['n'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, nasal = Feature.Plus)
SibeInv['s'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Plus, voiced = Feature.Minus)
SibeInv['k'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Minus, voiced = Feature.Minus)
SibeInv['g'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Minus, voiced = Feature.Plus)
SibeInv['x'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Minus, voiced = Feature.Minus)
SibeInv['y'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Minus, voiced = Feature.Plus)
SibeInv['q'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Plus, voiced = Feature.Minus)
SibeInv['G'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Plus, voiced = Feature.Plus)
SibeInv['X'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Plus, voiced = Feature.Minus)
SibeInv['R'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Plus, voiced = Feature.Plus)


Sibe = Language(SibeInv)

Sibe.defGlobalMarkedness({'low': Feature.Plus})

Sibe.addMorpheme("dimin", Morpheme([Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                                            low = Feature.Needs, 
                                            voiced = Feature.Minus),
                                    Phoneme(voc=Feature.Plus, round = Feature.Needs, 
                                            back = Feature.Plus, low = Feature.Minus),
                                    SibeInv['n']],
                                    tau = {'tauType': 'marked', "voc": Feature.Plus}, 
                                    delta = "left",  
                                    default = None))

Sibe.addMorpheme("reciprocal", Morpheme(Sibe.Parse('ndu')))
Sibe.addMorpheme("past", Morpheme([Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                                            low = Feature.Needs, 
                                            voiced = Feature.Minus),
                                    Sibe['u']],
                                    tau = {"tauType" : 'marked'}, 
                                    delta = "left",  
                                    default = None))

#END SIBE

#SANJIAZI MANCHU
SanManInv = doubleDict()
SanManInv['U'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         low = Feature.Minus)
SanManInv['i'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Minus)
SanManInv['I'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Minus)
SanManInv['u'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Minus)
SanManInv['E'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Plus)
SanManInv['a'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Plus)
SanManInv['o'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Plus)

SanManInv['C'] = Phoneme(voc = Feature.Minus)
SanManInv['d'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                       cont = Feature.Minus, voiced = Feature.Plus)
SanManInv['n'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, nasal = Feature.Plus)
SanManInv['k'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Minus, voiced = Feature.Minus)
SanManInv['g'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Minus, voiced = Feature.Plus)
SanManInv['x'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Minus, voiced = Feature.Minus)
SanManInv['y'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Minus, voiced = Feature.Plus)
SanManInv['q'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Plus, voiced = Feature.Minus)
SanManInv['G'] = Phoneme(voc = Feature.Minus, cont = Feature.Minus, 
                       low = Feature.Plus, voiced = Feature.Plus)
SanManInv['X'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Plus, voiced = Feature.Minus)
SanManInv['R'] = Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                       low = Feature.Plus, voiced = Feature.Plus)


SanjiaziManchu = Language(SanManInv)

SanjiaziManchu.addMorpheme("past", Morpheme([Phoneme(voc = Feature.Minus, cont = Feature.Plus, 
                                        low = Feature.Needs, voiced = Feature.Minus),
                                        Phoneme(voc = Feature.Plus, back = Feature.Plus,
                                        low = Feature.Needs, round = Feature.Needs)],
                                            ))


#END SANJIAZI MANCHU

#SHOR
ShorInv = doubleDict()
ShorInv['U'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         low = Feature.Minus)
ShorInv['i'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Minus)
ShorInv['I'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Minus)
ShorInv['u'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Minus)
ShorInv['O'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         low = Feature.Plus)
ShorInv['e'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Plus)
ShorInv['a'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Plus)
ShorInv['o'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Plus)

ShorInv['C'] = Phoneme(voc = Feature.Minus)
ShorInv['Y'] = Phoneme(voc = Feature.Minus, high = Feature.Plus,
     back = Feature.Minus, round = Feature.Minus)
ShorInv['N'] = Phoneme(voc = Feature.Minus, nasal = Feature.Plus)
ShorInv['r'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                        sonorant = Feature.Plus, nasal = Feature.Minus,
                        lateral = Feature.Minus)
ShorInv['t'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Minus)
ShorInv['s'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Plus, voiced = Feature.Minus)
ShorInv['d'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Plus)
ShorInv['l'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Plus)
ShorInv['k'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Minus)
ShorInv['g'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Plus)
ShorInv['n'] = Phoneme(voc = Feature.Minus, nasal = Feature.Plus,
                      coronal = Feature.Plus)

Shor = Language(ShorInv)

Shor.addtoContextSensitiveMarkedness(("round", Feature.Plus), [("back", Feature.Minus),
                                                               ("low", Feature.Plus)])
 
Shor.addMorpheme("abl", Morpheme([Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                           cont = Feature.Minus, voiced = Feature.Minus),
                                   Phoneme(voc = Feature.Plus, back = Feature.Plus,
                                           low = Feature.Plus, round = Feature.Needs),
                                   Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                           nasal = Feature.Plus)],
                                    tau = {'tauType' : 'marked'}
                                  ))

Shor.addMorpheme("loc", Morpheme([Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                           cont = Feature.Minus, voiced = Feature.Minus),
                                   Phoneme(voc = Feature.Plus, back = Feature.Minus,
                                           low = Feature.Plus, round = Feature.Needs)],
                                    tau = {'tauType' : 'marked'}
                                  ))

Shor.addMorpheme("aor", Morpheme([Phoneme(voc = Feature.Plus, low = Feature.Plus,
                                          back = Feature.Plus, round = Feature.Needs),
                                  Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                          sonorant = Feature.Plus, nasal = Feature.Minus,
                                          lateral = Feature.Minus)],
                                     tau = {'tauType' : 'marked'}
                                  ))      
#END SHOR

#KIRGHIZ
KirghizInv = doubleDict()
KirghizInv['U'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         low = Feature.Minus)
KirghizInv['i'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Minus)
KirghizInv['I'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Minus)
KirghizInv['u'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Minus)
KirghizInv['O'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Minus, 
                         low = Feature.Plus)
KirghizInv['e'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Minus, 
                         low = Feature.Plus)
KirghizInv['a'] = Phoneme(voc=Feature.Plus, round = Feature.Minus, back = Feature.Plus, 
                         low = Feature.Plus)
KirghizInv['o'] = Phoneme(voc=Feature.Plus, round = Feature.Plus, back = Feature.Plus, 
                         low = Feature.Plus)

KirghizInv['C'] = Phoneme(voc = Feature.Minus)
KirghizInv['y'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, 
                          cont = Feature.Plus, coronal = Feature.Plus, voiced = Feature.Plus)
KirghizInv['r'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                        sonorant = Feature.Plus, nasal = Feature.Minus,
                        lateral = Feature.Minus)
KirghizInv['t'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Minus)
KirghizInv['s'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Plus, voiced = Feature.Minus)
KirghizInv['z'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Plus, voiced = Feature.Plus)
KirghizInv['d'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Plus)
KirghizInv['l'] = Phoneme(voc = Feature.Minus, sonorant = Feature.Plus, voiced = Feature.Plus,
            nasal = Feature.Minus, lateral = Feature.Plus)
KirghizInv['k'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Minus)
KirghizInv['g'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, cont = Feature.Minus,
            voiced = Feature.Plus)
KirghizInv['n'] = Phoneme(voc = Feature.Minus, nasal = Feature.Plus,
                      coronal = Feature.Plus)
KirghizInv['m'] = Phoneme(voc = Feature.Minus, nasal = Feature.Plus,
                      labial = Feature.Plus)

KirghizA = Language(KirghizInv)

KirghizB = Language(KirghizInv)

KirghizB.addtoContextSensitiveMarkedness(("round", Feature.Plus), [("back", Feature.Minus),
                                                               ("low", Feature.Plus)])
 
KirghizA.addMorpheme("abl", Morpheme([Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                           cont = Feature.Minus, voiced = Feature.Needs),
                                   Phoneme(voc = Feature.Plus, back = Feature.Needs,
                                           low = Feature.Plus, round = Feature.Needs),
                                   Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                           nasal = Feature.Plus)],
                                    tau = {'tauType' : 'contrastive'}
                                  ))

KirghizB.addMorpheme("abl", Morpheme([Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                           cont = Feature.Minus, voiced = Feature.Needs),
                                   Phoneme(voc = Feature.Plus, back = Feature.Needs,
                                           low = Feature.Plus, round = Feature.Needs),
                                   Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                                           nasal = Feature.Plus)],
                                    tau = {'tauType' : 'marked'}
                                  ))

#END KIRGHIZ

#NAWURI
NawuriInv = doubleDict()

NawuriInv['i'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, low = Feature.Minus,
                         ATR = Feature.Plus, back = Feature.Minus, round = Feature.Minus)
NawuriInv['u'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, low = Feature.Minus,
                         ATR = Feature.Plus, back = Feature.Plus, round = Feature.Plus)
NawuriInv['I'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, low = Feature.Minus,
                         ATR = Feature.Minus, back = Feature.Minus, round = Feature.Minus)
NawuriInv['U'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, low = Feature.Minus,
                         ATR = Feature.Minus, back = Feature.Plus, round = Feature.Plus)
NawuriInv['e'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low = Feature.Minus,
                         ATR = Feature.Plus, back = Feature.Minus, round = Feature.Minus)
NawuriInv['o'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low = Feature.Minus,
                         ATR = Feature.Plus, back = Feature.Plus, round = Feature.Plus)
NawuriInv['E'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low = Feature.Minus,
                         ATR = Feature.Minus, back = Feature.Minus, round = Feature.Minus)
NawuriInv['O'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low = Feature.Minus,
                         ATR = Feature.Minus, back = Feature.Plus, round = Feature.Plus)
NawuriInv['a'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low = Feature.Plus,
                         ATR = Feature.Minus, back = Feature.Plus, round = Feature.Minus)

NawuriInv['C'] = Phoneme(voc = Feature.Minus, consonantal = Feature.Plus)
NawuriInv['g'] = Phoneme(voc = Feature.Minus, voiced = Feature.Plus, 
                         consonantal = Feature.Plus, velar = Feature.Plus)
NawuriInv['p'] = Phoneme(voc = Feature.Minus, round = Feature.Plus, 
                         voiced = Feature.Minus, labial = Feature.Plus, 
                         consonantal = Feature.Plus)
NawuriInv['b'] = Phoneme(voc = Feature.Minus, round = Feature.Plus, 
                         voiced = Feature.Plus, labial = Feature.Plus, 
                         consonantal = Feature.Plus)
NawuriInv['w'] = Phoneme(voc = Feature.Minus, round = Feature.Plus, 
                         voiced = Feature.Plus, labial = Feature.Plus, 
                         consonantal = Feature.Minus)

Nawuri = Language(NawuriInv)

Nawuri.addMorpheme("noun-class", Morpheme([NawuriInv['g'], 
                                           Phoneme(voc = Feature.Plus, high = Feature.Plus, 
                                                   low = Feature.Minus, ATR = Feature.Needs, 
                                                   back = Feature.Any, round = Feature.Needs)
                                           ], delta = 'r',
                                           tau = {'tauType' : 'All', 
                                                  'R' : {'consonantal' : Feature.Plus} },
                                            default = [NawuriInv['g'], NawuriInv['i']] ))



#END NAWURI

#KIMATUUMBI
KimatInv = doubleDict()

KimatInv['i'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Minus,
                        high = Feature.Plus, ATR = Feature.Plus, low = Feature.Minus)
KimatInv['I'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Minus,
                        high = Feature.Plus, ATR = Feature.Minus, low = Feature.Minus)
KimatInv['E'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Minus,
                        high = Feature.Minus, ATR = Feature.Minus, low = Feature.Minus)
KimatInv['u'] = Phoneme(voc = Feature.Plus, round = Feature.Plus, back = Feature.Plus,
                        high = Feature.Plus, ATR = Feature.Plus, low = Feature.Minus)
KimatInv['U'] = Phoneme(voc = Feature.Plus, round = Feature.Plus, back = Feature.Plus,
                        high = Feature.Plus, ATR = Feature.Minus, low = Feature.Minus)
KimatInv['O'] = Phoneme(voc = Feature.Plus, round = Feature.Plus, back = Feature.Plus,
                        high = Feature.Minus, ATR = Feature.Minus, low = Feature.Minus)
KimatInv['a'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Plus,
                        high = Feature.Minus, ATR = Feature.Minus, low = Feature.Plus)

KimatInv['C'] = Phoneme(voc = Feature.Minus)
KimatInv['l'] = Phoneme(voc = Feature.Minus, lateral = Feature.Plus)

Kimatuumbi = Language(KimatInv)

Kimatuumbi.addMorpheme('applicative', 
                       Morpheme([Phoneme(voc = Feature.Plus, round = Feature.Plus, 
                                         back = Feature.Plus, high = Feature.Needs,
                                         ATR = Feature.Needs, low = Feature.Minus),
                                         Kimatuumbi['l']],
                                delta = 'l', 
                                tau = {'tauType' : 'All', 
                                       'round' : Feature.Minus, 'high' : Feature.Minus},
                                default = [Kimatuumbi['u'],Kimatuumbi['l']])
                       )


#END KIMATUUMBI

#OROCH
OrochInv = doubleDict()

OrochInv['i'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Minus,
                        high = Feature.Plus, ATR = Feature.Plus)
OrochInv['u'] = Phoneme(voc = Feature.Plus, round = Feature.Plus, back = Feature.Plus,
                        high = Feature.Plus, ATR = Feature.Plus)
OrochInv['U'] = Phoneme(voc = Feature.Plus, round = Feature.Plus, back = Feature.Plus,
                        high = Feature.Plus, ATR = Feature.Minus)
OrochInv['A'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Minus,
                        high = Feature.Minus, ATR = Feature.Plus)
OrochInv['e'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Plus,
                        high = Feature.Minus, ATR = Feature.Plus)
OrochInv['a'] = Phoneme(voc = Feature.Plus, round = Feature.Minus, back = Feature.Plus,
                        high = Feature.Minus, ATR = Feature.Minus)
OrochInv['O'] = Phoneme(voc = Feature.Plus, round = Feature.Plus, back = Feature.Plus,
                        high = Feature.Minus, ATR = Feature.Minus)

OrochInv['C'] = Phoneme(voc = Feature.Minus)
OrochInv['d'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Minus, voiced = Feature.Plus)
OrochInv['s'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, 
                          cont = Feature.Plus, voiced = Feature.Minus)
OrochInv['r'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus,
                        sonorant = Feature.Plus, nasal = Feature.Minus,
                        lateral = Feature.Minus)

Oroch = Language(OrochInv)

Oroch.addMorpheme('foc', 
                    Morpheme([Oroch['d'], Phoneme(voc = Feature.Plus, round = Feature.Minus, 
                                                  back = Feature.Plus, high = Feature.Minus, 
                                                  ATR = Feature.Needs)
                              ], tau = {'tauType' : ['contrastive', 'marked'], 
                                        'voc': Feature.Plus }
                             )
                    )

Oroch.addtoGlobalMarkedness('ATR', Feature.Minus)




#END OROCH

#KIKONGO / LAMBA
KLInv = doubleDict()

KLInv['i'] = Phoneme(voc = Feature.Plus, consonantal = Feature.Minus,
                     high = Feature.Plus, low = Feature.Minus,
                     back = Feature.Minus, round = Feature.Minus)
KLInv['u'] = Phoneme(voc = Feature.Plus, consonantal = Feature.Minus,
                     high = Feature.Plus, low = Feature.Minus,
                     back = Feature.Plus, round = Feature.Plus)
KLInv['e'] = Phoneme(voc = Feature.Plus, consonantal = Feature.Minus,
                     high = Feature.Minus, low = Feature.Minus,
                     back = Feature.Minus, round = Feature.Minus)
KLInv['a'] = Phoneme(voc = Feature.Plus, consonantal = Feature.Minus,
                     high = Feature.Minus, low = Feature.Plus,
                     back = Feature.Plus, round = Feature.Minus)


KLInv['m'] = Phoneme(labial = Feature.Plus, consonantal = Feature.Plus,
                     sonorant = Feature.Plus, nasal = Feature.Plus)
KLInv['s'] = Phoneme(coronal = Feature.Plus, consonantal = Feature.Plus,
                     cont = Feature.Plus, voiced = Feature.Minus)
KLInv['l'] = Phoneme(consonantal = Feature.Plus, coronal = Feature.Plus,
                     sonorant = Feature.Plus, nasal = Feature.Minus)
KLInv['n'] = Phoneme(consonantal = Feature.Plus, coronal = Feature.Plus,
                     sonorant = Feature.Plus, nasal = Feature.Plus)
KLInv['k'] = Phoneme(velar = Feature.Plus, consonantal = Feature.Plus,
                     voiced = Feature.Minus)
KLInv['d'] = Phoneme(coronal = Feature.Plus, consonantal = Feature.Plus,
                     cont = Feature.Minus, voiced = Feature.Plus)
KLInv['t'] = Phoneme(coronal = Feature.Plus, consonantal = Feature.Plus,
                     cont = Feature.Minus, voiced = Feature.Minus)

Kikongo = Language(KLInv)
Lamba = Language(KLInv)

Kikongo.addMorpheme('applicative',
                    Morpheme([Phoneme(consonantal = Feature.Plus, coronal = Feature.Plus,
                     sonorant = Feature.Plus, nasal = Feature.Needs), Kikongo['a']],
                    tau = {'tauType' : 'marked'}, 
                    default = Kikongo.Parse('la')          
                             )
                    )

Lamba.addMorpheme('perf',
                    Morpheme([Phoneme(consonantal = Feature.Plus, coronal = Feature.Plus,
                     sonorant = Feature.Plus, nasal = Feature.Needs), Lamba['e']],
                    tau = {'tauType' : 'marked'}, 
                    beta = 1, gamma = 'countSylls',
                    default = Lamba.Parse('le')          
                             )
                    )
#END KIKONGO & LAMBA

#YUCATEC MAYA
YucInv = doubleDict()

YucInv['i'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, low= Feature.Minus,
                      back = Feature.Minus, round = Feature.Minus)
YucInv['u'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, low= Feature.Minus,
                      back = Feature.Plus, round = Feature.Plus)
YucInv['e'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low= Feature.Minus,
                      back = Feature.Minus, round = Feature.Minus)
YucInv['o'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low= Feature.Minus,
                      back = Feature.Plus, round = Feature.Plus)
YucInv['a'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, low= Feature.Plus,
                      back = Feature.Plus, round = Feature.Minus)    

YucInv['C']  = Phoneme(voc = Feature.Minus)
YucInv['l'] = Phoneme(voc = Feature.Minus, lateral = Feature.Plus)
YucInv['k'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus)

YucatecMaya = Language(YucInv)

YucatecMaya.addMorpheme('impf',
                        Morpheme([Phoneme(voc = Feature.Plus, high = Feature.Needs, 
                                          low= Feature.Needs, back = Feature.Needs, 
                                          round = Feature.Needs), YucatecMaya['l']],
                                beta = 2, gamma = 'countSegs',
                                default = YucatecMaya.Parse('al')
                                )
                        )   

YucatecMaya.addMorpheme('sbjct',
                        Morpheme([Phoneme(voc = Feature.Plus, high = Feature.Needs, 
                                          low= Feature.Needs, back = Feature.Needs, 
                                          round = Feature.Needs), YucatecMaya['k']],
                                beta = 2, gamma = 'countSegs',
                                default = YucatecMaya.Parse('ak')
                                )
                        )                 
#END YUCATEC MAYA

#CLASSICAL MANCHU
ClasMan = doubleDict()

ClasMan['i'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, ATR= Feature.Plus,
                      back = Feature.Minus, round = Feature.Minus)
ClasMan['u'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, ATR= Feature.Plus,
                      back = Feature.Plus, round = Feature.Plus)
ClasMan['U'] = Phoneme(voc = Feature.Plus, high = Feature.Plus, ATR= Feature.Minus,
                      back = Feature.Plus, round = Feature.Plus)
ClasMan['E'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, ATR= Feature.Plus,
                      back = Feature.Plus, round = Feature.Minus)
ClasMan['a'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, ATR= Feature.Minus,
                      back = Feature.Plus, round = Feature.Minus)    
ClasMan['O'] = Phoneme(voc = Feature.Plus, high = Feature.Minus, ATR= Feature.Minus,
                      back = Feature.Plus, round = Feature.Plus)  

ClasMan['C']  = Phoneme(voc = Feature.Minus)

ClassicalManchu = Language(ClasMan)
ClassicalManchu.addtoGlobalMarkedness('ATR', Feature.Minus)
ClassicalManchu.addMorpheme('adj',
                        Morpheme([ClassicalManchu['C'], ClassicalManchu['C'], 
                                  ClassicalManchu['C'], 
                                  Phoneme(voc = Feature.Plus, high = Feature.Minus, 
                                          ATR= Feature.Needs,
                                          back = Feature.Plus, round = Feature.Minus)],
                                sigma = 6, default = ClassicalManchu.Parse('CCCa'),
                                tau = {'tauType': ['marked'], 'voc' : Feature.Plus}
                                )
                        )   
#END CLASSICAL MANCHU

#HUNGARIAN
HungInv = doubleDict()

HungInv['U'] = Phoneme(voc = Feature.Plus, back = Feature.Minus, round = Feature.Plus,
                       ATR = Feature.Plus, high = Feature.Plus, low = Feature.Minus)
HungInv['O'] = Phoneme(voc = Feature.Plus, back = Feature.Minus, round = Feature.Plus,
                       ATR = Feature.Plus, high = Feature.Minus, low = Feature.Minus)
HungInv['i'] = Phoneme(voc = Feature.Plus, back = Feature.Minus, round = Feature.Minus,
                       ATR = Feature.Plus, high = Feature.Plus, low = Feature.Minus)
HungInv['e'] = Phoneme(voc = Feature.Plus, back = Feature.Minus, round = Feature.Minus,
                       ATR = Feature.Plus, high = Feature.Minus, low = Feature.Minus)
HungInv['E'] = Phoneme(voc = Feature.Plus, back = Feature.Minus, round = Feature.Minus,
                       ATR = Feature.Minus, high = Feature.Minus, low = Feature.Minus)
HungInv['u'] = Phoneme(voc = Feature.Plus, back = Feature.Plus, round = Feature.Plus,
                       ATR = Feature.Plus, high = Feature.Plus, low = Feature.Minus)
HungInv['o'] = Phoneme(voc = Feature.Plus, back = Feature.Plus, round = Feature.Plus,
                       ATR = Feature.Plus, high = Feature.Minus, low = Feature.Minus)
HungInv['a'] = Phoneme(voc = Feature.Plus, back = Feature.Plus, round = Feature.Minus,
                       ATR = Feature.Minus, high = Feature.Minus, low = Feature.Plus)
HungInv['A'] = Phoneme(voc = Feature.Plus, back = Feature.Plus, round = Feature.Plus,
                       ATR = Feature.Minus, high = Feature.Minus, low = Feature.Plus)

HungInv['C'] = Phoneme(voc = Feature.Minus)
HungInv['n'] = Phoneme(voc = Feature.Minus, coronal = Feature.Plus, nasal = Feature.Plus)
HungInv['k'] = Phoneme(voc = Feature.Minus, velar = Feature.Plus, voiced = Feature.Minus)

Hungarian = Language(HungInv)

Hungarian.addMorpheme("dat", Morpheme([Hungarian['n'], 
                                       Phoneme(voc = Feature.Plus, ATR = Feature.Minus,
                                               back = Feature.Needs, round = Feature.Any,
                                               high = Feature.Minus, low = Feature.Any),
                                       Hungarian['k']],
                                       tau = {'tauType' : ['contrastive']},
                                       default = Hungarian.Parse('nEk')
                                      ))

HungarianMD = deepcopy(Hungarian)
HungarianMD._morphemes['dat'].tau['tauType'] = ['marked']
HungarianMD.addtoGlobalMarkedness('back', Feature.Plus)

HungarianML = deepcopy(HungarianMD)
HungarianML._morphemes['dat'].beta = 2
HungarianML._morphemes['dat'].gamma = 'countSylls'


HungarianRS = deepcopy(Hungarian)
HungarianRS.addtoGlobalMarkedness('back', Feature.Plus)
HungarianRS._morphemes['dat'].tau['tauType'] = ['marked']
HungarianRS._morphemes['dat'].sigma = 5

HungarianTS = deepcopy(HungarianRS)
HungarianTS._morphemes['dat'].sigma = 6
#END HUNGARIAN

#JINGULU
JingInv = doubleDict()

JingInv['i'] = Phoneme(voc = Feature.Plus, round = Feature.Minus,
                       back = Feature.Minus, high = Feature.Plus)
JingInv['u'] = Phoneme(voc = Feature.Plus, round = Feature.Plus,
                       back = Feature.Plus, high = Feature.Plus)
JingInv['a'] = Phoneme(voc = Feature.Plus, round = Feature.Minus,
                       back = Feature.Plus, high = Feature.Minus)
JingInv['C'] = Phoneme(voc=Feature.Minus)

Jingulu = Language(JingInv)

Jingulu.addtoGlobalMarkedness("high", Feature.Plus)

Jingulu.addMorpheme("sibling", Morpheme([Jingulu['C'],
                                        Phoneme(voc = Feature.Plus, 
                                                               round = Feature.Minus,
                                                               back = Feature.Any, 
                                                               high = Feature.Needs),
                                        Jingulu['C'],
                                        Jingulu['C'],
                                        Phoneme(voc = Feature.Plus, 
                                                               round = Feature.Minus,
                                                               back = Feature.Any, 
                                                               high = Feature.Needs),
                                        Jingulu['C'],
                                        Jingulu['C'],
                                        Phoneme(voc = Feature.Plus, 
                                                               round = Feature.Minus,
                                                               back = Feature.Any, 
                                                               high = Feature.Needs)],
                                        delta = 'right',
                                        tau = {'tauType' : ['marked']},
                                        default = Jingulu.Parse('CaCCaCCa')
                                        )
                    )

#END JINGULU 
