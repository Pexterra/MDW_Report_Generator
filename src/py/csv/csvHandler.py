import cv2, os, pathlib, pandas as pd

from py.utils.incident import Incident

class CSVHandler(object):
	def CSVtoIncidents(self, csvFile, header='IncidentNr;Date;Involved;StartedBy;Title'):
		incidents : dict[int, Incident] = dict()
		if os.path.exists(csvFile):
			headerFound = False
			with open(csvFile) as f:
				for line in f:
					if header in line and not headerFound:
						headerFound = True
						continue
					data = line[:-1].split(';')
					inc = Incident()
					inc.setData(data[0], data[1], data[2], data[3], data[4])
					incidents[data[0]] = inc
		return incidents

	def saveToCSV(self, csv, saveTo = '_result.csv'):
		# creating directories if none existant
		if '/' in saveTo:
			directories = saveTo[:saveTo.rfind('/')]
			pathlib.Path(directories).mkdir(parents=True, exist_ok=True) 

		# saving csv
		with open(saveTo, "w") as text_file:
			text_file.write(csv)
		return saveTo

	def add_csv_to_excel(self, csv_filename, excel_filename):
		df = pd.read_csv(csv_filename, sep=';' ,encoding='latin-1')
		sheet_name = csv_filename[csv_filename.rfind('/')+1:csv_filename.rfind('.')]
		if not os.path.exists(excel_filename):
			with pd.ExcelWriter(excel_filename, mode='w') as writer:
				df.to_excel(writer, sheet_name=sheet_name, index=False)
		else:
			with pd.ExcelWriter(excel_filename, mode='a') as writer:
				df.to_excel(writer, sheet_name=sheet_name, index=False)