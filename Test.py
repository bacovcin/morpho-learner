from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([word('sin',[('ROOT','SING'),('TENSE','PRESENT')]),
    word('saN',[('ROOT','SING'),('TENSE','PAST')]),
    word('siNiN',[('ROOT','SING'),('TENSE','PARTICIPLE')]),
    word('riN',[('ROOT','RING'),('TENSE','PRESENT')]),
    word('raN',[('ROOT','RING'),('TENSE','PAST')]),
    word('riNiN',[('ROOT','RING'),('TENSE','PARTICIPLE')]),
    word('play',[('ROOT','PLAY'),('TENSE','PRESENT')]),
    word('played',[('ROOT','PLAY'),('TENSE','PAST')]),
    word('playiN',[('ROOT','PLAY'),('TENSE','PARTICIPLE')]),])
    modelSpace = create_model_space(lexicon,['ROOT','TENSE'])
    print modelSpace[0]