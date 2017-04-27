#--import---
import config #config file

import os #OS module
import MySQLdb #MySQL connection library 
import time #time module
import holidays # python library holdiays
import rfidiot


from datetime import date


#Uid aus Cardreader lesen
def getuid():
	card=rfidiot.card
	card.select()
	
	#Schleife - wenn keine uid vorhanden so lange lesen bis uid vorhanden, nach jedem Versuch 0.1 sek warten
	while not card.uid:
		card=rfidiot.card
		card.select()
		time.sleep(0.1)

	card=rfidiot.card
	card.select()
	return card.uid
	


def timecheck():

	#Werktag pruefen	
	if time.strftime("%w") == '0': #Sonntag
		check = 0
		return (bool(check))
	
	elif time.strftime("%w") > '0' and time.strftime("%w") < '6': #Werktags
		start	= config.accesstimes['startweekdays']
		end	= config.accesstimes['endweekdays']

	
	elif time.strftime("%w") == '6': #Samstag 
		start	= config.accesstimes['startsaturday']
		end	= config.accesstimes['endsaturday']
	
	#Pruefen der Uhrzeit	
	if  time.strftime("%H:%M") < end and start < time.strftime("%H:%M"):
		if time2min(end) - time2min(time.strftime("%H:%M")) > time2min(config.accesstimes['endbefore']):
			
			#Wenn Uhrzeit passt, pruefen ob Feiertag mit libary holidays
			if not date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d"))) in config.accesstimes['feiertage']:
				check = 1	#Ausgabe, wenn im Zeitraum
		else:
			check = 0	#Ausgabe, wenn zu knapp vor Ende
	else:
		check = 0	#Ausgabe, wenn nicht in Zeitraum

	#Rueckgabe des Ergebniss	
	return bool(check)

def time2min(x):
   return reduce(lambda a, b: 60 * int(a) + int(b), x.split(':'))




##Database Connection Object
#Benutzt Daten aus der config Datei, um eine Verbindung zur Datenbank herzustellen
db = MySQLdb.connect(	host=config.database['host'],
			user=config.dabase['username'],
			passwd=config.database['password'],
			db=config.dabatabe['databasename'])





####Test
print(getuid())
