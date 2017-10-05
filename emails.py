import config #Konfigurationsdatei
import smtplib
from email.mime.text import MIMEText
import socket
socket.has_ipv6
import sys

#Script zum Versenden von E-Mails


def sendmail (recipient, subject, message):

	#Nachricht erzeugen
	msg = MIMEText(message)
	msg['From'] = config.email['sender']
	msg['To'] = recipient
	msg['Subject'] = '[AMS Werkstatt] ' + subject

	#SMTP Verbindung herstellen
	server = smtplib.SMTP(config.email['smtpserver'])
	
	#TLS
	server.starttls()
	
	#Login
	server.login(config.email['smtpuser'], config.email['smtppasswort'])

	#E-Mail senden
	server.sendmail(config.email['sender'], recipient, msg.as_string())
	
	server.quit()


##Testemail senden
#sendmail('ivan.kirsten@auik.de','TEST','TEST') 


#E-Mail deklarationen

wilkommen = "Hallo %s  \nwiklkommen in unserer Vereinswerkstatt. Bitte kontrolliere vor Arbeitsbeginn den Einwandfreien Zusatnd der Werkstatt in Bezug auf Sauberkeit, Muell und Werkzeug. Falls dies nicht der vollsten zufriedenheit entsprechen sollte, bitte umgehend den Werksattwart kontaktieren (Ivan, 0160/97940583)."

doorclose = "Hallo %s \nDu hast die aus der Werkstatt erfolgreich abgemeldet und wir hoffen, Dein Besuch war erfolgriech. Bitte melde umgehend dem Werkstattwart (Ivan 0160/97940583), wenn etwas kaputt gegangen ist. Gute Heimfahrt!"
