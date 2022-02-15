def BubbleSortByLocations(targets, locations):
	finished = False
	while finished == False:
		finished = True
		for index in range(len(locations) - 1):
			if locations[index] < locations[index + 1]:
				tempIndex = locations[index + 1]
				tempWord = targets[index + 1]

				locations[index + 1] = locations[index]
				locations[index] = tempIndex

				targets[index + 1] = targets[index]
				targets[index] = tempWord

				finished = False
	return targets

def InsertionSortByLocations(targets, locations):
	finished = False
	while finished == False:
		finished = True
		for i in range(len(locations)-1):
			if locations[i] < locations[i+1]:
				for j in range (len(locations)):
					if locations[i+1] > locations[j]:

						targets.insert(j,targets[i+1])
						targets.pop(j)

						locations.insert(j,locations[i+1])
						locations.pop(j)
				finished = False

	return targets