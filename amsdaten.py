#Script liest die Daten aus der AMS-Excel Tabelle und schreibt sie in die Datenbank. Alle Daten aus der Datenbank werden zuvor geloescht.

#import
import config #Konfigurationsdatei

from openpyxl import load_workbook #Modul um Excel Dateien zu lesen
import MySQLdb #Modul fuer die Datenbankverbindung



#Datenbank Connection Module
db = MySQLdb.connect(	host=config.database['host'],
			user=config.database['username'],
			passwd=config.database['password'],
			db=config.database['databasename'])

#Datenbank Cursor
c=db.cursor()

#Workbook Oeffnen
wb = load_workbook(filename = config.amsdaten)
#Arbeitsblatt auswaehlen
ab = wb['AMS-Daten']

print(ab.cell(row=100, column=1).value)
