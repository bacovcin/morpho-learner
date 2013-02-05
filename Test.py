from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([
    word(r'arid',[('ROOT','RED'),('NUMBER','SG'),('GENDER','MASCULINE')]),
    word(r'rida',[('ROOT','RED'),('NUMBER','SG'),('GENDER','FEMININE')]),
    word(r'arud',[('ROOT','RED'),('NUMBER','PL'),('GENDER','MASCULINE')]),
    word(r'ruda',[('ROOT','RED'),('NUMBER','PL'),('GENDER','FEMININE')]),
    word(r'ablk',[('ROOT','WHITE'),('NUMBER','SG'),('GENDER','MASCULINE')]),
    word(r'blka',[('ROOT','WHITE'),('NUMBER','SG'),('GENDER','FEMININE')]),
    word(r'ablk',[('ROOT','WHITE'),('NUMBER','PL'),('GENDER','MASCULINE')]),
    word(r'blka',[('ROOT','WHITE'),('NUMBER','PL'),('GENDER','FEMININE')]),
    ])
    ordering = ['ROOT','NUMBER','GENDER']
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
