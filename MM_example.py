from learn import *
import sets
import string
if __name__ == '__main__':
    word_list = [
    word(r'wutus',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['COMMON','SG']))]}),
    word(r'witis',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['COMMON','SG']))]}),
    word(r'wutum',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['COMMON','PL']))]}),
    word(r'witim',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['COMMON','PL']))]}),
    word(r'wutun',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['NEUTER','SG']))]}),
    word(r'witin',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['NEUTER','SG']))]}),
    word(r'wutun',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['NEUTER','PL']))]}),
    word(r'witin',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['NEUTER','PL']))]}),
    word(r'yolus',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['COMMON','SG']))]}),
    word(r'yelis',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['COMMON','SG']))]}),
    word(r'yolum',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['COMMON','PL']))]}),
    word(r'yelim',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['COMMON','PL']))]}),
    word(r'yolun',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['NEUTER','SG']))]}),
    word(r'yelin',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['NEUTER','SG']))]}),
    word(r'yolun',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['NEUTER','PL']))]}),
    word(r'yelin',{'ROOT':'YELLOW','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['NEUTER','PL']))]})
    ]
    settings = Settings(2, 2, 5, 3, 2, 1, 1, 2)
    learnVocab(word_list,settings,iterate=True)
