import FileStream as File
import Sort as Sort
import enchant

INCORRECT = 0
RELOCATE = 1
CORRECT = 2

File.FileStream.openFile('wide_dictionary.txt')
File.FileStream.readFromFile()
dictionaryWordList = File.FileStream.m_MemoryStream.split('\n')
File.FileStream.closeFile()

File.FileStream.openFile('wide_dictionary_commonchars.txt')
File.FileStream.readFromFile()
dictionaryWordCommonLetters = File.FileStream.m_MemoryStream.split('\n')
File.FileStream.closeFile()

File.FileStream.openFile('training_data.txt')
File.FileStream.readFromFile()
trainingData = File.FileStream.m_MemoryStream.split('\n')
letterStatistics = list();

charNum = 1

for letterStat in trainingData:
	if charNum == 27:
		break

	temp = letterStat.split(',')
	for i in range(len(temp)):
		num = int(temp[i])
		temp[i] = num
	letterStatistics.append(temp)
	charNum += 1

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

currentWordList = dictionaryWordList
currentWordCommonChars = dictionaryWordCommonLetters
incorrectLetters = list()


isProcessedAlready = False 

while True:
	wordInput = input("The input:")
	correctness = input("The result:")

	wordInput = wordInput.lower()

	wordInput = list(wordInput)
	correctness = list(correctness)

	isFinished = True;
	for correct in correctness:
		if int(correct) != CORRECT:
			isFinished = False;
			break;

	if isFinished == False:

		size = len(wordInput)

		tempList = list()
		commList = list()
		index = 0

		# Filtering words based on their length of chars
		for word in currentWordList:
			chars = list(word)
			if len(chars) == int(size):
				tempList.append(word)
				commList.append(currentWordCommonChars[index])
			index += 1

		currentWordList = tempList
		currentWordCommonChars = commList

		# Preparing variables for comparison
		correctLetters = list()
		correctLetterIndex = list()

		orphanLetters = list()
		orphanLetterIndex = list()

		for i in range(len(wordInput)):

		# Letters that are right but wrong place
			if int(correctness[i]) == RELOCATE:
				orphanLetters.append(wordInput[i])
				orphanLetterIndex.append(int(i))

		# Correct letters
			if int(correctness[i]) == CORRECT:
				correctLetters.append(wordInput[i])
				correctLetterIndex.append(int(i))

		letterIsNotIncorrect = list()

		for letter in correctLetters:
			letterIsNotIncorrect.append(letter)
		for letter in orphanLetters:
			letterIsNotIncorrect.append(letter)

		# We dont want duplicate characters to be added to the incorrect letters list
		for i in range(len(wordInput)):
			if int(correctness[i]) == INCORRECT:
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

		# Preparing to filter word list to only display correct letters
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

			# If we passed the checks, re/add word to the list
			if isValid: 
				tempList.append(word)
				commList.append(currentWordCommonChars[index])
			index += 1

		currentWordList = tempList
		currentWordCommonChars = commList

		tempList = list()
		commList = list()
		index = 0;

		# Remove words if they contain any of the incorrect letters
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

		# The new word in the new list needs to contain the letter that is correct but in the wrong position

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

		# Preparing to check duplicate characters, this is expensive so save for last

		tempList = list()
		commList = list()
		index = 0;

		correctLetterCount = dict()
		incorrectLetterCount = dict()
		charPos = 0

		for char in wordInput:
			if int(correctness[charPos]) > INCORRECT:
				if (char in correctLetterCount) == False:
					correctLetterCount[char] = 1
				else:
					correctLetterCount.update({char:correctLetterCount[char] + 1})
			else:
				if (char in incorrectLetterCount) == False:
					incorrectLetterCount[char] = 1
				else:
					incorrectLetterCount.update({char:incorrectLetterCount[char] + 1})
			charPos += 1


	# Check if duplicate letters are correct or incorrect, then filter out of the list
		for word in currentWordList:
			valid = True
			validateCount = correctLetterCount.copy()
			for char in word:
				correctCharEmpty = True
				if (char in validateCount) == True:
					if validateCount[char] > 0:
						validateCount.update({char:validateCount[char] - 1})
						correctCharEmpty = False
					else:
						validateCount.pop(char)

				if correctCharEmpty == True:
					if (char in incorrectLetterCount) == True:
						valid = False
						break
					
			if valid == True:
				tempList.append(word)
				commList.append(currentWordCommonChars[index])
			index += 1;

		currentWordList = tempList
		currentWordCommonChars = commList

		tempList = list()
		commList = list()
		index = 0;

		# Check the spelling of the word to see if it is correct (I believe this removes non american spelling words)
		for word in currentWordList:
			if spelling.check(word):
				tempList.append(word)
				commList.append(currentWordCommonChars[index])
			index += 1

		currentWordList = tempList
		currentWordCommonChars = commList

		# Sort by word likeliness
		currentWordList = Sort.BubbleSortByLocations(currentWordList, currentWordCommonChars)

		print('')
		for i in range(len(currentWordList)):
			print(currentWordList[i] + ':' + str(currentWordCommonChars[i]), end=' ')
		print('')

		# Need to save the incorrect letters so we don't populate the list in the next run with the words excluded in this one
		isProcessedAlready = True
	else:
		# Add word statistics to some text file so we can teach AI to guess the word in the future based on chances
		index = 0
		for char in wordInput:
			letterStatistics[ord(char) - 97][index] += 1
			index += 1

		tempDataStatistics = ''

		for stats in letterStatistics:
			posIndex = 0
			for position in stats:
				tempDataStatistics += str(position)
				if len(stats) != posIndex + 1:
					tempDataStatistics += ','
				posIndex += 1
			tempDataStatistics += '\n'

		File.FileStream.openFile('training_data.txt')
		File.FileStream.m_MemoryStream = tempDataStatistics
		File.FileStream.writeToFile('training_data.txt')
		File.FileStream.closeFile()

		# Reset states for new game
		currentWordList = dictionaryWordList
		currentWordCommonChars = dictionaryWordCommonLetters
		incorrectLetters = list()
		isProcessedAlready = False 

		print("Congratulations! You Won!")
		print("")
		print("### New Game ###")