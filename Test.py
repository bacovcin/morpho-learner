from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([word('sin',[('ROOT','SING'),('TENSE','PRESENT')]),
    word('san',[('ROOT','SING'),('TENSE','PAST')]),
    word('sinin',[('ROOT','SING'),('TENSE','PARTICIPLE')]),
    word('rin',[('ROOT','RING'),('TENSE','PRESENT')]),
    word('ran',[('ROOT','RING'),('TENSE','PAST')]),
    word('rinin',[('ROOT','RING'),('TENSE','PARTICIPLE')]),
    word('play',[('ROOT','PLAY'),('TENSE','PRESENT')]),
    word('played',[('ROOT','PLAY'),('TENSE','PAST')]),
    word('playin',[('ROOT','PLAY'),('TENSE','PARTICIPLE')]),])
    model = build_vocabulary(lexicon,settings(1,1,1))
    print model
    for key in model:
        print key
        for item in model[key]:
            if item.exponent.phon != '':
                print item.morph_feature + ': ' + item.exponent.phon + ';' + str(item.context)
            else:
                print item.morph_feature + ': ' + 'NULL' + ';' + str(item.context)