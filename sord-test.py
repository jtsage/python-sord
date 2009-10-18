#!/usr/bin/python
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

#
import thread, threading, time, MySQLdb
from sord.art import *
from sord.functions import *
from sord.user import *
from sord.modules import *
from sord.menus import *

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
SORDDEBUG = True

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
	if ( not SORDDEBUG ):
		func_slowecho(connection, artwork.header())
		func_pauser(connection)
	
	quitter = False
	quitfull = False
	if ( SORDDEBUG):
		quitter = True
	while ( not quitter ):
		func_slowecho(connection, artwork.banner(mySord,mySQLcurs))
		data = connection.recv(1)
		if not data: break
		if ( data == "Q" or data == "q" ):
			quitter = True
			quitfull = True
		if ( data == "L" or data == "l" ):
			func_slowecho(connection, module_list(artwork, mySQLcurs, mySord.sqlPrefix()))
			pauser(connection)
		if ( data == "E" or data == "e" ):
			print 'User Logging In::' + str(thisClientAddress)
			quitter = True
			
	loggedin = False
	ittr = 0
	if ( SORDDEBUG ):
		loggedin = True
		currentUser = sordUser('jtsage')
		
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
				func_slowecho(connection, func_casebold("\r\nIncorrect Password\r\n", 1))
		else:
			if ( username == "new" ):
				func_slowecho(connection, func_casebold("\r\nNew User\r\n", 1))
			else:
				func_slowecho(connection, func_casebold("\r\nUser Name Not Found!\r\n",2))
				
	currentUser.login()
	print 'User Logged in::' + currentUser.thisFullname + ' ' + str(thisClientAddress)
	
	if currentUser.isDead() :
		quitfull = 2
		func_slowecho(connection, func_casebold("\r\nI'm Afraid You Are DEAD Right Now.  Sorry\r\n", 1))
		
	if ( not quitfull ):
		if ( not SORDDEBUG ):
			func_slowecho(connection, module_dailyhappen(True, mySQLcurs, mySord.sqlPrefix()))
			func_pauser(connection)
			func_slowecho(connection, module_who(artwork, mySQLcurs, mySord.sqlPrefix()))
			func_pauser(connection)
			func_slowecho(connection, module_viewstats(artwork, currentUser))
			func_pauser(connection)
	
	while ( not quitfull ):
		if ( not currentUser.expert ):
			func_slowecho(connection, menu_mainlong(artwork, currentUser, True))
		func_slowecho(connection, menu_mainshort(currentUser))
		data = connection.recv(2)
		if not data: break
		if ( data[0] == "q" or data[0] == "Q" ):
			quitfull = True
		if ( data[0] == "x" or data[0] == "X" ):
			currentUser.toggleXprt()
		if ( data[0] == "v" or data[0] == "V" ):
			func_slowecho(connection, module_viewstats(artwork, currentUser))
			func_pauser(connection)
		if ( data[0] == "d" or data[0] == "D" ):
			func_slowecho(connection, module_dailyhappen(True, mySQLcurs, mySord.sqlPrefix()))
			func_pauser(connection)
		if ( data[0] == "?" ):
			if ( currentUser.expert ):
				func_slowecho(connection, menu_mainlong(artwork, currentUser, True))
		if ( data[0] == "p" or data[0] == "P" ):
			func_slowecho(connection, module_who(artwork, mySQLcurs, mySord.sqlPrefix()))
			func_pauser(connection)
		if ( data[0] == "l" or data[0] == "L" ):
			func_slowecho(connection, module_list(artwork, mySQLcurs, mySord.sqlPrefix()))
			func_pauser(connection)
			
		"""
		case 'A': // ABDULS ARMOR
			module_abduls(); break;
		case 'K': // KING ARTHURS WEAPONS
			module_arthurs(); break;
		case 'Y': // THE BANK
			module_bank(); break;
		case 'H': // HEALERS HUT
			module_heal(); break;
		case 'F': // THE FOREST
			module_forest(); break;
		case 'M': // MAKE ANNOUNCMENT
			module_announce(); break;
		case 'W': // SEND MAIL MESSAGE
			control_sendmail($userid); break;
		case 'I': // RED DRAGON INN
			inn_logic(); break;
		case 'T': // WARRIOR TRAINING
			module_turgon(); break;
					
		if ( data == "\n" ):
			connection.send("NewLine")
		if ( data == "\r" ):
			connection.send("Return")
			quitfull = True
		func_slowecho(connection, ('Echo=>' + data))
"""
	func_slowecho(connection, func_casebold("\r\n\r\n   Quitting to the Fields... GoodBye!\r\n", 7))
	currentUser.logout()	
	connection.close()
	print 'Thread Disconnected::' + str(thisClientAddress)
	thread.exit()
	
def dispatcher():
	while True:
		connection, address = sockobj.accept()
		print 'Server connected by', address, 
		print 'at', now()
		thread.start_new(handleClient, (connection,))
			
dispatcher()
