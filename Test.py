from input_data import *
from chain_output import *
import string
if __name__ == '__main__':
    dic = Dictionaryify([
    word(r'arid',[('ROOT','RED'),('NUMBER','SG'),('GENDER','MASCULINE')]),
    word(r'rida',[('ROOT','RED'),('NUMBER','SG'),('GENDER','FEMININE')]),
    word(r'arud',[('ROOT','RED'),('NUMBER','PL'),('GENDER','MASCULINE')]),
    word(r'ruda',[('ROOT','RED'),('NUMBER','PL'),('GENDER','FEMININE')]),
    word(r'awit',[('ROOT','WHITE'),('NUMBER','SG'),('GENDER','MASCULINE')]),
    word(r'wita',[('ROOT','WHITE'),('NUMBER','SG'),('GENDER','FEMININE')]),
    word(r'awut',[('ROOT','WHITE'),('NUMBER','PL'),('GENDER','MASCULINE')]),
    word(r'wuta',[('ROOT','WHITE'),('NUMBER','PL'),('GENDER','FEMININE')]),
    word(r'ablk',[('ROOT','BLACK'),('NUMBER','SG'),('GENDER','MASCULINE')]),
    word(r'blka',[('ROOT','BLACK'),('NUMBER','SG'),('GENDER','FEMININE')]),
    word(r'ablk',[('ROOT','BLACK'),('NUMBER','PL'),('GENDER','MASCULINE')]),
    word(r'blka',[('ROOT','BLACK'),('NUMBER','PL'),('GENDER','FEMININE')]),
    ])
    lexicon = dic[0]
    ordering = dic[1]
    setting = settings(1,1,3,2,5000,10000,2)
    chains = build_models(create_model_space(lexicon, ordering),lexicon,setting,mp=False)
    printChains(chains)
