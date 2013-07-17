from input_data import *
from chain_output import *
import string
if __name__ == '__main__':
    dic = Dictionaryify([
    word(r'c{\ae}t',[('ROOT','CAT'),('NUMBER','SG')]),
    word(r'c{\ae}ts',[('ROOT','CAT'),('NUMBER','PL')]),
    word(r'toU',[('ROOT','TOE'),('NUMBER','SG')]),
    word(r'toUz',[('ROOT','TOE'),('NUMBER','PL')]),
    word(r'ful',[('ROOT','FOOL'),('NUMBER','SG')]),
    word(r'fulz',[('ROOT','FOOL'),('NUMBER','PL')]),
    word(r'dAg',[('ROOT','DOG'),('NUMBER','SG')]),
    word(r'dAgz',[('ROOT','DOG'),('NUMBER','PL')]),
    word(r'baIk',[('ROOT','BIKE'),('NUMBER','SG')]),
    word(r'baIks',[('ROOT','BIKE'),('NUMBER','PL')]),
    word(r'c{\ae}p',[('ROOT','CAP'),('NUMBER','SG')]),
    word(r'c{\ae}ps',[('ROOT','CAP'),('NUMBER','PL')]),
    word(r'c{\ae}b',[('ROOT','CAB'),('NUMBER','SG')]),
    word(r'c{\ae}bz',[('ROOT','CAB'),('NUMBER','PL')]),
    ])
    lexicon = dic[0]
    ordering = dic[1]
    setting = settings(1,1,3,2,5000,10000,2)
    chains = build_models(create_model_space(lexicon, ordering),lexicon,setting,mp=True)
    printChains(chains)
