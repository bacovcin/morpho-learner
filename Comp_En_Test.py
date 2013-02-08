from input_data import *
import string
if __name__ == '__main__':
    dic = Dictionaryify([
    word(r'fIS',[('ROOT','FISH'),('NUMBER','SG')]),
    word(r'fIS9z',[('ROOT','FISH'),('NUMBER','PL')]),
    word(r'dAg',[('ROOT','DOG'),('NUMBER','SG')]),
    word(r'dAgz',[('ROOT','DOG'),('NUMBER','PL')]),
    word(r'fIS',[('ROOT','FISH'),('TENSE','PRESENT')]),
    word(r'fISIN',[('ROOT','FISH'),('TAM','PRESENT PARTICIPLE')]),
    word(r'fISt',[('ROOT','FISH'),('TENSE','PAST')]),
    word(r'plej',[('ROOT','PLAY'),('TENSE','PRESENT')]),
    word(r'plejIN',[('ROOT','PLAY'),('TAM','PRESENT PARTICIPLE')]),
    word(r'plejd',[('ROOT','PLAY'),('TENSE','PAST')]),
    ])
    lexicon = dic[0]
    ordering = dic[1]
    models = build_models(create_model_space(lexicon, ordering),lexicon,settings(1,1,3,2),mp=False)
    smallest = check_models(models,settings(1,1,3,2))
    for i in range(len(smallest)):
	model = smallest[i]
	print 'Model Number ' + str(i+1) + ':'
        for item in model.vocab:
            print 'Morphological Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + ''.join(IPAword(item.exponent.phon))
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)
	print '\n\n' 
