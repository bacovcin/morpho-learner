from learn import *
word_list = [
    word(r'c{\ae}ts',{'ROOT':'CAT','OTHER':['PL']}),
    word(r'toU',{'ROOT':'TOE','OTHER':['SG']}),
    word(r'toUz',{'ROOT':'TOE','OTHER':['PL']}),
    word(r'fIS',{'ROOT':'FISH','OTHER':['SG']}),
    word(r'fIS9z',{'ROOT':'FISH','OTHER':['PL']}),
    word(r'dAg',{'ROOT':'DOG','OTHER':['SG']}),
    word(r'dAgz',{'ROOT':'DOG','OTHER':['PL']}),
    word(r'fIS',{'ROOT':'FISH','OTHER':['PRESENT']}),
    word(r'fISIN',{'ROOT':'FISH','OTHER':['PRESENT PARTICIPLE']}),
    word(r'fISt',{'ROOT':'FISH','OTHER':['PAST']}),
    word(r'plej',{'ROOT':'PLAY','OTHER':['PRESENT']}),
    word(r'plejIN',{'ROOT':'PLAY','OTHER':['PRESENT PARTICIPLE']}),
    word(r'plejd',{'ROOT':'PLAY','OTHER':['PAST']}),
    word(r'wOk',{'ROOT':'WALK','OTHER':['PRESENT']}),
    word(r'wOkt',{'ROOT':'WALK','OTHER':['PAST']}),
    word(r'wOkIN',{'ROOT':'WALK','OTHER':['PRESENT PARTICIPLE']}),
    word(r'brIN',{'ROOT':'BRING','OTHER':['PRESENT']}),
    word(r'brat',{'ROOT':'BRING','OTHER':['PAST']}),
    word(r'brININ',{'ROOT':'BRING','OTHER':['PRESENT PARTICIPLE']}),
    ]
model = model(settings(4,1,3,1))
aword = word(r'yuktubuu',{'ROOT':'WRITE','OTHER':['PAST','3RD PERSON','MASCULINE PL']})
nothingKnown(model,aword.phonology,aword.morphology['ROOT'],aword.morphology['OTHER'])
for x in model.roots[aword.morphology['ROOT']]:
    print ''.join(IPA[c] for c in x[0]) + ',' + str(x[1])
for morph in aword.morphology['OTHER']:
    for vi in model.vocab[morph]:
        print vi.morph_feature
        print 'Phon: ' + ''.join(IPA[c] for c in vi.exponent.phon)
        print vi.exponent.side
        print vi.context
        print vi.rules
raw_input()
