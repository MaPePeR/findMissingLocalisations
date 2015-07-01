from collections import defaultdict

def diffFiles(listOfFiles, args):
	dicts = []
	filenames = []
	for filename in listOfFiles:
		dicts.append(readLocalisations(filename))
		filenames.append(filename)
	diffDictKeys(dicts, filenames, args)

def diffDictKeys(dicts, filenames, args):
	if len(dicts) != len(filenames):
		raise "dicts and filenames have to have the same length!"
	if len(dicts) <= 1:
		raise "need at least two dictionarys"

	keySets = []
	for localisation in dicts:
		keySets.append(set(localisation.keys()))

	#Remove all the common keys from the keySets
	fullIntersection = set.intersection(*keySets)
	keySets = [x.difference(fullIntersection) for x in keySets]
	allKeys = set.union(*keySets)

	#Create a dict that stores which key is stored in which files.
	keyInFiles = defaultdict(set)
	for keySet, filename in zip(keySets, filenames):
		for key in keySet:
			keyInFiles[key].add(filename)
	
	fileSet = set(filenames)
	fileStatistics = {'+':defaultdict(int),'-':defaultdict(int)}

	print("Keys:")
	for key, keySet in keyInFiles.items():
		inFiles = keySet
		notInFiles = fileSet-keySet
		for filename in inFiles:
			fileStatistics['+'][filename]+=1
		for filename in notInFiles:
			fileStatistics['-'][filename]+=1
		print("%s:\n\tIn: %s\n\tNot in: %s" % (key, toCommaSeparatedList(inFiles), toCommaSeparatedList(notInFiles)))

	print("\nFiles:")
	if args.showCommon:
		print("Common: \n\t%s" % toCommaSeparatedList(fullIntersection))
	for keySet, filename in zip(keySets, filenames):
		print("%s:" % filename)
		if not args.onlyMissing:
			print("\tHas: %s" % toCommaSeparatedList(allKeys & keySet))
		print("\tMissing: %s" % toCommaSeparatedList(allKeys - keySet))

	
	print("\nStatistics:")
	print("\tCommon: %d" % len(fullIntersection))
	for filename in filenames:
		print("\t%s: +%d -%d" %(filename, fileStatistics['+'][filename], fileStatistics['-'][filename]))

def toCommaSeparatedList(l):
	return ", ".join(l)

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
	import argparse
	parser = argparse.ArgumentParser(description='Find missing keys in localisation files.')
	parser.add_argument("--show-common", help="Also list keys that are present in all files.", action="store_true", dest="showCommon", default=False)
	parser.add_argument("--only-missing", help="Only list keys that are missing in a file.", action="store_true", dest="onlyMissing", default=False)
	parser.add_argument("filename", nargs=1)
	parser.add_argument("filenames", nargs="+")
	args = parser.parse_args()
	diffFiles(args.filename + args.filenames, args)
