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

