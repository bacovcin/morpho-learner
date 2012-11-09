#######################################
# Demo of current Harmony algorithm
# November 12, 2008
# Code by Kobey Shwayder
# Based on algorithm by Andrew Nevins
#######################################

from Feature import *
from Languages import *
from Harmony import *

if __name__ == '__main__':
    #Remove the triple quotes from around each example to demonstrate
    # (be sure to put them back if you don't want to see that example again)
    
        #Phoneme indexing is done starting from 0:
        #        h e l l o
        #index   0 1 2 3 4    i.e. "looking at 1" means looking at "e"
        #range  0_1_2_3_4_5   i.e. "range 1:2" is "e"
        
        
    #Basics of Harmony
    '''
    #Turkish plural + genitive, root "pul"  answer "pullarIn"
    root = Turkish.Parse("pul")
    suffix = ['pl', 'gen']
    answer= Harmonize(Turkish, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer
    '''
    
    '''
    #Turkish plural + genitive, root "el"  answer "ellerin"
    root = Turkish.Parse("el")
    suffix = ['pl', 'gen']
    answer= Harmonize(Turkish, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer
    '''
    
    #Bidirectional Search
    '''
    #Woleaian bidirectional search, "UlUm"+theme+ 2nd.sg  answer "UlUmemu"
    root = Woleaian.Parse("UlUm")
    suffix = ['theme', '2sg']
    answer= Harmonize(Woleaian, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer
    '''
    
    '''
    #Woleaian bidirectional search fails, "mat"+theme+ 2nd.sg  answer "matamu"
    root = Woleaian.Parse("mat")
    suffix = ['theme', '2sg']
    answer= Harmonize(Woleaian, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer
    '''
    
    #Contrastive
    '''
    #Uyghur contrastive +/-back, yol + pl  answer "yollar"
    root = Uyghur.Parse("yol")
    suffix = ['pl']
    answer= Harmonize(Uyghur, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer
    '''
    
    '''
    #Uyghur contrastive +/-back, fails til + pl  answer "tillar
    root = Uyghur.Parse("til")
    suffix = ['pl']
    answer= Harmonize(Uyghur, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer
    '''

    #Positionally Contrastive
      #Done but difficult to demo because I haven't inputted sepcific Front/Back consonants
      #in this demo they are F and B respectively
    '''
    #Karaim positionally contrasitive ablative, FuF + abl =  FuFFaF
    root = Karaim.Parse("FuF")
    suffix = ['abl']
    answer= Harmonize(Karaim, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer  
    '''  
    
    #Universally Marked
    '''
    #Sibe marked low, sula + dimin, answer = sulaqIn
    root = Sibe.Parse("sula")
    suffix = ['dimin']
    answer= Harmonize(Sibe, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer  
    '''
    
    '''
    #Sibe marked low, farXu + dimin, answer = farXuqun
    root = Sibe.Parse("farXu")
    suffix = ['dimin']
    answer= Harmonize(Sibe, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer 
    '''
    
    #Context Sensitive Markedness: No good demo currently, sorry
    
    '''
    #Microvariation in Kirghiz
    #KirghizA  tuz+abl = tuzdon
    root = KirghizA.Parse('tuz')
    suffix = ['abl']
    answerA = Harmonize(KirghizA, root, suffixes = suffix, debug = True)
    print "answer= %s" % answerA
    print '\n    ----------------------------------    \n'
    #KirghizB  turmus+abl = turmustan
    root = KirghizB.Parse('turmus')
    suffix = ['abl']
    answerB = Harmonize(KirghizB, root, suffixes = suffix, debug = True)
    print "answer= %s" % answerB
    print '\n'
    print "A: tuz+abl: answer= %s" % answerA
    print "B: turmus+abl: answer= %s" % answerB
    '''
    
    
    #Oroch Set-Union for ATR harmony
    # A = ae  , is invisible.   sOrOdA + foc = sOrOdAda
    root = Oroch.Parse("sOrOdA")
    suffix = ['foc']
    answer= Harmonize(Oroch, root, prefixes = [], suffixes = suffix, debug = True)
    print "answer= %s" % answer 
    
    
    '''
    #Unbounded vs. Syllable Bounded Search
    #Kikongo
    root = Kikongo.Parse('ku.du.mu.ki.si.')
    suffix = ['applicative']
    answerA = Harmonize(Kikongo, root, suffixes = suffix, debug = True)
    print "answer= %s" % answerA
    print '\n    ----------------------------------    \n'
    #Lamba  turmus+abl = turmustan
    root = Lamba.Parse('ma.si.')
    suffix = ['perf']
    answerB = Harmonize(Lamba, root, suffixes = suffix, debug = True)
    print "answer= %s" % answerB
    print '\n'
    print "Kikongo: kudumukisi+applicative: answer= %s" % answerA
    print "Lamba:   ma.si+perf:             answer= %s" % answerB
    '''
    
    
