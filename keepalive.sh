#!/bin/bash
if ps -ef | grep -v grep | grep tuersteuerung.py ; then
   exit 0

else
   sudo python //home/pi/werkstattzugang/tuersteuerung.py &
   logger "Tuersteuerung neu gestartet"
   exit 0
fi
