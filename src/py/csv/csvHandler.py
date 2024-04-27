import cv2, os, pathlib, xlsxwriter, pandas as pd

from py.utils.incident import Incident

class CSVHandler(object):
	def CSVtoIncidents(self, csvFile, header='IncidentNr;Date;Involved;StartedBy;Title'):
		incidents : dict[int, Incident] = dict()
		if os.path.exists(csvFile):
			headerFound = False
			with open(csvFile) as file:
				for line in file:
					if header in line and not headerFound:
						headerFound = True
						continue
					data = line[:-1].split(';')
					incident = Incident()
					incident.setData(data[0], data[1], data[2], data[3], data[4])
					incidents[data[0]] = incident
		return incidents

	def saveToCSV(self, csv: str, path: str):
		# creating directories if none existant
		if '/' in path:
			directories : str = path[:path.rfind('/')]
			pathlib.Path(directories).mkdir(parents=True, exist_ok=True) 

		# saving csv
		with open(path, "w") as csvFile:
			csvFile.write(csv)
		return path

	def createOverviewSheet(self, csv_filenames, excel_filename, officersWithIncidents, outputFn):

		# Create a new Excel writer object
		with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:

			df = pd.DataFrame.from_dict(officersWithIncidents, orient='index', columns=['involved', 'started'])
			df.to_excel(writer, sheet_name='Overview')

			worksheet = writer.sheets['Overview']
		
			# adding hyperlinks to sheets
			for idx, sheet_name in enumerate(df.index):
				cell_ref = 'A{}'.format(idx + 2)  # Row index starts from 2 (header is on row 1)
				identifier = f'{sheet_name}'
				worksheet.write_url(cell_ref, f'internal:\'{sheet_name}\'!A1', string=identifier)

			outputFn(f'Created excel file with overview [../Reports/Incidents/Incidents.xlsx]')

			for file in csv_filenames:
				sheetName = file[file.rfind('/')+1:file.rfind('.')]
				df = pd.read_csv(file, sep=';' ,encoding='latin-1')
				df.to_excel(writer, sheet_name=sheetName, index=False)
				outputFn(f'Added sheet "{sheetName}" to Excel file [../Reports/Incidents/Incidents.xlsx]')