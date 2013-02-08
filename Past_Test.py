from input_data import *
import string
if __name__ == '__main__':
    dic = Dictionaryify([
    word(r'rIN',[('ROOT','RING'),('TNS','PRS')]),
    word(r'r{\ae}N',[('ROOT','RING'),('TNS','PST')]),
    #word(r'sIN',[('ROOT','SING'),('TNS','PRS')]),
    #word(r's{\ae}N',[('ROOT','SING'),('TNS','PST')]),
    word(r'bId',[('ROOT','BID'),('TNS','PRS')]),
    word(r'b{\ae}d',[('ROOT','BID'),('TNS','PST')]),
    word(r'wOk',[('ROOT','WALK'),('TNS','PRS')]),
    word(r'wOkt',[('ROOT','WALK'),('TNS','PST')]),
    word(r'brIN',[('ROOT','BRING'),('TNS','PRS')]),
    word(r'brat',[('ROOT','BRING'),('TNS','PST')]),
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
