from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([
    word('abida',[('ROOT','r1'),('THEME','v1'),('TENSE','t1')]),
    word('ideab',[('ROOT','r1'),('THEME','v2'),('TENSE','t1')]),
    word('abiba',[('ROOT','r1'),('THEME','v1'),('TENSE','t2')]),
    word('ibeab',[('ROOT','r1'),('THEME','v2'),('TENSE','t2')]),
    word('abuda',[('ROOT','r2'),('THEME','v1'),('TENSE','t1')]),
    word('udeab',[('ROOT','r2'),('THEME','v2'),('TENSE','t1')]),
    word('abuba',[('ROOT','r2'),('THEME','v1'),('TENSE','t2')]),
    word('ubeab',[('ROOT','r2'),('THEME','v2'),('TENSE','t2')])
    ])
    ordering = ['ROOT','THEME','TENSE']
    models = build_models(create_model_space(lexicon, ordering),lexicon)
    smallest = check_models(models,settings(1,1))
    for model in smallest:
        for item in model.vocab:
            print 'Morphological Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + str(item.exponent.phon)
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)
    
