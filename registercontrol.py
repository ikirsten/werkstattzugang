import config # configurationsdatei aufrufen
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

def pinsetup(register):
	if register == 'tuer':
		GPIO.setup(config.pinstuer['registerser'], GPIO.OUT)
		GPIO.setup(config.pinstuer['registersck'], GPIO.OUT)
		GPIO.setup(config.pinstuer['registerrck'], GPIO.OUT)



def writepins(register, output):

        sleep=0.01

        if register == 'tuer':
                ser = config.pinstuer['registerser']
                sck = config.pinstuer['registersck']
                rck = config.pinstuer['registerrck']

        if register == 'monitoring':
                #Pins eintragen
		print('nichts definiert')


        #Werte ins register Speichern
	for i in (range(0,8)):
                GPIO.output(ser,output[i])
                time.sleep(sleep)
                GPIO.output(sck, 1)
                time.sleep(sleep)
                GPIO.output(sck,0)

        #Register schallten
        GPIO.output(rck,1)
        time.sleep(sleep)
        GPIO.output(rck,0)


#Test

#test = (1,0,1,0,1,0,0,1)
#test2 = (1,0,0,1,0,1,0,1)
#test3 = (1,0,1,0,0,0,0,0)
#
#pinsetup('tuer')

#writepins('tuer',test)

#time.sleep(4)
#print('Nachste Stellung')

#writepins('tuer',test2)
#time.sleep(4)

#print('kritischer test')
#writepins('tuer',test3)
#time.sleep(2)

#print('ausgang')
#writepins('tuer', test)

#while True:
#	writepins('tuer', test)
#	writepins('tuer', test2)




#GPIO.cleanup()
