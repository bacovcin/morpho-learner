from progressbar import *
from size_sort import *
from Comb import *
from itertools import repeat
from Phonology import *
from random import randint
from random import random

class word(object):
    def __init__(self,phon,morph):
        self.phonology = PhonParse(phon)#list of segments with features
        self.morphology = list(morph)   #ordered list of m-feature
                                        #sets  associated with word

class exponent(object):
        def __init__(self,phonology,side):
            self.phon = phonology       #phonology of exponent
            self.side = side            #adfix type [(p)refix,(s)uffix,(b)ase]
            

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

def DictToTuple(adict):
    nl = []
    for key in adict:
	nl.append((key,adict[key]))
    return tuple(sorted(nl))

def Dictionaryify(input):
    lexicon = {} 
    orderings = []
    for word in input:
        ordering = []
        for morph in word.morphology:
	    ordering.append(morph[0])
            try:
                lexicon[morph[0]][morph[1]].append(word)
            except:
                try:
                    lexicon[morph[0]][morph[1]] = [word]
                except:
                    lexicon[morph[0]] = {morph[1]:[word]}
	for i in range(len(ordering)):
	    try:
		orderings[i].add(ordering[i])
	    except:
		def ord_app(orderings,i,ordering):
		    orderings.append(set([]))
		    try:
	                orderings[i].add(ordering[i])
        	    except:
			ord_app(orderings,i,ordering)
		    return orderings
		ord_app(orderings,i,ordering)
    return (lexicon,[tuple(x) for x in orderings])

def find_common_substring(word_list):
    is_common_substr = lambda s, strings: all(''.join(s) in ''.join(x) for x in strings)
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

def find_common_prefix(word_list):
    is_common_substr = lambda s, strings: all(''.join(s) in ''.join(x) for x in strings)
    long_string = ""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string

    result = ''
    i = len(long_string)
    for j in range(len(long_string)):
        if len(long_string[j:i]) > len(result):
            if is_common_substr(long_string[j:i],word_list):
                result = long_string[j:i]
    return result

def find_common_suffix(word_list):
    is_common_substr = lambda s, strings: all(''.join(s) in ''.join(x) for x in strings)
    long_string = ""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string
    result = ''
    j = 0
    for i in range(len(long_string),-1,-1):
        if len(long_string[j:i]) > len(result):
            if is_common_substr(long_string[j:i],word_list):
                result = long_string[j:i]
    return result

def create_mp_model(model,lexicon,setting,debug = False):
    '''adds morpho-phonological rules to models that fail to generate the data with only contextual allomorphy'''
    testModel = {}
    vocab = []
    for k in range(len(model)-1,-1,-1):
        curMorph = model[k]
        bSet = curMorph[1][0][1]
        pSet = curMorph[1][1][1]
        sSet = curMorph[1][2][1]
        morph = curMorph[0]
        testModel[morph] = {}
        for subSet in list(x for x in sSet):
            words = subSet
	    context =  set([y[1] for x in subSet for y in x.morphology])-set([morph])
	    wordList = []
            for w in words:
                curPhon = w.phonology
                for j in range(len(w.morphology)-1,-1,-1):
                    aMorph = w.morphology[j][1]
		    try:
                        for side in testModel[aMorph]:
                            for expon in testModel[aMorph][side]:
                                if w.morphology in expon[1]:
                                    if expon[0] == '':
                                        pass
				    elif side == 's':
                                        if len(expon[0]) != 0:
                                            curPhon = curPhon[:-len(expon[0])]
                                    elif side == 'p':
                                        if len(expon[0]) != 0:
                                            curPhon = curPhon[len(expon[0]):]
		    except:
			break
                wordList.append((curPhon,w.morphology))
	    if debug:
	        print 'Starting Report:'
	        print morph
		print 'Suffix'
                raw_input([IPAword(x.phonology) for x in words])
 	    shortlen = 100
	    for w in wordList:
	        if len(w[0]) < shortlen:
	            shortlen = len(w[0])
	    for j in range(-shortlen-1,0,1):
	 	possible_suffixes = {}
		for w in wordList:
		    try:
		        possible_suffixes[tuple(IPAword(w[0][j:]))][0] = possible_suffixes[tuple(IPAword(w[0][j:]))][0] + 1
			possible_suffixes[tuple(IPAword(w[0][j:]))][1].append(w[1])
		    except:
			possible_suffixes[tuple(IPAword(w[0][j:]))] = [1,[w[1]]]
		similarityInx = 0
		suffixList = []
		for key in possible_suffixes:
		    if possible_suffixes[key][0] > similarityInx:
			similarityInx = possible_suffixes[key][0]
			suffixList = [key]
		    elif possible_suffixes[key][0] == similarityInx:
                        suffixList.append(key)
		if similarityInx < setting.erat:
		    continue
		elif len(suffixList) > 1:
		    suffix = suffixList[randint(0,len(suffixList)-1)]
	        else:
	            suffix = suffixList[0]
		break
	    else:
                testModel[morph]['s'] = [[[],[y for x in possible_suffixes for y in possible_suffixes[x]]]]
		vocab.append(vocab_item(morph,[],'s',list(context)))
                continue
            suffix_pairs = set([(suffix,y) for y in possible_suffixes if y != suffix])
	    testModel[morph]['s']= [[[IPA[c] for c in suffix],possible_suffixes[suffix][1]]]
	    vocab.append(vocab_item(morph,[IPA[c] for c in suffix],'s',list(context)))
	    for pair in suffix_pairs:
                a = [IPA[c] for c in pair[0]]
                b = [IPA[c] for c in pair[1]]
	        phonOut = []
	        for j in range(len(a)):
	            if featureDifference(a[j], b[j]) <= setting.natural:
		        phonOut = phonOut + IPAword([b[j]])
		    else:
		        phonOut = []
		testModel[morph]['s'].append([[IPA[c] for c in phonOut],possible_suffixes[pair[1]][1]])
        for subSet in list(x for x in pSet):
            words = subSet
	    context = set([y[1] for x in subSet for y in x.morphology])-set([morph])
            wordList = []
	    for w in words:
                curPhon = w.phonology
                for j in range(len(w.morphology)-1,-1,-1):
                    aMorph = w.morphology[j][1]
                    try:
                        for side in testModel[aMorph]:
                            for expon in testModel[aMorph][side]:
                                if w.morphology in expon[1]:
                                    if expon[0] == '':
                                        pass
                                    elif side == 's':
                                        if len(expon[0]) != 0:
                                            curPhon = curPhon[:-len(expon[0])]
                                    elif side == 'p':
                                        if len(expon[0]) != 0:
                                            curPhon = curPhon[len(expon[0]):]
                    except:
                        break
                wordList.append((curPhon,w.morphology))      
	    if debug:
	        print 'Starting Report:'
	        print morph
	        print 'Prefix'
                raw_input([IPAword(x.phonology) for x in words])
	    shortlen = 100
	    for w in wordList:
		if len(w[0]) < shortlen:
	   	    shortlen = len(w[0])
	    for j in range(shortlen,0,-1):
		possible_prefixes = {}
		for w in wordList:
		    try:
		        possible_prefixes[tuple(IPAword(w[0][:j]))][0] = possible_prefixes[tuple(IPAword(w[0][:j]))][0] + 1
			possible_prefixes[tuple(IPAword(w[0][:j]))][1].append(w[1])
		    except:
			possible_prefixes[tuple(IPAword(w[0][:j]))] = [1,[w[1]]]
		similarityInx = 0
		prefixList = []
		for key in possible_prefixes:
		    if possible_prefixes[key][0] > similarityInx:
			similarityInx = possible_prefixes[key][0]
			prefixList = [key]
		    elif possible_prefixes[key][0] == similarityInx:
                        prefixList.append(key)
		if similarityInx < setting.erat:
		    continue
		elif len(prefixList) > 1:
		    prefix = prefixList[randint(0,len(prefixList)-1)]
		else:
		    prefix = prefixList[0]
		break
	    else:
                testModel[morph]['p'] = [[[],[y for x in possible_prefixes for y in possible_prefixes[x]]]]
		vocab.append(vocab_item(morph,[],'p',list(context)))
                continue
	    prefix_pairs = set([(prefix,y) for y in possible_prefixes if y != prefix])
	    testModel[morph]['p'] = [[[IPA[c] for c in prefix],possible_prefixes[prefix][1]]]
	    vocab.append(vocab_item(morph,[IPA[c] for c in prefix],'p',list(context)))
	    for pair in prefix_pairs:
                a = [IPA[c] for c in pair[0]]
                b = [IPA[c] for c in pair[1]]
	        phonOut = []
	        for j in range(len(a)):
	            if featureDifference(a[j], b[j]) <= setting.natural:
		        phonOut = phonOut + IPAword([b[j]])
		    else:
		        phonOut = []
		testModel[morph]['p'].append([[IPA[c] for c in phonOut],possible_prefixes[pair[1]][1]])
        for subSet in list(x for x in bSet):
            words = subSet
            context = set([y[1] for x in subSet for y in x.morphology])-set([morph])
	    wordList = []
	    for w in words:
                curPhon = w.phonology
                for j in range(len(w.morphology)-1,-1,-1):
                    aMorph = w.morphology[j][1]
                    try:
                        for side in testModel[aMorph]:
                            for expon in testModel[aMorph][side]:
                                if w.morphology in expon[1]:
                                    if expon[0] == '':
                                        pass
                                    elif side == 's':
                                        if len(expon[0]) != 0:
                                            curPhon = curPhon[:-len(expon[0])]
                                    elif side == 'p':
                                        if len(expon[0]) != 0:
                                            curPhon = curPhon[len(expon[0]):]
                    except:
                        break
                wordList.append((curPhon,w.morphology))	    
	    if debug:
	        print 'Starting Report:'
	        print morph
	        print 'Base'
                raw_input([IPAword(x[0]) for x in wordList])
	    count = 0
	    roots = []
	    wordList_p = [tuple(IPAword(x[0])) for x in wordList]
	    for word in set(wordList_p):
		if wordList_p.count(word) > count:
		    count = wordList_p.count(word)
		    roots = [word]
		elif wordList_p.count(word) == count:
		    roots.append(word)
	    if len(roots) > 1:
		root = roots[randint(-1,len(roots)-1)]
		testModel[morph]['b'] = [[IPA[c] for c in root],[x[1] for x in wordList]]
		vocab.append(vocab_item(morph,[IPA[c] for c in root],'b',list(context)))
	    else:
		testModel[morph]['b'] = [[IPA[c] for c in roots[0]],[x[1] for x in wordList]]
		vocab.append(vocab_item(morph,[IPA[c] for c in roots[0]],'b',list(context)))
    return vocab  

def add_mprules(cModel,lexicon,setting,debug=True):
    '''adds morpho-phonological rules to models that fail to generate the data with only contextual allomorphy'''
    mprules = []
    workingModel = create_mp_model(cModel,lexicon,setting,debug=False)
    problems = check_vocab(workingModel,lexicon)
    for problem in problems:
	#print 'Problem: ' + str(problem)i
	processes = generateProcesses([IPA[c] for c in problem[0]], [IPA[c] for c in problem[1]],debug=False)
	for i in range(len(processes)):
	    for loc in processes[i][2]:
		try:
		    nloc = frozenset(loc[:3]+[DictToTuple(loc[3])])
		except:
		    nloc = frozenset(loc)
		try:
		    key = (processes[i][0],IPA[processes[i][1]])
		except:
		    key = (processes[i][0],processes[i][1])
		try:
		    mprules[i][key].append(nloc)
		except:
		    try:
			mprules[i][key] = [nloc]
		    except:
			mprules.append({})
			mprules[i][key] = [nloc]
    print 'Simplifying Rules:\n'
    for i in range(len(mprules)):
	print mprules[i]
	for key in mprules[i]:
	    print key
	    new = []
	    for loc in set(mprules[i][key]):
		new.append((mprules[i][key].count(loc),loc))
	    raw_input(sorted(new)[-1]) 
    raw_input()    
    old_model = list(workingModel)
    if debug:
        for item in old_model:
            print 'Morphological Feature: ' + str(item.morph_feature)
            print 'Phonology: ' + ''.join(IPAword(item.exponent.phon))
            print 'Side: ' + str(item.exponent.side)
            print 'Context: ' + str(item.context)
        raw_input('\n\n')
    new_model = model(old_model,mprules)
    return new_model

def create_model_space(lexicon,ordering):
    morph_list = []
    for i in range(len(ordering)):
	cur_order = ordering[i]
	for cur_type in cur_order:
	    for cur_morph in lexicon[cur_type].keys():
		comb = set_combs(set(lexicon[cur_type][cur_morph]))
		morphSet = []
		if i == 0:
		    for x in comb:
   		        morphSet.append([cur_morph,(('b',x),('p',frozenset([])),('s',frozenset([])))])
		else:
		    for x in comb:
			for y in set_combs(x):
			    if len(y) == 1:
                                z = tuple(y)
				morphSet.append((cur_morph,(('b',frozenset([])),('p',frozenset([])),('s',z[0]))))
                                morphSet.append((cur_morph,(('b',frozenset([])),('p',z[0]),('s',frozenset([])))))
                            elif len(y) == 2:
                                z = tuple(y)
                                morphSet.append((cur_morph,(('b',frozenset([])),('p',z[0]),('s',z[1]))))
                                morphSet.append((cur_morph,(('b',frozenset([])),('p',z[1]),('s',z[0]))))
	        morph_list.append(morphSet)
    output = morph_list
    return output

def check_vocab(vocab,lexicon):
        problems = set([])
        for type in lexicon.keys():
            for key in lexicon[type].keys():
                for word in lexicon[type][key]:
                    morphs = tuple(y[1] for y in word.morphology)
                    phonology = []
                    item_list = []
                    for morph in morphs:
                        for item in vocab:
                            if (item.morph_feature == morph) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                                if item.exponent.side == 'b':
                                    phonology = item.exponent.phon
                                elif item.exponent.side == 'p':
                                    phonology = item.exponent.phon + phonology
                                elif item.exponent.side == 's':
                                    phonology = phonology + item.exponent.phon
                                item_list.append(item)
                    if phonology != word.phonology:
                        problems.add((tuple(IPAword(phonology)),tuple(IPAword(word.phonology))))
        return problems

def build_model(curModel, lexicon):
    vocab = []
    for k in range(len(curModel)):
        curMorph = curModel[k]
        bSet = curMorph[1][0][1]
	pSet = curMorph[1][1][1]
    	sSet = curMorph[1][2][1]
        morph = curMorph[0]
        for subSet in list(x for x in bSet):
            words = [x.phonology for x in subSet]
	    context = set([y[1] for x in subSet for y in x.morphology])-set([morph])
            vocab.append(vocab_item(morph,[IPA[c] for c in find_common_substring([IPAword(x) for x in words])],'b',list(context)))
        for subSet in pSet:
            before = set([])
            after = set([])
	    context = set([y[1] for x in subSet for y in x.morphology])-set([morph])
            for word in subSet:
                morphs = tuple(y[1] for y in word.morphology)
                phon = []
                for item in vocab:
                    if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                        if item.exponent.side == 'b':
                            phon = item.exponent.phon
                        elif item.exponent.side == 'p':
                            phon = item.exponent.phon + phon
                        elif item.exponent.side == 's':
                            phon = phon + item.exponent.phon
                if phon != []:
                    splice_b = []
                    splice_a = []
                    store = []
                    found = 0
                    for l in range(len(word.phonology)):
                        x = word.phonology[l]
                        if found < len(phon):
                            if x == phon[found]:
                                store.append(x)
                                found = found + 1
                            else:
                                for y in store:
                                    splice_b.append(y)
                                found = 0
                                store = []
                                splice_b.append(x)
                        else:
                            splice_a.append(x)
                else:
                    splice_b = word.phonology
                    splice_a = word.phonology
                before.add(tuple(IPAword(splice_b)))
                after.add(tuple(IPAword(splice_a)))
	    vocab.append(vocab_item(morph,[IPA[c] for c in find_common_prefix(before)],'p',list(context)))
        for subSet in sSet:
            before = set([])
            after = set([])
	    context = set([y[1] for x in subSet for y in x.morphology])-set([morph])
            for word in subSet:
                morphs = tuple(y[1] for y in word.morphology)
                phon = ''
                for item in vocab:
                    if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                        if item.exponent.side == 'b':
                            phon = item.exponent.phon
                        elif item.exponent.side == 'p':
                            phon = item.exponent.phon + phon
                        elif item.exponent.side == 's':
                            phon = phon + item.exponent.phon
                if phon != []:
	            splice_b = []
                    splice_a = []
                    store = []
                    found = 0
                    for l in range(len(word.phonology)):
	                x = word.phonology[l]
	                if found < len(phon):
		            if x == phon[found]:
			        store.append(x)
		                found = found + 1
			    else:
                                for y in store:
		                    splice_b.append(y)
		                found = 0
                    	        store = []
		                splice_b.append(x)
			else:
			    splice_a.append(x)
		else:
                    splice_b = word.phonology
                    splice_a = word.phonology
                before.add(tuple(IPAword(splice_b)))
                after.add(tuple(IPAword(splice_a)))
            vocab.append(vocab_item(morph,[IPA[c] for c in find_common_suffix(after)],'s',list(context)))
    return vocab

def build_models(modelSpace, lexicon, settings, mp = True):
    chains = []
    for j in xrange(settings.chainnum):
	chains.append([])
        curModelShape = []
        for morph in modelSpace:
	    curModelShape.append(morph[randint(0,len(morph)-1)])
        curVocab = build_model(curModelShape,lexicon)
        curVocValue = len(check_vocab(curVocab,lexicon))
        if curVocValue > 0:
	    if mp == True:
	        curModel = add_mprules(curModelShape,lexicon,settings)
	        curValue = (len(curModel.vocab)*settings.vlength) + rule_eval(curModel.mprules)
	    else:
	        curModel = model(curVocab,[])
	        curValue = (len(curModel.vocab)*settings.vlength)+(curVocValue * 5)
        else:
	    curModel = model(curVocab,[])
	    curValue = (len(curModel.vocab)*settings.vlength)+(curVocValue * 5)
        widgets = ['Burning-in Chain ' + str(j + 1) + ': ',
                Percentage(), ' ', Bar(marker=RotatingMarker()),' ', ETA()]
        pbar = ProgressBar(widgets=widgets,maxval=settings.burnin).start()
        for i in range(settings.burnin):
	    newModelShape = curModelShape
	    while 1==1:
                changeMorph = randint(0,len(modelSpace)-1)
                typeComp = random()
	        option = list(newModelShape)
                option[changeMorph] = modelSpace[changeMorph][randint(0,len(modelSpace[changeMorph])-1)]
	        if option != newModelShape:
		    newModelShape = option
		    break
	    newVocab = build_model(newModelShape,lexicon)
            newVocValue = len(check_vocab(newVocab,lexicon))
	    newValue = 0
            for item in newVocab:
                if item.exponent.side == 'b':
                    newValue = newValue + 50*settings.vlength
                else:
                    newValue = newValue + 5*settings.vlength
            if newVocValue > 0:
                if mp == True:
                    newModel = add_mprules(newModelShape,lexicon,settings)
                    newValue = (len(newModel.vocab)*settings.vlength) + rule_eval(newModel.mprules)
                else:
                    newModel = model(newVocab,[])
                    newValue = newValue+(newVocValue * 50)
            else:
                newModel = model(newVocab,[])
                newValue = newValue+(newVocValue * 50)
            if (curValue >= newValue) or (.01*(random() < (float(newValue)/float(curValue)))):
	        curModelShape = newModelShape
	        curModel = newModel
	        curValue = newValue
	    pbar.update(i+1)
        pbar.finish()
        widgets = ['Running Chain ' + str(j + 1) + ': ',
                Percentage(), ' ', Bar(marker=RotatingMarker()),' ', ETA()]
        pbar = ProgressBar(widgets=widgets,maxval=settings.chainlen).start()
        for i in range(settings.chainlen):
	    newModelShape = curModelShape
	    while 1==1:
                changeMorph = randint(0,len(modelSpace)-1)
                typeComp = random()
                option = list(newModelShape)
                option[changeMorph] = modelSpace[changeMorph][randint(0,len(modelSpace[changeMorph])-1)]
                if option != newModelShape:
                    newModelShape = option
                    break
	    newVocab = build_model(newModelShape,lexicon)
            newVocValue = len(check_vocab(newVocab,lexicon))
	    newValue = 0
	    for item in newVocab:
	        if item.exponent.side == 'b':
		    newValue = newValue + 50*settings.vlength
	        else:
		    newValue = newValue + 5*settings.vlength
            if newVocValue > 0:
                if mp == True:
                    newModel = add_mprules(newModelShape,lexicon,settings)
                    newValue = (len(newModel.vocab)*settings.vlength) + rule_eval(newModel.mprules)
                else:
                    newModel = model(newVocab,[])
                    newValue = newValue+(newVocValue * 50)
            else:
                newModel = model(newVocab,[])
                newValue = newValue+(newVocValue * 50)
	    if (curValue >= newValue) or (random() < (.01*(float(newValue)/float(curValue)))):
	        curModelShape = newModelShape
	        curModel = newModel
	        curValue = newValue
	    chains[-1].append(curModel)
            pbar.update(i+1)
    pbar.finish()
    return chains
