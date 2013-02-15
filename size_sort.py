from progressbar import *
from Comb import *
def size_sort(ms):
	'''Sorts an iterable with elements of various length into groups by length of element'''
	results = []
	widgets = ['Sorting Morpheme Contexts: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
                   ' ', ETA()]
        pbar = ProgressBar(widgets=widgets,maxval=len(ms)).start()
	for i in xrange(len(ms)):
		morph = ms[i]
		results.append([])
		for model in morph:
			length = 0
			for side in model[1]:
				length = length + len(side[1])
			try:
				results[i][length-1].append(model)
			except:
				for j in range(length-len(results[i])):
					results[i].append([])
				results[i][length-1].append(model)
		pbar.update(i)
	pbar.finish()
	return results

def create_list(ms, size):
	output = []
	for i in range(size,-1,-1):
		if i == 0:
			output.append([])
			for morph in ms:
	                	output.append([])
        		        for model in morph[0]:
	        	                output[-1].append(model)
		if i != 0:
	                sizeSet1 = []
			for morph in ms:
				sizeSet1.append([])
				try:
					for model in morph[i]:
						sizeSet1[0].append(model)
				except:
					continue
					
        	        sizeSet2 = create_list(ms,size-i)
                	modelList = add_lists(sizeSet1,sizeSet2)
			output = output + modelList
	return output

def add_lists(list1,list2):
	pass

def sized_model(ms, size):
	bareModelList = []
	for morph in ms:
		bareModelList.append([])
		for model in morph[0]:
			bareModelList[-1].append(model)
	bareModels = product(bareModelList)
	modelList = create_list(ms,size)
