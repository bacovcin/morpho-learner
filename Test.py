from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([word('abida',[('ROOT','r1'),('THEME','v1'),('TENSE','t1')]),
    word('abuda',[('ROOT','r1'),('THEME','v2'),('TENSE','t1')]),
    word('abiba',[('ROOT','r1'),('THEME','v1'),('TENSE','t2')]),
    word('abuba',[('ROOT','r1'),('THEME','v2'),('TENSE','t2')]),
    word('efide',[('ROOT','r2'),('THEME','v1'),('TENSE','t1')]),
    word('efude',[('ROOT','r2'),('THEME','v2'),('TENSE','t1')]),
    word('efibe',[('ROOT','r2'),('THEME','v1'),('TENSE','t2')]),
    word('efube',[('ROOT','r2'),('THEME','v2'),('TENSE','t2')])])
    ordering = ['ROOT','THEME','TENSE']
    models = build_models(create_model_space(lexicon, ordering),lexicon)
    smallest = check_models(models,settings(1,1))
    for item in smallest[0].vocab:
        print 'Morphological Feature: ' + str(item.morph_feature)
        print 'Phonology: ' + str(item.exponent.phon)
        print 'Side: ' + str(item.exponent.side)
        print 'Context: ' + str(item.context)
    