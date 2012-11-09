from Feature import *

def format(x):
    '''change a phoneme into an string or vice versa'''
    if isinstance(x, Phoneme):
        return x.__repr__()
    if isinstance(x, str):
        if x.startswith("<Phoneme"):
            arg = ""
            features = x[10:][:-1].split(", ")
            for feat in features:
                arg += feat[1:] + "="
                if feat[0] == '+':
                    arg += str(Feature.Plus)
                elif feat[0] == '-':
                    arg += str(Feature.Minus)
                elif feat[0] == '?':
                    arg += str(Feature.Needs)
                elif feat[0] == 'm':
                    arg += str(Feature.Marked)
                elif feat[0] == 'u':
                    arg += str(Feature.Unmarked)
                elif feat[0] == '@':
                    arg += str(Feature.Any)
                else:
                    raise ValueError("No such feature value: " + feat[0])
                arg += ", "
            arg = arg[:-2]
            return eval("Phoneme(" + arg + ")")
    return x
            
            

class doubleDict:
    '''An implementation of a two way dictionary for phonemes'''
    def __init__(self, initdict = {}):
        self._dict = initdict.copy()
        self._reverse = {}
        for key in self._dict.keys():
            self._reverse[self._dict[key]] = key
    def __setitem__(self, key, val):
        '''d[key] = val'''
        if isinstance(key, Phoneme): key = format(key)
        if isinstance(val, Phoneme): val = format(val)
        if self.has(key):
            raise ValueError('instance already has key %s' %key)
        elif self.has(val):
            raise ValueError('instance already has value %s' %val)
        else:
            self._dict[key] = val
            self._reverse[val] = key
    def __getitem__(self, key):
        '''d[key]'''
        if isinstance(key, Phoneme): 
            AnyMatches = [m for m in key._features if key[m] == Feature.Any]
            if AnyMatches == []:                        
                key = format(key)
            else:
                key = self.tryconfig(AnyMatches, key)
        if self._dict.has_key(key):
            return format(self._dict[key])
        elif self._reverse.has_key(key):
            return format(self._reverse[key])
        else:
            #print key
            if ['.', '*'].count(key) > 0:
                return key
            raise LookupError('instance has no key/value %s' %key)
    def tryconfig(self, AnyMatch, key):
        '''recursively try values for each feature in AnyMatch'''
        if AnyMatch == []:
            #if we get here then the phoneme isn't in the inventory
            return False
        else: 
            for val in [Feature.Plus, Feature.Minus]:
                key[AnyMatch[0]] = val
                if self.has(key): return format(key) 
                #self.has(key) will call AnyMatch if there are other Any values   
    def __delitem__(self, key):
        '''del d[key]'''
        if isinstance(key, Phoneme): key = format(key)
        if self._dict.has_key(key):
            val = self._dict[key]
            del self._dict[key]
            del self._reverse[val]
        elif self._reverse.has_key(key):
            val = self._reverse[key]
            del self._reverse[key]
            del self._dict[val]
        else:
            raise LookupError('instance has no key/value %s' %key)
    def __repr__(self):
        '''returns string of dict'''
        return self._dict.__repr__()
    def pprint(self):
        '''nicely printed dictionary'''
        string = ""
        for k in self._dict.keys():
            string += k + " = "
            string += format(self._dict[k]).__repr__()
            string += "\n"
        return string
    def has(self, key):
        '''returns whether dict or reverse has key'''
        if isinstance(key, Phoneme): 
            AnyMatches = [m for m in key._features if key[m] == Feature.Any]
            if AnyMatches == []:                      
                key = format(key)
            else:
                key = self.tryconfig(AnyMatches, key)
        if self._dict.has_key(key) or self._reverse.has_key(key):
            return True
        else:
            return False
    def __len__(self):
        '''returns length of dict'''
        return self._dict.__len__()
    def copy(self):
        '''returns doubleDict with same copy'''
        return self.__class__(self._dict)
    def keys(self):
        return self._dict.keys()
    def vals(self):
        return self._reverse.keys()
