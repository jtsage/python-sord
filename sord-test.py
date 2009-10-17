#!/usr/bin/python
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

#
import thread, time
from sord.art import *
from sord.functions import *
from config import sord
from socket import *
myHost = ''
myPort = 6969
mySord = sord()

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)

IAC  = chr(255) # "Interpret As Command"
DONT = chr(254)
DO   = chr(253)
WONT = chr(252)
WILL = chr(251)
LINEMODE = chr(34) # Linemode option

def pauser(connection):
	#data = connection.recv(1024) #clear buffer
	slowwrite(connection, func_casebold("\n    :-: Press Any Key :-:", 2))
	pauser_quit = False
	while ( not pauser_quit ):
		data = connection.recv(5)
		if not data: break
		pauser_quit = True
		connection.send("\n")

def slowwrite(connection, data):
	for thisData in list(data):
		time.sleep(0.001)
		connection.send(thisData)

def now():				#Server Time
	return time.ctime(time.time())
	
		
def handleClient(connection):
	time.sleep(1)
	connection.send(IAC + DO + LINEMODE) # drop to character mode.
	data = connection.recv(1024) # dump garbage.
	artwork = art()
	connection.send("Welcome to SORD\n")
	slowwrite(connection, artwork.line())
	pauser(connection)
	slowwrite(connection, artwork.banner(mySord))
	slowwrite(connection, artwork.header())
	while True:
		data = connection.recv(1)
		if not data: break
		slowwrite(connection, ('Echo=>' + data))
	connection.close()
	print 'Thread Disconnected'
	
def dispatcher():
	while True:
		connection, address = sockobj.accept()
		print 'Server connected by', address, 
		print 'at', now()
		thread.start_new(handleClient, (connection,))
			
dispatcher()
