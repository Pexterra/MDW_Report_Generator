import sys, os

from datetime import timedelta
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

from py.reportGenerator import ReportGenerator

if __name__ == '__main__':
	app = QGuiApplication(sys.argv)
	QQuickStyle.setStyle("Material")
	engine = QQmlApplicationEngine()

	qml_file = './qml/ReportGenerator.qml'
	engine.load(qml_file)

	sys.exit(app.exec())