from random import *
from decimal import *

def amount(): 
    return uniform(.02,0.12)

def changeWeights(a):
    b = [list(x) for x in a]
    for i in range(1000):
        r = random()
        q = 0
        for j in range(len(b)):
            q = q + b[j][1]
            if r <= q:
                am = amount()
                if b[j][1] + am >= 1.0:
                    b[j][1] = 1.0
                    b = [b[j]]
                else:
		    ivalue = b[j][1]
		    print ivalue
		    print ivalue + am
		    b[j][1] = ivalue + am
		    for k in range(len(b)):
			if k != j:
			    print (b[k][1]/(1.0-ivalue))
			    b[k][1] = (b[k][1]/(1.0-ivalue))*(1.0-(ivalue+am))
		break
        for item in b:
	   print item[0] + ': ' + str(Decimal(item[1]).quantize(Decimal('1.00000000')))
        print 'Sum: ' + str(sum([item[1] for item in b]))
	raw_input('Press enter to continue.')

import string
a = [[x,1.0/len(string.lowercase)] for x in string.lowercase]
for item in a:
    print item[0] + ': ' + str(Decimal(item[1]).quantize(Decimal('1.000')))
print 'Sum: ' + str(Decimal(sum([item[1] for item in a])).quantize(Decimal('1.00000')))
raw_input('Press enter to continue.')
changeWeights(a)
