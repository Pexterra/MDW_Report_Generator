import cv2, os, pathlib
import pandas as pd
import numpy as np
import pytesseract
from datetime import datetime
import locale

class CSVHandler(object):
	def initializeCSV(self, header, CSVtoLoad = None):
		self.header = header
		self.csv = ""
		self.CSV_rows = []
		if CSVtoLoad:
			if os.path.exists(CSVtoLoad):
				with open(CSVtoLoad) as f:
					self.CSV_rows = [line for line in f]
			else:
				print(f'unable to locate {CSVtoLoad}, setting up header for csv')
				self.csv = f"{header}\n"
		else:
			self.csv = f"{header}\n"
		return True

	def addImageData(self, pathToImage):
		rows	: list = self._getRowsFromImage(pathToImage)
		rowLength = len(rows)

		for iRow in range(0, rowLength):
			rows[iRow] = rows[iRow].replace(';', '')
			data: str = ""

			# getting identifier & date
			if not self._isIdentifier(rows[iRow]):
				continue
			else:
				data += self._getIDAndDate(rows[iRow])

			# getting footer with reporter & additional info
			result, success = self._getFooter(rows, iRow, rowLength)
			if not success:
				continue
			else:
				data += result

			# getting title
			result, success = self._getTitle(rows, iRow)
			if not success:
				continue
			else:
				data += result

			# formatting end of data
			data = self._formatEndOfData(data)

			# appending data
			self._verifyAndAddUniqueData(data)

	def _verifyAndAddUniqueData(self, data):
		# checking if all columns are filled
		if data.count(';') == self.header.count(';'):
			#looking for duplicates
			data_identification = data[:data.find(';')]
			for csvRow in self.CSV_rows[1:]:
				csv_identification = csvRow[:csvRow.find(';')]
				if data_identification == csv_identification:
					data_title = data[data.rfind(';')+1:]
					csv_title = csvRow[csvRow.rfind(';')+1:]
					if len(data_title) > len(csv_title):
						self.CSV_rows.remove(csvRow)
						self.CSV_rows.append(data)
						return
					return
			self.CSV_rows.append(data)
					

	def _isIdentifier(self, row):
		if row.startswith('#') and (row.endswith('AM') or row.endswith('PM')):
			return True
		return False

	def _getIDAndDate(self, row):
		identifier = row[:row.find(' ')]
		unformatedDate = row[row.find(' ')+1:]
		locale.setlocale(locale.LC_ALL, 'en_US.utf8')
		date = datetime.strptime(unformatedDate, '%B %d, %Y - %I:%M %p')
		return f"{identifier};{date};"

	def _getFooter(self, rows, iRow, maxRows):
		result = ""
		if not iRow +1 <= maxRows:
			return result, False # invalid line
		else:
			row = rows[iRow+ 1]
			if '(A)' in row:
				reporter = row[row.find('(A)')+4:]
				if row.startswith('(A)'):
					result = f'None;{reporter};'
				else:
					additionalInfo = row[:row.find('(A)') -1]
					result = f'{additionalInfo};{reporter};'
			return result, True

	def _getTitle(self, rows, iRow):
		result = ""
		for i in range(iRow - 1, -1, -1):
			if '(A)' in rows[i]:
				break
			else:
				result = ' ' + rows[i] + result
		if result != "":
			if result.startswith(' '):
				result = result[1:]
			result += ';'
			return result, True
		else:
			return result, False

	def _formatEndOfData(self, data):
		if data.endswith(';'):
				data = data[:-1]
		data += '\n'
		return data

	def _getRowsFromImage(self, pathToImage: str) -> list:
		image = cv2.imread(pathToImage)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
		
		data: str = pytesseract.image_to_string(thresh, lang='eng',config='--psm 6')
		rows: list = data.split('\n')
		for row in rows:
			if row == "":
				rows.remove(row)
		return rows

	def addDataFromImageFolder(self, pathToFolder, extention='.png'):
		imageFound = False
		for file in os.listdir(pathToFolder):
			if file.endswith(".png"):
				self.addImageData(f'{pathToFolder}/{file}')
				imageFound = True
		return imageFound

	def saveLinesToCSV(self, pathToCSV = '_result.csv'):
		if len(self.CSV_rows) != 0:
			for line in self.CSV_rows:
				self.csv += line
		else:
			return False
		# creating directories if none existant
		if '/' in pathToCSV:
			directories = pathToCSV[:pathToCSV.rfind('/')]
			pathlib.Path(directories).mkdir(parents=True, exist_ok=True) 

		# saving csv
		with open(pathToCSV, "w") as text_file:
			text_file.write(self.csv)
		return True