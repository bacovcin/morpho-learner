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


