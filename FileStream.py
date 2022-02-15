import os.path

class FileStream:

	m_FileStream = None
	m_MemoryStream = ''
	m_FilePathSpec = ''
	m_CurrentFileName = ''

	def createFile(self,fileName):
		if self.m_FileStream == None:
			fileName = self.resolveCSVFileType(fileName)
			self.m_FileStream = open(fileName, 'w')
			self.m_CurrentFileName = os.path.basename(fileName)
			self.m_FileStream = open(fileName, 'r')
			self.m_FilePathSpec = fileName
			print('(createFile) File created.')
			return True

	def openFile(self,fileName):
		if self.m_FileStream == None:
			fileName = fileName.replace('/', '\\')
			if os.path.isfile(fileName):
				self.m_FileStream = open(fileName, 'r')
				self.m_CurrentFileName = os.path.basename(fileName)
				self.m_FilePathSpec = fileName
				print('File ' + self.m_CurrentFileName + ' opened.')
				return True
			else:
				print('File ' + self.m_CurrentFileName + ' doesn\'t exist.')
				return False
		else:
			print('(openFile) There is a file currently opened.')
			return False

	def closeFile(self):
		if os.path.isfile(self.m_FilePathSpec) and self.m_FileStream != None:
			self.m_FileStream.close()
			self.m_FileStream = None
			print('File ' + self.m_CurrentFileName + ' closed.')
			self.m_CurrentFileName = ''
			self.m_MemoryStream = ''
			return True
		else:
			print('(closeFile) No file is opened.')
			return False

	def writeToFile(self, fp):
		fp.replace('/', "\\")
		if os.path.isfile(self.m_FilePathSpec):
			self.m_FileStream = open(fp, 'w')
			self.m_FileStream.write(self.m_MemoryStream)
			self.m_FileStream.close()
			return True
		else:
			print('(writeToFile) No file is opened.')
			return False

	def readFromFile(self):
		if os.path.isfile(self.m_FilePathSpec):
			self.m_MemoryStream = self.m_FileStream.read()
			print('Read from file to memory.')
			return True
		else:
			print('(readFromFile) No file is opened.')
			return False

FileStream = FileStream()