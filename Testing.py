from learn import *

class settings(object):
    def __init__(self, phon, change, sub, samplesize):
        self.phon = phon              #weight of the deletion/insertion penalty in morphophonology
	self.change = change	      #weight of the change penalty in morphophonology
        self.sub = sub                #weight of the subtraction penalty in allomorphy
	self.samplesize = samplesize

a = PhonParse(r'black')
b = PhonParse(r'lacku')

mysets = settings(2,1,1,10)
resultsr = optimiseRootPhon(a,b,mysets,debug=True)
resultss = optimiseSuffixPhon(a,b,mysets)#,debug=True)
resultsp = optimisePrefixPhon(a,b,mysets)#,debug=True)
print 'Resultsr: ' + ''.join(IPA[c] for c in resultsr[0])
print 'Resultss: ' + ''.join(IPA[c] for c in resultss[0])
print 'Resultsp: ' + ''.join(IPA[c] for c in resultsp[0])

