from input_data import *
import string
if __name__ == '__main__':
    dic = Dictionaryify([
    word(r'arid',[('ROOT','RED'),('NUMBER','SG'),('GENDER','MASCULINE')]),
    word(r'rida',[('ROOT','RED'),('NUMBER','SG'),('GENDER','FEMININE')]),
    word(r'arud',[('ROOT','RED'),('NUMBER','PL'),('GENDER','MASCULINE')]),
    word(r'ruda',[('ROOT','RED'),('NUMBER','PL'),('GENDER','FEMININE')]),
    word(r'ablk',[('ROOT','WHITE'),('NUMBER','SG'),('GENDER','MASCULINE')]),
    word(r'blka',[('ROOT','WHITE'),('NUMBER','SG'),('GENDER','FEMININE')]),
    word(r'ablk',[('ROOT','WHITE'),('NUMBER','PL'),('GENDER','MASCULINE')]),
    word(r'blka',[('ROOT','WHITE'),('NUMBER','PL'),('GENDER','FEMININE')]),
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
