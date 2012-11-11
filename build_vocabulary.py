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

def build_vocabulary(lexicon, settings):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    
    