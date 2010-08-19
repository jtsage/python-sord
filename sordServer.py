#!/usr/bin/python
""" Saga of the Red Dragon - Main Program Loop

  * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
  * All attempts were made to be as close to the original as possible, 
  * including some original artwork, the original fight equations, and 
  * most especially the original spelling and punctuation mistakes.  Enjoy.

  * @author J.T.Sage
  * @copyright 2009-2011
  * @license http://sord.jtsage.com/LICENSE Disclaimer's License
  * @version 2.0
  * Aug 16, 2010 - magic number: 5384 (2536)
"""
import thread, time, sys, traceback, random, socket, sqlite3
import sord

config = sord.config.config.sordConfig(1)
log = sord.base.logger.sordLogger()

try:
	sockobj = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	sockobj.bind(('', config.port))
	sockobj.listen(5)
except:
	print "Socket In Use!"
	sys.exit()
	
def handleClient(connection, config, log):
	try:
		loggedin = False
		time.sleep(1)
		thisClientAddress = connection.getpeername()
		connection.send(chr(255) + chr(253) + chr(34)) # drop to character mode.
		connection.send(chr(255) + chr(251) + chr(1))  # no local echo (client side)
		data = connection.recv(1024) # dump garbage.

		connection.send("Welcome to SORD\r\n")
		connection.settimeout(120)
		sqc = sord.base.dbase.getDB(config)
		art = sord.game.art.sordArtwork(config, sqc)
		sord.base.dbase.dayRollover(config, sqc, log)
		
		""" Line speed and noise options """
		sord.base.func.pauser(connection)
		if ( not config.fulldebug ):
			lineconfig = sord.base.func.getclientconfig(connection, log)
		else:
			lineconfig = (3,0)
		
		if ( not config.fulldebug ):
			if ( not config.ansiskip ):
				sord.base.func.slowecho(connection, art.header(), lineconfig[0], lineconfig[1])
			sord.base.func.pauser(connection)
	
		intro = sord.game.main.intro(connection, config, art, log, sqc, lineconfig)
		if ( not config.fulldebug ):
			intro.run()

		ittr = 0
		if ( config.fulldebug ):
			loggedin = True
			currentUser = sord.base.user.sorduser(config.gameadmin, sqc, connection, art, config, log, lineconfig[0], lineconfig[1])
	
		""" Login Code """
		while ( not loggedin ):
			username = ""
			password = ""
			currentUser = ""
			ittr += 1
			if ( ittr > 3 ):
				sord.base.func.slowecho(connection, sord.base.func.casebold("\r\n\r\nDisconnecting - Too Many Login Attempts\r\n", 1), lineconfig[0], lineconfig[1])
				log.add('  !!! Too Many Login Attemtps::' + str(thisClientAddress))
				raise Exception, "Too many bad logins!"
			sord.base.func.slowecho(connection, sord.base.func.casebold("\r\n\r\nWelcome Warrior!  Enter Your Login Name (OR '\x1b[1m\x1b[31mnew\x1b[32m') :-: ", 2), lineconfig[0], lineconfig[1])
			username = sord.base.func.getLine(connection, True)
			currentUser = sord.base.user.sorduser(username, sqc, connection, art, config, log, lineconfig[0], lineconfig[1])
			if ( currentUser.thisUserID > 0 ):
				sord.base.func.slowecho(connection, sord.base.func.casebold("\r\nPassword :-: ",2), lineconfig[0], lineconfig[1]);  
				password = sord.base.func.getLine(connection, False)
				password = password.strip()
				if ( password == currentUser.thisPassword ):
					loggedin = True
				else:
					sord.base.func.slowecho(connection, sord.base.func.casebold("\r\nIncorrect Password\r\n", 1), lineconfig[0], lineconfig[1])
			else:
				if ( username == "new" ):
					log.add('   ** New User! ' + str(thisClientAddress))
					newusername = sord.game.util.newuser(currentUser)
					currentUser = sorduser(newusername, sqc, connection, art, config, log, lineconfig[0], lineconfig[1])
					newclass = currentUser.cls
					currentUser.updateSkillUse(newclass, 1)
					currentUser.updateSkillPoint(newclass, 1)
					loggedin = True
					log.add('   ** User Created: ' + newusername)
				else:
					sord.base.func.slowecho(connection, sord.base.func.casebold("\r\nUser Name Not Found!\r\n",2), lineconfig[0], lineconfig[1])
				
		currentUser.login()
		log.add('   ** User Logged in::' + currentUser.thisFullname + ' ' + str(thisClientAddress))

		if not currentUser.alive :
			currentUser.write(sord.base.func.casebold("\r\nI'm Afraid You Are DEAD Right Now.  Sorry\r\n", 1))
			raise Exception('normal', "User is DOA.  Bummer for them.")
		
		if ( not config.fulldebug ):
			currentUser.write(sord.game.util.dailyhappen(True, currentUser))
			currentUser.pause()
			currentUser.write(sord.game.util.who(currentUser))
			currentUser.pause()
			currentUser.write(sord.game.util.viewstats(currentUser))
			currentUser.pause()
			currentUser.write(sord.game.util.readmail(currentUser))
	
		townSquare = sord.game.main.mainmenu(currentUser)
		townSquare.run()

		exitQuote = ['The black thing inside rejoices at your departure.', 'The very earth groans at your depature.', 'The very trees seem to moan as you leave.', 'Echoing screams fill the wastelands as you close your eyes.', 'Your very soul aches as you wake up from your favorite dream.']
		exitTop = len(exitQuote) - 1
		exitThis = exitQuote[random.randint(0, exitTop)]
		connection.send(sord.base.func.casebold("\r\n\r\n   "+exitThis+"\r\n\r\n", 7))
		connection.send("NO CARRIER\r\n\r\n")
		if ( loggedin ):
			currentUser.logout()
		connection.shutdown(socket.SHUT_RD)
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
		elif type(e) is socket.error:
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
			connection.shutdown(socket.SHUT_RD)
			connection.close()
		thread.exit()
	
def sordLoop(config, log):
	""" Spawn server thread, run command center """
	log.add("-=-=-=-=-=-= SORD Server Version " + config.version + " =-=-=-=-=-=-")	
	sord.base.dbase.initialTest(config, log)
	log.add(" === Starting Server on port: "+str(config.port))
	igms = list()
	for item in sord.igm.igmlist:
		igms.append(item[2])
	log.add(" === Found IGMs: "+str(igms))
	
	thread.start_new(telnetServe, (config, log))
	
	display = sord.base.commandcenter.sordCommandCenter(config, log)
	display.run()
	
	try:
		sockobj.shutdown(2)
	except:
		pass
	sockobj.close()
	sys.exit()

def telnetServe(config, log):
	""" Server listening thread """
	try:
		while True:
			connection, address = sockobj.accept()
			log.add('  *** Server connected by'+str(address))
			thread.start_new(handleClient, (connection,config,log))
			log.addcon()
	except Exception as e:
		print str(e)
		

sordLoop(config, log) # MAIN PROGRAM LOOP!


