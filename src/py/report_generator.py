from time import strftime, localtime
from PySide6.QtCore import QObject, Slot, Property, Signal
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

from py.csv.ImageToCSV import CSVHandler

QML_IMPORT_NAME = "ReportGenerator"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class ReportGenerator(QObject):
	def __init__(self):
		super().__init__()
		self._folder = ''
		self._output = ''

	def setFolder(self, folder):
		self._folder = folder[8:]
		self.addToOutput(f'Image folder set: {self.folder}')
		self.folderChanged.emit()

	def getFolder(self):
		return self._folder

	def addToOutput(self, text):
		currentTime = strftime("%H:%M:%S", localtime())
		self._output += f'[{currentTime}] {text}\n'
		self.outputChanged.emit()

	def getOutput(self):
		return self._output

	@Slot(str, str)
	def createReport(self, tag, reportName):
		if tag == "":
			tag = 'Untagged'
		if reportName == "":
			reportName = 'result'
		reportName = reportName + '.csv'

		csvHandler = CSVHandler()
		msg = csvHandler.initializeCSV(header='IncidentNr;Date;AdditionalTags;StartedBy;Title', CSVtoLoad=f'../Reports/{tag}/{reportName}')
		self.addToOutput(msg)
		images, imageCount = csvHandler.getImages(self.folder)
		if imageCount != 0:
			self.addToOutput(f'Found {str(imageCount)} images in the folder')
			for image in images:
				msg = csvHandler.addImageData(image)
				self.addToOutput(msg)
			csvHandler.saveLinesToCSV(pathToCSV=f'../Reports/{tag}/{reportName}')
			self.addToOutput(f"Saved report to ./Reports/{tag}/{reportName}")
		else:
			self.addToOutput(f"No image data found in {self._folder}")


	folderChanged = Signal()
	folder = Property(str, getFolder, setFolder, notify=folderChanged)

	outputChanged = Signal()
	output = Property(str, getOutput, addToOutput, notify=outputChanged)