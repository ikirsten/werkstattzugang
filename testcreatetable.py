#Script um das Anlegen einer Tabelle zu testen

import config #config file
import MySQLdb #MySQL connection library

db = MySQLdb.connect(	host=config.database['host'],
			user=config.database['username'],
			passwd=config.database['password'],
			db=config.database['databasename'])

c=db.cursor()

#c.execute("""CREATE TABLE [IF NOT EXISTS] test ( 
#id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
#AMSID VARCHAR (128) NOT NULL default '');""");

tablecreation = """
CREATE TABLE IF NOT EXISTS werketest (
ams_id INTEGER PRIMARY KEY,
cards_uid CHAR(8));"""
c.execute(tablecreation)


sql_command = """
CREATE TABLE IF NOT EXISTS employee ( 
staff_number INTEGER PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1), 
joining DATE,
birth_date DATE);"""

c.execute(sql_command)


c.close()
db.close()
