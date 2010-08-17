#!/usr/bin/python
""" Saga of the Red Dragon - Main Program Loop

  * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
  * All attempts were made to be as close to the original as possible, 
  * including some original artwork, the original fight equations, and 
  * most especially the original spelling and punctuation mistakes.  Enjoy.

  * @author J.T.Sage
  * @copyright 2009-2011
  * @license http://sord.jtsage.com/LICENSE Disclaimer's License
  * @version 1.1
  * Aug 16, 2010 - magic number: 5779
  
  @todo IGM framework"""
import thread, threading, time, sys, traceback, random, curses, re
#import MySQLdb
import sqlite3
from os.path import isfile
from os import unlink
from shutil import copy
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
myPort = 6969 #+ random.randint(1, 8)
mySord = sord()

try:
	sockobj = socket(AF_INET6, SOCK_STREAM)
	sockobj.bind((myHost, myPort))
	sockobj.listen(5)
except:
	print "Socket In Use!"
	sys.exit()

IAC  = chr(255) # "Interpret As Command"
DONT = chr(254)
DO   = chr(253)
WONT = chr(252)
WILL = chr(251)
ECHO = chr(1)
LINEMODE = chr(34) # Linemode option
SORDDEBUG = False # Change in command center now!
SKIPLONGANSI = False # Change in command center now!


def testdb(log):
	""" Check for db existence and check version """
	if ( isfile("./" + mySord.sqlitefile()) ):
		sqc = sqlite3.connect("./" + mySord.sqlitefile())
		sqr = sqc.cursor()
		sqc.execute("vacuum")
		sqc.commit()
		for row in sqr.execute("select value from sord where name=?", ('version',)):
			version, = row
			if ( version > 0 ):
				log.add(" === SQLite Database is up to date")
			else:
				log.add(" === SQLite Database is out of date (corrupt), rebuilding...")
				updatedb(log)
		sqc.close()
	else:
		createdb(log)
		
def updatedb(log):
	""" Update sord datebase - for now, nuke and start over """
	copy("./" + mySord.sqlitefile(), "./" + mySord.sqlitefile()+".bak")
	unlink("./" + mySord.sqlitefile())
	createdb()
		
def createdb(log):
	""" Create new sord database """
	log.add(" === Creating New Database - First Run!")
	sqc = sqlite3.connect("./" + mySord.sqlitefile())
	
	statstable = [ # (name, default value)
		('cls' , 1) , ('sex', 1), ('flirt', 0), ('sung', 0), ('master', 0),
		('atinn', 0), ('horse', 0), ('fairy', 0), ('ffight', 20), ('pfight', 3),
		('gems', 0), ('gold', 500), ('bank', 0), ('level', 1), ('charm', 0),
		('spclm', 0), ('spclt', 0), ('spcld', 0), ('used', 0), ('dragon', 0),
		('uset', 0), ('usem', 0), ('str', 10), ('defence', 1), ('exp', 1),
		('hp', 20), ('hpmax', 20), ('weapon', 1), ('armor', 1), ('pkill', 0),
		('dkill', 0), ('fuck', 0), ('alive', 1) ]
	statssql = "create table stats ( userid INTEGER"
	for stat in statstable:
		name, defu = stat
		statssql = statssql + ", " + name + " INTEGER DEFAULT " + str(defu)
	statssql = statssql + " )"
	with sqc:
		sqc.execute("create table sord ( name TEXT, value integer)")
		sqc.execute("insert into sord values (?,?)", ('version', '1'))
		sqc.execute("insert into sord values (?,?)", ('gdays', '0'))
		sqc.execute("insert into sord values (?,?)", ('lastday', '201000101'))
		
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
		sqc.execute("create table users ( userid INTEGER PRIMARY KEY, username TEXT, password TEXT, fullname TEXT, last TEXT )")
		sqc.execute("insert into users ( userid, username, password, fullname ) values (?, ?, ?, ?)", (1, mySord.gameadmin(), mySord.gameadminpass(), mySord.admin()))
		sqc.execute("insert into stats ( userid ) values (?)", (1,))


def now():			  #Server Time
	return time.ctime(time.time())
	
def handleClient(connection, log):
	try:
		loggedin = False
		sqc = sqlite3.connect("./" + mySord.sqlitefile())
		sqr = sqc.cursor()

		randdaily = [ 
			'More children are missing today.',
			'A small girl was missing today.',
			'The town is in grief.  Several children didnt come home today.',
			'Dragon sighting reported today by a drunken old man.',
			'Despair covers the land - more bloody remains have been found today.',
			'A group of children did not return from a nature walk today.',
			'The land is in chaos today.  Will the abductions ever stop?',
			'Dragon scales have been found in the forest today..Old or new?',
			'Several farmers report missing cattle today.',
			'A Child was found today!  But scared deaf and dumb.']

		time.sleep(1)
		thisClientAddress = connection.getpeername()
		connection.send(IAC + DO + LINEMODE) # drop to character mode.
		connection.send(IAC + WILL + ECHO) # no local echo
		data = connection.recv(1024) # dump garbage.
		artwork = art()
	
		connection.send("Welcome to SORD\r\n")
		connection.settimeout(120)
		
		""" Daily Update routine """
		checklast = 0
		timestr = '%Y%j00'
		if ( mySord.dayLength() > 24 ) :
			days = mySord.dayLength() // 24
			checklast = time.strftime('%Y%j00', time.localtime(time.mktime(time.localtime()) - (days*24*60*60)))
		elif ( mySord.dayLength() == 6 ) :
			if ( int(time.strftime('%H', time.localtime())) < 6 ): end = '00' 
			elif ( int(time.strftime('%H', time.localtime())) < 12 ): end = '06' 
			elif ( int(time.strftime('%H', time.localtime())) < 18 ): end = '12' 
			else: end = '18' 
			timestr = '%Y%j' + end
			checklast = time.strftime('%Y%j'+end, time.localtime())
		elif ( mySord.dayLength() == 8 ) :
			if ( int(time.strftime('%H', time.localtime())) < 8 ): end = '00' 
			elif ( int(time.strftime('%H', time.localtime())) < 16 ): end = '08' 
			else: end = '16' 
			timestr = '%Y%j' + end
			checklast = time.strftime('%Y%j'+end, time.localtime())
		elif ( mySord.dayLength() == 12 ) :
			if ( int(time.strftime('%H', time.localtime())) < 12 ): end = '00' 
			else: end = '12' 
			timestr = '%Y%j' + end
			checklast = time.strftime('%Y%j'+end, time.localtime())
		else:
			checklast = time.strftime('%Y%j00', time.localtime())
			
		for row in sqr.execute("select value from sord where name=?", ('lastday',)):
			lday, = row
			if ( int(lday) < int(checklast) ):
				connection.send("Updating... to NEW DAY... ")
				log.add(" === DAY ROLLOVER")
				rsaying = randdaily[random.randint(0, 9)]
				laster = time.strftime('%Y%j', time.localtime(time.mktime(time.localtime()) - (mySord.deleteInactive()*24*60*60)))
				sqc.execute("UPDATE stats set ffight = ? WHERE 1", (mySord.forestFights(), ))
				sqc.execute("UPDATE stats set pfight = ? WHERE 1", (mySord.playerFights(), ))
				sqc.execute("UPDATE stats set usem = spclm WHERE 1")
				sqc.execute("UPDATE stats set used = (spcld / 5 ) + 1 WHERE spcld > 0")
				sqc.execute("UPDATE stats set uset = (spclt / 5 ) + 1 WHERE spclt > 0")
				sqc.execute("INSERT INTO daily ( 'data' ) VALUES ( ? )", ( "{31}"+rsaying, ))
				sqc.execute("UPDATE stats set bank = bank + ( bank * ("+str(mySord.bankInterest())+"/100) ) WHERE bank > 0")
				sqc.execute("DELETE from users WHERE last < ?", (laster,))
				sqc.execute("UPDATE stats set flirt = 0, sung = 0, master = 0, alive = 1 WHERE 1")
				sqc.execute("UPDATE stats set hp = hpmax WHERE hp < hpmax")
				sqc.execute("UPDATE sord set value = value + 1 WHERE 'name' = 'gdays'")
				sqc.execute("UPDATE sord set value = ? WHERE name = 'lastday'", (time.strftime(timestr, time.localtime()),))
				sqc.commit()
				connection.send(" DONE!\r\n")
		
		""" Line speed and noise options """
		func_pauser(connection)
		LINESPEED = 0
		LINENOISE = 0
		func_slowecho(connection, "\r\n"+func_normmenu('(A) 1200 Baud'))
		func_slowecho(connection, func_normmenu('(B) 2400 Baud'))
		func_slowecho(connection, func_normmenu('(C) 28800 Baud'))
		func_slowecho(connection, func_normmenu('(D) T1 Line (no delay)'))
		func_slowecho(connection, func_casebold('\r\n  Emulated Linespeed [B] : ', 7))
		linespeeds = ['2400', '1200', '28800', 'ISDN' ]
		quitter = False
		while ( not quitter):
			data = connection.recv(2)
			if not data: break
			elif ( data == "A" or data == "a" ):
				connection.send('A')
				LINESPEED = 1
				quitter = True
			elif ( data == "B" or data == "b" ):
				connection.send('B')
				LINESPEED = 0
				quitter = True
			elif ( data == "C" or data == "c" ):
				connection.send('C')
				LINESPEED = 2
				quitter = True
			elif ( data == "D" or data == "d" ):
				connection.send('D')
				LINESPEED = 3
				quitter = True
			else:
				connection.send('B')
				LINESPEED = 0
				quitter = True
		log.add('   ** User at emulated linespeed::' + linespeeds[LINESPEED] + ' ' + str(thisClientAddress))
		func_slowecho(connection, func_casebold('\r\n  Emulated Line Noise [y/N] : ', 7))
		quitter = False
		while ( not quitter):
			data = connection.recv(2)
			if not data: break
			elif ( data == "Y" or data == "y" ):
				connection.send('Y')
				log.add('   ** User at emulated line noise:: ' + str(thisClientAddress))
				LINENOISE = 1
				quitter = True
			else:
				connection.send('N')
				LINENOISE = 0
				quitter = True
		
		if ( not SORDDEBUG ):
			if ( not SKIPLONGANSI ):
				func_slowecho(connection, artwork.header(), LINESPEED, LINENOISE)
			func_pauser(connection)
	
		""" Intro Menu """
		quitter = False
		quitfull = False
		if ( SORDDEBUG):
			quitter = True
		skipDisp = False
		while ( not quitter ):
			if ( not skipDisp ):
				func_slowecho(connection, artwork.banner(mySord,sqr), LINESPEED, LINENOISE)
			skipDisp = False
			data = connection.recv(2)
			if not data: break
			elif ( data == "Q" or data == "q" ):
				connection.send('Q')
				quitter = True
				quitfull = True
			elif ( data == "L" or data == "l" ):
				connection.send('L')
				func_slowecho(connection, module_list(artwork, sqc, ''), LINESPEED, LINENOISE)
				func_pauser(connection)
			elif ( data == "E" or data == "e" ):
				connection.send('E')
				log.add('   ** User Logging In::' + str(thisClientAddress))
				quitter = True
			elif ( data == 'S' or data == 's' ):
				func_slowecho(connection, "S\r\n")
				for storyitem in story:
					func_slowecho(connection, func_casebold("  \x1b[37m" + storyitem + "\r\n", 7), LINESPEED, LINENOISE)
				func_pauser(connection)
			else:
				skipDisp = True

		ittr = 0
		if ( SORDDEBUG ):
			loggedin = True
			currentUser = sorduser(mySord.gameadmin(), sqc, connection, artwork, LINESPEED, LINENOISE)
	
		""" Login Code """
		while ( not loggedin and not quitfull ):
			username = ""
			password = ""
			currentUser = ""
			ittr += 1
			if ( ittr > 3 ):
				func_slowecho(connection, func_casebold("\r\n\r\nDisconnecting - Too Many Login Attempts\r\n", 1), LINESPEED, LINENOISE)
				log.add('  !!! Too Many Login Attemtps::' + str(thisClientAddress))
				raise Exception, "Too many bad logins!"
			func_slowecho(connection, func_casebold("\r\n\r\nWelcome Warrior!  Enter Your Login Name (OR '\x1b[1m\x1b[31mnew\x1b[32m') :-: ", 2), LINESPEED)
			username = func_getLine(connection, True)
			currentUser = sorduser(username, sqc, connection, artwork, LINESPEED, LINENOISE)
			if ( currentUser.thisUserID > 0 ):
				func_slowecho(connection, func_casebold("\r\nPassword :-: ",2), LINESPEED, LINENOISE);  
				password = func_getLine(connection, False)
				password = password.strip()
				if ( password == currentUser.thisPassword ):
					loggedin = True
				else:
					func_slowecho(connection, func_casebold("\r\nIncorrect Password\r\n", 1), LINESPEED, LINENOISE)
			else:
				if ( username == "new" ):
					log.add('   ** New User! ' + str(thisClientAddress))
					newusername = module_newuser(currentUser)
					currentUser = sorduser(newusername, sqc, connection, artwork, LINESPEED, LINENOISE)
					newclass = currentUser.cls
					currentUser.updateSkillUse(newclass, 1)
					currentUser.updateSkillPoint(newclass, 1)
					loggedin = True
					log.add('   ** User Created: ' + newusername)
				else:
					func_slowecho(connection, func_casebold("\r\nUser Name Not Found!\r\n",2), LINESPEED, LINENOISE)
				
		if ( not quitfull ):
			currentUser.login()
			log.add('   ** User Logged in::' + currentUser.thisFullname + ' ' + str(thisClientAddress))

			if not currentUser.alive :
				quitfull = 2
				currentUser.write(func_casebold("\r\nI'm Afraid You Are DEAD Right Now.  Sorry\r\n", 1))
		
		if ( not quitfull ):
			if ( not SORDDEBUG ):
				currentUser.write(module_dailyhappen(True, sqc))
				currentUser.pause()
				currentUser.write(module_who(artwork, sqc))
				currentUser.pause()
				currentUser.write(module_viewstats(currentUser))
				currentUser.pause()
	
		""" Main Menu Logic """
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
				currentUser.write(module_dailyhappen(True, sqc))
				currentUser.pause()
			elif ( data[0] == "?" ):
				connection.send('?')
				currentUser.jennielevel = 0
				if ( currentUser.expert ):
					currentUser.write(menu_mainlong(currentUser))
			elif ( data[0] == "p" or data[0] == "P" ):
				connection.send('P')
				currentUser.jennielevel = 0
				currentUser.write(module_who(artwork, sqc))
				currentUser.pause()
			elif ( data[0] == "l" or data[0] == "L" ):
				connection.send('L')
				currentUser.jennielevel = 0
				currentUser.write(module_list(artwork, sqc))
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
					log.add(" !!! ENTERING USER EDITOR !!!")
					editor_main_logic(currentUser)
					log.add(" !!! EXITING USER EDITOR !!!")
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
		connection.send("NO CARRIER\r\n\r\n")
		if ( loggedin ):
			currentUser.logout()
		connection.shutdown(SHUT_RD)
		connection.close()
		sqc.close()
		log.add('  *** Thread Disconnected:' + str(thisClientAddress))
		log.remcon()
		thread.exit()
		
	except Exception as e:
		skipClose = False
		if ( e[0] == "timed out" ):
			log.add("  *** Network Timeout: " + str(thisClientAddress))
			connection.send("\r\n\r\n\x1b[0mNetwork Connection has timed out.  120sec of inactivity.\r\n\r\n")
			connection.send("NO CARRIER\r\n\r\n")
		elif ( e[0] == "normal" ):
			log.add("  *** Normal Exit ("+e[1]+"): " + str(thisClientAddress))
		elif type(e) is error:
			log.add("  *** Remote Closed Host: " + str(thisClientAddress))
			skipClose = True
		else:
			log.add("  !!! Program Error Encountered("+ str(e) + "): " + str(thisClientAddress))
			try:
				connection.send("\r\n\x1b[0mProgram Error Encountered ( "+str(e)+" ), Closing Connection.\r\n")
				connection.send("NO CARRIER\r\n\r\n")
			except:
				log.add("   && No message to client")
			formatted = traceback.format_exc().splitlines()
			for formattedline in formatted:
				log.add("    ~~~ " + formattedline)
		if ( loggedin ):
			currentUser.logout()
		log.remcon()
		if ( not skipClose ):
			connection.shutdown(SHUT_RD)
			connection.close()
		thread.exit()
	
def dispatcher():
	""" Spawn server thread, run command center """
	global SORDDEBUG, SKIPLONGANSI
	log = mainLogger(myPort)
	log.add("-=-=-=-=-=-= SORD Server Version " + mySord.version() + " =-=-=-=-=-=-")
	testdb(log)
	log.add(" === Starting Server on port: "+str(myPort))
	if ( SORDDEBUG ):
		log.add(" !!! DEBUG MODE ENABLED !!!")
	if ( SKIPLONGANSI ):
		log.add(" !!! LONG ANSI DISABLED !!!")
	thread.start_new(mainlisten, (log, ))
	cmdscreen = curses.initscr()
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLACK)
	curses.noecho()
	curses.curs_set(0)
	cmdscreen.timeout(1000)
	toty, totx = cmdscreen.getmaxyx()
	loglines = toty - 7
	
	cmdscreen.attron(curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.border(0)
	cmdscreen.hline((toty-3), 1,  curses.ACS_HLINE, (totx-2))
	cmdscreen.hline(2, 1, curses.ACS_HLINE, (totx-2))
	cmdscreen.attroff(curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addstr((toty-3), (totx-13), '(Q,D,A,S,?)')
	cmdscreen.addstr(1,(totx / 2)-21, 'Saga Of The Red Dragon -=- Command Center', curses.A_BOLD)
	cmdscreen.addstr(1,(totx / 2)-21, 'S', curses.color_pair(3) | curses.A_BOLD)
	cmdscreen.addstr(1,(totx / 2)-16, 'O', curses.color_pair(3) | curses.A_BOLD)
	cmdscreen.addstr(1,(totx / 2)-13, 'T', curses.color_pair(3) | curses.A_BOLD)
	cmdscreen.addstr(1,(totx / 2)-9, 'R', curses.color_pair(3) | curses.A_BOLD)
	cmdscreen.addstr(1,(totx / 2)-5, 'D', curses.color_pair(3) | curses.A_BOLD)
	cmdscreen.addstr(1,(totx / 2)-20, 'aga', curses.color_pair(3))
	cmdscreen.addstr(1,(totx / 2)-15, 'f', curses.color_pair(3))
	cmdscreen.addstr(1,(totx / 2)-12, 'he', curses.color_pair(3))
	cmdscreen.addstr(1,(totx / 2)-8, 'ed', curses.color_pair(3))
	cmdscreen.addstr(1,(totx / 2)-4, 'ragon', curses.color_pair(3))
	cmdscreen.addstr(1,(totx / 2)+7, 'ommand', curses.color_pair(0))
	cmdscreen.addstr(1,(totx / 2)+15, 'enter', curses.color_pair(0))
	cmdscreen.addstr(2,7, 'server')
	cmdscreen.addstr(2,14, 'log')
	cmdscreen.addstr((toty-3),7,'server')
	cmdscreen.addstr((toty-3),14, 'stats')
	cmdscreen.addch(toty-1,24,curses.ACS_BTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-1,44,curses.ACS_BTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-1,60,curses.ACS_BTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-3,24,curses.ACS_TTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-3,44,curses.ACS_TTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-3,60,curses.ACS_TTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-3,0,curses.ACS_LTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-3,totx-1,curses.ACS_RTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(2,0,curses.ACS_LTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(2,totx-1,curses.ACS_RTEE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addstr(toty-2,2,'Connected Peers: ', curses.color_pair(2))
	cmdscreen.addstr(toty-2,26,'Total Peers: ', curses.color_pair(2))
	cmdscreen.addstr(toty-2,46,'Port: ', curses.color_pair(2))
	cmdscreen.addstr(toty-2,62,'Time: ', curses.color_pair(2))
	cmdscreen.addch(toty-2,24,curses.ACS_VLINE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-2,44,curses.ACS_VLINE, curses.color_pair(5) | curses.A_BOLD)
	cmdscreen.addch(toty-2,60,curses.ACS_VLINE, curses.color_pair(5) | curses.A_BOLD)
	
	print help
	
	while True:
		try:
			lineno = 3
			linelength = totx - 4
			for line in log.show(loglines):
				thisattr = curses.color_pair(0)
				if ( line.find('===') > -1 ):
					thisattr = curses.color_pair(4) | curses.A_BOLD
				elif ( line.find(' *** ') > -1 ):
					thisattr = curses.color_pair(4)
				elif ( line.find(' ** ') > -1 ):
					thisattr = curses.color_pair(1) | curses.A_BOLD
				elif ( line.find(' !!! ') > -1 ):
					thisattr = curses.color_pair(3)
				elif ( line.find(' ~~~ ') > -1 ):
					thisattr = curses.color_pair(3) | curses.A_BOLD
				elif ( line.find(' && ') > -1 ):
					thisattr = curses.color_pair(3) | curses.A_BOLD
				elif ( line.find('-=-') > -1 ):
					thisattr = curses.color_pair(0) | curses.A_BOLD
				cmdscreen.addstr(lineno, 2, line.ljust(linelength)[:linelength], (thisattr))
				cmdscreen.chgat(lineno, 2, 17, curses.color_pair(0))
				cmdscreen.chgat(lineno, 19, 2, curses.color_pair(5) | curses.A_BOLD)
				lineno += 1
			cmdscreen.addstr(toty-2,19,str(log.getactive()), curses.color_pair(4))
			cmdscreen.addstr(toty-2,39,str(log.gettotal()), curses.color_pair(4))
			cmdscreen.addstr(toty-2,52,str(log.getport()), curses.color_pair(4) | curses.A_BOLD)
			cmdscreen.addstr(toty-2,67,'            ')
			cmdscreen.addstr(toty-2,68,time.strftime('%H:%M:%S', time.localtime()), curses.color_pair(4))
			cmdscreen.refresh()
			key = cmdscreen.getch()
			if ( key == ord('Q') or key == ord('q') ):
				raise KeyboardInterrupt
			if ( key == ord('D') or key == ord('d') ):
				if ( SORDDEBUG ) :
					SORDDEBUG = False
					log.add("  !!! DEBUG MODE DISABLED !!!")
					cmdscreen.addch(toty-3,2,curses.ACS_HLINE,curses.color_pair(5)|curses.A_BOLD)
				else:
					SORDDEBUG = True
					log.add("  !!! DEBUG MODE ENABLED !!!")
					cmdscreen.addstr(toty-3,2,'D',curses.A_BOLD)
			if ( key == ord('A') or key == ord('a') ):
				if ( SKIPLONGANSI ) :
					SKIPLONGANSI = False
					log.add("  !!! LONG ANSI ENABLED !!! ")
					cmdscreen.addch(toty-3,4,curses.ACS_HLINE,curses.color_pair(5)|curses.A_BOLD)
				else:
					SKIPLONGANSI = True
					log.add("  !!! LONG ANSI DISABLED !!! ")
					cmdscreen.addstr(toty-3,4,'A',curses.A_BOLD)
			if ( key == ord('S') or key == ord('s') ):
				f = open("sord.log", 'w')
				for line in log.show(100):
					f.write(line+"\n")
				f.close()
				log.add("   && Wrote log to file (sord.log)")
			if ( key == ord('?') ):
				log.add("(Q) Quit to shell")
				log.add("(A) Toggle Long ANSI Display")
				log.add("(D) Toggle Debug (autologin / skip intros) Mode")
				log.add("(S) Save Current Log to File")

		except KeyboardInterrupt:
			curses.endwin()
			print "\nS.O.R.D. Server Exiting. (main)  GoodBye!"
			sockobj.shutdown(2)
			sockobj.close()
			sys.exit()

def mainlisten(log):
	""" Server listening thread """
	while True:
		try:
			connection, address = sockobj.accept()
			log.add('  *** Server connected by'+str(address))
			thread.start_new(handleClient, (connection,log))
			log.addcon()
		except KeyboardInterrupt:
			print "\n === Stopping Server"
			sockobj.shutdown(2)
			sockobj.close()
			sys.exit()
			
class mainLogger():
	""" Logger class """
	def __init__(self, port):
		self.__port = port
		self.__mainLogger = list()
		self.__activePeers = 0
		self.__totalPeers = 0
	def add(self, value):
		tmptime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
		self.__mainLogger.append(tmptime+" :: "+value)
		self.__mainLogger = self.__mainLogger[-100:]
	def show(self, value):
		return self.__mainLogger[(value * -1):]
	def addcon(self):
		self.__activePeers += 1
		self.__totalPeers += 1
	def remcon(self):
		self.__activePeers -= 1
	def getactive(self):
		return self.__activePeers
	def gettotal(self):
		return self.__totalPeers
	def getport(self):
		return self.__port


dispatcher()  #MAIN PROGRAM LOOP
