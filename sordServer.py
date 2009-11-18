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
  @todo IGM framework, main menu '1' for image."""
import thread, threading, time, MySQLdb, sys, traceback
from socket import *
from sord.art import *
from sord.functions import *
from sord.user import *
from sord.modules import *
from sord.menus import *
from sord.messaging import *
from sord.rdi import *
from sord.forest import *
from sord.data import *

from socket import *
from config import sord
myHost = ''  #all hosts.
myPort = 6969
mySord = sord()

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
#SKIPLONGANSI = True

def now():			  #Server Time
	return time.ctime(time.time())
	
def handleClient(connection):
	global connectedHosts
	try:
		loggedin = False
		mySQLconn = MySQLdb.connect(host=str(mySord.sqlServer()), db=str(mySord.sqlDatabase()), user=str(mySord.sqlUser()), passwd=str(mySord.sqlPass()))
		mySQLcurs = mySQLconn.cursor()
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
				func_slowecho(connection, artwork.banner(mySord,mySQLcurs))
			skipDisp = False
			data = connection.recv(1)
			if not data: break
			elif ( data == "Q" or data == "q" ):
				quitter = True
				quitfull = True
			elif ( data == "L" or data == "l" ):
				func_slowecho(connection, module_list(artwork, mySQLcurs, mySord.sqlPrefix()))
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
			currentUser = sordUser('jtsage', mySQLconn, mySQLcurs, connection, artwork)
	
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
					print '   ** New User! ' + str(thisClientAddress)
					newusername = module_newuser(currentUser)
					currentUser = sordUser(newusername, mySQLconn, mySQLcurs, connection, artwork)
					newclass = currentUser.getClass()
					currentUser.updateSkillUse(newclass, 1)
					currentUser.updateSkillPoint(newclass, 1)
					loggedin = True
				else:
					func_slowecho(connection, func_casebold("\r\nUser Name Not Found!\r\n",2))
				
		if ( not quitfull ):
			currentUser.login()
			print '   ** User Logged in::' + currentUser.thisFullname + ' ' + str(thisClientAddress)

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
				currentUser.write(module_dailyhappen(True, mySQLcurs, mySord.sqlPrefix()))
				currentUser.pause()
			elif ( data[0] == "?" ):
				connection.send('?')
				currentUser.jennielevel = 0
				if ( currentUser.expert ):
					currentUser.write(menu_mainlong(currentUser))
			elif ( data[0] == "p" or data[0] == "P" ):
				connection.send('P')
				currentUser.jennielevel = 0
				currentUser.write(module_who(artwork, mySQLcurs, mySord.sqlPrefix()))
				currentUser.pause()
			elif ( data[0] == "l" or data[0] == "L" ):
				connection.send('L')
				currentUser.jennielevel = 0
				currentUser.write(module_list(artwork, mySQLcurs, mySord.sqlPrefix()))
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
		print '  *** Thread Disconnected:' + str(thisClientAddress) + " at " + now()
		connectedHosts -= 1
		print "  --- Connected Hosts: " + str(connectedHosts)
		thread.exit()
		
	except Exception as e:
		skipClose = False
		if ( e[0] == "timed out" ):
			print "  *** Network Timeout: " + str(thisClientAddress) + " at " + now()
			connection.send("\r\n\r\nNetwork Connection has timed out.  120sec of inactivity.\r\n\r\n")
		elif type(e) is error:
			print "  *** Remote Closed Host: " + str(thisClientAddress) + " at " + now()
			skipClose = True
		else:
			print "  !!! Program Error Encountered("+ str(e) + "): " + str(thisClientAddress) + " at " + now()
			try:
				connection.send("\r\nProgram Error Encountered ( "+str(e)+" ), Closing Connection.\r\n")
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
			sockobj.close()
			sys.exit()

dispatcher()  #MAIN PROGRAM LOOP
