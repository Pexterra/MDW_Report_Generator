import os
from time import strftime, localtime
from collections import OrderedDict

import pandas as pd

from PySide6.QtCore import QObject, Slot, Property, Signal, QThreadPool
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

from py.csv.csvHandler import CSVHandler
from py.utils.incident import Incident
from py.utils.thread import Worker
from py.imageHandling.imageToIncident import ImageToIncident, DataTracker


QML_IMPORT_NAME = "ReportGenerator"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class ReportGenerator(QObject):
	def __init__(self):
		super().__init__()
		self._folder = ''
		self._output = ''
		self.threadPool = QThreadPool()

	def setFolder(self, folder):
		self._folder = folder[8:]
		self.addToOutput(f'Image folder set: {self.folder}')
		self.folderChanged.emit()

	def getFolder(self):
		return self._folder

	def addToOutput(self, text):
		currentTime = strftime("%H:%M:%S", localtime())
		self._output = f'[{currentTime}] {text}\n'+ self._output
		self.outputChanged.emit()

	def getOutput(self):
		return self._output

	@Slot()
	def createReport(self):
		#self._createReport(self.addToOutput)
		self.worker = Worker(self._createReport, self.addToOutput)
		self.threadPool.start(self.worker)

	def _createReport(self, outputFn):
		subFolder = 'Incidents'

		csvHandler : CSVHandler= CSVHandler()
		imgToIncident : ImageToIncident = ImageToIncident()
		dataTracker : DataTracker= DataTracker()

		reportName = '_Incidents'
		incidents : dict[int, Incident] = csvHandler.CSVtoIncidents(f'../Reports/{subFolder}/csv/{reportName}.csv')
		folders = self._getFoldersWithImages()
		for folder in folders:
			images, imageCount = imgToIncident.getImages(folder)
			outputFn(f'Found {str(imageCount)} images in {folder}')
			for image in images:
				imgToIncident.getIncidentsFromImage(image, incidents, dataTracker, outputFn)

		incidents = OrderedDict(sorted(incidents.items()))
		officers = []
		for incident in incidents.values():
			officers.append(incident.startedBy)
		officers = list(set(officers))

		reports = []
		reportName = '_Incidents'

		fullReport = 'IncidentNr;Date;Involved;StartedBy;Title\n'
		for incident in incidents.values():
			fullReport += f'{incident.ID};{incident.date};{incident.involvedOfficers};{incident.startedBy};{incident.title}\n'
		reports.append(csvHandler.saveToCSV(fullReport, f'../Reports/{subFolder}/csv/{reportName}.csv'))
		outputFn(f'Created full incident report [../Reports/{subFolder}/csv/{reportName}.csv]')

		officers = sorted(officers)
		for officer in officers:
			report = 'IncidentNr;Date;Involved;StartedBy;Title\n'
			for incident in incidents.values():
				if officer in incident.involvedOfficers or officer in incident.startedBy:
					report += f'{incident.ID};{incident.date};{incident.involvedOfficers};{incident.startedBy};{incident.title}\n'
			reports.append(csvHandler.saveToCSV(report, f'../Reports/{subFolder}/csv/{officer}.csv'))
			outputFn(f'Created csv for {officer} [../Reports/{subFolder}/csv/{officer}.csv]')

		if os.path.exists(f'../Reports/{subFolder}/Incidents.xlsx'):
			os.remove(f'../Reports/{subFolder}/Incidents.xlsx')
		for report in reports:
			csvHandler.add_csv_to_excel(report, f'../Reports/{subFolder}/Incidents.xlsx')
		outputFn(f'Created full incident Excel file [../Reports/{subFolder}/Incidents.xlsx]')


	def _getFoldersWithImages(self, extention = '.png'):
		folders = []
		for root, dirs, files in os.walk(self._folder):
			for file in files:
				if file.lower().endswith('.png'):
					folders.append(root)
					break
		return folders

	folderChanged = Signal()
	folder = Property(str, getFolder, setFolder, notify=folderChanged)

	outputChanged = Signal()
	output = Property(str, getOutput, addToOutput, notify=outputChanged)