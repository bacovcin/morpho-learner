from input_data import *
import string
if __name__ == '__main__':
    lexicon = Dictionaryify([
    word(r'rIN',[('ROOT','RING'),('TNS','PRS')]),
    word(r'r{\ae}N',[('ROOT','RING'),('TNS','PST')]),
    #word(r'sIN',[('ROOT','SING'),('TNS','PRS')]),
    #word(r's{\ae}N',[('ROOT','SING'),('TNS','PST')]),
    word(r'bId',[('ROOT','BID'),('TNS','PRS')]),
    word(r'b{\ae}d',[('ROOT','BID'),('TNS','PST')]),
    word(r'wOk',[('ROOT','WALK'),('TNS','PRS')]),
    word(r'wOkt',[('ROOT','WALK'),('TNS','PST')])
    ])
    ordering = ['ROOT','TNS']
    models = build_models(create_model_space(lexicon, ordering),lexicon,settings(1,1,3,2),mp=True)
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