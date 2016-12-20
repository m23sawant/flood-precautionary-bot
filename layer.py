# -*- coding: utf-8 -*-
import os, subprocess, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.common.tools                               import Jid                               #is writing, writing pause
allowedPersons=['YYXXXXXXXXXX'] #Filter the senders numbers with country code without +
ap = set(allowedPersons)

name = "Whatsapp Name"
filelog = "/root/.yowsup/Not allowed.log"

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            time.sleep(0.5)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            time.sleep(0.5)
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            time.sleep(0.5)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set is writing
            time.sleep(2)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set no is writing
            time.sleep(1)
            self.onTextMessage(messageProtocolEntity) #Send the answer
            time.sleep(3)
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print entity.ack()
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify()
        message    = messageProtocolEntity.getBody().lower()
        recipient  = messageProtocolEntity.getFrom()
        textmsg    = TextMessageProtocolEntity

        #For a break to use the character \n
        #The sleep you write so #time.sleep(1)

        if messageProtocolEntity.getFrom(False) in ap:
            if message == 'hi':
                answer = "Hi "+namemitt+" " 
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'what can you do':
                answer = "Hi "+namemitt+"\n\nYou can ask me these things:\n\nTemperature\nDistance of water from top\nStatus"
                self.toLower(textmsg(answer, to = recipient ))
                print answer

            elif message == 'temperature':
                t=float(subprocess.check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)[:-1])
                ts=str(t)
                answer = 'My temperature is '+ts+' °C'
                self.toLower(textmsg(answer, to = recipient ))
                print answer

	    elif message == 'distance' or  'status':
		GPIO.setmode(GPIO.BCM)
		TRIG = 23 
		ECHO = 24
		print "Distance Measurement In Progress"
		GPIO.setup(TRIG,GPIO.OUT)
		GPIO.setup(ECHO,GPIO.IN)
		GPIO.output(TRIG, False)
		print "Waiting For Sensor To Settle"
		time.sleep(2)
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		while GPIO.input(ECHO)==0:
		  pulse_start = time.time()
		while GPIO.input(ECHO)==1:
		  pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
	        if (distance<20):
			status='The area is Unsafe !!!'
		else:
			status='The area is Safe :D' 
		print "Distance:",distance,"cm"
		GPIO.cleanup()
		if (message=='distance'):
		
			answer = 'The distance of water from top is %fcm'%distance
		else:
			answer = status
		self.toLower(textmsg(answer,to=recipient))
		print answer
		
	    else:
                answer = "Sorry "+namemitt+", I can not understand what you're asking me.\n Try : 'what can you do'" 
                self.toLower(textmsg(answer, to = recipient))
                print answer

        else:
            answer = "Hi "+namemitt+", I'm sorry, but you're not subscribed.\nPlease follow our social media accounts\nFacebook: goo.gl/q9aF53\nTwitter: goo.gl/JoXSC2"
            time.sleep(20)
            self.toLower(textmsg(answer, to = recipient))
            print answer
            out_file = open(filelog,"a")
            out_file.write("------------------------"+"\n"+"Sender:"+"\n"+namemitt+"\n"+"Number sender:"+"\n"+recipient+"\n"+"Message text:"+"\n"+message+"\n"+"------------------------"+"\n"+"\n")
            out_file.close()
