from input_data import *
from chain_output import *
import string
if __name__ == '__main__':
    dic = Dictionaryify([
    
    word(r'c{\ae}t',[('ROOT','CAT'),('NUMBER','SG')]),
    word(r'c{\ae}ts',[('ROOT','CAT'),('NUMBER','PL')]),
    word(r'toU',[('ROOT','TOE'),('NUMBER','SG')]),
    word(r'toUz',[('ROOT','TOE'),('NUMBER','PL')]),
    word(r'fIS',[('ROOT','FISH'),('NUMBER','SG')]),
    word(r'fIS9z',[('ROOT','FISH'),('NUMBER','PL')]),
    word(r'dAg',[('ROOT','DOG'),('NUMBER','SG')]),
    word(r'dAgz',[('ROOT','DOG'),('NUMBER','PL')]),
    word(r'fIS',[('ROOT','FISH'),('TENSE','PRESENT')]),
    word(r'fISIN',[('ROOT','FISH'),('TAM','PRESENT PARTICIPLE')]),
    word(r'fISt',[('ROOT','FISH'),('TENSE','PAST')]),
    word(r'plej',[('ROOT','PLAY'),('TENSE','PRESENT')]),
    word(r'plejIN',[('ROOT','PLAY'),('TAM','PRESENT PARTICIPLE')]),
    word(r'plejd',[('ROOT','PLAY'),('TENSE','PAST')]),
    word(r'wOk',[('ROOT','WALK'),('TENSE','PRESENT')]),
    word(r'wOkt',[('ROOT','WALK'),('TENSE','PAST')]),
    word(r'wOkIN',[('ROOT','WALK'),('TAM','PRESENT PARTICIPLE')]),
    word(r'brIN',[('ROOT','BRING'),('TENSE','PRESENT')]),
    word(r'brat',[('ROOT','BRING'),('TENSE','PAST')]),
    word(r'brINiN',[('ROOT','BRING'),('TAM','PRESENT PARTICIPLE')]),
    ])
    lexicon = dic[0]
    ordering = dic[1]
    setting = settings(1,1,3,2,5000,10000,2)
    chains = build_models(create_model_space(lexicon, ordering),lexicon,setting,mp=False)
    printChains(chains)
