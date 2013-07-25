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

def test_vocab(vocab, roots, word_list, iterate):
    test = [test_word(vocab,roots,word) for word in word_list]
    if iterate:
        print 'Words: ' + str([''.join(IPA[c] for c in word.phonology) for word in word_list])
        print 'Results: ' + str(test)
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
			    if context in item.context and item.exponent.phon != []:
				if item.exponent.side == 'p':
				    phon = item.exponent.phon + phon
				else:
				    phon = phon + item.exponent.phon
				context = morph
				morphs.remove(morph)
			    elif context in item.context and item.exponent.phon == []:
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
    return [p,s]

def clean_vocab(vocab):
    for morph in vocab.keys():
	for itemnum in range(len(vocab[morph])):
	   item = vocab[morph][itemnum]
	   for itemnum2 in range(len(vocab[morph])):
		item2 = vocab[morph][itemnum2]
		if itemnum != itemnum2:
  		    for context in item.context:
		        if context in item2.context:
			    if len(item.exponent.phon) <= len(item2.exponent.phon):
			        vocab[morph][itemnum2].context.remove(context)
			    else:
			        vocab[morph][itemnum].context.remove(context)
	itemnum = 0
        while itemnum < len(vocab[morph]):
            item = vocab[morph][itemnum]
            if item.context == []:
                del vocab[morph][itemnum]
            else:
                itemnum = itemnum + 1
	i = 0
	while i < len(vocab[morph]):
	    j = 0
	    while j < len(vocab[morph]):
		item = vocab[morph][i]
		item2 = vocab[morph][j]
		if item2.exponent.side == item.exponent.side and item2.exponent.phon == item.exponent.phon and i != j:
		    newcontext = item.context + item2.context
		    vocab[morph][i].context = []
		    for context in newcontext:
			if context not in item.context:
			    vocab[morph][i].context.append(context)
		    vocab[morph].remove(item2)
		    if i > j:
			i = i - 1
		else:
		    j = j + 1
	    i = i + 1
    return vocab
	    

def null_context_search(vocab,morphs,unused_morphs,pands):
    for morph in morphs:
        try:
            cont = 0
	    removal = []
            for itemnum in range(len(vocab[morph])):
	        item = vocab[morph][itemnum]
                if item.context == [] and item.exponent.phon != []:
                    if item.exponent.side == 'p':
                        for partnum in range(len(pands[0])):
                            part = pands[0][partnum]
                            if not isinstance(part,tuple):
                                subset = find_common_substring([part,item.exponent.phon])
                                if subset != []:
                                    unused_morphs.remove(morph)
                                    item.exponent.phon == subset
                                    subpands = find_pands(part,item.exponent.phon)
                                    pands[0][partnum] = (morph,item)
                                    usenum = partnum
                                    if subpands[0] != []:
                                        pands[0].insert(partnum,subpands[0])
                                        usenum = usenum + 1
                                    if subpands[1] != []:
                                        pands[0].insert(usenum+1,subpands[1])
		  		    cont = 1
                                    break
			else:
			    removal.append(item)
	            else:
                        for partnum in range(len(pands[1])):
                            part = pands[1][partnum]
                            if not isinstance(part,tuple):
                                subset = find_common_substring([part,item.exponent.phon])
                                if subset != []:
                                    unused_morphs.remove(morph)
                                    item.exponent.phon == subset
                                    subpands = find_pands(part,item.exponent.phon)
                                    pands[1][partnum] = (morph,item)
                                    usenum = partnum
                                    if subpands[0] != []:
                                        pands[1].insert(partnum,subpands[0])
                                        usenum = usenum + 1
                                    if subpands[1] != []:
                                        pands[1].insert(usenum+1,subpands[1])
				    cont = 1
                                    break
		        else:
			    removal.append(item)
		    if cont != 0:
                        break
	    for item in removal:	
	        vocab[morph].remove(item)
        except KeyError:
            continue
    return (vocab,unused_morphs,pands)

def other_item_search(vocab,morphs,unused_morphs,pands):
    for morph in morphs:
        try:
            cont = 0
            newitem = []
            for itemnum in range(len(vocab[morph])):
                item = vocab[morph][itemnum]	
		if item.context != [] and item.exponent.phon != []:
		    if item.exponent.side == 'p':
                        for partnum in range(len(pands[0])):
                            part = pands[0][partnum]
                            if not isinstance(part,tuple):
                                if is_ordered_subset(item.exponent.phon,part):
                                    unused_morphs.remove(morph)
                                    subpands = find_pands(part,item.exponent.phon)
                                    pands[0][partnum] = (morph,item)
                                    usenum = partnum
                                    if subpands[0] != []:
                                        pands[0].insert(partnum,subpands[0])
                                        usenum = usenum + 1
                                    if subpands[1] != []:
                                        pands[0].insert(usenum+1,subpands[1])
				    cont = 1
                                    break
		        else:
			    for partnum in range(len(pands[0])):
                                part = pands[0][partnum]
                                if not isinstance(part,tuple):
                                    subset = find_common_substring([part,item.exponent.phon])
                                    if subset != []:
                                        unused_morphs.remove(morph)
				        newitem.append(vocab_item(morph,subset,'p',[]))
                                        subpands = find_pands(part,subset)
                                        pands[0][partnum] = (morph,newitem[-1])
                                        usenum = partnum
                                        if subpands[0] != []:
                                            pands[0].insert(partnum,subpands[0])
                                            usenum = usenum + 1
                                        if subpands[1] != []:
                                            pands[0].insert(usenum+1,subpands[1])
                                        cont = 1
                                        break
		    else:
                        for partnum in range(len(pands[1])):
                            part = pands[1][partnum]
                            if not isinstance(part,tuple):
                                if is_ordered_subset(item.exponent.phon,part):
                                    unused_morphs.remove(morph)
                                    subpands = find_pands(part,item.exponent.phon)
                                    pands[1][partnum] = (morph,item)
                                    usenum = partnum
                                    if subpands[0] != []:
                                        pands[1].insert(partnum,subpands[0])
                                        usenum = usenum + 1
                                    if subpands[1] != []:
                                        pands[1].insert(usenum+1,subpands[1])
		       	 	    cont = 1
                                    break
			else:
			    for partnum in range(len(pands[1])):
                                part = pands[1][partnum]
                                if not isinstance(part,tuple):
                                    subset = find_common_substring([part,item.exponent.phon])
                                    if subset != []:
                                        unused_morphs.remove(morph)
			  	        newitem.append(vocab_item(morph,subset,'s',[]))
                                        subpands = find_pands(part,subset)
                                        pands[1][partnum] = (morph,newitem[-1])
                                        usenum = partnum
                                        if subpands[0] != []:
                                            pands[1].insert(partnum,subpands[0])
                                            usenum = usenum + 1
                                        if subpands[1] != []:
                                            pands[1].insert(usenum+1,subpands[1])
                                        cont = 1
                                        break
                    if cont != 0:
		        break
	    for item in newitem:
	        vocab[morph].append(item)
	except KeyError:
	    continue
    return (vocab,unused_morphs,pands)

def learn_vocab(word_list, debug = False, iterate = False, output = True):
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
    while not test_vocab(vocab,roots,word_list,iterate):
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
		print 'ROOTS: ' + str(roots.keys())
		print 'VOCAB: ' + str(vocab.keys())
		if iterate:
                    print 'Iteration #' + str(iteration)
                    for root in roots.keys():
                        print root + ': ' + ''.join([IPA[c] for c in roots[root]])
                    for key in vocab.keys():
                        print '\n' + key + ':'
                        for item in vocab[key]:
                            print 'Exponent Phonology: ' + ''.join([IPA[c] for c in item.exponent.phon])
                            print 'Exponent Side: ' + item.exponent.side
                            print 'Context: ' + str(item.context)
	    #END-OF-DEBUG
	    if not test_word(vocab, roots, word):
	        if word.morphology['ROOT'] not in roots.keys():
		    old = [x in vocab.keys() for x in word.morphology['OTHER']]
		    if True not in old:
			if debug:
			    raw_input('Type 1')
			#All new
			roots[word.morphology['ROOT']] = word.phonology
			context  = word.morphology['ROOT']
			for morph in word.morphology['OTHER']:
			    vocab[morph] = [vocab_item(morph,[],'s',[context])]
                        #    vocab[morph] = [vocab_item(morph,word.phonology,'s',[])]
		    else:
			#New root, old others
			if debug:
                            raw_input('Type 2')
			pands = list([[word.phonology],[word.phonology]])
			unused_morphs = list(word.morphology['OTHER'])
			ncs = null_context_search(vocab,list(unused_morphs),unused_morphs,pands)
			vocab = ncs[0]
			unused_morphs = ncs[1]
			pands = ncs[2]
			ois = other_item_search(vocab,list(unused_morphs),unused_morphs,pands)
                        vocab = ois[0]
                        unused_morphs = ois[1]
                        pands = ois[2]
                        morphs = list(unused_morphs)
			context = word.morphology['ROOT']
			for morph in unused_morphs:
			    vocab[morph] = [vocab_item(morph,[],'s',[context])]
			for i in range(len(pands[0])-1,-1,-1):
		            part = pands[0][i]
			    if not isinstance(part,tuple):
				pre = part
				break
			for i in range(len(pands[1])):
                            part = pands[1][i]
                            if not isinstance(part,tuple):
				suf = part
                                break
			roots[word.morphology['ROOT']] = find_common_substring([pre,suf])
			context = word.morphology['ROOT']
                        for i in range(len(pands[0])-1,-1,-1):
                            if isinstance(pands[0][i],tuple):
                                morph = pands[0][i][0]
				itemnum = vocab[morph].index(pands[1][i][1])
                                if context not in vocab[morph][itemnum].context:
                                    vocab[morph][itemnum].context.append(context)
                                context = morph
                        context = word.morphology['ROOT']
                        for i in range(len(pands[1])):
                            if isinstance(pands[1][i],tuple):
                                morph = pands[1][i][0]
				itemnum = vocab[morph].index(pands[1][i][1])
                                if context not in vocab[morph][itemnum].context:
                                    vocab[morph][itemnum].context.append(context)
                                context = morph
		else:
		    old = [x in vocab.keys() for x in word.morphology['OTHER']]
                    if True not in old:
			#old root, new others
			if debug:
                            raw_input('Type 3')
			subset = find_common_substring([word.phonology,roots[word.morphology['ROOT']]])
                        roots[word.morphology['ROOT']] = subset
			pands = find_pands(word.phonology,subset)
			morphs = list(word.morphology['OTHER'])
			for morph in morphs:
			    if pands[0] != []:
				vocab[morph] = [vocab_item(morph,pands[0],'p',[])]
			    if pands[1] != []:
				vocab[morph] = [vocab_item(morph,pands[1],'s',[])]
			if pands[0] == [] and pands[1] == []:
			    for morph in morphs:
				vocab[morph] = [vocab_item(morph,[],'s',[word.morphology['ROOT']])]
		    else:
			#old root, old others
			if debug:
                            raw_input('Type 4')
			subset = find_common_substring([word.phonology,roots[word.morphology['ROOT']]])
			roots[word.morphology['ROOT']] = subset
			presuf = find_pands(word.phonology,subset)
			pands = [[],[]]
			if presuf[0] != []:
			    pands[0].append(list(presuf[0]))
			if presuf[1] != []:
                            pands[1].append(list(presuf[1]))
			unused_morphs = list(word.morphology['OTHER'])
			#check current vocab
			for morph in word.morphology['OTHER']:
			    try:
				cont = 0
				removal = []
				for itemnum in range(len(vocab[morph])):
				    item = vocab[morph][itemnum]
				    if (word.morphology['ROOT'] in item.context or
				       True in [mor in item.context for mor in word.morphology['OTHER']]):
					if item.exponent.side == 'p':
					    for partnum in range(len(pands[0])):
						part = pands[0][partnum]
						if not isinstance(part,tuple):
					            if is_ordered_subset(item.exponent.phon,part):
						        unused_morphs.remove(morph)
							subpands = find_pands(part,item.exponent.phon)
						        pands[0][partnum] = (morph,item)
							usenum = partnum
                                                        if subpands[0] != []:
                                                            pands[0].insert(partnum,subpands[0])
                                                            usenum = usenum + 1
                                                        if subpands[1] != []:
                                                            pands[0].insert(usenum+1,subpands[1])
							cont = 1
							break
					    else:
						try:
                                                    vocab[morph][itemnum].context.remove(word.morphology['ROOT'])
                                                except ValueError:
						    pass
                                                for mor in word.morphology['OTHER']:
                                                    try:
                                                        vocab[morph][itemnum].context.remove(mor)
                                                    except ValueError:
                                                        continue
						if vocab[morph][itemnum].context == []:
						    removal.append(item)
					else:
					    for partnum in range(len(pands[1])):
                                                part = pands[1][partnum]
						if not isinstance(part,tuple):
                                                    if is_ordered_subset(item.exponent.phon,part):
                                                        unused_morphs.remove(morph)
							subpands = find_pands(part,item.exponent.phon)
                                                        pands[1][partnum] = (morph,item)
							usenum = partnum
							if subpands[0] != []:
                                                            pands[1].insert(partnum,subpands[0])
							    usenum = usenum + 1
							if subpands[1] != []:
                                                            pands[1].insert(usenum+1,subpands[1])
							cont = 1
						        break
                                            else:
						try:
						    vocab[morph][itemnum].context.remove(word.morphology['ROOT'])
						except ValueError:
						    pass
						for mor in word.morphology['OTHER']:
						    try:
                                                        vocab[morph][itemnum].context.remove(mor)
						    except ValueError:
							continue
						if vocab[morph][itemnum].context == []:
						    removal.append(item)
				    if cont != 0:
				        break
				for item in removal:
                                    vocab[morph].remove(item)
			    except KeyError:
				continue
			morphs = list(unused_morphs)
			ncs = null_context_search(vocab,list(unused_morphs),unused_morphs,pands)
			vocab = ncs[0]
			pands = ncs[2]
			ois = other_item_search(vocab,list(unused_morphs),unused_morphs,pands)
                        vocab = ois[0]
                        unused_morphs = ois[1]
                        pands = ois[2]
                        morphs = list(unused_morphs)
			for morph in unused_morphs:
			    for partnum in range(len(pands[0])):
				part = pands[0][partnum]
				if not isinstance(part,tuple):
				    item = vocab_item(morph,part,'p',[])
				    try:
					vocab[morph].append(item)
				    except:
					vocab[morph] = [item]
				    pands[0][partnum] = (morph,item)
				    break
			    else:
				for partnum in range(len(pands[1])):
				    part = pands[1][partnum]
				    if not isinstance(part,tuple):
                                        item = vocab_item(morph,part,'s',[])
                                        try:
                                            vocab[morph].append(item)
                                        except:
                                            vocab[morph] = [item]
					pands[1][partnum] = (morph,item)
                                        break
				else:
				    item = vocab_item(morph,[],'s',[word.morphology['ROOT']])
                                    try:
                                        vocab[morph].append(item)
                                    except:
                                        vocab[morph] = [item]
			i = 0
			while i < len(pands[0]):
			    try:
			        if not isinstance(pands[0][i],tuple):
				    try:
				        while not isinstance(pands[0][i+1],tuple):
    					    pands[0][i] = pands[0][i] + pands[0][i+1]
					    del pands[0][i+1]	
				        old = pands[0][i+1]
					morph = old[0]
					oldnum = vocab[morph].index(old[1])
					try:
					    vocab[morph][oldnum].context.remove(word.morphology['ROOT'])
					except:
					    pass
					for mor in word.morphology['OTHER']:
					    try:
						vocab[mor][oldnum].context.remove(mor)
					    except:
						continue
                                        new = vocab_item(morph,pands[0][i]+old[1].exponent.phon,'p',[])
                                        vocab[morph].append(new)
					pands[0][i+1] = (morph,new)
				    except IndexError:
				        old = pands[0][i-1]
				        morph = old[0]
					oldnum = vocab[morph].index(old[1])
                                        try:
                                            vocab[morph][oldnum].context.remove(word.morphology['ROOT'])
                                        except:
                                            pass
                                        for mor in word.morphology['OTHER']:
                                            try:
                                                vocab[mor][oldnum].context.remove(mor)
                                            except:
                                                continue
				        new = vocab_item(morph,old[1].exponent.phon+pands[0][i],'p',[])
			                vocab[morph].append(new)
				        pands[0][i-1] = (morph,new)
				    del pands[0][i]
			        else:
				    i = i + 1
			    except:
				break
			i = len(pands[1])-1
                        while i >= 0:
			    try:
                                if not isinstance(pands[1][i],tuple):
                                    if i != 0:
                                        while not isinstance(pands[1][i-1],tuple):
                                            pands[1][i] = pands[1][i-1] + pands[1][i]
                                            del pands[1][i-1]
                                        old = pands[1][i-1]
					morph = old[0]
					oldnum = vocab[morph].index(old[1])
                                        try:
                                            vocab[morph][oldnum].context.remove(word.morphology['ROOT'])
                                        except:
                                            pass
                                        for mor in word.morphology['OTHER']:
                                            try:
                                                vocab[mor][oldnum].context.remove(mor)
                                            except:
                                                continue
                                        new = vocab_item(morph,old[1].exponent.phon+pands[1][i],'s',[])
                                        vocab[morph].append(new)
                                        pands[1][i-1] = (morph,new)
                                    else:
                                        old = pands[1][i+1]
                                        morph = old[0]
					oldnum = vocab[morph].index(old[1])
                                        try:
                                            vocab[morph][oldnum].context.remove(word.morphology['ROOT'])
                                        except:
                                            pass
                                        for mor in word.morphology['OTHER']:
                                            try:
                                                vocab[mor][oldnum].context.remove(mor)
                                            except:
                                                continue
                                        new = vocab_item(morph,pands[1][i]+old[1].exponent.phon,'s',[])
                                        vocab[morph].append(new)
                                        pands[1][i+1] = (morph,new)
                                    del pands[1][i]
                                i = i - 1
			    except IndexError:
			        break
			context = word.morphology['ROOT']
                        for i in range(len(pands[0])-1,-1,-1):
                            if isinstance(pands[0][i],tuple):
                                morph = pands[0][i][0]
				itemnum = vocab[morph].index(pands[0][i][1])
                                if context not in vocab[morph][itemnum].context:
                                    vocab[morph][itemnum].context.append(context)
                                context = morph
                        context = word.morphology['ROOT']
                        for i in range(len(pands[1])):
                            if isinstance(pands[1][i],tuple):
                                morph = pands[1][i][0]
				itemnum = vocab[morph].index(pands[1][i][1])
                                if context not in vocab[morph][itemnum].context:
                                    vocab[morph][itemnum].context.append(context)
                                context = morph
	#Clean up and iterate printout
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
	    if iteration > 2:
	        raw_input('To continue press any button...')
    if not iterate:
        iteration = iteration + 1
    if output:
        print 'Iteration #' + str(iteration)
        for root in roots.keys():
	    print root + ': ' + ''.join([IPA[c] for c in roots[root]])
        for key in vocab.keys():
	    print '\n' + key + ':'
	    for item in vocab[key]:
	        print 'Exponent Phonology: ' + ''.join([IPA[c] for c in item.exponent.phon])
	        print 'Exponent Side: ' + item.exponent.side
	        print 'Context: ' + str(item.context)
    return iteration
