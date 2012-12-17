from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([word('abide',[('ROOT','r1'),('THEME','v1'),('TENSE','t1')]),
    word('abeba',[('ROOT','r1'),('THEME','v2'),('TENSE','t1')]),
    word('abide',[('ROOT','r1'),('THEME','v1'),('TENSE','t2')]),
    word('abeba',[('ROOT','r1'),('THEME','v2'),('TENSE','t2')]),
    word('efude',[('ROOT','r2'),('THEME','v1'),('TENSE','t1')]),
    word('efoba',[('ROOT','r2'),('THEME','v2'),('TENSE','t1')]),
    word('efude',[('ROOT','r2'),('THEME','v1'),('TENSE','t2')]),
    word('efoba',[('ROOT','r2'),('THEME','v2'),('TENSE','t2')])])
    ordering = ['ROOT','THEME','TENSE']
    models = build_models(create_model_space(lexicon, ordering),lexicon)
    for type in models[0]:
        for item in type:
            print 'Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + str(item.exponent.phon)
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)