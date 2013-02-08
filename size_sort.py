from progressbar import *
def size_sort(ms):
	'''Sorts an iterable with elements of various length into groups by length of element'''
	results = []
	widgets = ['Sorting Model Space: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
                   ' ', ETA()]
        pbar = ProgressBar(widgets=widgets,maxval=len(ms)).start()
	for i in xrange(len(ms)):
		model = ms[i]
		length = 0
		for morpheme in model:
			for side in morpheme[1]:
				length = length + len(side[1])
		try:
			results[length-1].append(model)
		except:
			for i in range(length-len(results)):
				results.append([])
			results[length-1].append(model)
		pbar.update(i)
	pbar.finish()
	return results
