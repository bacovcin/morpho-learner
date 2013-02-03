from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([
    word(r'pater',[('ROOT','FATHER'),('CASE','NOM')]),
    word(r'patrey',[('ROOT','FATHER'),('CASE','DAT')]),
    word(r'blahs',[('ROOT','BLAH'),('CASE','NOM')]),
    word(r'blahey',[('ROOT','BLAH'),('CASE','DAT')]),
    word(r'wugs',[('ROOT','WUG'),('CASE','NOM')]),
    word(r'wugey',[('ROOT','WUG'),('CASE','DAT')]),
    ])
    ordering = ['ROOT','CASE']
    models = build_models(create_model_space(lexicon, ordering),lexicon,settings(1,1,3,2))
    smallest = check_models(models,settings(1,1,3,2))
    for i in range(len(smallest)):
	model = smallest[i]
	print 'Model Number ' + str(i) + ':'
        for item in model.vocab:
            print 'Morphological Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + str(item.exponent.phon)
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)
	print '\n\n' 
