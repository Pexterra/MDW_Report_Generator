import cv2, pytesseract, locale, os
from py.utils.incident import Incident
from datetime import datetime

class DataTracker(object):
	def __init__(self):
		self.updated : int = 0
		self.unidentifyable : int = 0
		self.ImagesWithProblems : list[str] = []

class ImageToIncident(object):

	def getIncidentsFromImage(self, pathToImage, existingIncidents: dict[int, Incident], dataTracker : DataTracker, outputFn = None):
		rows : list = self._getRowsFromImage(pathToImage)
		rowLength = len(rows)

		self.existingIncidents = existingIncidents.copy()

		for iRow in range(0, rowLength):
			row = rows[iRow]

			#cleaning up row
			row = row.strip()
			for char in ['-', '_', '=',',','~', ';', '.', u'\u2014']:
				if char in row:
					row = row.replace(char, '')

			# getting identifier & date
			if not self._isIdentifier(row):
				continue
			else:
				self._getIDAndDate(row)

			# getting footer with reporter & additional info
			success = self._getTags(rows, iRow, rowLength)
			if not success:
				dataTracker.unidentifyable += 1
				dataTracker.ImagesWithProblems.append(pathToImage)
				continue

			# getting title
			success = self._getTitle(rows, iRow)
			if not success:
				dataTracker.unidentifyable += 1
				dataTracker.ImagesWithProblems.append(pathToImage)
				continue

			dataTracker.updated += 1
			existingIncidents[self.incident.ID] = self.incident
			if outputFn:
				outputFn(f"Added/Updated Incident: {self.incident.ID}\n\t (A) {self.incident.startedBy}\n\t\t (O) {self.incident.involvedOfficers} \n\t\t\t{self.incident.title}")
					
	def _isIdentifier(self, row):
		if row.startswith('#') and (row.endswith('AM') or row.endswith('PM')):
			return True
		return False

	def _getIDAndDate(self, row):
		stateID = row[1:row.find(' ')]
		stateID = ''.join([i for i in stateID if (i.isdigit())])
		if stateID in self.existingIncidents:
			self.incident = self.existingIncidents[stateID]
		else:
			self.incident = Incident()
			self.incident.ID = stateID
		unformatedDate = row[row.find(' ')+1:]
		locale.setlocale(locale.LC_ALL, 'en_US.utf8')
		self.incident.date = datetime.strptime(unformatedDate.strip(), '%B %d %Y  %I:%M %p')

	def _getTags(self, rows, iRow, maxRows):
		if not iRow +1 <= maxRows:
			return False
		else:
			#cleaning up row‘
			row = rows[iRow+ 1]
			row = row.strip()
			row = ''.join([i for i in row if (i.isalpha()) or i == '(' or i == ')' or i == ' '])

			if '(A)' in row:
				self.incident.startedBy = row[row.find('(A)')+4:]
				if not row.startswith('(A)'):
					additionalInfo = row[:row.find('(A)') -1]
					additionalInfo = additionalInfo.strip()
					officerName = additionalInfo[additionalInfo.find('Officers')+9:]
					if officerName not in self.incident.involvedOfficers and 'Officers' in additionalInfo:
						if self.incident.involvedOfficers != "":
							self.incident.involvedOfficers += ','
						self.incident.involvedOfficers += officerName
			return True

	def _getTitle(self, rows, iRow):
		result = ""
		for i in range(iRow - 1, -1, -1):
			if ' (A) ' in rows[i]:
				break
			else:
				result = ' ' + rows[i] + result

		if result == "":
			return False

		result = result.strip() 
		result = ''.join([i for i in result if (i.isalpha()) or (i.isdigit()) or (i in ['(', ')', '|', '/', '-', '#', '+', ' '])])
		if len(self.incident.title) < len(result):
			self.incident.title = result

		return True

	def _getRowsFromImage(self, pathToImage: str) -> list:
		image = cv2.imread(pathToImage)
		image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
		
		data: str = pytesseract.image_to_string(image, lang='eng',config='--psm 4')
		rows: list = data.split('\n')

		for row in rows:
			if row == "":
				rows.remove(row)
		return rows

	def getImages(self, pathToFolder, extention='.png'):
		images : list[str] = []
		imageCount = 0
		for file in os.listdir(pathToFolder):
			if file.endswith(".png"):
				images.append(f'{pathToFolder}/{file}')
				imageCount += 1
		return images, imageCount