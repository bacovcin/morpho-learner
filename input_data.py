from size_sort import *
from Comb import *
from itertools import repeat
from Phonology import *
from random import randint

class word(object):
    def __init__(self,phon,morph):
        self.phonology = phon           #list of segments with features
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
    def __init__(self, length, phon, nat, exponrat):
        self.vlength = length         #weight of the list length penalty
        self.phon = phon              #weight of the phonology vs. allomorphy 
        self.natural = nat            #maximum number of feature changes in a 'natural' change
	self.erat = exponrat	      #percentage of forms that need to share an exponent for it to be used

class model(object):
    def __init__(self, vocab, mprules):
        self.vocab = vocab
        self.mprules = mprules

def Dictionaryify(input):
    lexicon = {} 
    for word in input:
        for morph in word.morphology:
            try:
                lexicon[morph[0]][morph[1]].append(word)
            except:
                try:
                    lexicon[morph[0]][morph[1]] = [word]
                except:
                    lexicon[morph[0]] = {morph[1]:[word]}
    return lexicon

def find_common_substring(word_list):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    long_string = ""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string

    result = ''
    for j in range(len(long_string)):
        for i in range(len(long_string),-1,-1):
            if len(long_string[j:i]) > len(result):
                if is_common_substr(long_string[j:i],word_list):
                    result = long_string[j:i]
    return result

def find_common_prefix(word_list):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
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
    is_common_substr = lambda s, strings: all(s in x for x in strings)
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

def create_mp_model(model,lexicon,setting):
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
		    print 'Starting Report:'
		    print morph
		    print 'Suffix'
                    raw_input([x.phonology for x in words])
		    shortlen = 100
		    for word in words:
			if len(word.phonology) < shortlen:
				shortlen = len(word.phonology)
		    for j in range(-shortlen-1,0,1):
			possible_suffixes = {}
			for word in words:
			    try:
			        possible_suffixes[word.phonology[j:]][0] = possible_suffixes[word.phonology[j:]][0] + 1
				possible_suffixes[word.phonology[j:]][1].append(word.morphology)
			    except:
				possible_suffixes[word.phonology[j:]] = [1,[word.morphology]]
			similarityInx = 0
			suffixList = []
			for key in possible_suffixes:
			    if possible_suffixes[key][0] > similarityInx:
				similarityInx = possible_suffixes[key][0]
				suffixList = [key]
			    elif possible_suffixes[key][0] == similarityInx:
                                suffixList.append(key)
			if float(similarityInx)/float(len(words)) < setting.erat:
			    continue
			elif len(suffixList) > 1:
			    suffix = suffixList[randint(0,len(suffixList)-1)]
			    break
			else:
			    suffix = suffixList[0]
			    break
		    else:
			testModel[morph]['s'] = [['',[y for x in possible_suffixes for y in possible_suffixes[x][1:]]]]
			vocab[i].append(vocab_item(morph,'','s',list(subSet)))
			continue
		    suffix_pairs = set([(suffix,y) for y in possible_suffixes if y != suffix])
		    testModel[morph]['s'] = [[suffix,possible_suffixes[suffix][1]]]
		    vocab[i].append(vocab_item(morph,suffix,'s',list(subSet)))
		    for pair in suffix_pairs:
		        a = PhonParse(pair[0])
		        b = PhonParse(pair[1])
		        phonOut = r''
		        for i in range(len(a)):
		            if len(featureDifference(a[i], b[i])) <= setting.natural:
				print b[i]
				print IPAword([b[i]])[0]
			        phonOut = phonOut + IPAword([b[i]])[0]
			    else:
			        phonOut = r''
			testModel[morph]['s'].append([phonOut,possible_suffixes[pair[1]][1]])
                for subSet in list(x for x in pSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    print 'Starting Report:'
		    print morph
		    print 'Prefix'
                    raw_input([x.phonology for x in words])
		    shortlen = 100
		    for word in words:
			if len(word.phonology) < shortlen:
				shortlen = len(word.phonology)
		    for j in range(shortlen,0,-1):
			possible_prefixes = {}
			for word in words:
			    try:
			        possible_prefixes[word.phonology[:j]][0] = possible_prefixes[word.phonology[:j]][0] + 1
				possible_prefixes[word.phonology[:j]][1].append(word.morphology)
			    except:
				possible_prefixes[word.phonology[:j]] = [1,[word.morphology]]
			similarityInx = 0
			prefixList = []
			for key in possible_prefixes:
			    if possible_prefixes[key][0] > similarityInx:
				similarityInx = possible_prefixes[key][0]
				prefixList = [key]
			    elif possible_prefixes[key][0] == similarityInx:
                                prefixList.append(key)
			if float(similarityInx)/float(len(words)) < setting.erat:
			    continue
			elif len(prefixList) > 1:
			    prefix = prefixList[randint(0,len(prefixList)-1)]
			    break
			else:
			    prefix = prefixList[0]
			    break
		    else:
                        testModel[morph]['p'] = [[r'',[y for x in possible_prefixes for y in possible_prefixes[x][1:]]]]
			vocab[i].append(vocab_item(morph,'','p',list(subSet)))
                        continue	
		    prefix_pairs = set([(prefix,y) for y in possible_prefixes if y != prefix])
  		    testModel[morph]['p'] = [[prefix,possible_prefixes[prefix][1]]]
		    vocab[i].append(vocab_item(morph,prefix,'p',list(subSet)))
		    for pair in prefix_pairs:
		        a = PhonParse(pair[0])
		        b = PhonParse(pair[1])
	                phonOut = r''
		        for i in range(len(a)):
		            if len(featureDifference(a[i], b[i])) <= setting.natural:
			        phonOut = phonOut + IPAword([b[i]])
			    else:
			        phonOut = r''
			testModel[morph]['p'].append([phonOut,possible_prefixes[pair[1]][1]])
	    elif i > 0:
                for subSet in list(x for x in sSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    wordList = []
                    for word in words:
                        curPhon = word.phonology
                        for j in range(len(word.morphology)-1,i,-1):
                            aMorph = word.morphology[j][1]
                            for side in testModel[aMorph]:
                                for expon in testModel[aMorph][side]:
                                    if word.morphology in expon[1]:
                                        if expon[0] == '':
                                            pass
                                        elif side == 's':
                                            curPhon = expon[0].join(curPhon.split(expon[0])[:-1])
                                        elif side == 'p':
                                            curPhon = expon[0].join(curPhon.split(expon[0])[1:])
                        wordList.append((curPhon,word.morphology))
		    print 'Starting Report:'
		    print morph
		    print 'Suffix'
                    raw_input([x.phonology for x in words])
		    shortlen = 100
		    for word in wordList:
			if len(word[0]) < shortlen:
				shortlen = len(word[0])
		    for j in range(-shortlen-1,0,1):
			possible_suffixes = {}
			for word in wordList:
			    try:
			        possible_suffixes[word[0][j:]][0] = possible_suffixes[word[0][j:]][0] + 1
				possible_suffixes[word[0][j:]][1].append(word[1])
			    except:
				possible_suffixes[word[0][j:]] = [1,[word[1]]]
			similarityInx = 0
			suffixList = []
			for key in possible_suffixes:
			    if possible_suffixes[key][0] > similarityInx:
				similarityInx = possible_suffixes[key][0]
				suffixList = [key]
			    elif possible_suffixes[key][0] == similarityInx:
                                suffixList.append(key)
			if float(similarityInx)/float(len(words)) < setting.erat:
			    continue
			elif len(suffixList) > 1:
			    suffix = suffixList[randint(0,len(suffixList)-1)]
			else:
			    suffix = suffixList[0]
		    else:
                        testModel[morph]['s'] = [['',[y for x in possible_suffixes for y in possible_suffixes[x]]]]
			vocab[i].append(vocab_item(morph,'','s',list(subSet)))
                        continue
   		    suffix_pairs = set([(suffix,y) for y in possible_suffixes if y != suffix])
		    testModel[morph]['s']= [[suffix,possible_suffixes[suffix][1]]]
		    vocab[i].append(vocab_item(morph,suffix,'s',list(subSet)))
	  	    for pair in suffix_pairs:
		        a = PhonParse(pair[0])
		        b = PhonParse(pair[1])
		        phonOut = r''
		        for i in range(len(a)):
		            if len(featureDifference(a[i], b[i])) <= setting.natural:
			        phonOut = phonOut + IPAword([b[i]])
			    else:
			        phonOut = r''
			testModel[morph]['s'].append([phonOut,possible_suffixes[pair[1]][1]])
                for subSet in list(x for x in pSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    wordList = []
		    for word in words:
                        curPhon = word.phonology
                        for j in range(len(word.morphology)-1,i,-1):
                            aMorph = word.morphology[j][1]
                            for side in testModel[aMorph]:
                                for expon in testModel[aMorph][side]:
                                    if word.morphology in expon[1]:
                                        if expon[0] == '':
                                            pass
                                        elif side == 's':
                                            curPhon = expon[0].join(curPhon.split(expon[0])[:-1])
                                        elif side == 'p':
                                            curPhon = expon[0].join(curPhon.split(expon[0])[1:])
                        wordList.append((curPhon,word.morphology))
		    print 'Starting Report:'
		    print morph
		    print 'Prefix'
                    raw_input([x.phonology for x in words])
		    shortlen = 100
		    for word in wordList:
			if len(word[0]) < shortlen:
				shortlen = len(word[0])
		    for i in range(shortlen,0,-1):
			possible_prefixes = {}
			for word in words:
			    try:
			        possible_prefixes[word[0][:j]][0] = possible_prefixes[word[0][:j]][0] + 1
				possible_prefixes[word[0][:j]][1].append(word[1])
			    except:
				possible_prefixes[word[0][:j]] = [1,[word[1]]]
			similarityInx = 0
			prefixList = []
			for key in possible_prefixes:
			    if possible_prefixes[key][0] > similarityInx:
				similarityInx = possible_prefixes[key][0]
				prefixList = [key]
			    elif possible_prefixes[key][0] == similarityInx:
                                prefixList.append(key)
			if float(similarityInx)/float(len(words)) < setting.erat:
			    continue
			elif len(prefixList) > 1:
			    prefix = prefixList[randint(0,len(prefixList)-1)]
			else:
			    prefix = prefixList[0]
		    else:
                        testModel[morph]['p'] = [['',[y for x in possible_suffixes for y in possible_suffixes[x]]]]
			vocab[i].append(vocab_item(morph,'','p',list(subSet)))
                        continue
		    prefix_pairs = set([(prefix,y) for y in possible_prefixes if y != prefix])
		    testModel[morph]['p'] = [[prefix,possible_prefixes[prefix][1]]]
		    vocab[i].append(vocab_item(morph,prefix,'p',list(subSet)))
		    for pair in prefix_pairs:
		        a = PhonParse(pair[0])
		        b = PhonParse(pair[1])
		        phonOut = r''
		        for i in range(len(a)):
		            if len(featureDifference(a[i], b[i])) <= setting.natural:
			        phonOut = phonOut + IPAword([b[i]])
			    else:
			        phonOut = r''
			testModel[morph]['p'].append([phonOut,possible_prefixes[pair[1]][1]])
	    elif i == 0:
                for subSet in list(x for x in bSet):
                    words = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
		    wordList = []
		    print testModel.keys()
		    for word in words:
			curPhon = word.phonology
			for j in range(len(word.morphology)-1,0,-1):
			    aMorph = word.morphology[j][1]
			    for side in testModel[aMorph]:
				for expon in testModel[aMorph][side]:
				    if word.morphology in expon[1]:
					if expon[0] == '':
					    pass
					elif side == 's':
					    curPhon = expon[0].join(curPhon.split(expon[0])[:-1])
					elif side == 'p':
					    curPhon = expon[0].join(curPhon.split(expon[0])[1:])
			wordList.append((curPhon,word.morphology))					    
		    print 'Starting Report:'
		    print morph
		    print 'Base'
                    raw_input([x[0] for x in wordList])
		    longlen = 0
		    roots = []
		    for word in wordList:
			if len(word[0]) > longlen:
			    longlen = len(word[0])
			    roots = [word[0]]
			elif len(word[0]) == longlen:
			    roots.append(word[0])
		    if len(roots) > 1:
			root = roots[randint(0,len(roots)-1)]
			testModel[morph]['b'] = [root,[x[1] for x in wordList]]
			vocab[i].append(vocab_item(morph,root,'b',list(subSet)))
		    else:
			testModel[morph]['b'] = [roots[0],[x[1] for x in wordList]]
			vocab[i].append(vocab_item(morph,roots[0],'b',list(subSet)))
    return vocab  

def add_mprules(model,lexicon,setting):
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
    workingModel = create_mp_model(model,lexicon,setting)
    problems = check_vocab(workingModel,lexicon)
    for problem in problems:
	print generateProcesses(PhonParse(problem[0]), PhonParse(problem[1]))
	mprules.append(rule)
    #for item in workingModel:
    #	print 'Morpheme: ' + item
    #	for side in workingModel[item]:
    #	    print 'Side: ' + side
    #	    print 'Exponent: ' + str(workingModel[item][side])
    raw_input()
    return model(list(y for x in workingModel for y in x),mprules)

def create_model_space(lexicon, ordering):
    listOfTypeModels = []
    for i in range(len(ordering)):
        type = ordering[i]
        listOfMorphs = []
        for morph in lexicon[type]:
	    print 'Morph: ' + morph
            setOfTriggers = set(frozenset(lexicon[y].keys())
                                for y in set(ordering) - set([type]))
	    trueSet = set()
            for x in set(product(set_combs(x) for x in setOfTriggers)):
                trueSet.add(frozenset(frozenset(z for a in y for z in a) for y in set(product(x))))
	    morphSet = []
	    if i == 0:
	        for x in trueSet:
		   morphSet.append([morph,(('b',x),('p',frozenset([])),('s',frozenset([])))])
	    else:
	        for x in trueSet:
		    for y in set_combs(x):
	                if len(y) == 1:
			    z = tuple(y)
			    morphSet.append((morph,(('b',frozenset([])),('p',z[0]),('s',frozenset([])))))
			    morphSet.append((morph,(('b',frozenset([])),('p',frozenset([])),('s',z[0]))))
			elif len(y) == 2:
			    z = tuple(y)
                            morphSet.append((morph,(('b',frozenset([])),('p',z[0]),('s',z[1]))))
                            morphSet.append((morph,(('b',frozenset([])),('p',z[1]),('s',z[0]))))
	    listOfMorphs.append(tuple(morphSet))
        listOfTypeModels.append(tuple(product([[type],tuple(product(listOfMorphs))])))
        try:
            i = i + 1
            print i
        except:
            i = 1
            print i
    outStart = tuple(product(listOfTypeModels))
    output = tuple(size_sort(outStart))
    return output

def check_vocab(vocab,lexicon):
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
                    return False
    return True

def build_models(modelSpace, lexicon, settings):
    models = []
    sucess = 0
    fail = 0
    compSize = -1
    while sucess == 0:
	compSize = compSize + 1
        for i in range(len(modelSpace[compSize])):
            curModel = modelSpace[compSize][i]
            vocab = []
            for j in range(len(curModel)):
                curMorphType = curModel[j]
                type = curMorphType[0]
                for k in range(len(curMorphType[1])):
                    curMorph = curMorphType[1][k]
                    bSet = curMorph[1][0][1]
		    pSet = curMorph[1][1][1]
		    sSet = curMorph[1][2][1]
                    morph = curMorph[0]
                    if j == 0:
                        for subSet in list(x for x in bSet):
                            #raw_input(curMorph[1][1])
                            words = [x.phonology for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
                            #print subSet
                            #print str(list(set(set([y[1] for y in x.morphology])-set([morph])) for x in lexicon[type][morph]))
                            #raw_input(words)
                            try:
                                vocab[j].append(vocab_item(morph,find_common_substring(words),'b',list(subSet)))
                            except:
                                vocab.append([vocab_item(morph,find_common_substring(words),'b',list(subSet))])
                    else:
                        vocab.append([])
                        for subSet in pSet:
                            fullWords = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(set(subSet))]
                            before = set([])
                            after = set([])
                            for word in fullWords:
                                morphs = tuple(y[1] for y in word.morphology)
                                phon = ''
                                for l in range(j):
                                    for item in vocab[l]:
                                        if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                                            if item.exponent.side == 'b':
                                                phon = item.exponent.phon
                                            elif item.exponent.side == 'p':
                                                phon = item.exponent.phon + phon
                                            elif item.exponent.side == 's':
                                                phon = phon + item.exponent.phon
                                try:
                                    splice = word.phonology.split(phon)
                                except:
                                    splice = [word.phonology,word.phonology]
                                before.add(splice[0])
                                after.add(phon.join(splice[1:]))
                            vocab[j].append(vocab_item(morph,find_common_prefix(before),'p',list(subSet)))
                        for subSet in sSet:
                            fullWords = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(set(subSet))]
                            before = set([])
                            after = set([])
                            for word in fullWords:
                                morphs = tuple(y[1] for y in word.morphology)
                                phon = ''
                                for l in range(j):
                                    for item in vocab[l]:
                                        if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                                            if item.exponent.side == 'b':
                                                phon = item.exponent.phon
                                            elif item.exponent.side == 'p':
                                                phon = item.exponent.phon + phon
                                            elif item.exponent.side == 's':
                                                phon = phon + item.exponent.phon
                                try:
                                    splice = word.phonology.split(phon)
                                except:
                                    splice = [word.phonology,word.phonology]
                                before.add(splice[0])
                                after.add(phon.join(splice[1:]))
                            vocab[j].append(vocab_item(morph,find_common_suffix(after),'s',list(subSet)))
                        #for key in vocab[j][-1].__dict__.keys():
                        #    if key == 'exponent':
                        #        for key2 in vocab[j][-1].exponent.__dict__.keys():
                        #            print vocab[j][-1].exponent.__dict__[key2]
                        #    else:
                        #        print vocab[j][-1].__dict__[key]
                        #raw_input(1)
            if check_vocab(vocab,lexicon):
                sucess = sucess + 1
                models.append(model(list(y for x in vocab for y in x),[]))
            else:
                fail = fail + 1
                models.append(add_mprules(curModel,lexicon,settings))
            print 'Section ' + str(compSize) + ' out of ' + str(len(modelSpace)) + ': ' +  str("%.2f" % ((float(i)/float(len(modelSpace[compSize])))*float(100))) + '% complete'
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
