from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([
    word('riN',[('ROOT','RING'),('TAM','PRESENT')]),
    word('ruN',[('ROOT','RING'),('TAM','PARTICIPLE')]),
   # word('raN',[('ROOT','RING'),('TAM','PAST')]),
    word('siN',[('ROOT','SING'),('TAM','PRESENT')]),
    word('suN',[('ROOT','SING'),('TAM','PARTICIPLE')]),
   # word('saN',[('ROOT','SING'),('TAM','PAST')]),
   # word('briN',[('ROOT','BRING'),('TAM','PRESENT')]),
   # word('braUt',[('ROOT','BRING'),('TAM','PARTICIPLE')]),
   # word('braN',[('ROOT','BRING'),('TAM','PAST')]),
    word('play',[('ROOT','PLAY'),('TAM','PRESENT')]),
    word('played',[('ROOT','PLAY'),('TAM','PARTICIPLE')]),
   # word('played',[('ROOT','PLAY'),('TAM','PAST')]),
    ])
    ordering = ['ROOT','TAM']
    ms = create_model_space(lexicon, ordering) 
    models = build_models(ms,lexicon)
    smallest = check_models(models,settings(1,1))
    for model in smallest:
        for item in model.vocab:
            print 'Morphological Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + str(item.exponent.phon)
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)
    
