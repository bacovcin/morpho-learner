def size_sort(ms):
	'''Sorts an iterable with elements of various length into groups by length of element'''
	results = []
	for model in ms:
		length = 0
		for x in model:
			for morpheme in x[1]:
				for side in morpheme[1]:
					length = length + len(side[1])
		try:
			results[length-1].append(model)
		except:
			for i in range(length-len(results)):
				results.append([])
			results[length-1].append(model)
	return results
