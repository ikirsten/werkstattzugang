#Script zum Anlegen der Datenbanktabellen fuer die Tuersteuerung

import config #config file
import MySQLdb #MySQL connection library

db = MySQLdb.connect(	host=config.database['host'],
			user=config.database['username'],
			passwd=config.database['password'],
			db=config.database['databasename'])

c=db.cursor()

#Tabelle erstellen mit den Daten der Mitgliederliste
ams_mitglieder = """
CREATE TABLE IF NOT EXISTS ams_mitglieder (
ams_nr SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
vorname VARCHAR (128) NOT NULL,
nachname VARCHAR (128) NOT NULL,
ams_mitglied VARCHAR (4) NOT NULL,
ams_status VARCHAR (10) default NULL,
avd_mitglied VARCHAR (4) NOT NULL default 'Nein',
einzugsermaechtigung VARCHAR (1) default 'R',
rundschreiben_post VARCHAR (4) default 'Nein',
strasse VARCHAR (128) default NULL,
land VARCHAR (3) default 'DEU',
plz VARCHAR (8) default NULL,
ort VARCHAR (64) default NULL,
tel VARCHAR (64) default NULL,
mobil VARCHAR (64) default NULL,
email VARCHAR (128) default NULL,
geburtstag DATE,
ams_ein DATE,
ams_aus DATE,
avd_ein DATE,
avd_aus DATE,
vorl_ein DATE,
vorl_aus DATE,
aktive_ein DATE,
aktive_aus DATE,
alte_ein DATE,
alte_aus DATE,
ehren_ein DATE,
ehren_aus DATE,
aenderung VARCHAR(128),
anderungsdatum DATE);"""

c.execute(ams_mitglieder)


#Tabelle erstellen mit den UIDs der RFID Karten
cards = """
CREATE TABLE IF NOT EXISTS cards (
ams_nr SMALLINT UNSIGNED NOT NULL,
cards_uid CHAR(16) NOT NULL PRIMARY KEY);"""

c.execute(cards)


#Tabelle mit Berechitungen erstellen
cards_userrights = """
CREATE TABLE IF NOT EXISTS cards_userrights (
ams_nr SMALLINT UNSIGNED PRIMARY KEY,
berechtigung VARCHAR (16));"""

c.execute(cards_userrights)

#Log Tabelle loeschen
#deletewerkelog = """
#Drop TABLE werkelog; """

#c.execute(deletewerkelog)

#LOG Tabelle erstellen
werkelog = """
CREATE TABLE IF NOT EXISTS werkelog (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
log_datum TIMESTAMP NOT NULL DEFAULT NOW(),
typ VARCHAR (32),
meldung VARCHAR (128));"""

c.execute(werkelog)


c.close()
db.close()
