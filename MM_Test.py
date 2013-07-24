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
    word(r'rotus',{'ROOT':'RED','OTHER':['COMMON','NOMINATIVE','SG']}),
    word(r'rotuz',{'ROOT':'RED','OTHER':['COMMON','NOMINATIVE','PL']}),
    word(r'rotnus',{'ROOT':'RED','OTHER':['NEUTER','NOMINATIVE','SG']}),
    word(r'rotnuz',{'ROOT':'RED','OTHER':['NEUTER','NOMINATIVE','PL']}),
    word(r'rotis',{'ROOT':'RED','OTHER':['COMMON','OBLIQUE','SG']}),
    word(r'rotiz',{'ROOT':'RED','OTHER':['COMMON','OBLIQUE','PL']}),
    word(r'rotnis',{'ROOT':'RED','OTHER':['NEUTER','OBLIQUE','SG']}),
    word(r'rotniz',{'ROOT':'RED','OTHER':['NEUTER','OBLIQUE','PL']})
    ]
    #setting = settings(1,1,3,2,5000,10000,2)
    model = learn_vocab(word_list,iterate=True)#,debug=True)
