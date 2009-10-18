#!/usr/bin/python
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

#
import thread, threading, time, MySQLdb
from sord.art import *
from sord.functions import *
from sord.user import *
from sord.modules import *

from config import sord
from socket import *
myHost = ''
myPort = 6969
mySord = sord()


sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)

mySQLconn = MySQLdb.connect(host='localhost', db='sord', user='sord', passwd='dr0s')
mySQLcurs = mySQLconn.cursor()

IAC  = chr(255) # "Interpret As Command"
DONT = chr(254)
DO   = chr(253)
WONT = chr(252)
WILL = chr(251)
ECHO = chr(1)
LINEMODE = chr(34) # Linemode option

def now():				#Server Time
	return time.ctime(time.time())
	
		
def handleClient(connection):
	time.sleep(1)
	thisClientAddress = connection.getpeername()
	connection.send(IAC + DO + LINEMODE) # drop to character mode.
	connection.send(IAC + WILL + ECHO) # no local echo
	data = connection.recv(1024) # dump garbage.
	artwork = art()
	
	connection.send("Welcome to SORD\r\n")
	func_pauser(connection)
	#func_slowecho(connection, artwork.header())
	func_pauser(connection)
	
	quitter = False
	quitfull = False
	while ( not quitter ):
		func_slowecho(connection, artwork.banner(mySord,mySQLcurs))
		data = connection.recv(1)
		if not data: break
		if ( data == "Q" or data == "q" ):
			quitter = True
			quitfull = True
			func_slowecho(connection, "\r\nQuitting to the fields...\r\n\r\n")
		if ( data == "L" or data == "l" ):
			func_slowecho(connection, module_list(artwork, mySQLcurs, mySord.sqlPrefix()))
			pauser(connection)
		if ( data == "E" or data == "e" ):
			print 'User Logging In::' + str(thisClientAddress)
			quitter = True
			
	loggedin = False
	ittr = 0
	while ( not loggedin ):
		username = ""
		password = ""
		currentUser = ""
		ittr += 1
		if ( ittr > 3 ):
			func_slowecho(connection, func_casebold("\r\n\r\nDisconnecting - Too Many Login Attempts\r\n", 1))
			print 'Too Many Login Attemtps::' + str(thisClientAddress)
			connection.close()
			thread.exit()
		func_slowecho(connection, func_casebold("\r\n\r\nWelcome Warrior!  Enter Your Login Name (OR '\x1b[1m\x1b[31mnew\x1b[32m') :-: ", 2))
		username = func_getLine(connection, True)
		currentUser = sordUser(username)
		if ( currentUser.thisUserID > 0 ):
			func_slowecho(connection, func_casebold("\r\nPassword :-: ",2));  
			password = func_getLine(connection, False)
			password = password.strip()
			if ( password == currentUser.thisPassword ):
				loggedin = True
			else:
				func_slowecho(connection, func_casebold("\r\nIncorrect Password\r\n::"+password+"::", 1))
		else:
			if ( username == "new" ):
				func_slowecho(connection, func_casebold("\r\nNew User\r\n", 1))
			else:
				func_slowecho(connection, func_casebold("\r\nUser Name Not Found!\r\n",2))
				
	currentUser.login()
	print 'User Logged in::' + currentUser.thisFullname + ' ' + thisClientAddress
	
	while ( not quitfull ):
		data = connection.recv(1)
		if not data: break
		if ( data == "\n" ):
			connection.send("NewLine")
		if ( data == "\r" ):
			connection.send("Return")
		func_slowecho(connection, ('Echo=>' + data))

	currentUser.logout()	
	connection.close()
	print 'Thread Disconnected::' + str(thisClientAddress)
	
def dispatcher():
	while True:
		connection, address = sockobj.accept()
		print 'Server connected by', address, 
		print 'at', now()
		thread.start_new(handleClient, (connection,))
			
dispatcher()
