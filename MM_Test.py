from learn import *
import string
if __name__ == '__main__':
    word_list = [
    word(r'witas',{'ROOT':'WHITE','OTHER':['COMMON','NOMINATIVE','SG']}),
    word(r'witaz',{'ROOT':'WHITE','OTHER':['COMMON','NOMINATIVE','PL']}),
    word(r'witnas',{'ROOT':'WHITE','OTHER':['NEUTER','NOMINATIVE','SG']}),
    word(r'witnaz',{'ROOT':'WHITE','OTHER':['NEUTER','NOMINATIVE','PL']}),
    word(r'witis',{'ROOT':'WHITE','OTHER':['COMMON','OBLIQUE','SG']}),
    word(r'witiz',{'ROOT':'WHITE','OTHER':['COMMON','OBLIQUE','PL']}),
    word(r'witnis',{'ROOT':'WHITE','OTHER':['NEUTER','OBLIQUE','SG']}),
    word(r'witniz',{'ROOT':'WHITE','OTHER':['NEUTER','OBLIQUE','PL']}),
    word(r'blayas',{'ROOT':'BLACK','OTHER':['COMMON','NOMINATIVE','SG']}),
    word(r'blayaz',{'ROOT':'BLACK','OTHER':['COMMON','NOMINATIVE','PL']}),
    word(r'blaynas',{'ROOT':'BLACK','OTHER':['NEUTER','NOMINATIVE','SG']}),
    word(r'blaynaz',{'ROOT':'BLACK','OTHER':['NEUTER','NOMINATIVE','PL']}),
    word(r'blayis',{'ROOT':'BLACK','OTHER':['COMMON','OBLIQUE','SG']}),
    word(r'blayiz',{'ROOT':'BLACK','OTHER':['COMMON','OBLIQUE','PL']}),
    word(r'blaynis',{'ROOT':'BLACK','OTHER':['NEUTER','OBLIQUE','SG']}),
    word(r'blayniz',{'ROOT':'BLACK','OTHER':['NEUTER','OBLIQUE','PL']}),
    word(r'grawas',{'ROOT':'GREEN','OTHER':['COMMON','NOMINATIVE','SG']}),
    word(r'grawaz',{'ROOT':'GREEN','OTHER':['COMMON','NOMINATIVE','PL']}),
    word(r'grawnas',{'ROOT':'GREEN','OTHER':['NEUTER','NOMINATIVE','SG']}),
    word(r'grawnaz',{'ROOT':'GREEN','OTHER':['NEUTER','NOMINATIVE','PL']}),
    word(r'grawis',{'ROOT':'GREEN','OTHER':['COMMON','OBLIQUE','SG']}),
    word(r'grawiz',{'ROOT':'GREEN','OTHER':['COMMON','OBLIQUE','PL']}),
    word(r'grawnis',{'ROOT':'GREEN','OTHER':['NEUTER','OBLIQUE','SG']}),
    word(r'grawniz',{'ROOT':'GREEN','OTHER':['NEUTER','OBLIQUE','PL']}), 
    ]
    #setting = settings(1,1,3,2,5000,10000,2)
    learn_vocab(word_list,output=False,iterate=True,debug=True)
    trials = []
    for i in range(1000):
        trials.append(learn_vocab(word_list,output=False,iterate=True))#,iterate=True)#,debug=True)
        print i
    i = 0.0
    for trial in trials:
        i = i + trial
    print "Average iteration (out of 1000): " + str(i/1000.0)
