#!/usr/bin/python
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

#
import thread, threading, time, MySQLdb, sys
from sord.art import *
from sord.functions import *
from sord.user import *
from sord.modules import *
from sord.menus import *
from sord.messaging import *
from sord.rdi import *
from sord.forest import *

from config import sord
from socket import *
myHost = ''  #all hosts.
myPort = 6969
mySord = sord()

sockobj = socket(AF_INET6, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)

IAC  = chr(255) # "Interpret As Command"
DONT = chr(254)
DO   = chr(253)
WONT = chr(252)
WILL = chr(251)
ECHO = chr(1)
LINEMODE = chr(34) # Linemode option
SORDDEBUG = False
SORDDEBUG = True

def now():			  #Server Time
	return time.ctime(time.time())
	
def handleClient(connection):
	mySQLconn = MySQLdb.connect(host=str(mySord.sqlServer()), db=str(mySord.sqlDatabase()), user=str(mySord.sqlUser()), passwd=str(mySord.sqlPass()))
	mySQLcurs = mySQLconn.cursor()
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
		currentUser = sordUser('jtsage', mySQLconn, mySQLcurs, connection, artwork)

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
		currentUser = sordUser(username, mySQLconn, mySQLcurs, connection, artwork)
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
				print 'New User! ' + str(thisClientAddress)
				newusername = module_newuser(currentUser)
				currentUser = sordUser(newusername, mySQLconn, mySQLcurs)
				newclass = currentUser.getClass()
				currentUser.updateSkillUse(newclass, 1)
				currentUser.updateSkillPoint(newclass, 1)
				loggedin = True
			else:
				func_slowecho(connection, func_casebold("\r\nUser Name Not Found!\r\n",2))
				
	currentUser.login()
	print 'User Logged in::' + currentUser.thisFullname + ' ' + str(thisClientAddress)

	if currentUser.isDead() :
		quitfull = 2
		currentUser.write(func_casebold("\r\nI'm Afraid You Are DEAD Right Now.  Sorry\r\n", 1))
		
	if ( not quitfull ):
		if ( not SORDDEBUG ):
			currentUser.write(module_dailyhappen(True, mySQLcurs, mySord.sqlPrefix()))
			currentUser.pause()
			currentUser.write( module_who(artwork, mySQLcurs, mySord.sqlPrefix()))
			currentUser.pause()
			currentUser.write(module_viewstats(currentUser))
			currentUser.pause()
	
	skipDisp = False
	while ( not quitfull ):
		if ( not skipDisp ):
			if ( not currentUser.expert ):
				currentUser.write(menu_mainlong(currentUser))
			currentUser.write(menu_mainshort(currentUser))
		skipDisp = False
		data = connection.recv(2)
		if not data: break
		elif ( data[0] == "q" or data[0] == "Q" ):
			connection.send('Q')
			quitfull = True
		elif ( data[0] == "x" or data[0] == "X" ):
			connection.send('X')
			currentUser.toggleXprt()
		elif ( data[0] == "v" or data[0] == "V" ):
			connection.send('V')
			currentUser.write(module_viewstats(currentUser))
			currentUser.pause()
		elif ( data[0] == "d" or data[0] == "D" ):
			connection.send('D')
			currentUser.write(module_dailyhappen(True, mySQLcurs, mySord.sqlPrefix()))
			currentUser.pause()
		elif ( data[0] == "?" ):
			connection.send('?')
			if ( currentUser.expert ):
				currentUser.write(menu_mainlong(currentUser))
		elif ( data[0] == "p" or data[0] == "P" ):
			connection.send('P')
			currentUser.write(module_who(artwork, mySQLcurs, mySord.sqlPrefix()))
			currentUser.pause()
		elif ( data[0] == "l" or data[0] == "L" ):
			connection.send('L')
			currentUser.write(module_list(artwork, mySQLcurs, mySord.sqlPrefix()))
			currentUser.pause()
		elif ( data[0] == "a" or data[0] == "A" ):
			connection.send('A')
			module_abduls(currentUser)
		elif ( data[0] == "k" or data[0] == "K" ):
			connection.send('K')
			module_arthurs(currentUser)
		elif ( data[0] == "y" or data[0] == "Y" ):
			connection.send('Y')
			module_bank(currentUser)
		elif ( data[0] == "h" or data[0] == "H" ):
			connection.send('H')
			module_heal(currentUser)
		elif ( data[0] == "m" or data[0] == "M" ):
			connection.send('M')
			msg_announce(currentUser)
		elif ( data[0] == "w" or data[0] == "W" ):
			connection.send('W')
			msg_sendmail(currentUser)
		elif ( data[0] == "i" or data[0] == "I" ):
			connection.send('I')
			rdi_logic(currentUser)
		elif ( data[0] == "f" or data[0] == "F" ):
			connection.send('F')
			module_forest(currentUser)
		else:
			skipDisp = True
		
		"""
		case 'T': // WARRIOR TRAINING
			module_turgon(); break;
		case 'S': // SLAUGHTER
"""
	currentUser.write(func_casebold("\r\n\r\n   Quitting to the Fields... GoodBye!\r\n", 7))
	currentUser.logout()
	connection.shutdown(SHUT_RD)
	connection.close()
	print 'Thread Disconnected::' + str(thisClientAddress)
	thread.exit()
	
def dispatcher():
	while True:
		try:
			connection, address = sockobj.accept()
			print 'Server connected by', address, 
			print 'at', now()
			thread.start_new(handleClient, (connection,))
		except KeyboardInterrupt:
			print 'Closing listener and exiting.'
			sockobj.close()
			sys.exit()

dispatcher()  #MAIN PROGRAM LOOP
