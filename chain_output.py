import string
from Phonology import *

def printChains(chains):
    valid_models = []
    for models in chains:
        valid_models.append([])
        for model in set(models):
            if (float(models.count(model))/float(len(models))) > .01:
                valid_models[-1].append(model)
    for chainnum in range(len(valid_models)):
        print 'Chain Number ' + str(chainnum) + ':'
        for i in range(len(valid_models[chainnum])):
            model = valid_models[chainnum][i]
            print 'Model Number ' + str(i+1) + ':'
            count = float(float(models.count(model))/float(len(models)))
            print 'Count %.4f: ' % count
            for item in model.vocab:
                print 'Morphological Feature: ' + str(item.morph_feature)
                print 'Phonology: ' + ''.join(IPAword(item.exponent.phon))
                print 'Side: ' + str(item.exponent.side)
                print 'Context: ' + str(item.context)
            print '\n\n'
    return
