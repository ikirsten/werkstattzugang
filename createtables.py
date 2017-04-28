#Script zum Anlegen der Datenbanktabellen für die Tuersteuerung

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
vorname NOT NULL VARCHAR (128);
nachname NOT NULL VARCHAR (128);
ams_mitglied NOT NULL VARCHAR (4);
ams_status VARCHAR (10) default NULL;
avd_mitglied NOT NULL VARCHAR (4) default 'Nein';
einzugsermaechtigung VARCHAR (1) defautl 'R';
rundschreiben_post VARCHAR (4) defautl 'Nein';
strasse VARCHAR (128) default NULL;
land VARCHAR (3) default 'DEU';
plz VARCHAR (8) default NULL;
ort VARCHAR (64) default NULL;
tel VARCHAR (64) default NULL;
mobil VARCHAR (64) default NULL;
email VARCHAR (128) default NULL;
geburtstag DATE;
ams_ein DATE;
ams_aus DATE;
avd_ein DATE;
avd_aus DATE;
vorl_ein DATE:
vorl_aus DATE;
aktive_ein DATE;
aktive_aus DATE;
alte_ein DATE;
alte_aus DATE;
ehren_ein DATE;
ehren_aus DATE;
aenderung VARCHAR(128);
anderungsdatum DATE);"""

c.execute(ams_mitglieder)


#Tabelle erstellen mit den UIDs der RFID Karten
cards = """
CREATE TABLE IF NOT EXISTS cards (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
ams_nr SMALLINT UNSIGNED,
cards_uid CHAR(8));"""

c.execute(cards)


#Tabelle mit Berechitungen erstellen
cards_userrights = """
CREATE TABLE IF NOT EXISTS cards (
ams_nr SMALLINT UNSIGNED PRIMARY KEY,
berechtigung VARCHAR (8));"""


#LOG Tabelle erstellen
werkelog = """
CREATE TABLE IF NOT EXISTS werkelog (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
datum DATE,
zeit TIME,
typ VARCHAR (32),
meldung CHAR;"""

c.execute(werkelog)

c.close()
db.close()
