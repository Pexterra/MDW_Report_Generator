from datetime import datetime

class Incident(object):
	def __init__(self):
		self.ID : int = 0
		self.date : datetime
		self.involvedOfficers : str = ""
		self.startedBy : str = ""
		self.title : str = ""

	def setData(self, ID, date, involvedOfficers, startedBy, title):
		self.ID = ID
		self.date = date
		self.involvedOfficers = involvedOfficers
		self.startedBy = startedBy
		self.title = title