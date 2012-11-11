class word(object):
    def __init__(self,phon,morph):
        self.phonology = phon #list of segments with features
        self.morphology = set(morph) #set of m-features associated with word

class exponent(object):
        def __init__(self,phonology,side):
            self.phon = phonology #phonology of exponent
            self.side = side #adfix type (suffix/prefix/?infix) 0 = undefined
            

class vocab_item(object):
    def __init__(self,morph_feature,phonology,side,context):
        self.morph_feature = morph_feature #m-feature to be spelled out
        self.exponent = exponent(phonology,side) #exponent and adfix status
        self.context = context #when to use this item
        
class settings(object):
    def __init__(self, complexity, length, phon):
        self.complexity = complexity #reward for null phonology
        self.length = length         #weight of the list length penalty
        self.phon = phon             #weight of the phonology vs. allomorphy 
                                     #penalty, which can be negative


def Dictionaryify(input):
    lexicon = {}
    for word in input:
        for morph in word.morphology:
            try:
                lexicon[morph].append(word)
            except:
                lexicon[morph] = [word]
    return lexicon

def find_common_substring(word_list):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    long_string =""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string

    result = ''
    for j in range(len(long_string)):
        for i in range(len(long_string)-1,-1,-1):
            if len(long_string[j:i]) > len(result):
                if is_common_substr(long_string[j:i],word_list):
                    result = long_string[j:i]
    return result

def build_vocabulary(lexicon, settings):
    vocab = {}
    for morph in lexicon.keys():
        try:
            vocab[morph[0]][morph[1]] = lexicon[morph]
        except:
            vocab[morph[0]] = {morph[1]:lexicon[morph]}
    models = []
    model = {}
    for key in vocab['ROOT']:
        #Model 1 assumes no root suppletion, various other models attempt to
        #force root suppletion by subgrouping
        for morpheme in vocab['ROOT'][key]:
            word_list = []
            for form in vocab['ROOT'][key]:
                word_list.append(form.phonology)
            for morph in morpheme.morphology.difference(set([('ROOT',key)])):
                try:
                    for vi in model['ROOT']:
                        if vi.morph_feature == key:
                            vi.context.append(morph)
                            break
                    else:
                        model['ROOT'].append(vocab_item(key,find_common_substring(word_list),0,[morph]))
                except:
                    model['ROOT'] = [vocab_item(key,find_common_substring(word_list),0,[morph])]
                    
        for morpheme in vocab['ROOT'][key]:
            if morpheme.phonology != find_common_substring(word_list):
                for i in range(len(morpheme.phonology)):
                    if morpheme.phonology[:i] == find_common_substring(word_list):
                        for morph in morpheme.morphology.difference(set([('ROOT',key)])):
                            try:
                                for vi in model[morph[0]]:
                                    print vi.morph_feature
                                    if vi.morph_feature == morph[1]:
                                        if vi.exponent.phon == morpheme.phonology[i:]:
                                            vi.context.append(('ROOT',key))
                                        else:
                                            model[morph[0]].append(vocab_item(morph[1],morpheme.phonology[i:],0,[('ROOT',key)]))
                                        break
                                else:
                                    model[morph[0]].append(vocab_item(morph[1],morpheme.phonology[i:],0,[('ROOT',key)]))
                            except:
                                model[morph[0]] = [vocab_item(morph[1],morpheme.phonology[i:],0,[('ROOT',key)])]
                        break
            else:
                for morph in morpheme.morphology.difference(set([('ROOT',key)])):
                    try:
                        for vi in model[morph[0]]:
                            print vi.morph_feature
                            if vi.morph_feature == morph[1]:
                                if vi.exponent.phon == '':
                                    vi.context.append(('ROOT',key))
                                else:
                                    model[morph[0]].append(vocab_item(morph[1],'',0,[('ROOT',key)]))
                                break
                        else:
                            model[morph[0]].append(vocab_item(morph[1],'',0,[('ROOT',key)]))
                    except:
                            model[morph[0]] = [vocab_item(morph[1],'',0,[('ROOT',key)])]
    chosen_model = model
    return chosen_model