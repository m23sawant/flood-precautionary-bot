#!/usr/bin/env python
import sys,smtplib,datetime,os
from twython import Twython
CONSUMER_KEY = '<Your Consumer Key>'
CONSUMER_SECRET = '<Your Consumer Secret>'
ACCESS_KEY = '<Your Access Key>'
ACCESS_SECRET = '<Your Access Secret>'
smtpUser='<Email id which you will use to send email>'
smtpPass='<Email id password>'
toAdd='<Email id to whome you have to send the email>'
fromAdd='<Email id which you will use to send email>'
subject='Flood Warning'
header='To: '+ toAdd + '\n' + 'From: ' +fromAdd + '\n' + 'Subject: ' + subject
s=smtplib.SMTP('smtp.gmail.com',587)
now = datetime.datetime.now().time()
tym = datetime.datetime.now(tz=None)
tyme=now.isoformat()
s.ehlo()
s.starttls()
s.ehlo()
s.login(smtpUser, smtpPass)
api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 23 
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
while(True):
        tim=datetime.datetime.now()
	GPIO.output(TRIG, False)
    	print "Waiting For Sensor To Settle"
    	time.sleep(5)
    	GPIO.output(TRIG, True)
    	time.sleep(0.00001)
    	GPIO.output(TRIG, False)
    	while GPIO.input(ECHO)==0:
      	  pulse_start = time.time()
    	while GPIO.input(ECHO)==1:
    	  pulse_end = time.time()
    	pulse_duration = pulse_end - pulse_start
    	distance = pulse_duration * 17150
    	distance = round(distance)
	print(distance)
	if(distance<20):
		api.update_status(status='Please Stay Away. Distance= %dcm at %s'%(distance,tim))
		body='Stay Away. Distance from top= %dcm'%distance
		s.sendmail(fromAdd, toAdd, header + '\n\n' +body)
GPIO.cleanup()
