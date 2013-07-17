from progressbar import *
from Phonology import *
from random import *

class word(object):
    def __init__(self,phon,morph):
        self.phonology = PhonParse(phon)#list of segments with features
        self.morphology = morph   #dictionary containing the root and an unordered list of other m-features

class exponent(object):
        def __init__(self,phonology,side):
            self.phon = phonology       #phonology of exponent
            self.side = side            #adfix type [(p)refix,(s)uffix]
            

class vocab_item(object):
    def __init__(self,morph_feature,phonology,side,context):
        self.morph_feature = morph_feature       #m-feature to be spelled out
        self.exponent = exponent(phonology,side) #exponent and adfix status
        self.context = context                   #when to use this item
        
class settings(object):
    def __init__(self, length, phon, nat, exponnum, burnin, chainlen, chainnum):
        self.vlength = length         #weight of the list length penalty
        self.phon = phon              #weight of the phonology vs. allomorphy 
        self.natural = nat            #maximum number of feature changes in a 'natural' change
	self.erat = exponnum	      #minimum number of forms that need to share an exponent for it to be used
	self.chainlen = chainlen      #number of iterations in the Markov chain
	self.burnin = burnin	      #number of iterations before saving any data
	self.chainnum = chainnum      #number of chains to run

class model(object):
    def __init__(self, vocab, mprules):
        self.vocab = vocab
        self.mprules = mprules

def is_ordered_subset(listb,lista):
    for i in range(len(lista)):
        for j in range(len(lista),i,-1):
            if listb == lista[i:j]:
                return True
    return False

def find_common_substring(word_list):
    is_common_substr = lambda subword, words: all(is_ordered_subset(subword,x) for x in words)
    long_string = []
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string
    result = []
    for j in range(len(long_string)):
        for i in range(len(long_string),-1,-1):
            if len(long_string[j:i]) > len(result):
                if is_common_substr(long_string[j:i],word_list):
                    result = long_string[j:i]
    return result

def test_vocab(vocab, roots, word_list):
    test = [test_word(vocab,roots,word) for word in word_list]
    return all(test)

def test_word(vocab, roots, word):
    try:
	phon = roots[word.morphology['ROOT']]
	context = word.morphology['ROOT']
	morphs = list(word.morphology['OTHER'])
	while morphs != []:
	    try:
		morph_copy = list(morphs)
		for morph in morph_copy:
		    if context in [c for item in vocab[morph] for c in item.context]:
			for item in vocab[morph]:
			    if context in item.context:
				if item.exponent.side == 'p':
				    phon = item.exponent.phon + phon
				else:
				    phon = phon + item.exponent.phon
				context = morph
				morphs.remove(morph)
		else:
		    if morphs == morph_copy:
			return False
	    except:
		return False
	if phon == word.phonology:
	    return True
	else:
	    return False
    except:
	return False
    return Error 

def find_pands(word,subset):
    sindex = 0
    p = []
    test = []
    s = []
    for i in range(len(word)):
	if sindex != -1:
	    if word[i] == subset[sindex]:
	        test.append(word[i])
	        if sindex == len(subset)-1:
		    sindex = -1
		else:
		    sindex = sindex + 1
	    else:
		p = p + test
		p.append(word[i])
	else:
	    s.append(word[i])
    return (p,s)

def clean_vocab(vocab):
    for morph in vocab.keys():
	i = 0
	while i < len(vocab[morph]):
	    j = 0
	    while j < len(vocab[morph]):
		item = vocab[morph][i]
		item2 = vocab[morph][j]
		if item2.exponent.side == item.exponent.side and item2.exponent.phon == item.exponent.phon and i != j:
		    item.context = item.context + item2.context
		    vocab[morph].remove(item2)
		    if i > j:
			i = i - 1
		else:
		    j = j + 1
	    i = i + 1
    return vocab
	    

def learn_vocab(word_list, debug = False, iterate = False):
    def reordered(alist):
	listcopy = list(alist)
	newlist = []
	length = len(listcopy)
	for i in range(length):
	    newlist.append(listcopy.pop(randint(0,len(listcopy)-1)))
	return newlist
    vocab = {}
    roots = {}
    iteration = 0
    while not test_vocab(vocab,roots,word_list):
	for word in reordered(word_list):
	    if debug:
		print 'ROOT: ' + word.morphology['ROOT']
		print 'Word.phonology: ' + ''.join([IPA[c] for c in word.phonology])
		try:
		    print 'Root phonology: ' + ''.join([IPA[c] for c in roots[word.morphology['ROOT']]])
		except:
		    print 'Root phonology: UNKNOWN'
		context = word.morphology['ROOT']
		morphs = list(word.morphology['OTHER'])
		while morphs != []:
                    morph_copy = list(morphs)
                    for morph in morph_copy:
			try:
			    print 'Contexts: ' + str([c for item in vocab[morph] for c in item.context])
                            if context in [c for item in vocab[morph] for c in item.context]:
			        print 'Morph: ' + morph
                                for item in vocab[morph]:
                                    if context in item.context:
					print 'Morph phonololgy: ' + ''.join([IPA[c] for c in item.exponent.phon])
					print 'Morph side: ' + item.exponent.side
                                        context = morph
                                        morphs.remove(morph)
			except:
			     morphs.remove(morph)
			     print 'Morph: ' + morph
                             print 'Morph phonololgy: UNKOWN 1'
                             print 'Morph side: UNKNOWN 1'
                    else:
                        if morphs == morph_copy:
                            for morph in morphs:
				print 'Morph: ' + morph
				print 'Morph phonololgy: UNKOWN 2'
				print 'Morph side: UNKNOWN 2' 
			    morphs = []
		print roots.keys()
		print vocab.keys()
		raw_input()
	    if not test_word(vocab, roots, word):
	        if word.morphology['ROOT'] not in roots.keys():
		    old = [x in vocab.keys() for x in word.morphology['OTHER']]
		    if True not in old:
			roots[word.morphology['ROOT']] = word.phonology
			context = word.morphology['ROOT']
			for morph in word.morphology['OTHER']:
			    vocab[morph] = [vocab_item(morph,[],'s',[context])]
			    context = morph
		    else:
			phon = list(word.phonology)
			unused_morphs = list(word.morphology['OTHER'])
			for morph in word.morphology['OTHER']:
			    try:
				removal = []
				for item in vocab[morph]:
				    if item.exponent.phon != []:
				        try:
				            if item.exponent.side == 'p':
					        for i in range(len(item.exponent.phon)):
					            if item.exponent.phon[i] != phon[i]:
						        break
					        else:
						    for item2 in vocab[morph]:
							if word.morphology['ROOT'] in item2.context:
							    item2.context.remove(word.morphology['ROOT'])
							    if item2.context == []:
								removal.append(item2)
					            item.context.append(word.morphology['ROOT'])
					            phon = phon[len(item.exponent.phon):]
						    unused_morphs.remove(morph)
				            else:
                                                for i in range(-1,(len(item.exponent.phon)*-1)-1,-1):
                                                    if item.exponent.phon[i] != phon[i]:
                                                        break
                                                else:
                                                    for item2 in vocab[morph]:
                                                        if word.morphology['ROOT'] in item2.context:
                                                            item2.context.remove(word.morphology['ROOT'])
                                                            if item2.context == []:
                                                                removal.append(item2)
                                                    item.context.append(word.morphology['ROOT'])
                                                    phon = phon[:-len(item.exponent.phon)]
						    unused_morphs.remove(morph)
				        except:
					    continue
				for x in removal:
				    vocab[morph].remove(x)
			    except:
				continue
			roots[word.morphology['ROOT']] = phon
			context = word.morphology['ROOT']
                        for morph in unused_morphs:
			    if morph not in vocab.keys():
                                vocab[morph] = [vocab_item(morph,[],'s',[context])]
                                context = morph
			    else:
				vocab[morph].append(vocab_item(morph,[],'s',[context]))
                                context = morph
		else:
		    old = [x in vocab.keys() for x in word.morphology['OTHER']]
                    if True not in old:
			subset = find_common_substring([word.phonology,roots[word.morphology['ROOT']]])
                        roots[word.morphology['ROOT']] = subset
			context = word.morphology['ROOT']
			pands = find_pands(word.phonology,subset)
			morphs = list(word.morphology['OTHER'])
			if pands[0] == []:
			    if pands[1] == []:
				mindex = 0
			    else:
				mindex = 1
				vocab[morphs[0]] = [vocab_item(morph,pands[1],'s',[context])]
				context = morphs[0]
			else:
			    if pands[1] == []:
                                mindex = 1
                                vocab[morphs[0]] = [vocab_item(morph,pands[0],'p',[context])]
                            else:
                                mindex = 2
				vocab[morphs[0]] = [vocab_item(morph,pands[0],'p',[context])]
                                vocab[morphs[1]] = [vocab_item(morph,pands[1],'s',[context])]
                                context = morphs[1]
                        for morph in word.morphology['OTHER'][mindex:]:
                            vocab[morph] = [vocab_item(morph,[],'s',[context])]
			    context = morph
		    else:
			phon = list(word.phonology)
                        unused_morphs = list(word.morphology['OTHER'])
                        for morph in word.morphology['OTHER']:
                            try:
				removal = []
                                for item in vocab[morph]:
				    if item.exponent.phon != []:
                                        try:
                                            if item.exponent.side == 'p':
                                                for i in range(len(item.exponent.phon)):
                                                    if item.exponent.phon[i] != phon[i]:
                                                        break
                                                else:
                                                    for item2 in vocab[morph]:
                                                        if word.morphology['ROOT'] in item2.context:
                                                            item2.context.remove(word.morphology['ROOT'])
                                                            if item2.context == []:
                                                                removal.append(item2)
                                                    item.context.append(word.morphology['ROOT'])
                                                    phon = phon[len(item.exponent.phon):]
                                                    unused_morphs.remove(morph)
                                            else:
                                                for i in range(-1,(len(item.exponent.phon)*-1)-1,-1):
                                                    if item.exponent.phon[i] != phon[i]:
                                                        break
                                                else:
                                                    for item2 in vocab[morph]:
                                                        if word.morphology['ROOT'] in item2.context:
                                                            item2.context.remove(word.morphology['ROOT'])
                                                            if item2.context == []:
                                                                removal.append(item2)
                                                    item.context.append(word.morphology['ROOT'])
                                                    phon = phon[:-len(item.exponent.phon)]
                                                    unused_morphs.remove(morph)
                                        except:
                                            continue
				for x in removal:
				     vocab[morph].remove(x)
                            except:
                                continue
			subset = find_common_substring([phon,roots[word.morphology['ROOT']]])
                        roots[word.morphology['ROOT']] = subset
			pands = find_pands(phon,subset)
			if unused_morphs == [] and subset != phon:
			    subset = find_common_substring([word.phonology,roots[word.morphology['ROOT']]])
			    pands = find_pands(word.phonology,subset)
			    for morph in word.morphology['OTHER']:
				try:
				    for item in vocab[morph]:
					if word.morphology['ROOT'] in item.context:
					    item.context.remove(word.morphology['ROOT'])
					    unused_morphs.append(morph)
				except:
				    continue
                        context = word.morphology['ROOT']
                        morphs = list(unused_morphs)
                        if pands[0] == []:
                            if pands[1] == []:
                                mindex = 0
                            else:
                                mindex = 1
				if morphs[0] not in vocab.keys():
                                    vocab[morphs[0]] = [vocab_item(morph,pands[1],'s',[context])]
				else:
				    vocab[morphs[0]].append(vocab_item(morph,pands[1],'s',[context]))
                                context = morphs[0]
                        else:
                            if pands[1] == []:
                                mindex = 1
			        if morphs[0] not in vocab.keys():
                                    vocab[morphs[0]] = [vocab_item(morph,pands[0],'p',[context])]
                                else:
                                    vocab[morphs[0]].append(vocab_item(morph,pands[0],'p',[context]))
                            else:
                                mindex = 2
				if morphs[0] not in vocab.keys():
                                    vocab[morphs[0]] = [vocab_item(morph,pands[0],'p',[context])]
                                else:
                                    vocab[morphs[0]].append(vocab_item(morph,pands[0],'p',[context]))
				if morphs[1] not in vocab.keys():
                                    vocab[morphs[1]] = [vocab_item(morph,pands[1],'s',[context])]
                                else:
                                    vocab[morphs[1]].append(vocab_item(morph,pands[1],'s',[context]))
                                context = morphs[1]
                        for morph in unused_morphs[mindex:]:
                            if morph not in vocab.keys():
                                vocab[morph] = [vocab_item(morph,[],'s',[context])]
                                context = morph
                            else:
                                vocab[morph].append(vocab_item(morph,[],'s',[context]))
                                context = morph
	vocab = clean_vocab(vocab)
	if iterate:
	    iteration = iteration + 1
	    print 'Iteration #' + str(iteration)
	    for root in roots.keys():
                print root + ': ' + ''.join([IPA[c] for c in roots[root]])
            for key in vocab.keys():
                print '\n' + key + ':'
                for item in vocab[key]:
                    print 'Exponent Phonology: ' + ''.join([IPA[c] for c in item.exponent.phon])
                    print 'Exponent Side: ' + item.exponent.side
                    print 'Context: ' + str(item.context)
	    raw_input('To continue press any button...')
    for root in roots.keys():
	print root + ': ' + ''.join([IPA[c] for c in roots[root]])
    for key in vocab.keys():
	print '\n' + key + ':'
	for item in vocab[key]:
	    print 'Exponent Phonology: ' + ''.join([IPA[c] for c in item.exponent.phon])
	    print 'Exponent Side: ' + item.exponent.side
	    print 'Context: ' + str(item.context)

