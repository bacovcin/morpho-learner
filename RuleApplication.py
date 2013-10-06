from Phonology import *
from itertools import *
import copy

def applyProcess(rule,phon,reverse=False):
    rtype = rule[0]
    rvalue = rule[1]
    ltype = rule[2][0][0]
    lside = rule[2][0][1]
    ldir = rule[2][0][2]
    lfeats = rule[2][0][3]
    output = phon
    if reverse == True:
	if rtype == 'ins':
	    rtype = 'del'
	elif rtype == 'del':
	    rtype = 'ins'
	    rvalue = '_'
        elif rtype == 'featch':
	    if lside == 'none':
		for feat in rvalue:
		    try:
			lfeats[feat] = rvalue[feat]
		    except:
			pass
		for feat in rvalue:
		    rvalue[feat] = FeatureOpposite(rvalue[feat])
    if rtype == 'ins':
	if ltype == 'abs':
	    if ldir == 'right':
	        output.insert(len(output)-(lfeats+1),rvalue)
	    elif ldir == 'left':
	        output.insert(lfeats,rvalue)
	elif ltype == 'rel':
	    if ldir == 'right':
		for i in range(len(output)):
		    for feat in lfeats:
			if lfeats[feat] == output[i]._features[feat]:
			    continue
			else:
			    break
		    else:
			if lside == 'right':
			    output.insert(i+1,rvalue)
			elif lside == 'left':
			    output.insert(i,rvalue)
			break
	    elif ldir == 'left':
                for i in range(len(output)-1,-1,-1):
                    for feat in lfeats:
                        if lfeats[feat] == output[i]._features[feat]:
                            continue
                        else:
                            break
                    else:
                        if lside == 'right':
                            output.insert(i+1,rvalue)
                        elif lside == 'left':
                            output.insert(i,rvalue)
                        break
    elif rtype == 'del':
        if ltype == 'abs':
	    if ldir == 'right':
                del(output[len(output)-(lfeats+1)])
            elif ldir == 'left':
                del(output[lfeats])
	elif ltype == 'rel':
            if ldir == 'right':
                for i in range(len(output)):
                    for feat in lfeats:
                        if lfeats[feat] == output[i]._features[feat]:
                            continue
                        else:
                            break
                    else:
                        if lside == 'right':
                            del(output[i+1])
                        elif lside == 'left':
                            del(output[i-1])
			elif lside == 'none':
			    del(output[i])
                        break
            elif ldir == 'left':
                for i in range(len(output)-1,-1,-1):
                    for feat in lfeats:
                        if lfeats[feat] == output[i]._features[feat]:
                            continue
                        else:
                            break
                    else:
			if lside == 'right':
                            del(output[i+1])
                        elif lside == 'left':
                            del(output[i-1])
                        elif lside == 'none':
                            del(output[i])
			break
    elif rtype == 'featch':
        if ltype == 'abs':
            for feat in rvalue:
		if ldir == 'right':
                    output[len(output)-(lfeats+1)]._features[feat] = rvalue[feat]
                elif ldir == 'left':
                    output[lfeats]._features[feat] = rvalue[feat]
        elif ltype == 'rel':
            if ldir == 'right':
                for i in range(len(output)):
                    for feat in lfeats:
                        if lfeats[feat] == output[i]._features[feat]:
                            continue
                        else:
                            break
                    else:
			for feat in rvalue:
                            if lside == 'right':
                                output[i+1]._features[feat] = rvalue[feat]
                            elif lside == 'left':
				output[i-1]._features[feat] = rvalue[feat]
                            elif lside == 'none':
				output[i]._features[feat] = rvalue[feat]
                        break
	elif ldir == 'left':
                for i in range(len(output)-1,-1,-1):
                    for feat in lfeats:
                        if lfeats[feat] == output[i]._features[feat]:
                            continue
                        else:
                            break
                    else:
			for feat in rvalue:
                            if lside == 'right':
                                output[i+1]._features[feat] = rvalue[feat]
                            elif lside == 'left':
                                output[i-1]._features[feat] = rvalue[feat]
                            elif lside == 'none':
                                output[i]._features[feat] = rvalue[feat]
                        break
    return output

def createRuleSpace(rule):
    def product(args):
        pools = map(tuple, args) 
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)
    space = []
    for loctuple in product(sorted([process[2] for process in rule],key=lambda self:len(self))):
	newrule = []
	for i in range(len(rule)):
	    newrule.append([rule[i][0],rule[i][1],[loctuple[i]]])
	space.append(newrule)
    return space
