from progressbar import *
from size_sort import *
from Comb import *
from itertools import repeat
from Phonology import *
from random import randint

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
    def __init__(self, length, phon, nat, exponnum):
        self.vlength = length         #weight of the list length penalty
        self.phon = phon              #weight of the phonology vs. allomorphy 
        self.natural = nat            #maximum number of feature changes in a 'natural' change
	self.erat = exponnum	      #minimum number of forms that need to share an exponent for it to be used

class model(object):
    def __init__(self, vocab, mprules):
        self.vocab = vocab
        self.mprules = mprules

def Dictionarify(input):
    lexicon = {} 
<<<<<<< HEAD
    orderings = []
=======
    orderings = {}
>>>>>>> experimental
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
<<<<<<< HEAD
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
=======
	cur_ord = orderings
	for order in ordering:
	    try:
		cur_ord = cur_ord[order]
	    except:
		cur_ord[order] = {}
		cur_ord = cur_ord[order]
    return (lexicon,orderings)
>>>>>>> experimental

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
    for i in range(len(model)-1,-1,-1):
	vocab.append([])
    for i in range(len(model)-1,-1,-1):
	curMorphType = model[i]
	type = curMorphType[0]
        for k in range(len(curMorphType[1])):
            curMorph = curMorphType[1][k]
            bSet = curMorph[1][0][1]
            pSet = curMorph[1][1][1]
            sSet = curMorph[1][2][1]
            morph = curMorph[0]
	    testModel[morph] = {}
	    if i == len(model)-1:
                for subSet in list(x for x in sSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    
		    if debug:
			print 'Starting Report:'
		    	print morph
		    	print 'Suffix'
                    	raw_input([IPAword(x.phonology) for x in words])
		    shortlen = 100
		    for w in words:
			if len(w.phonology) < shortlen:
				shortlen = len(w.phonology)
		    for j in range(-shortlen-1,0,1):
			possible_suffixes = {}
			for w in words:
			    try:
			        possible_suffixes[tuple(IPAword(w.phonology[j:]))][0] = possible_suffixes[tuple(IPAword(w.phonology[j:]))][0] + 1
				possible_suffixes[tuple(IPAword(w.phonology[j:]))][1].append(w.morphology)
			    except:
				possible_suffixes[tuple(IPAword(w.phonology[j:]))] = [1,[w.morphology]]
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
			    break
			else:
			    suffix = suffixList[0]
			    break
		    else:
			testModel[morph]['s'] = [[[],[y for x in possible_suffixes for y in possible_suffixes[x][1:]]]]
			vocab[i].append(vocab_item(morph,[],'s',list(subSet)))
			continue
		    suffix_pairs = set([(suffix,y) for y in possible_suffixes if y != suffix])
		    testModel[morph]['s'] = [[[IPA[c] for c in suffix],possible_suffixes[suffix][1]]]
		    vocab[i].append(vocab_item(morph,[IPA[c] for c in suffix],'s',list(subSet)))
		    for pair in suffix_pairs:
                        a = [IPA[c] for c in pair[0]]
                        b = [IPA[c] for c in pair[1]]		        
			phonOut = []
		        for j in range(len(a)):
		            if len(featureDifference(a[j], b[j])) <= setting.natural:
			        phonOut = phonOut + IPAword([b[j]])
			    else:
			        phonOut = []
			testModel[morph]['s'].append([[IPA[c] for c in phonOut],possible_suffixes[pair[1]][1]])
                for subSet in list(x for x in pSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    if debug:
		        print 'Starting Report:'
		        print morph
		        print 'Prefix'
                        raw_input([IPAword(x.phonology) for x in words])
		    shortlen = 100
		    for w in words:
			if len(w.phonology) < shortlen:
				shortlen = len(w.phonology)
		    for j in range(shortlen,0,-1):
			possible_prefixes = {}
			for w in words:
			    try:
			        possible_prefixes[tuple(IPAword(w.phonology[:j]))][0] = possible_prefixes[tuple(IPAword(w.phonology[:j]))][0] + 1
				possible_prefixes[tuple(IPAword(w.phonology[:j]))][1].append(w.morphology)
			    except:
				possible_prefixes[tuple(IPAword(w.phonology[:j]))] = [1,[w.morphology]]
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
			    break
			else:
			    prefix = prefixList[0]
			    break
		    else:
                        testModel[morph]['p'] = [[[],[y for x in possible_prefixes for y in possible_prefixes[x][1:]]]]
			vocab[i].append(vocab_item(morph,[],'p',list(subSet)))
                        continue
		    prefix_pairs = set([(prefix,y) for y in possible_prefixes if y != prefix])
  		    testModel[morph]['p'] = [[[IPA[c] for c in prefix],possible_prefixes[prefix][1]]]
		    vocab[i].append(vocab_item(morph,[IPA[c] for c in prefix],'p',list(subSet)))
		    for pair in prefix_pairs:
		        a = [IPA[c] for c in pair[0]]
		        b = [IPA[c] for c in pair[1]]
	                phonOut = []
		        for j in range(len(a)):
		            if len(featureDifference(a[j], b[j])) <= setting.natural:
			        phonOut = phonOut + IPAword([b[j]])
			    else:
			        phonOut = []
			testModel[morph]['p'].append([[IPA[c] for c in phonOut],possible_prefixes[pair[1]][1]])
	    elif i > 0:
                for subSet in list(x for x in sSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    wordList = []
                    for w in words:
                        curPhon = w.phonology
                        for j in range(len(w.morphology)-1,i,-1):
                            aMorph = w.morphology[j][1]
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
		    else:
                        testModel[morph]['s'] = [[[],[y for x in possible_suffixes for y in possible_suffixes[x]]]]
			vocab[i].append(vocab_item(morph,[],'s',list(subSet)))
                        continue
   		    suffix_pairs = set([(suffix,y) for y in possible_suffixes if y != suffix])
		    testModel[morph]['s']= [[[IPA[c] for c in suffix],possible_suffixes[suffix][1]]]
		    vocab[i].append(vocab_item(morph,[IPA[c] for c in suffix],'s',list(subSet)))
	  	    for pair in suffix_pairs:
                        a = [IPA[c] for c in pair[0]]
                        b = [IPA[c] for c in pair[1]]
		        phonOut = []
		        for j in range(len(a)):
		            if len(featureDifference(a[j], b[j])) <= setting.natural:
			        phonOut = phonOut + IPAword([b[j]])
			    else:
			        phonOut = []
			testModel[morph]['s'].append([[IPA[c] for c in phonOut],possible_suffixes[pair[1]][1]])
                for subSet in list(x for x in pSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    wordList = []
		    for w in words:
                        curPhon = w.phonology
                        for j in range(len(w.morphology)-1,i,-1):
                            aMorph = w.morphology[j][1]
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
		    else:
                        testModel[morph]['p'] = [[[],[y for x in possible_prefixes for y in possible_prefixes[x]]]]
			vocab[i].append(vocab_item(morph,[],'p',list(subSet)))
                        continue
		    prefix_pairs = set([(prefix,y) for y in possible_prefixes if y != prefix])
		    testModel[morph]['p'] = [[[IPA[c] for c in prefix],possible_prefixes[prefix][1]]]
		    vocab[i].append(vocab_item(morph,[IPA[c] for c in prefix],'p',list(subSet)))
		    for pair in prefix_pairs:
                        a = [IPA[c] for c in pair[0]]
                        b = [IPA[c] for c in pair[1]]
		        phonOut = []
		        for j in range(len(a)):
		            if len(featureDifference(a[j], b[j])) <= setting.natural:
			        phonOut = phonOut + IPAword([b[j]])
			    else:
			        phonOut = []
			testModel[morph]['p'].append([[IPA[c] for c in phonOut],possible_prefixes[pair[1]][1]])
	    elif i == 0:
                for subSet in list(x for x in bSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    wordList = []
		    for word in words:
			curPhon = word.phonology
			for j in range(len(word.morphology)-1,0,-1):
			    aMorph = word.morphology[j][1]
			    for side in testModel[aMorph]:
				for expon in testModel[aMorph][side]:
				    if word.morphology in expon[1]:
					if expon[0] == []:
					    pass
					elif side == 's':
					    if len(expon[0]) != 0:
						curPhon = curPhon[:-len(expon[0])]
					elif side == 'p':
					    if len(expon[0]) != 0:
                                                curPhon = curPhon[len(expon[0]):]
			wordList.append((curPhon,word.morphology))					    
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
			vocab[i].append(vocab_item(morph,[IPA[c] for c in root],'b',list(subSet)))
		    else:
			testModel[morph]['b'] = [[IPA[c] for c in roots[0]],[x[1] for x in wordList]]
			vocab[i].append(vocab_item(morph,[IPA[c] for c in roots[0]],'b',list(subSet)))
    return vocab  

def add_mprules(cModel,lexicon,setting,debug=True):
    '''adds morpho-phonological rules to models that fail to generate the data with only contextual allomorphy'''
    def check_vocab(vocab,lexicon):
	problems = []
        for type in lexicon.keys():
            for key in lexicon[type].keys():
                for word in lexicon[type][key]:
                    morphs = tuple(y[1] for y in word.morphology)
                    phonology = ''
		    item_list = []
                    for morph_list in vocab:
                        for item in morph_list:
                            if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                                if item.exponent.side == 'b':
                                    phonology = item.exponent.phon
                                elif item.exponent.side == 'p':
                                    phonology = item.exponent.phon + phonology
                                elif item.exponent.side == 's':
                                    phonology = phonology + item.exponent.phon
			        item_list.append(item)
                    if phonology != word.phonology:
                        problems.append((phonology,word.phonology))
        return problems
    mprules = []
    workingModel = create_mp_model(cModel,lexicon,setting,debug=True)
    problems = check_vocab(workingModel,lexicon)
    for problem in problems:
	print generateProcesses(problem[0], problem[1])
	#mprules.append(rule)
    old_model = list(y for x in workingModel for y in x)
    if debug:
         for item in old_model:
             print 'Morphological Feature: ' + str(item.morph_feature)
             print 'Phonology: ' + ''.join(IPAword(item.exponent.phon))
             print 'Side: ' + str(item.exponent.side)
             print 'Context: ' + str(item.context)
         raw_input('\n\n')
    new_model = model(old_model,mprules)
    return new_model

<<<<<<< HEAD
def create_model_space2(lexicon,ordering):
    morph_list = []
=======
def create_model_space(lexicon,ordering):
    listOfTypeModels = []
>>>>>>> experimental
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
    outStart = tuple(product_wbar(morph_list))
    output = tuple(size_sort(outStart))
    for x in output:
	for y in x:
	    print y
    raw_input()
    return output

def check_vocab(vocab,lexicon):
    for type in lexicon.keys():
        for key in lexicon[type].keys():
            for word in lexicon[type][key]:
                morphs = tuple(y[1] for y in word.morphology)
                phonology = []
		item_list = []
                for item in vocab:
                    if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                        if item.exponent.side == 'b':
                            phonology = item.exponent.phon
                        elif item.exponent.side == 'p':
                            phonology = item.exponent.phon + phonology
                        elif item.exponent.side == 's':
                            phonology = phonology + item.exponent.phon
			item_list.append(item)
                if phonology != word.phonology:
                    return False
    return True

def build_models(modelSpace, lexicon, settings, mp = True):
    models = []
    sucess = 0
    fail = 0
    compSize = -1
    while sucess == 0:
	compSize = compSize + 1
	widgets = ['Section ' + str(compSize) + ' out of ' + str(len(modelSpace)) + ': ',
                        Percentage(), ' ', Bar(marker=RotatingMarker()),' ', ETA()]
        try:
            pbar = ProgressBar(widgets=widgets,maxval=len(modelSpace[compSize])).start()
	except:
	    pbar = ProgressBar(widgets=widgets,maxval=1).start()
        for i in xrange(len(modelSpace[compSize])):
            curModel = modelSpace[compSize][i]
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
            if check_vocab(vocab,lexicon):
                sucess = sucess + 1
                models.append(model(vocab,[]))
            else:
                fail = fail + 1
		if mp:
                    models.append(add_mprules(curModel,lexicon,settings))
	    pbar.update(i+1)
    	pbar.finish()
    print 'Success: ' + str(sucess)
    print 'Fail: ' + str(fail)
    return models

def check_models(models,settings):
    "checks for the smallest model, and returns a list of the smallest models"
    for i in range(len(models)):
        model = models[i]
        try:
            if cur_len > (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon):
                cur_len = (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon)
        except:
            cur_len = (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon)
    smallest = []
    i = 0
    for i in range(len(models)):
        model = models[i]
        if (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon) == cur_len:
            i = i + 1
            smallest.append(model)
    print i
    return smallest
