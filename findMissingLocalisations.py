from collections import defaultdict

def diffFiles(listOfFiles):
	dicts = []
	filenames = []
	for filename in listOfFiles:
		dicts.append(readLocalisations(filename))
		filenames.append(filename)
	diffDictKeys(dicts, filenames)

def diffDictKeys(dicts, filenames):
	if len(dicts) != len(filenames):
		raise "dicts and filenames have to have the same length!"
	if len(dicts) <= 1:
		raise "need at least two dictionarys"

	keySets = []
	for localisation in dicts:
		keySets.append(set(localisation.keys()))

	#Remove all the common keys from the keySets
	fullIntersection = intersectMultiple(keySets)
	keySets = [x.difference(fullIntersection) for x in keySets]

	#Create a dict that stores which key is stored in which files.
	keyInFiles = defaultdict(set)
	for keySet, filename in zip(keySets, filenames):
		for key in keySet:
			keyInFiles[key].add(filename)
	
	fileSet = set(filenames)
	fileStatistics = {'+':defaultdict(int),'-':defaultdict(int)}
	for key, keySet in keyInFiles.items():
		inFiles = keySet
		notInFiles = fileSet-keySet
		for filename in inFiles:
			fileStatistics['+'][filename]+=1
		for filename in notInFiles:
			fileStatistics['-'][filename]+=1
		print("%s:\n\tIn: %s\n\tNot in: %s" % (key, toCommaSeparatedList(inFiles), toCommaSeparatedList(notInFiles)))
	
	print("\nStatistics:")
	print("\tCommon: %d" % len(fullIntersection))
	for filename in filenames:
		print("\t%s: +%d -%d" %(filename, fileStatistics['+'][filename], fileStatistics['-'][filename]))

def toCommaSeparatedList(l):
	return ", ".join(l)

def intersectMultiple(listOfSets):
	if len(listOfSets) <= 1:
		raise "need at least two sets"
	fullIntersection = listOfSets[0].intersection(listOfSets[1])
	for s in listOfSets[2:]:
		fullIntersection = fullIntersection.intersection(s)
	return fullIntersection

def readLocalisations(filename):
	localisation = {}
	with open(filename, "r", encoding="utf8") as h:
		for line in h:
			if line.strip() == "":
				continue
			splitted = line.split("=", 1)
			if (len(splitted) == 2):
				key = splitted[0]
				value = splitted[1].strip()
				localisation[key] = value
			else:
				print("Can not parse line '%s' in '%s'" % (line, filename))
	return localisation


if __name__ == "__main__":
	import sys
	diffFiles(sys.argv[1:])
