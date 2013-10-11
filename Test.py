from learn import *
import sets
import string
if __name__ == '__main__':
    word_list = [
    word(r'wutus',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['NOMINATIVE'])),('PHI',frozenset(['COMMON','SG']))]}),
    word(r'witis',{'ROOT':'WHITE','OTHER':[('CASE',frozenset(['OBLIQUE'])),('PHI',frozenset(['COMMON','SG']))]}),
    ]
    # (insert, delete, skel, root, major, minor, sub, samplesize)
    settings = Settings(3, 3, 5, 3, 2, 1, 2, 1)
    learnVocab(word_list,settings,iterate=True)
