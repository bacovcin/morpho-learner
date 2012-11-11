from input_data import *
if __name__ == '__main__':
    lexicon = Dictionaryify([word('sing',[('ROOT','SING'),('TENSE','PRESENT')]),
    word('ring',[('ROOT','RING'),('TENSE','PRESENT')]),
    word('sang',[('ROOT','SING'),('TENSE','PAST')]),
    word('rang',[('ROOT','RING'),('TENSE','PAST')]),
    word('play',[('ROOT','PLAY'),('TENSE','PRESENT')]),
    word('played',[('ROOT','PLAY'),('TENSE','PAST')]),])
    print lexicon