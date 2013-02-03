from progressbar import *
from itertools import combinations
def set_combs(initSet):
    for i in range(1,len(initSet)+1,1):
        subSet = set(frozenset(x) for x in combinations(initSet,i))
        for x in subSet:
            #print len(initSet-x)
            #print 'initSet: ' + str(initSet)
            #print 'x: ' + str(x)
            #raw_input('initSet-x: ' +str(initSet-x))
            try:
                newSet.add(frozenset([frozenset(x),frozenset(initSet-x)])-frozenset([frozenset([])]))
            except:
                newSet = set([frozenset([frozenset(x),frozenset(initSet-x)])-frozenset([frozenset([])])])
            if len(initSet-x) > 1:
                #print 'additionSet:\n'
                additionSet = set_combs(set(initSet-x))
                for y in additionSet:
                    if y != frozenset([]):
                        #print 'x: ' + str(x)
                        #print 'y: ' + str(y)
                        #print 'additionSet:' + str(additionSet)
                        #raw_input(str(frozenset.union(frozenset([x]),frozenset.union(frozenset(y)))))
                        newSet.add(frozenset.union(frozenset([x]),frozenset.union(frozenset(y))))
            #print 'newSet: ' + str(newSet)
    return newSet


set_combs.__doc__ = """initSet set(1,2,3,4) -> frozenset([frozenset([1, 4]), frozenset([2]), frozenset([3])])
frozenset([frozenset([1, 3, 4]), frozenset([2])])
frozenset([frozenset([3, 4]), frozenset([2]), frozenset([1])])
frozenset([frozenset([1, 2]), frozenset([4]), frozenset([3])])
frozenset([frozenset([3]), frozenset([1, 2, 4])])
frozenset([frozenset([2, 4]), frozenset([1, 3])])
frozenset([frozenset([1, 2]), frozenset([3, 4])])
frozenset([frozenset([4]), frozenset([2]), frozenset([3]), frozenset([1])])
frozenset([frozenset([2, 4]), frozenset([3]), frozenset([1])])
frozenset([frozenset([4]), frozenset([2, 3]), frozenset([1])])
frozenset([frozenset([2, 3, 4]), frozenset([1])])
frozenset([frozenset([4]), frozenset([1, 2, 3])])
frozenset([frozenset([1, 2, 3, 4])])
frozenset([frozenset([1, 3]), frozenset([4]), frozenset([2])])
frozenset([frozenset([2, 3]), frozenset([1, 4])])"""

def product(alist):
    pools = map(tuple, (x for x in alist))
    result = [[]]
    for i in xrange(len(pools)):
        result = [x+[y] for x in result for y in pools[i]]
    for prod in result:
        yield tuple(prod)

def product_wbar(alist):
    pools = map(tuple, (x for x in alist))
    result = [[]]
    widgets = ['Multiplying Sets: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
                   ' ', ETA()]
    pbar = ProgressBar(widgets=widgets).start()
    for i in xrange(len(pools)):
        pbar.update(i+1)
        result = [x+[y] for x in result for y in pools[i]]
    pbar.finish()
    for prod in result:
        yield tuple(prod)
