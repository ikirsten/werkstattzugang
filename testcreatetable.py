#Script um das Anlegen einer Tabelle zu testen

import config #config file
import MySQLdb #MySQL connection library

db = MySQLdb.connect(	host=config.database['host'],
			user=config.dabase['username'],
			passwd=config.database['password'],
			db=config.dabatabe['databasename'])

c=db.cursor()
c.execute(CREATE TABLE [IF NOT EXISTS] tabellenname (id INT NOT NULL AUTO_INCREMENT, AMSID VARCHAR (128) NOT NULL default '');


