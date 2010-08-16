#!/usr/bin/python
""" Saga of the Red Dragon - Main Program Loop

  * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
  * All attempts were made to be as close to the original as possible, 
  * including some original artwork, the original fight equations, and 
  * most especially the original spelling and punctuation mistakes.  Enjoy.

  * @author J.T.Sage
  * @copyright 2009-2011
  * @license http://sord.jtsage.com/LICENSE Disclaimer's License
  * @version 0.9.9
  @todo IGM framework"""
import thread, threading, time, sys, traceback, random
#import MySQLdb
import sqlite3
from os.path import isfile
from os import unlink
from socket import *
from sord.art import *
from sord.functions import *
from sord.user2 import *
from sord.modules import *
from sord.menus import *
from sord.messaging import *
from sord.rdi import *
from sord.forest import *
from sord.data import *
from sord.usereditor import *

from socket import *
from config import sord
myHost = ''  #all hosts.
myPort = 6969 + random.randint(1, 8)
mySord = sord()
print myPort

try:
	sockobj = socket(AF_INET6, SOCK_STREAM)
	sockobj.bind((myHost, myPort))
	sockobj.listen(5)
except:
	print "Socket In Use!"
	sys.exit()


connectedHosts = 0
IAC  = chr(255) # "Interpret As Command"
DONT = chr(254)
DO   = chr(253)
WONT = chr(252)
WILL = chr(251)
ECHO = chr(1)
LINEMODE = chr(34) # Linemode option
SORDDEBUG = False
SORDDEBUG = True
SKIPLONGANSI = False
SKIPLONGANSI = True

def testdb():
	if ( isfile("./" + mySord.sqlitefile()) ):
		sqc = sqlite3.connect("./" + mySord.sqlitefile())
		sqr = sqc.cursor()
		for row in sqr.execute("select value from sord where name=?", ('version',)):
			version, = row
			if ( version > 0 ):
				print " =+= SQLite Database is up to date"
			else:
				print " =+= SQLite Database is out of date, updating..."
				updatedb()
		sqc.close()
	else:
		createdb()
		
def updatedb():
	unlink("./" + mySord.sqlitefile())
	createdb()
		
def createdb():
	print " =+= Creating New Database - First Run!"
	sqc = sqlite3.connect("./" + mySord.sqlitefile())
	
	statstable = [ # (name, default value)
		('cls' , 1) , ('sex', 1), ('flirt', 0), ('sung', 0), ('master', 0),
		('atinn', 0), ('horse', 0), ('fairy', 0), ('ffight', 20), ('pfight', 3),
		('gems', 0), ('gold', 500), ('bank', 0), ('level', 1), ('charm', 0),
		('spclm', 0), ('spclt', 0), ('spcld', 0), ('used', 0),
		('uset', 0), ('usem', 0), ('str', 10), ('defence', 1), ('exp', 1),
		('hp', 20), ('hpmax', 20), ('weapon', 1), ('armor', 1), ('pkill', 0),
		('dkill', 0), ('fuck', 0) ]
	statssql = "create table stats ( userid INTEGER"
	for stat in statstable:
		name, defu = stat
		statssql = statssql + ", " + name + " INTEGER DEFAULT " + str(defu)
	statssql = statssql + " )"
	with sqc:
		sqc.execute("create table sord ( name TEXT, value integer)")
		sqc.execute("insert into sord values (?,?)", ('version', '1'))
		sqc.execute("insert into sord values (?,?)", ('gdays', '1'))
		
		sqc.execute("create table daily ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT )")
		sqc.execute("insert into daily (data) values (?)", ('{31}Welcome to {1}{37}S{0}{32}.O.R.D', ))
		sqc.execute("insert into daily (data) values (?)", ('{31}Despair covers the land - more bloody remains have been found today.',))
		
		sqc.execute("create table dhtpatrons (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT)")
		sqc.execute("insert into dhtpatrons (data, nombre) values (?, ?)", ('{34}Welcome to the {31}Dark Horse Tavern', 'Chance'))
		
		sqc.execute("create table dirt (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT)")
		sqc.execute("insert into dirt (data, nombre) values (?, ?)", ('{32}Mighty quiet around here...', 'Jack the Ripper'))
		
		sqc.execute("create table flowers ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT )")
		sqc.execute("insert into flowers (data, nombre) values (?, ?)", ('{34}Does this kimono make me look {31}fat?', 'Fairy #1'))
		sqc.execute("insert into flowers (data, nombre) values (?, ?)", ('{36}No, just {1}ugly', 'Fairy #2'))
		
		sqc.execute("create table mail ( id INTEGER PRIMARY KEY AUTOINCREMENT, 'from' INTEGER, 'to' integer, message text, sent text)")
		sqc.execute("create table online ( userid integer, whence text )")
		
		sqc.execute("create table patrons ( id INTEGER PRIMARY KEY, data text, nombre TEXT)" )
		sqc.execute("insert into patrons (data, nombre) values (?, ?)", ('{34}Welcome to the {31}Red Dragon {34}Inn', 'The Bartender'))
		
		sqc.execute(statssql)
		sqc.execute("create table users ( userid INTEGER PRIMARY KEY, username TEXT, password TEXT, fullname TEXT, last TEXT, alive INTEGER DEFAULT 1 )")
		sqc.execute("insert into users ( userid, username, password, fullname ) values (?, ?, ?, ?)", (1, mySord.gameadmin(), mySord.gameadminpass(), mySord.admin()))
		sqc.execute("insert into stats ( userid ) values (?)", (1,))


def now():			  #Server Time
	return time.ctime(time.time())
	
def handleClient(connection):
	global connectedHosts
	try:
		loggedin = False
		sqc = sqlite3.connect("./" + mySord.sqlitefile())
		sqr = sqc.cursor()
		#mySQLconn = MySQLdb.connect(host=str(mySord.sqlServer()), db=str(mySord.sqlDatabase()), user=str(mySord.sqlUser()), passwd=str(mySord.sqlPass()))
		#mySQLcurs = mySQLconn.cursor()
		time.sleep(1)
		thisClientAddress = connection.getpeername()
		connection.send(IAC + DO + LINEMODE) # drop to character mode.
		connection.send(IAC + WILL + ECHO) # no local echo
		data = connection.recv(1024) # dump garbage.
		artwork = art()
	
		connection.send("Welcome to SORD\r\n")
		connection.settimeout(120)
		func_pauser(connection)
		if ( not SORDDEBUG ):
			if ( not SKIPLONGANSI ):
				func_slowecho(connection, artwork.header())
			func_pauser(connection)
	
		quitter = False
		quitfull = False
		if ( SORDDEBUG):
			quitter = True
		skipDisp = False
		while ( not quitter ):
			if ( not skipDisp ):
				func_slowecho(connection, artwork.banner(mySord,sqr))
			skipDisp = False
			data = connection.recv(1)
			if not data: break
			elif ( data == "Q" or data == "q" ):
				quitter = True
				quitfull = True
			elif ( data == "L" or data == "l" ):
				func_slowecho(connection, module_list(artwork, sqr, mySord.sqlPrefix()))
				func_pauser(connection)
			elif ( data == "E" or data == "e" ):
				print '   ** User Logging In::' + str(thisClientAddress)
				quitter = True
			elif ( data == 'S' or data == 's' ):
				func_slowecho(connection, "S\r\n")
				for storyitem in story:
					func_slowecho(connection, func_casebold("  \x1b[37m" + storyitem + "\r\n", 7))
				func_pauser(connection)
			else:
				skipDisp = True

		ittr = 0
		if ( SORDDEBUG ):
			loggedin = True
			currentUser = sorduser('jtsage', sqc, connection, artwork)
	
		while ( not loggedin and not quitfull ):
			username = ""
			password = ""
			currentUser = ""
			ittr += 1
			if ( ittr > 3 ):
				func_slowecho(connection, func_casebold("\r\n\r\nDisconnecting - Too Many Login Attempts\r\n", 1))
				print '  !!! Too Many Login Attemtps::' + str(thisClientAddress)
				raise Exception, "Too many bad logins!"
			func_slowecho(connection, func_casebold("\r\n\r\nWelcome Warrior!  Enter Your Login Name (OR '\x1b[1m\x1b[31mnew\x1b[32m') :-: ", 2))
			username = func_getLine(connection, True)
			currentUser = sorduser(username, sqc, connection, artwork)
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
					print '   ** New User! ' + str(thisClientAddress)
					newusername = module_newuser(currentUser)
					currentUser = sorduser(newusername, sqc, connection, artwork)
					newclass = currentUser.cls
					currentUser.updateSkillUse(newclass, 1)
					currentUser.updateSkillPoint(newclass, 1)
					loggedin = True
				else:
					func_slowecho(connection, func_casebold("\r\nUser Name Not Found!\r\n",2))
				
		if ( not quitfull ):
			currentUser.login()
			print '   ** User Logged in::' + currentUser.thisFullname + ' ' + str(thisClientAddress)

			if not currentUser.alive :
				quitfull = 2
				currentUser.write(func_casebold("\r\nI'm Afraid You Are DEAD Right Now.  Sorry\r\n", 1))
		
		if ( not quitfull ):
			if ( not SORDDEBUG ):
				currentUser.write(module_dailyhappen(True, sqr, mySord.sqlPrefix()))
				currentUser.pause()
				currentUser.write( module_who(artwork, sqr, mySord.sqlPrefix()))
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
				currentUser.jennielevel = 0
				currentUser.toggleXprt()
			elif ( data[0] == "v" or data[0] == "V" ):
				connection.send('V')
				currentUser.jennielevel = 0
				currentUser.write(module_viewstats(currentUser))
				currentUser.pause()
			elif ( data[0] == "d" or data[0] == "D" ):
				connection.send('D')
				currentUser.jennielevel = 0
				currentUser.write(module_dailyhappen(True, sqr, mySord.sqlPrefix()))
				currentUser.pause()
			elif ( data[0] == "?" ):
				connection.send('?')
				currentUser.jennielevel = 0
				if ( currentUser.expert ):
					currentUser.write(menu_mainlong(currentUser))
			elif ( data[0] == "p" or data[0] == "P" ):
				connection.send('P')
				currentUser.jennielevel = 0
				currentUser.write(module_who(artwork, sqr, mySord.sqlPrefix()))
				currentUser.pause()
			elif ( data[0] == "l" or data[0] == "L" ):
				connection.send('L')
				currentUser.jennielevel = 0
				currentUser.write(module_list(artwork, sqr, mySord.sqlPrefix()))
				currentUser.pause()
			elif ( data[0] == "a" or data[0] == "A" ):
				connection.send('A')
				currentUser.jennielevel = 0
				module_abduls(currentUser)
			elif ( data[0] == "k" or data[0] == "K" ):
				connection.send('K')
				currentUser.jennielevel = 0
				module_arthurs(currentUser)
			elif ( data[0] == "y" or data[0] == "Y" ):
				connection.send('Y')
				currentUser.jennielevel = 0
				module_bank(currentUser)
			elif ( data[0] == "h" or data[0] == "H" ):
				connection.send('H')
				currentUser.jennielevel = 0
				module_heal(currentUser)
			elif ( data[0] == "m" or data[0] == "M" ):
				connection.send('M')
				currentUser.jennielevel = 0
				msg_announce(currentUser)
			elif ( data[0] == "w" or data[0] == "W" ):
				connection.send('W')
				currentUser.jennielevel = 0
				msg_sendmail(currentUser)
			elif ( data[0] == "i" or data[0] == "I" ):
				connection.send('I')
				rdi_logic(currentUser)
			elif ( data[0] == "f" or data[0] == "F" ):
				connection.send('F')
				currentUser.jennielevel = 0
				module_forest(currentUser)
			elif ( data[0] == 't' or data[0] == 'T' ):
				connection.send('T')
				currentUser.jennielevel = 0
				module_turgon(currentUser)
			elif ( data[0] == "1" ):
				connection.send("1\r\n")
				currentUser.jennielevel = 0
				currentUser.write(artwork.info(currentUser))
				currentUser.pause()
			elif ( data[0] == 's' or data[0] == 'S' ):
				connection.send('S')
				currentUser.jennielevel = 0
				module_killer(currentUser)
			elif ( data[0] == 'j' or data[0] == 'J' ):
				skipDisp = True
				if currentUser.jennielevel == 0 :
					currentUser.jennielevel = 1
				else:
					currentUser.jennielevel = 0
			elif ( data[0] == 'e' or data[0] == 'E' ):
				skipDisp = True
				if currentUser.jennielevel == 1:
					currentUser.jennielevel = 2
				else:
					currentUser.jennielevel = 0
			elif ( data[0] == 'n' or data[0] == 'N' ):
				skipDisp = True
				if currentUser.jennielevel == 2:
					currentUser.jennielevel = 3
				elif currentUser.jennielevel == 3:
					currentUser.jennielevel = 4
				else:
					currentUser.jennielevel = 0
			elif ( data[0] == "!" ):
				if (currentUser.thisUserID == 1):
					print " !!! ENTERING USER EDITOR !!!"
					editor_main_logic(currentUser)
					print " !!! EXITING USER EDITOR !!!"
				else:
					skipDisp = True
			elif ( data[0] == "@" ):
				currentUser.toggleQuick()
				currentUser.write('@')
			else:
				skipDisp = True
				currentUser.jennielevel = 0

		exitQuote = ['The black thing inside rejoices at your departure.', 'The very earth groans at your depature.', 'The very trees seem to moan as you leave.', 'Echoing screams fill the wastelands as you close your eyes.', 'Your very soul aches as you wake up from your favorite dream.']
		exitTop = len(exitQuote) - 1
		exitThis = exitQuote[random.randint(0, exitTop)]
		connection.send(func_casebold("\r\n\r\n   "+exitThis+"\r\n\r\n", 7))
		if ( loggedin ):
			currentUser.logout()
		connection.shutdown(SHUT_RD)
		connection.close()
		sqc.close()
		print '  *** Thread Disconnected:' + str(thisClientAddress) + " at " + now()
		connectedHosts -= 1
		print "  --- Connected Hosts: " + str(connectedHosts)
		thread.exit()
		
	except Exception as e:
		skipClose = False
		if ( e[0] == "timed out" ):
			print "  *** Network Timeout: " + str(thisClientAddress) + " at " + now()
			connection.send("\r\n\r\n\x1b[0mNetwork Connection has timed out.  120sec of inactivity.\r\n\r\n")
		elif ( e[0] == "normal" ):
			print "  *** Normal Exit ("+e[1]+"): " + str(thisClientAddress) + " at " + now()
		elif type(e) is error:
			print "  *** Remote Closed Host: " + str(thisClientAddress) + " at " + now()
			skipClose = True
		else:
			print "  !!! Program Error Encountered("+ str(e) + "): " + str(thisClientAddress) + " at " + now()
			try:
				connection.send("\r\n\x1b[0mProgram Error Encountered ( "+str(e)+" ), Closing Connection.\r\n")
			except:
				print "   && No message to client"
			formatted = traceback.format_exc().splitlines()
			for formattedline in formatted:
				print "    ~~~ " + formattedline
		if ( loggedin ):
			currentUser.logout()
		connectedHosts -= 1
		if ( not skipClose ):
			connection.shutdown(SHUT_RD)
			connection.close()
		print "  --- Connected Hosts: " + str(connectedHosts)
		thread.exit()
	
def dispatcher():
	global connectedHosts
	print "-=-=-=-=-=-= SORD Server Version " + mySord.version() + " =-=-=-=-=-=-"
	print " === Starting Server"
	if ( SORDDEBUG ):
		print " !!! DEBUG MODE ENABLED !!!"
	if ( SKIPLONGANSI ):
		print " !!! LONG ANSI DISABLED !!!"
	while True:
		try:
			connection, address = sockobj.accept()
			print '  *** Server connected by', address, 
			print 'at', now()
			thread.start_new(handleClient, (connection,))
			connectedHosts += 1
			print "  --- Connected Hosts: " + str(connectedHosts)
		except KeyboardInterrupt:
			print "\n === Stopping Server"
			sockobj.shutdown(2)
			sockobj.close()
			sys.exit()
			

testdb()
dispatcher()  #MAIN PROGRAM LOOP
