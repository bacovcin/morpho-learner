from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([
    word(r'fIS',[('ROOT','FISH'),('NUMBER','SG')]),
    word(r'fIS9z',[('ROOT','FISH'),('NUMBER','PL')]),
    word(r'dAg',[('ROOT','DOG'),('NUMBER','SG')]),
    word(r'dAgz',[('ROOT','DOG'),('NUMBER','PL')]),
    word(r'c\ae t',[('ROOT','CAT'),('NUMBER','SG')]),
    word(r'c\ae ts',[('ROOT','CAT'),('NUMBER','PL')]),
    word(r'toU',[('ROOT','TOE'),('NUMBER','SG')]),
    word(r'toUz',[('ROOT','TOE'),('NUMBER','PL')])
    ])
    ordering = ['ROOT','NUMBER']
    models = build_models(create_model_space(lexicon, ordering),lexicon,settings(1,1,3,2),mp=False)
    smallest = check_models(models,settings(1,1,3,2))
    for i in range(len(smallest)):
	model = smallest[i]
	print 'Model Number ' + str(i+1) + ':'
        for item in model.vocab:
            print 'Morphological Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + str(item.exponent.phon)
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)
	print '\n\n' 
