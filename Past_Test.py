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
    setting = settings(1,1,3,2,5000,10000)
    models = build_models(create_model_space(lexicon, ordering),lexicon,setting,mp=False)
    valid_models = []
    curModel = models[0]
    for model in set(models):
        if (float(models.count(model))/float(len(models))) > .01:
            count = models.count(model)
            valid_models.append(model)
    print 'Count: ' + str(float(count)/float(len(models)))
    for i in range(len(valid_models)):
        model = valid_models[i]
        print 'Model Number ' + str(i+1) + ':'
        print 'Count: ' + str(float(count)/float(len(models)))
        for item in model.vocab:
            print 'Morphological Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + ''.join(IPAword(item.exponent.phon))
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)
        print '\n\n'
