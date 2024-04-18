import sys

from datetime import timedelta
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

from lib.csv.ImageToCSV import CSVHandler

@QmlElement
class ReportCreator(QObject):
	def __init__(self):
		super().__init__()
		self.folder = ''

	@Slot(str, result=str)
	def setFolder(self, folder):
		self.folder = folder[8:]
		return folder[folder.rfind('/')+1:]

	@Slot(str, str, result=str)
	def createReport(self, tag='Untagged', reportName='result'):
		if tag == "":
			tag = 'Untagged'
		if reportName == "":
			reportName = 'result'
		reportName = reportName + '.csv'
		csvHandler = CSVHandler()
		csvHandler.initializeCSV(header='IncidentNr;Date;AdditionalTags;StartedBy;Title', CSVtoLoad=f'./Reports/{tag}/{reportName}')
		csvHandler.addDataFromImageFolder(self.folder)
		csvHandler.saveLinesToCSV(pathToCSV=f'./Reports/{tag}/{reportName}')
		return f'Saved report to ./Reports/{tag}/{reportName}'

if __name__ == '__main__':
	app = QGuiApplication(sys.argv)
	#app.setWindowIcon(QIcon('./lib/images/calendar.png'))
	QQuickStyle.setStyle("Material")
	engine = QQmlApplicationEngine()

	qml_file = './lib/qml/gui.qml'
	engine.load(qml_file)

	sys.exit(app.exec())