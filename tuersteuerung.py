#--import---
import config #config file
import registercontrol #74HC595 Big Banging Steuerung
import emails #Scrpit fuer das Versenden von E-Mails

import os #OS module
import MySQLdb #MySQL connection library 
import time #time module
import holidays # python library holdiays
import rfidiot #rfidiot library zur Steurung des Readers und autom. auslesen der UID
import smtplib #Library zum versenden von E-mails

from datetime import date

import RPi.GPIO as GPIO #Library zur Ansteuerung der Pins





###GPIO Steuerung

#Setzte Physikalische Pin Nummerierung
GPIO.setmode(GPIO.BOARD)

#PIN Definitionen
GPIO.setup(config.pinstuer['tuerstatus'], GPIO.IN) # TUER Input
GPIO.setup(config.pinstuer['notschalter'], GPIO.IN) #Notschlater Input
GPIO.setup(config.pinstuer['tuertaster'], GPIO.IN) #Taster Tuer
registercontrol.pinsetup('tuer')





##Defintion der Funktionen
#Uid aus Cardreader lesen
def getuid():
	card=rfidiot.card
	card.select()

	#LED READER gruen schalten 
	global reader 
	reader = 'green'
	registercontrol.writepins('tuer', tuerreginput())
	
	#Schleife - wenn keine uid vorhanden so lange lesen bis uid vorhanden, nach jedem Versuch 0.1 sek warten
	while not card.uid:
		card=rfidiot.card
		card.select()
		time.sleep(0.1)

	card=rfidiot.card
	card.select()

	#LED READER rot schalten
	reader = 'red'
	registercontrol.writepins('tuer', tuerreginput())

	return card.uid

def tuerreginput():
	if reader == 'red':
		r3 = [1,0]
	if reader == 'green':
		r3 = [0,1]
	if tuerstatus == 'red':
		r4 = [1,0]
	if tuerstatus == 'green':
		r4 = [0,1]
	if tuerstatus == 'off':
		r4 = [0,0]
	if notschalter == 'red':
		r5 = [1,0]
	if notschalter == 'green':
		r5 = [0,1]
	#print(tuerctl)
	#print(r5+r4+r3+warnlicht+tuerctl)
	return(r5+r4+r3+warnlicht+tuerctl)

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


#Funktion zum oeffnen der Tuer
def dooropen():
	global tuerctl
	global warnlicht
	print('Tuer geoeffnet fuer: ' + user[0])
	
	#Tuer oeffnen
	tuerctl = [1] #Tuer offen
	registercontrol.writepins('tuer', tuerreginput())

	print(user[0])
	print(user[2])
	print(emails.wilkommen % user[0])
	
	#Ins Log schreiben
	c.execute(log_control, 'Tuer fuer: ' + user[0] + 'freigegeben')
	db.commit()
	
	#Wilkommnesemail senden
	emails.sendmail(user[2], 'Wilkommen in der Werkstatt', emails.wilkommen % (user[0]))


	while not GPIO.input(config.pinstuer['tuertaster']):
		print('Schleife Tuer')
		#Wenn Zeit kurz vor Ende, Warnlicht anschalten
		if not timecheck ():
			warnlicht = [0]
			registercontrol.writepins('tuer', tuerreginput())
			
			#warnlicht wieder ausschalten
			#warnlicht = [1]
			#registercontrol.writepins('tuer', tuerreginput())
		time.sleep(1)
		
	
	#Wenn Schalter gedrueckt wurde:
	warnlicht = [0] #Warnlicht an
	doorclose()
	registercontrol.writepins('tuer', tuerreginput())
	#Tuer Schliessen	
	#Display beschriften

def doorclose():
	global tuerstatus
	global tuerctl
	global warnlicht
	
	#Warten, bis Tuer geoeffnet --> LED Tuer blinkt
	while GPIO.input(config.pinstuer['tuerstatus']):
		time.sleep(0.5)
		tuerstatus = 'red'
		registercontrol.writepins('tuer', tuerreginput())
		time.sleep(0.5)
		tuerstatus = 'off'
		registercontrol.writepins('tuer', tuerreginput())
	
	#Wenn Tuer geoeffnet --> LED TUER leuchtet rot
	time.sleep(0.5)
	tuerstatus = 'red'
	registercontrol.writepins('tuer', tuerreginput())
	
	#Warten bis Tuer geschlossen
	while not GPIO.input(config.pinstuer['tuerstatus']):
		time.sleep(0.1)
	
	time.sleep(2)	
	#Strom auf Tuer geben und Warnlicht ausschalten
	tuerstatus = 'red'
	tuerctl = [0] #Tuer zu
	warnlicht = [1] #Warnlicht aus
	registercontrol.writepins('tuer', tuerreginput())

	emails.sendmail(user[2], 'Auf Wiedersehen in der Werkstatt', emails.doorclose % (user[0]))

	print('Tuer Schliessen')
	


def showblinkcodes (anzahl):
	global warnlicht
	global tuerctl
	for y in range(0,anzahl):
		time.sleep(0.5)
		registercontrol.writepins('tuer', [0,0,0,0,0,0]+warnlicht+tuerctl)
		time.sleep(0.5)
		registercontrol.writepins('tuer', tuerreginput())



##Eventprozedur


##Eventdeklarationen
def tueraufzu(x):
	global tuerstatus
	time.sleep(0.1)
	if GPIO.input(x):
		tuerstatus = 'off'
	else:
		#Tuer offen
		tuerstatus = 'green'
		#Pruefen, ob Anmeldung vorliegt
		if tuerctl == [0]:
			#Fehler im System
			print("Tuer ohne anmeldung geoeffnet")
			c.execute(log_carderror,('TUER OHNE ANMELDUNG OFFEN'))
			showblinkcodes(10)
			#E-Mail senden
			emails.sendmail(config.email['werkstattwart'], 'TUER OHNE ANMELDUNG OFFEN', 'Tuer wurde geoeffnet, ohne dass eine Anmeldung erfolgte')
		
	
	registercontrol.writepins('tuer', tuerreginput())
	print('Tuerstatus veraendert :' , GPIO.input(x))


#Beispieldeklaration
GPIO.add_event_detect(config.pinstuer['tuerstatus'], GPIO.BOTH, callback = tueraufzu, bouncetime = 1000)
#GPIO.add_event_detect(config.pinstuer['tuerstatus'], GPIO.FALLING, callback = tuerauf, bouncetime = 200)




##Initialisierung
tuerctl = [0] #Tuer zu
warnlicht = [1] #Warnlicht aus
reader = 'red'
tuerstatus  = 'red'
notschalter = 'red'
if not GPIO.input(config.pinstuer['tuerstatus']):
	tuerstatus = 'green'
if GPIO.input(config.pinstuer['notschalter']):
	notschalter = 'green'
registercontrol.writepins('tuer',tuerreginput())












##Database Connection Object
#Benutzt Daten aus der config Datei, um eine Verbindung zur Datenbank herzustellen
db = MySQLdb.connect(	host=config.database['host'],
			user=config.database['username'],
			passwd=config.database['password'],
			db=config.database['databasename'])

#Cursor Object
c=db.cursor()











##LOG Definitionen
#LOG Scritpstart
log_scriptstart = """
INSERT INTO werkelog (
typ, meldung)
Values
('TUERSYSTEM', 'Script wurde gestartet');"""

#LOG Karte gelesen
log_cardread = """
INSERT INTO werkelog (
typ, meldung)
Values
('TUER', 'Karte gelesen: ' %s);"""

#Log root Karte verwendet
log_rootcard = """
INSERT INTO werkelog (
typ, meldung)
Values
('TUER', 'ROOT Card: ' %s ' gelesen.');"""

#Log Kartenfehler
log_carderror ="""
INSERT INTO werkelog (
typ, meldung)
VALUES
('TUER', 'ERROR: ' %s);""" 

#Easylog
log_control ="""
INSERT INTO werkelog (
typ, meldung)
VALUES
('TUER', %s);"""


##SQL Suchabrfagen Definition

#Karten UID Suchen und AMSID ausgaben
search_uid = """
SELECT ams_nr FROM cards WHERE cards_uid = %s"""

#Berechtigungen der AMSID suchen
search_permission = """
select berechtigung FROM cards_userrights WHERE ams_nr = %s"""

#User der AMSID suchen
search_user = """
select vorname, nachname, email, mobil FROM ams_mitglieder WHERE ams_nr = %s"""










#Testablauf


showblinkcodes(1)

#Log scriptstart schreiben und E-Mail senden
c.execute(log_scriptstart)
db.commit()
emails.sendmail(config.email['werkstattwart'],'Tuersteuerung gestartet','Die Tuersteuerung der Werkstatt wurde gestartet')


#Dauerschleife initalisieren
try:
	while True:
	
		#Karte lesen und in Varibale schreiben. Danach ist Leser deaktiviert
		card = getuid()
		
		#Gelesene Karte in Log-Datenbank schreiben
		c.execute(log_cardread, (card))
		db.commit()		
		
		#Pruefen ob root Karte
		if card in config.mastercards:
			user = 'MASTER', config.mastercards[card]
			dooropen()
		
			#Ins Log schreiben
			c.execute(log_rootcard, (config.mastercards[card]))
			db.commit()
		
		
			##--- E-Mail versenden
			print(user[0])
			##--- LEDs steuern	
	
		else:
			#Pruefen, ob uid in DB und attribute eruieren
			if c.execute(search_uid, (card)):
			
				#Folgendes wird ausgefuert, wenn Karte gefunden wurde
				
				#Wenn UID in DB, amsid abfragen
				amsnr = str(c.fetchone()[0])
				print(amsnr)	
	
				#Berechtigung pruefen und Abfragen
				if c.execute(search_permission, (amsnr)):
					permission = str(c.fetchone()[0])
					#print(permission)
				else:
					#Fehler ins Log schreiben: keine Berechtigungen definiert
					c.execute(log_carderror, ('Keine Berechtigung fuer KARTE: ' + card +  'und AMS NR: ' + amsnr + ' definiert.'))
					db.commit()
					showblinkcodes(5)
			
				#Daten aus AMS Datenbank ababfragen
				if c.execute(search_user, (amsnr)):
					user = c.fetchall()[0]
					#print(user[0] + ' ' + user[1] + ' ' + user[2] + ' ' + user[3])
				else:
					print("Fehler")
					#Fehler ins log schreiben
					c.execute(log_carderror, ('Keine AMS Daten fuer KARTE: ' + card + ' und AMS NR: ' + amsnr + 'definiert'))
					db.commit()
					showblinkcodes(6)
			
			
				#Tueroffnungsszenarien nach Berechtigung
				
				#Admin
				if permission == 'admin':
					dooropen()
				
				#ams
				if permission == 'ams':
					if timecheck ():
						dooropen()
					else:
						print("Ausserhalb oeffnungszeiten")
						showblinkcodes(3)
						#Blinccodes Tuer
		
				#gesperrt
				if permission == 'gesperrt':
					print()
					showblinkcodes(4)
			
	
		
			else:
		
				#Zu der ueberprueften Karte konnte kein Eintrag gefunden werden
				c.execute(log_carderror, ('Karte: ' + card + ' wurde nicht gefunden'))
				db.commit()
				print("Karte nicht erkannt")
				showblinkcodes(2)
				#Rueckmeldung blikncodes Tuer
			
		

		print(card)
	


finally:
	GPIO.cleanup()
	c.close()
	db.close()
