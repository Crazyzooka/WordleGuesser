import FileStream as File
import Sort as Sort
import enchant

File.FileStream.openFile('wide_dictionary.txt')
File.FileStream.readFromFile()
currentWordList = File.FileStream.m_MemoryStream.split('\n')
File.FileStream.closeFile()

File.FileStream.openFile('wide_dictionary_commonchars.txt')
File.FileStream.readFromFile()
currentWordCommonChars = File.FileStream.m_MemoryStream.split('\n')
File.FileStream.closeFile()

spelling = enchant.Dict('en_US')

#tempStream = list()

#for word in currentWordList:
#	chars = list(word)
#	commonChars = ['e','t','a','i','o','s','h','r']
#	commonCount = 0

#	for char in chars:
#		for common in commonChars:
#			if char == common:
#				commonCount += 1
#				commonChars.remove(char)
#				break
#	tempStream.append(str(commonCount) + '\n')

#final = ''.join(str(e) for e in tempStream)

#File.FileStream.m_MemoryStream = final
#File.FileStream.writeToFile('wide_dictionary_commonchars.txt')
#File.FileStream.closeFile()

global incorrectLetters
isProcessedAlready = False

while True:
	wordInput = input("The input:")
	correctness = input("The result:")

	size = len(wordInput)

	tempList = list()
	commList = list()
	index = 0

	for word in currentWordList:
		chars = list(word)
		if len(chars) == int(size):
			tempList.append(word)
			commList.append(currentWordCommonChars[index])
		index += 1

	currentWordList = tempList
	currentWordCommonChars = commList

	wordInput = list(wordInput)
	correctness = list(correctness)

	correctLetters = list()
	correctLetterIndex = list()

	orphanLetters = list()
	orphanLetterIndex = list()

	if isProcessedAlready == False:
		incorrectLetters = list()

	letterIsNotIncorrect = list()

	for i in range(len(wordInput)):

		if int(correctness[i]) == 1:
			orphanLetters.append(wordInput[i])
			orphanLetterIndex.append(int(i))

		if int(correctness[i]) == 2:
			correctLetters.append(wordInput[i])
			correctLetterIndex.append(int(i))

	for letter in correctLetters:
		letterIsNotIncorrect.append(letter)
	for letter in orphanLetters:
		letterIsNotIncorrect.append(letter)

	for i in range(len(wordInput)):
		if int(correctness[i]) == 0:
			isInList = False
			for j in range(len(correctLetters)):
				if letterIsNotIncorrect[j] == wordInput[i]:
					isInList = True
					break

			for j in range(len(orphanLetters)):
				if letterIsNotIncorrect[j] == wordInput[i]:
					isInList = True
					break

			if isInList == False:
				incorrectLetters.append(wordInput[i])

	tempList = list()
	commList = list()
	index = 0;

	for word in currentWordList:
		chars = list(word)
		isValid = True

		if len(correctLetters) > 0:
		# Check if the correct letters are in the correct position
			for i in range(len(correctLetters)):
				if chars[correctLetterIndex[i]] != correctLetters[i]:
					isValid = False
					break

		# Check for orphan letters
		if len(orphanLetters) > 0:
			for i in range(len(orphanLetters)):
				if chars[orphanLetterIndex[i]] == orphanLetters[i]:
						isValid = False

		if isValid: 
			tempList.append(word)
			commList.append(currentWordCommonChars[index])
		index += 1

	currentWordList = tempList
	currentWordCommonChars = commList

	tempList = list()
	commList = list()
	index = 0;

	for word in currentWordList:
		chars = list(word)
		isValid = True

		if len(incorrectLetters) > 0:
		# Check if there are any incorrect letters
			for i in range(len(chars)):
				for j in range(len(incorrectLetters)):
					if chars[i] == incorrectLetters[j]:
						isValid = False
						break
				if isValid == False:
					break

		if isValid: 
			tempList.append(word)
			commList.append(currentWordCommonChars[index])
		index += 1

	currentWordList = tempList
	currentWordCommonChars = commList

	tempList = list()
	commList = list()
	index = 0;

	for word in currentWordList:
		chars = list(word)
		isValid = True
		if len(orphanLetters) > 0:
			for i in range(len(orphanLetters)):
				doesLetterExist = False
				for j in range(len(chars)):
					if chars[j] == orphanLetters[i]:
						doesLetterExist = True
						break
				if doesLetterExist == False:
					isValid = False
					break
			
		if isValid: 
			tempList.append(word)
			commList.append(currentWordCommonChars[index])

		index += 1

	currentWordList = tempList
	currentWordCommonChars = commList

	tempList = list()
	commList = list()
	index = 0;

	for word in currentWordList:
		if spelling.check(word):
			tempList.append(word)
			commList.append(currentWordCommonChars[index])
		index += 1

	currentWordList = tempList
	currentWordCommonChars = commList

	currentWordList = Sort.BubbleSortByLocations(currentWordList, currentWordCommonChars)

	print('')
	for i in range(len(currentWordList)):
		print(currentWordList[i] + ':' + str(currentWordCommonChars[i]), end=' ')
	print('')

	isProcessedAlready = True