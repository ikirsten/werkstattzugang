#--import---
import config #config file

import os #OS module
import MySQLdb #MySQL connection library 
import rfidiot
import time


#getuid
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


#Datennbankverbindung herstellen
db = MySQLdb.connect(	host=config.database['host'],
			user=config.database['username'],
			passwd=config.database['password'],
			db=config.database['databasename'])	
c=db.cursor()
	
#Werte von User abfragen
ams = int(input("AMS-Mitgliedsnummer: "))

role = raw_input("Berechtigung: ")

carduid = getuid()
print(carduid)

#Karte in cards hinzufuegen
adduser = """
INSERT INTO cards (
ams_nr, cards_uid)
Values
(%s, %s); """


setuserrights = """
INSERT INTO cards_userrights (
ams_nr, berechtigung)
Values
(%s, %s); """


c.execute(adduser, (ams,carduid))
c.execute(setuserrights, (ams,role))
db.commit()
