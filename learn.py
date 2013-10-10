from progressbar import *
from Phonology import *
from random import *
from decimal import *
from RuleApplication import *
import sets
import copy

def weighted(weights):
    r = random()
    q = 0
    for i in range(len(weights)):
        q = q + weights[i]
        if r <= q:
            return i

def product(args):
    pools = map(tuple, args)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

class word(object):
    def __init__(self,phon,morph):
        self.phonology = PhonParse(phon)#list of segments with features
        self.morphology = morph   #dictionary containing the root and an ordered list of other m-features

class exponent(object):
    def __init__(self,phonology,side):
        self.phon = phonology       #phonology of exponent
        self.side = side            #adfix type [(p)refix,(s)uffix]
            
class vocab_item(object):
    def __init__(self,morph_features,phonology,side,context,rule):
        self.morph_features = morph_features       #m-feature to be spelled out
        self.exponent = exponent(phonology,side) #exponent and adfix status
        self.context = context                   #a dictionary linking contexts to their confidence values
        self.rule = rule			 #the rule applied by this vocab_item
        
class Settings(object):
    def __init__(self, insert, delete, skel, root, major, minor, sub, samplesize):
        self.insert = insert          #weight of the insertion penalty in morphophonology subsetting
        self.delete = delete	      #weight of the deletion penalty in morphophonologiy subsetting
        self.skel = skel              #weight of the penelty for skeletal feature changes in morphophonology subsetting
        self.root = root              #weight of the penelty for root feature changes in morphophonology subsetting
        self.major = major            #weight of the penelty for major feature changes in morphophonology subsetting
        self.minor = minor            #weight of the penelty for minor feature changes in morphophonology subsetting
        self.sub = sub                #weight of the subtraction penalty in allomorphy
        self.samplesize = samplesize

class Model(object):
    def __init__(self,settings):
        self.roots = {}
        self.linear = {} #Assigns each morpheme category a change of being a prefix for every prefix-suffix context
        self.vocab = {}
        self.settings = settings

def iterateOutput(model,word_list,iteration):
    print 'Iteration #' + str(iteration)
    for root in model.roots.keys():
        print root + ': ' + ''.join([IPA[c] for x in model.roots[root] for c in x[0]])
        for key in model.vocab.keys():
            print '\n' + key + ':'
            for item in model.vocab[key]:
                print 'Exponent Phonology: ' + ''.join([IPA[c] for c in item.exponent.phon])
                print 'Exponent Side: ' + item.exponent.side
                print 'Context: ' + str(item.context)
                print 'Rule: ' + str(item.rule)
    if iteration > 0:
        raw_input('To continue press any button...')
    return 

def isOrderedSubset(listb,lista):
    for i in range(len(lista)):
        for j in range(len(lista),i,-1):
            if listb == lista[i:j]:
                return True
    return False

def findCommonSubstring(root,word):
    word_list = [root.value,word]
    isCommonSubstr = lambda subword, words: all(isOrderedSubset(subword,x) for x in words)
    long_string = []
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string
    result = []
    for j in range(len(long_string)):
        for i in range(len(long_string),-1,-1):
            if len(long_string[j:i]) > len(result):
                if isCommonSubstr(long_string[j:i],word_list):
                    result = long_string[j:i]
    return result

def valueAlign(align,settings):
    value = 0
    for i in range(len(align[0])):
        if align[0][i] == '_':
            value = value + settings.insert
        elif align[1][i] == '_':
            value = value + settings.delete
        elif align[0][i] != align[1][i]:
            value = value + featureDifference(align[0][i],align[1][i],
                skel_weight = settings.skel,root_weight = settings.root,
                major_weight = settings.major,minor_weight = settings.minor)
    return value

def optimisePrefixPhon(phon1,phon2,settings,debug=False):
    align = StrAlign(phon1,phon2,deletion_weight = -10, addition_weight = -10, 
                    match_weight = 200,featurediff_weight = -5)
    alignSpace = []
    round_num = 0
    for i in range(len(align[0])+1):
        if debug:
            print 'Round: ' + str(round_num + 1)
            print ''.join(IPA[c] for c in align[0][i:])
            print ''.join(IPA[c] for c in align[1][i:])
        i_align = [align[0][i:],align[1][i:]]
        round_num += 1
        new_align = StrAlign([x for x in i_align[0] if x !='_'],
                            [x for x in i_align[1] if x !='_'],
                            deletion_weight = -10, addition_weight = -10,
                            match_weight = 200,featurediff_weight = -5)
        new_value = valueAlign(new_align,settings) + (i*settings.sub)
        if debug:
            print ''.join(IPA[c] for c in new_align[0])
            print ''.join(IPA[c] for c in new_align[1])
            print 'New_value: ' + str(new_value)
        alignSpace.append(new_value)
    cur_value = 0
    for i in range(len(alignSpace)):
        if debug:
            print 'i: ' + str(i)
            print 'cur_values: ' + str(cur_value)
            print 'value: ' + str(alignSpace[cur_value])
            print 'new_value: ' + str(alignSpace[i])
        if alignSpace[i] < alignSpace[cur_value]:
            cur_value = i
    output = [[x for x in align[0][cur_value:] if x != '_'],
            [x for x in align[1][cur_value:] if x != '_']]
    return output

def optimiseSuffixPhon(phon1,phon2,settings,debug=False):
    align = StrAlign(phon1,phon2,deletion_weight = -10, addition_weight = -10, match_weight = 200,featurediff_weight = -5)
    alignSpace = range(len(align[0]),-1,-1)
    round_num = 0
    for i in range(len(align[0]),-1,-1):
        if debug:
            print 'Round: ' + str(round_num+1)
            print ''.join(IPA[c] for c in align[0][:i])
            print ''.join(IPA[c] for c in align[1][:i])
        i_align = [align[0][:i],align[1][:i]]
        round_num += 1
        new_align = StrAlign([x for x in i_align[0] if x !='_'],
                            [x for x in i_align[1] if x !='_'],
                            deletion_weight = -10, addition_weight = -10, 
                            match_weight = 200,featurediff_weight = -5)
        new_value = valueAlign(new_align,settings) + ((len(align[0])-i)*settings.sub)
        if debug:
            print ''.join(IPA[c] for c in new_align[0])
            print ''.join(IPA[c] for c in new_align[1])
            print 'New_value: ' + str(new_value)
        alignSpace[i] = new_value
    cur_value = 0
    for i in range(len(alignSpace)):
        if debug:
            print 'i: ' + str(i)
            print 'cur_value: ' + str(cur_value)
            print 'value: ' + str(alignSpace[cur_value])
            print 'new_value: ' + str(alignSpace[i])
        if alignSpace[i] < alignSpace[cur_value]:
            cur_value = i
    output = [[x for x in align[0][:cur_value] if x != '_'],
            [x for x in align[1][:cur_value] if x != '_']]
    return output


def optimiseRootPhon(phon1,phon2,settings,debug=False):
    align = StrAlign(phon1,phon2,deletion_weight = -10, addition_weight = -10, match_weight = 200,featurediff_weight = -5)
    alignSpace = []
    round_num = 0
    for i in range(len(align[0])+1):
        if debug:
            print 'New prefix level'
            print ''.join(IPA[c] for c in align[0][i:])
            print ''.join(IPA[c] for c in align[1][i:])
        i_align = [align[0][i:],align[1][i:]]
        if i_align != [[],[]]:
            alignSpace.append([0]*len(i_align[0]))
            for j in range(len(i_align[0])-1,-1,-1):
                round_num += 1
                new_align = StrAlign([x for x in i_align[0][:j+1] if x !='_'],
                                [x for x in i_align[1][:j+1] if x !='_'],
                                deletion_weight = -10, addition_weight = -10,
                                match_weight = 200,featurediff_weight = -5)
                new_value = (valueAlign(new_align,settings) + 
                    (i*settings.sub)+((len(align[0][i:])-(j+1))*settings.sub))
                if debug:
                    print 'Round: ' + str(round_num)
                    print ''.join(IPA[c] for c in new_align[0])
                    print ''.join(IPA[c] for c in new_align[1])
                    print 'New_value: ' + str(new_value)
                alignSpace[i][j] = new_value
        else:
            round_num += 1
            if debug:
                print 'Round: ' + str(round_num)
                print 'New_value: ' + str(i*settings.sub)
            alignSpace.append([i*settings.sub])
    cur_values = [0,len(align[0])-1]
    for i in range(len(alignSpace)):
        for j in range(len(alignSpace[i])-1,-1,-1):
            if debug:
                print 'i: ' + str(i)
                print 'j: ' + str(j)
                print 'cur_values: ' + str(cur_values)
                print 'value: ' + str(alignSpace[cur_values[0]][cur_values[1]])
                print 'new_value: ' + str(alignSpace[i][j])
            if alignSpace[i][j] < alignSpace[cur_values[0]][cur_values[1]]:
                cur_values = [i,j]
    output = [[x for x in align[0][cur_values[0]:cur_values[0]+cur_values[1]+1]
                                                                if x != '_'],
            [x for x in align[1][cur_values[0]:cur_values[0]+cur_values[1]+1] 
                                                                if x != '_']]
    return output

def updateLinearization(model,line,context,side):
    if line not in model.linear.keys():
        if side == 'p':
            model.linear[line] = {context:0.6}
        else:
            model.linear[line] = {context:0.4}
    elif context not in model.linear[line].keys():
        if side == 'p':
            model.linear[line][context] = 0.6
        else:
            model.linear[line][context] = 0.4
    else:
        amount = uniform(0.03,0.07)
        if side == 'p':
            if model.linear[line][context] + amount >= 1.0:
                model.linear[line][context] = 1.0
            else:
                model.linear[line][context] = model.linear[line][context] + amount
        else:
            if model.linear[line][context] - amount <= 0.0:
                model.linear[line][context] = 0.0
            else:
                model.linear[line][context] = model.linear[line][context] - amount
    return model

def updateRootConfidence(model,root,phon):
    if phon not in [x[0] for x in model.roots[root]]:
        amount = 1.0/(len(model.roots[root])+1)
        for i in range(len(model.roots[root])):
            model.roots[root][i][1] = (model.roots[root][i][1]/1.0)*(1.0-amount)
        model.roots[root].append([phon,amount])
    else:
        amount = uniform(0.03,0.07)
        for i in range(len(model.roots[root])):
            if model.roots[root][i][0] == phon:
                if model.roots[root][i][1] + amount >= 1.0:
                    model.roots[root][i][1] = 1.0
                    model.roots[root] = [model.roots[root][i]]
                    break
                else:
                    model.roots[root][i][1] = model.roots[root][i][1] + 1.0
                    rvalue = model.roots[root][i][1]
                    for j in range(len(model.roots[root])):
                        if j != i:
                            cvalue = model.roots[root][j][1]
                            model.roots[root][j][1] = ((cvalue/(1.0-rvalue))*
                                                        (1.0-(rvalue+amount)))
    return model

def updateItemConfidence(model,item):
    def addNewItem(model,item):
        competitors = [x for x in model.vocab[rootmorph] 
                                if (x.exponent.side == item.exponent.side and
                                item.context in x.context.keys() and
                                x.morph_features == item.morph_features[1])]
        if len(competitors) == 0:
            newitem = vocab_item(item.morph_features[1],phon,item.exponent.side,
                                         {item.context:1.0},item.rule)
            model.vocab[rootmorph].append(newitem)
        else:
            total = float(sum([x.context[item.context] for x in competitors]))
            if total != 0:
                newitem = vocab_item(item.morph_features[1],phon,item.exponent.side,
                                         {item.context:float(total)/
                                        (float(len(competitors))+1)},item.rule)
                model.vocab[rootmorph].append(newitem)
                newtotal = total - float(total)/(float(len(competitors))+1)
                for comp in competitors:
                    comp.context[item.context] = (comp.context[item.context]/float(total))*newtotal
        return model
    phon = item.exponent.phon
    rootmorph = item.morph_features[0]
    if rootmorph not in model.vocab.keys():
        newitem = vocab_item(item.morph_features[1],phon,item.exponent.side,
                            {item.context:1.0},item.rule)
        model.vocab[rootmorph] = [newitem]
    else:
        contendors = [x for x in model.vocab[rootmorph] 
                if (x.exponent.phon == item.exponent.phon and
                x.exponent.side == item.exponent.side) and
                len(x.morph_features.intersection(item.morph_features[1])) != 0
                and x.rule == item.rule]
        if len(contendors) == 0:
            model = addNewItem(model,item)
        else:
            contendors = sorted(contendors,
                key=lambda self:len(x.morph_features.intersection(item.morph_features[1])))
            newrule = []
            for contendor in contendors:
                newrules = {}
                if len(contendor.rule) == len(item.rule):
                    break
                else:
                    rule_compat = 1
                    for i in range(len(contendor.rule)):
                        if contendor.rule[i] == item.rule[i]:
                            continue
                        else:
                            comp = set([(x, item.rule[i][2][0][3][x]) for x in item.rule[i][2][0][3]]).intersection(
                                set([(x, contendor.rule[i][2][0][3][x]) for x in contendor.rule[i][2][0][3]]))
                            if (contendor.rule[i][:2] == item.rule[i][:2] and 
                                contendor.rule[i][2][0][0] == 'rel' and 
                                item.rule[i][2][0][0] == 'rel' and
                                item.rule[i][2][0][2] == contendor.rule[i][2][0][2] and
                                len(comp) != 0):
                                if comp == contendor.rule[i][2][0][3]:
                                    continue
                                else:
                                    newdict = {}
                                    for x in comp:
                                        newdict[x[0]] = x[1]
                                    newrules[i] = newdict
                            else:
                                rule_compat = 0
                        if rule_compat == 1 and newrules == {}:
                            break
                        elif rule_compat == 1:
                            newrule = item.rule
                            for i in range(len(newrule)):
                                if i in newrules:
                                    newrule[i][2][0][3] = newrules[i]
                            model = addNewItem(model,item)
                            newitem = item
                            newitem[-1] = newrule
                            model = addNewItem(model,newitem)
                            return model
                        else:
                            continue
            else:
                model = addNewItem(model,item)
                return model
            competitors = [x for x in model.vocab[rootmorph] if (x.exponent.side == item.exponent.side and
                                                                 item.context in x.context.keys()) and
                                                                 contendor.morph_features.issubset(x.morph_features) and
                                                                x.morph_features - item.morph_features[1] == []]
            if contendor.morph_features == contendor.morph_features.intersection(item.morph_features[1]):
                competitors = [x for x in model.vocab[rootmorph] if (x.exponent.side == item.exponent.side and
                                                                     item.context in x.context.keys()) and
                                                                     contendor.morph_features.issubset(x.morph_features) and
                                                                     x.morph_features - item.morph_features[1] == []]
                total = float(sum([x.context[item.context] for x in competitors]))
                if item.context in contendor.context.keys():
                    amount = uniform(0.03,0.07)
                    if contendor.context[item.context] + amount > 1.0:
                        contendor.context[item.context] = 1.0
                        for competitor in competitors:
                            del(competitor.context[item.context])
                    else:
                        contendor.context[item.context] = contendor.context[item.context] + amount
                        newtotal = total - contendor.context[item.context]
                        for comp in competitors:
                            comp.context[item.context] = (comp.context[item.context]/total)*newtotal
                else:
                    contendor.context[item.context] = total/(float(len(competitors))+1)
                    newtotal = total - contendor.context[item.context]
                    for comp in competitors:
                        comp.context[item.context] = (comp.context[item.context]/total)*newtotal
            else:
                newmf = contendor.morph_features.intersection(item.morph_features[1])
                total = float(sum([x.context[item.context] for x in competitors]))
                newitem = vocab_item((rootmorph,newmf),phon,
                        item.exponent.side,item.context,
                        item.rule)
                model = addNewItem(model,newitem)
    return model


def testWord(model, word):
    root = word.morphology['ROOT']
    morphs = copy.deepcopy(word.morphology['OTHER'])
    items = []
    try:
        phon = model.roots[root][weighted([x[1] for x in model.roots[root]])]
        items.append((root,phon))
        pcontext = ('ROOT',root)
        scontext = ('ROOT',root)
        for morph in morphs:
            if morph in model.linear.keys():
                linearchoices = [model.linear[morph][x] for x in model.linear[morph].keys() 
                                    if (x[0] == pcontext
                                    and x[1] == scontext)]
                if linearchoices == []:
                    linearchoices = [model.linear[morph][x] for x in model.linear[morph].keys()
                                                                    if (x[0][0] == pcontext[0]
                                                                    and x[1] == scontext)]
                if linearchoices == []:
                    linearchoices = [model.linear[morph][x] for x in model.linear[morph].keys()
                                                                    if (x[0] == pcontext
                                                                    and x[1][0] == scontext[0])]
                if linearchoices == []:
                    linearchoices = [model.linear[morph][x] for x in model.linear[morph].keys()
                                                                    if (x[0][0] == pcontext[0]
                                                                    and x[1][0] == scontext[0])]
                if linearchoices == []:
                    return False
            else:
                linearchoices = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                                                    for x in model.linear[m].keys()      
                                                    if (x[0] == pcontext
                                                        and x[1] == scontext)]
                if linearchoices == []:
                    linearchoices = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                                                        for x in model.linear[m].keys()
                                                        if (x[0][0] == pcontext[0]
                                                            and x[1] == scontext)]
                if linearchoices == []:
                    linearchoices = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                                                                for x in model.linear[m].keys()
                                                                    if (x[0] == pcontext
                                                                    and x[1][0] == scontext[0])]
                if linearchoices == []:
                    linearchoices = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                                                                for x in model.linear[m].keys()
                                                                    if (x[0][0] == pcontext[0]
                                                                    and x[1][0] == scontext[0])]
                if linearchoices == []:
                    return False
        pchance = float(sum(linearchoices))/float(len(linearchoices))
        rule = []
        icontext = []
        if random() >= pchance: #Greater than prefix-chance means suffix
            choiceset = [x for x in model.vocab[morph[0]] if (x.morph_features.issubset(morph[1])
                                                                  and x.exponent.side == 'p'
                                                                  and scontext in x.context.keys())]
            choiceset = sorted(choiceset, key= lambda self: -len(self.morph_features))
            if choiceset != []:
                choice = choiceset[weighted(x.context[scontext] for x in choiceset)]
            else:
                choiceset = [x for x in model.vocab[morph[0]] if (x.morph_features.issubset(morph[1])
                                                                  and x.exponent.side == 'p'
                                                                  and scontext[0] in [y[0] for y in  x.context.keys()])]
                choiceset = [x for x in sorted(choiceset, key= lambda self: -len(self.morph_features))]
                choicep = [(float(sum([y.context[x] for x in self.context.keys() if x[0] == scontext[0]]))/
                                float(len([y.context[x] for x in self.context.keys() if x[0] == scontext[0]]))) 
                                for y in choiceset]
                choice = choiceset[weighted(choicep)]
            icontext = scontext
            scontext = morph
            if choice.rule != []:
                rule = choice.rule
                phon = applyProcess(rule,phon)
            phon = phon + choice.exponent.phon
        else:
            choiceset = [x for x in model.vocab[morph[0]] if (x.morph_features.issubset(morph[1])
                                                                  and x.exponent.side == 's'
                                                                  and pcontext in x.context.keys())]
            choiceset = sorted(choiceset, key= lambda self: -len(self.morph_features))
            if choiceset != []:
                choice = choiceset[weighted(x.context[pcontext] for x in choiceset)]
            else:
                choiceset = [x for x in model.vocab[morph[0]] if (x.morph_features.issubset(morph[1])
                                                                  and x.exponent.side == 's'
                                                                  and pcontext[0] in [y[0] for y in  x.context.keys()])]
                choiceset = [x for x in sorted(choiceset, key= lambda self: -len(self.morph_features))]
                choicep = [(float(sum([y.context[x] for x in self.context.keys() if x[0] == scontext[0]]))/
                            float(len([y.context[x] for x in self.context.keys() if x[0] == scontext[0]])))
                                for y in choiceset]
                choice = choiceset[weighted(choicep)]
            icontext = pcontext
            pcontext = morph
            if choice.rule != []:
                rule = choice.rule
                phon = applyProcess(rule,phon)
            phon = choice.exponent.phon + phon
        items.append(vocab_item(vocab_item((morph[0],choice.morph_features),
                        choice.exponent.phon,choice.exponent.side,
                        icontext,rule)))
        if phon == word.phonology:
            model = updateRootConfidence(model,items[0][0],items[0][1])
            pcontext = items[0][0]
            scontext = items[0][0]
            for i in items[1:]:
                model = updateLinearization(model,i.morph_features,(pcontext,scontext),i.exponent.side)
                model = updateItemConfidence(model,i)
            return True
        else:
            return False
    except KeyError:
        return False
    return Error 

def testVocab(model, word_list, printout):
    test = [testWord(model,word) for word in word_list]
    if printout:
        print 'Words: ' + str([''.join(IPA[c] for c in word.phonology) for word in word_list])
        print 'Results: ' + str(test)
    return all(test)

def findPandS(word,subset):
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

def cleanModel(vocab):
    return vocab
    
def debugOutput(model,word):
    return

def nothingKnown(model,phon,root,morphs):
    model.roots[root] = [[phon,1.0]]
    linearizations = [[('ROOT',root)]]
    for morph in morphs:
        newlinearizations = []
        for line in linearizations:
            pcontext = line[0]
            scontext = line[-1]
            newlinearizations.append([morph]+line)
            newlinearizations.append(line+[morph])
            if morph not in model.linear.keys():
                model.linear[morph] = {}
            model.linear[morph][(pcontext,scontext)]=0.5
        linearizations = newlinearizations
    for line in linearizations:
        side = 'p'
        for i in range(len(line)):
            morph = line[i]
            if morph[0] != 'ROOT':
                if side == 'p':
                    newitem = vocab_item(morph,[],'p',line[i+1],[])
                    updateItemConfidence(model,newitem)
                else:
                    newitem = vocab_item(morph,[],'s',line[i-1],[])
                    updateItemConfidence(model,newitem)
            else:
                side = 's'
    return model

def rootUnknown(model,phon,root,morphs):
    return model

def rootKnown(model,phon,root,morphs):
    class linear(object):
        def __init__(self,line,p):
            self.line = line
            self.p = p
    class possible_analysis(object):
        def __init__(self,line,p,stem,rootstem,pphon,sphon,pcon,scon,pitems):
            self.line = line
            self.p = p
            self.stem = stem
            self.rootstem = rootstem
            self.pphon = pphon
            self.sphon = sphon
            self.pcon = pcon
            self.scon = scon
            self.pitems = pitems
    def generatePossibleAnalyses(model,cur_analysis,cur_morph,cur_side,rmorphs):
        output = []
        if cur_morph[0] in model.vocab.keys():
            cur_items = [x for x in model.vocab[cur_morph[0]] if (x.morph_features.issubset(cur_morph[1])
                                                                and x.exponent.side == cur_side)]
        else:
            cur_items = []
        if len(rmorphs) == 0:
            rules = createRuleSpace(generateProcesses(cur_analysis.rootstem,cur_analysis.stem))
            p = 0.5
            if cur_side == 'p':
                items = [x for x in cur_items if x.exponent.phon == cur_analysis.pphon]
                if items == []:
                    newitem = vocab_item(cur_morph,cur_analysis.pphon,cur_side,cur_analysis.pcon,rules)
                    output = [possible_analysis(cur_analysis.line,cur_analysis.p*p,
                                            cur_analysis.pphon+cur_analysis.stem,
                                            cur_analysis.pphon+cur_analysis.stem,
                                            [],
                                            cur_analysis.sphon,
                                            cur_morph,cur_analysis.scon,
                                            cur_analysis.pitems + [newitem])]
                else:
                    item = items[0]
                    if item != []:
                        con = cur_analysis.pcon
                        if con in item.context.keys():
                            p = item.context[con]
                        elif con[0] in [x[0] for x in item.context.keys()]:
                            values = [item.context[x] for x in item.context.keys() if x[0] == con[0]]
                            p = float(sum(values))/float(len(values))
                        else:
                            p = 1.0/float(len(cur_items))
                    newitem = vocab_item((cur_morph[0],item.morph_features),cur_analysis.pphon,cur_side,cur_analysis.pcon,rules)
                    output = [possible_analysis(cur_analysis.line,cur_analysis.p*p,
                                            cur_analysis.pphon+cur_analysis.stem,
                                            cur_analysis.pphon+cur_analysis.stem,
                                            [],
                                            cur_analysis.sphon,
                                            cur_morph,cur_analysis.scon,
                                            cur_analysis.pitems + [newitem])]
            else:
                items = [x for x in cur_items if x.exponent.phon == cur_analysis.sphon]
                if items == []:
                    newitem = vocab_item(cur_morph,cur_analysis.sphon,cur_side,cur_analysis.scon,rules)
                    output = [possible_analysis(cur_analysis.line,cur_analysis.p*p,
                                        cur_analysis.stem+cur_analysis.sphon,
                                        cur_analysis.stem+cur_analysis.sphon,
                                        cur_analysis.pphon,
                                        [],
                                        cur_morph,cur_analysis.scon,
                                        cur_analysis.pitems + [newitem])]
                else:
                    item = items[0]
                    if item != []:
                        con = cur_analysis.scon
                        if con in item.context.keys():
                            p = item.context[con]
                        elif con[0] in [x[0] for x in item.context.keys()]:
                            values = [item.context[x] for x in item.context.keys() if x[0] == con[0]]
                            p = float(sum(values))/float(len(values))
                        else:
                            p = 1.0/float(len(cur_items))
                    newitem = vocab_item((cur_morph[0],item.morph_features),cur_analysis.sphon,cur_side,cur_analysis.scon,rules)
                    output = [possible_analysis(cur_analysis.line,cur_analysis.p*p,
                                        cur_analysis.stem+cur_analysis.sphon,
                                        cur_analysis.stem+cur_analysis.sphon,
                                        cur_analysis.pphon,
                                        [],
                                        cur_morph,cur_analysis.scon,
                                        cur_analysis.pitems + [newitem])]
        else:
            if cur_items == []:
                p = [.7]
                if cur_side == 'p':
                    item = vocab_item(cur_morph,cur_analysis.pphon,'p',cur_analysis.pcon,createRuleSpace(generateProcesses(cur_analysis.rootstem,cur_analysis.stem)))
                else:
                    item = vocab_item(cur_morph,cur_analysis.sphon,'s',cur_analysis.scon,createRuleSpace(generateProcesses(cur_analysis.rootstem,cur_analysis.stem)))
                if item.exponent.phon == []:
                    p[-1] = p[-1]*0.7
                if cur_side == 'p':
                    output = output + generatePossibleAnalyses(model,
                                possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                    item.exponent.phon+cur_analysis.stem,
                                                    item.exponent.phon+cur_analysis.stem,
                                                    [],
                                                    cur_analysis.sphon,
                                                    cur_morph,cur_analysis.scon,
                                                    cur_analysis.pitems + [item]),
                                    rmorphs[0],cur_side,rmorphs[1:])
                else:
                    output = output + generatePossibleAnalyses(model,
                                    possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                    cur_analysis.stem+item.exponent.phon,
                                                    cur_analysis.stem+item.exponent.phon,
                                                    cur_analysis.pphon,
                                                    [],
                                                    cur_analysis.pcon,cur_morph,
                                                    cur_analysis.pitems + [item]),
                                    rmorphs[0],cur_side,rmorphs[1:])
            else:
                p = []
                for item in cur_items:
                    if cur_side == 'p':
                        con = cur_analysis.pcon
                    else:
                        con = cur_analysis.scon
                    if con in item.context.keys():
                        p.append(item.context[con])
                    elif con[0] in [x[0] for x in item.context.keys()]:
                        values = [item.context[x] for x in item.context.keys() if x[0] == con[0]]
                        p.append(float(sum(values))/float(len(values)))
                    else:
                        p.append(1.0/float(len(cur_items)))
                    if item.exponent.phon == []:
                        p[-1] = p[-1]*0.5
                    if cur_side == 'p':
                        phonopt = optimisePrefixPhon(cur_analysis.pphon,item.exponent.phon,model.settings)
                        context = cur_analysis.pcon
                    else:
                        phonopt = optimiseSuffixPhon(cur_analysis.sphon,item.exponent.phon,model.settings)
                        context = cur_analysis.scon
                    rules = createRuleSpace(generateProcesses(cur_analysis.rootstem,cur_analysis.stem))
                    if phonopt[0] == phonopt[1]:
                        newitem = vocab_item((cur_morph[0],item.morph_features),phonopt[0],cur_side,context,rules)
                        if cur_side == 'p':
                            output = output + generatePossibleAnalyses(model,
                                        possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                        phonopt[0]+cur_analysis.stem,
                                                        phonopt[0]+cur_analysis.stem,
                                                        cur_analysis.pphon[len(phonopt[0]):],
                                                        cur_analysis.sphon,
                                                        cur_morph,cur_analysis.scon,
                                                        cur_analysis.pitems + [newitem]),
                                        rmorphs[0],cur_side,rmorphs[1:])
                    else:
                        output = output + generatePossibleAnalyses(model,
                                        possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                        cur_analysis.stem+phonopt[0],
                                                        cur_analysis.stem+phonopt[0],
                                                        cur_analysis.pphon,
                                                        cur_analysis.sphon[:len(phonopt[0])],
                                                        cur_analysis.pcon,cur_morph,
                                                        cur_analysis.pitems + [newitem]),
                                        rmorphs[0],cur_side,rmorphs[1:])
                else:
                    try:
                        p[-1] = p[-1] * 0.5
                    except:
                        pass
                    newitem = vocab_item((cur_morph[0],item.morph_features),phonopt[0],cur_side,context,rules)
                    if cur_side == 'p':
                        output = output + generatePossibleAnalyses(model,
                                            possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                            phonopt[0]+cur_analysis.stem,
                                                            phonopt[0]+cur_analysis.stem,
                                                            cur_analysis.pphon[len(phonopt[0]):],
                                                            cur_analysis.sphon,
                                                            cur_morph,cur_analysis.scon,
                                                            cur_analysis.pitems + [newitem]),
                                            rmorphs[0],cur_side,rmorphs[1:])
                    else:
                        output = output + generatePossibleAnalyses(model,
                                            possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                            cur_analysis.stem+phonopt[0],
                                                            cur_analysis.stem+phonopt[0],
                                                            cur_analysis.pphon,
                                                            cur_analysis.sphon[:len(phonopt[0])],
                                                            cur_analysis.pcon,cur_morph,
                                                            cur_analysis.pitems + [newitem]),
                                            rmorphs[0],cur_side,rmorphs[1:])
                newitem = vocab_item((cur_morph[0],item.morph_features),phonopt[1],cur_side,context,rules)
                if cur_side == 'p':
                    output = output + generatePossibleAnalyses(model,
                                        possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                        phonopt[0]+cur_analysis.stem,
                                                        phonopt[1]+cur_analysis.stem,
                                                        cur_analysis.pphon[len(phonopt[0]):],
                                                        cur_analysis.sphon,
                                                        cur_morph,cur_analysis.scon,
                                                        cur_analysis.pitems + [newitem]),
                                        rmorphs[0],cur_side,rmorphs[1:])
                else:
                    output = output + generatePossibleAnalyses(model,
                                        possible_analysis(cur_analysis.line,cur_analysis.p*p[-1],
                                                        cur_analysis.stem+phonopt[0],
                                                        cur_analysis.stem+phonopt[1],                                                                                   cur_analysis.pphon,
                                                        cur_analysis.sphon[:len(phonopt[0])],
                                                        cur_analysis.pcon,cur_morph,
                                                        cur_analysis.pitems + [newitem]),
                                        rmorphs[0],cur_side,rmorphs[1:])
        return output
    linearizations = [linear([(('ROOT',root),'r')],1.0)]
    for morph in morphs:
        newlinearizations = []
        for l in linearizations:
            pcontext = l.line[0][0]
            scontext = l.line[-1][0]
            if morph in model.linear.keys():
                if (pcontext,scontext) in model.linear[morph].keys():
                    prob = model.linear[morph][(pcontext,scontext)]
                else:
                    values = [model.linear[morph][x] for x in model.linear[morph].keys() if (x[0] == pcontext
                                                    and x[1] == scontext)]
                    if values == []:
                        values = [model.linear[morph][x] for x in model.linear[morph].keys() if (x[0][0] == pcontext[0]
                                                                                         and x[1] == scontext)]
                    if values == []:
                        values = [model.linear[morph][x] for x in model.linear[morph].keys() if (x[0] == pcontext
                                                                                         and x[1][0] == scontext[0])]
                    if values == []:
                        values = [model.linear[morph][x] for x in model.linear[morph].keys() if (x[0][0] == pcontext[0]
                                                                                         and x[1][0] == scontext[0])]
                    if values == []:
                        prob = 0.5
                    else:
                        prob = float(sum(values))/float(len(values))
                        model.linear[morph][(pcontext,scontext)] = prob
            elif morph[0] in [x[0] for x in model.linear.keys()]:
                values = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                            for x in model.linear[m].keys() if (x[0] == pcontext
                                                                and x[1] == scontext)]
                if values == []:
                    values = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                                                     for x in model.linear[m].keys() if (x[0][0] == pcontext[0]
                                                                                     and x[1] == scontext)]
                if values == []:
                    values = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                                                     for x in model.linear[m].keys() if (x[0] == pcontext
                                                                                     and x[1][0] == scontext[0])]
                if values == []:
                    values = [model.linear[m][x] for m in model.linear.keys() if m[0] == morph[0]
                                                     for x in model.linear[m].keys() if (x[0][0] == pcontext[0]
                                                                                     and x[1][0] == scontext[0])]
                if values == []:
                    prob = 0.5
                else:
                    prob = float(sum(values))/float(len(values))
                    model.linear[morph]={}
                    model.linear[morph][(pcontext,scontext)] = prob
            else:
                prob = 0.5
            newlinearizations.append(linear(l.line+[(morph,'s')],l.p*(1.0-prob)))
            newlinearizations.append(linear([(morph,'p')]+l.line,l.p*prob))
        linearizations = newlinearizations
    newroots = []
    for r in model.roots[root]:
        newroots.append((optimiseRootPhon(phon,r[0],model.settings),r[1]))
    posanal = []
    analyses = []
    for l in linearizations:
        if l.p == 0.0:
            continue
        rootanal = []
        for r in newroots:
            pands = findPandS(phon,r[0][0])
            if r[0][0] == r[0][1]:
                rootanal.append(possible_analysis(l.line,l.p*r[1],r[0][0],r[0][1],
                                            pands[0],pands[1],('ROOT',root),('ROOT',root),
                                            [(('ROOT',root),r[0][1])]))
            else:
                rootanal.append(possible_analysis(l.line,l.p*(0.5*r[1]),r[0][0],r[0][0],
                                            pands[0],pands[1],('ROOT',root),('ROOT',root),
                                            [(('ROOT',root),r[0][0])]))
                rootanal.append(possible_analysis(l.line,l.p*(0.5*r[1]),r[0][0],r[0][1],
                                            pands[0],pands[1],('ROOT',root),('ROOT',root),
                                            [(('ROOT',root),r[0][1])]))
        prefixes = [x[0] for x in l.line if x[1] == 'p']
        suffixes = [x[0] for x in l.line if x[1] == 's']
        for ra in rootanal:
            if len(prefixes) > 0:
                panal = generatePossibleAnalyses(model,ra,prefixes[0],'p',prefixes[1:])
                for pa in panal:
                    if len(suffixes) > 0:
                        sanal = generatePossibleAnalyses(model,pa,suffixes[0],'s',suffixes[1:])
                        analyses = analyses + sanal
                    else:
                        analyses = analyses + panal
            else:
                if len(suffixes) > 0:
                    sanal = generatePossibleAnalyses(model,ra,suffixes[0],'s',suffixes[1:])
                    analyses = analyses + sanal
                else:
                    analyses = analyses + [ra]
    sortedanalyses = sorted(analyses, key=lambda self:-self.p)
    best = [x for x in sortedanalyses if x.p == sortedanalyses[0].p]
    for analysis in best:
        pcon = analysis.line[0]
        scon = analysis.line[0]
        for l in analysis.line[1:]:
            model = updateLinearization(model,l[0],(pcon,scon),l[1])
            if l[1] == 'p':
                pcon = l[0]
            else:
                scon = l[0]
        item = analysis.pitems[0]
        model = updateRootConfidence(model,item[0][1],item[1])
        for item in analysis.pitems[1:]:
            model = updateItemConfidence(model,item)
    return model	        


def learnVocab(word_list, settings, debug = False, iterate = False, output = True):
    model = Model(settings)
    iteration = 0
    while not testVocab(model,word_list,(iterate and ((output) or (iteration > 2)))):
        if not debug:
            newlist = []
            for i in range(model.settings.samplesize):
                newlist.append(word_list[randint(0,len(word_list)-1)])
        else:
            newlist = word_list
        if iterate and ((output) or (iteration > 2)):
            print 'Word list: ' + str([''.join(IPA[c] for c in word.phonology) for word in newlist])
        for word in newlist:
            morphs = word.morphology['OTHER']
            phon = word.phonology
            root = word.morphology['ROOT']
            if debug:
                debugOutput(model,word)
            if not testWord(model, word):
                if (word.morphology['ROOT'] not in model.roots.keys()) and (False in [x in model.vocab.keys()
                                            for x in word.morphology['OTHER']]):
                    model = nothingKnown(model,phon,root,morphs)
                elif word.morphology['ROOT'] not in model.roots.keys():
                    model = rootUnknown(model,phon,root,morphs)
                else:
                    model = rootKnown(model,phon,root,morphs)
        #Clean up and iterate printout
        #model = clean_model(model)
        if iterate and ((model) or (iteration > 2)):
            iterateOutput(model,word_list,iteration)
    return model
