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


#Pindeklarationen (GPIO = Board --> Pysikalische Pinnummern)
pinstuer = dict(
	tuerstatus	= 7,	#Eingang Tuer (Offen/Zu)
	tuertaster	= 12,	#Eingang Taster zum Abmelden
	notschalter	= 16,	#Eingang Statusueberwachung Notschalter
	registerser	= 11,	#Register Serieller Eingang
	registersck	= 13,	#Register Schiebetakt
	registerrck	= 15,	#Register Speichertakt
)

#E-Mail Einstellungen
email = dict(
	werkstattwart	= 'werkstattwart@amsev.de', #Weiterleitung auf aktuellen Werkstattwart
	vorstand	= 'vorstand@amsev.de',	#Benachrichtigung des Vorstands
	sender		= 'werkstatt@amsev.de', #Absender
	smtpserver	= 'amsev.de'
	smtuser		= 'werkstatt@amsev.de'
	smtppasswort	= 'vp0a^6C3'


#Pfad AMS-Daten
amsdaten = 'AMS_Daten.xlsx'
