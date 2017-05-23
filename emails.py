import config #Konfigurationsdatei

#Script zum Versenden von E-Mails


def sendmail (recipient, subject, message):

	#Nachricht erzeugen
	msg = MIMEText(message)
	msg['From'] = config.email['sender']
	msg['To'] = recipient
	msg['Subject'] = subject

	#SMTP Verbindung herstellen
	server = smtplib.SMTP(config.email['smtpserver'])
	
	#TLS
	if usetls
		server.starttls()
	
	#Login
	server.login(config.email
