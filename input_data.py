class word(object):
    def __init__(self):
        self.phonology = [] #list of segments with features
        self.morphology = set([]) #set of m-features associated with word

class exponent(object):
        def __init__(self,phonology,side):
            self.phon = phonology #phonology of exponent
            self.side = side #adfix type (suffix/prefix/?infix) 0 = undefined
            

class vocab_item(object):
    def __init__(self,morpheme,phonology,side,context):
        self.morph_feature = morph_feature #m-feature to be spelled out
        self.exponent = exponent(phonology,side) #exponent and adfix status
        self.context = context #when to use this item

def Dictionaryify(input):
    lexicon = {}
    for word in input:
        for morph in word.morphology:
            try:
                lexicon[morph].append(word)
            except:
                lexicon[morph] = [word]

def initialize_vocabulary(lexicon):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    vocab = []
    for morph in lexicon.keys():
        word_list = []
        for form in lexicon[morph]:
            word_list.append(form.phonology)
        
        long_string =""
        for string in l:
            if len(string) > len(long_string):
                long_string = string

        result = ''
        for j in range(len(long_string)):
            for i in range(len(long_string)-1,-1,-1):
                if len(long_string[j:i]) > len(result):
                    if is_common_substr(long_string[j:i],l):
                        result = long_string[j:i]
        
        vocab.append(vocab_item(morph,result,0,[]))