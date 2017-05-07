import holidays

#---Access times---

accesstimes = dict(
	feiertage	= holidays.DE(prov='BW'),
	startweekdays	= '07:00', #Starttime on weekdays
	endweekdays	= '21:30', #Endtime on weekdays
	startsaturday	= '08:00', #Starttime on saturdays
	endsaturday	= '18:00', #Endtime on saturdays
	endbefore	= '00:10', #Letzerzugang vor Ende Eintrittszeit
)

#Karten, die ohne pruefung zur oeffnung der Tuer fuehren
mastercards = {'63827184': 'Karte 1',}


database = dict(
	username	= 'testamspi',
	password	= 'Qnu4g34!',
	host		= 'amsev.de',
	databasename	= 'testwerke',
)

#Pfad AMS-Daten
amsdaten = 'AMS_Daten.xlsx'
