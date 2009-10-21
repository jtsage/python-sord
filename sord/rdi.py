#!/usr/bin/python
""" Red Dragon Inn
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage """
import random, time
from functions import *

def rdi_menu_main(art, user):
	""" Main Menu """
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mThe Inn\x1b[0m\r\n"
	thismenu += art.blueline();
	thismenu += "\x1b[32m  You enter the inn and are immediately hailed by several of the patrons.\x1b[0m\r\n"
	thismenu += "\x1b[32m  You respond with a wave and scan the room.  The room is filled with\x1b[0m\r\n"
	thismenu += "\x1b[32m  smoke from the torches that line the walls.  Oaken tables and chairs\x1b[0m\r\n"
	thismenu += "\x1b[32m  are scattered across the room.  You smile as the well-rounded Violet\x1b[0m\r\n"
	thismenu += "\x1b[32m  brushes by you....\x1b[0m\r\n\r\n"
	thismenu += func_menu_2col("(C)onverse with the patrons", "(D)aily News", 5, 5)
	if ( user.getSex() == 1 ):
		flirtwith = "Violet"
	else:
		flirtwith = "Seth Able"
	thismenu += menu_2col("(F)lirt with "+flirtwith, "(T)alk to the Bartender", 5, 5)
	thismenu += menu_2col("(G)et a Room", "(V)iew Your Stats", 5, 5)
	thismenu += menu_2col("(H)ear Seth Able The Bard", "(M)ake Announcment", 5, 5)
	thismenu += menu_2col("(R)eturn To Town", "", 5, 5)
	return thismenu

def rdi_prompt(user):
	""" User Prompt"""
	ptime = func_maketime(user)
	thismenu  = "\r\n  \x1b[1;35mThe Red Dragon Inn\x1b[0m\x1b[1;30m (? for menu)\x1b[0m\r\n"
	thismenu += "  \x1b[1;30m(C,D,F,T,G,V,H,M,R)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def rdi_logic(connection, art, user):
	""" Red Dragon Inn, main loop """
	thisQuit = False
	while ( not thisQuit ):
		if (  not user.expert ):
			func_slowecho(connection, rdi_menu_main(art, user))
		func_slowecho(connection, rdi_prompt(user))
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			connection.send('R')
			thisQuit = True
		if ( data[0] == '?' ):
			connection.send('?')
			if ( user.expert):
				func_slowecho(connection, rdi_menu_main(art, user))
		if ( data[0] == 'd' or data[0] == 'D' ):
			connection.send('D')
			func_slowecho(connection, module_dailyhappen(True, user.db, user.thisSord.sqlPrefix()))
			func_pauser(connection)
		if ( data[0] == 't' or data[0] == 'T' ):
			connection.send('T')
			rdi_bartend(connection, art, user)
		if ( data[0] == 'v' or data[0] == 'V' ):
			connection.send('V')
			func_slowecho(connection, module_viewstats(art, user))
			func_pauser(connection)
		if ( data[0] == 'm' or data[0] == 'M' ):
			connection.send('M')
			msg_announce(connection, user)
		if ( data[0] == 'f' or data[0] == 'F' ):
			connection.send('F')
			if ( user.didFlirt() ):
				func_slowecho(connection, func_casebold("\r\n  You have already flirted once today\r\n", 2))
			else:
				rdi_flirt(connection, user)
			func_pauser(connection)
		if ( data[0] == 'c' or data[0] == 'C' ):
			connection.send('C')
			rdi_converse(connection, user)
		if ( data[0] == 'h' or data[0] == 'H' ):
			connection.send('H')
			rdi_menu_bard(connection, art, user)
		if ( data[0] == 'g' or data[0] == 'G' ):
			connection.send('G')
			rdi_getroom(connection, user)

def rdi_getroom(connection, user):
	""" Red Dragon Inn Get a Room """
	price = user.getLevel() * 400
	func_slowecho(connection, "\r\n  \x1b[32mThe bartender approaches you at the mention of a room.\x1b[0m\r\n")
	func_slowecho(connection, "  \x1b[35m\"You want a room, eh?  That'll be "+price+" gold!\"\x1b[0m\r\n")
	func_slowecho(connection, "  \x1b[32mDo you agree? \x1b[1m: \x1b[0m")
	yesno = connection.recv(2)
	if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
		if ( user.getGold() < price ):
			func_slowecho(connection, "\r\n  \x1b[35m\"How bout you find yourself a nice stretch of cardboard box ya bum?\x1b[0m\r\n")
		else:
			user.updateGold(price * -1)
			thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"stats SET atinn = 1 WHERE userid = "+str(user.thisUserID)
			user.db.execute(thisSQL)
			user.logout()
			connection.close()
			thread.exit()
	else:
		func_slowecho(connection, "\r\n  \x1b[35m\"Suit yourself...\"\x1b[0m\r\n")

def rdi_converse(connection, user):
	""" Converse with patrons """
	thisSQL = "SELECT data, nombre FROM (SELECT * FROM "+user.thisSord.sqlPrefix()+"patrons ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id"
	output  = "\r\n\r\n  \x1b[1;37mConverse with the Patrons\x1b[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	user.db.execute(thisSQL)
	for (nombre, data) in user.db.fetchall():
		output += "    \x1b[32m"+nombre+" \x1b[1;37msays... \x1b[0m\x1b[32m" + func_colorcode(data)
		output += "\x1b[0m\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	output += "\r\n  \x1b[32mAdd to the conversation? \x1b[1m: \x1b[0m"
	func_slowecho(connection, output)
	yesno = connection.recv(2)
	if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
		func_slowecho(connection, func_casebold("\r\n  What say you? :-: ", 2))
		ann = func_getLine(connection, True)
		safeann = user.dbc.escape_string(ann)
		thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"patrons ( `data`, `nombre` ) VALUES ('"+safeann+"', '"+user.thisFullname+"')"
		user.db.execute(thisSQL)
		func_slowecho(connection, func_casebold("\r\n  Wisdom added!\r\n", 2))
		func_pauser(connection)

def rdi_menu_bard(connection, art, user):
	""" Talk with the bard """
	ptime = func_maketime(user)
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mSeth Able\x1b[0m\n"
	thismenu += art.blueline()
	thismenu += "  \x1b[32mYou stumble over to a dank corner of the Inn.\n  Seth able looks at you expectantly...\r\n\r\n"
	thismenu += func_normmenu("(A)sk Seth Able to Sing")
	thismenu += func_normmenu("(R)eturn to the Inn")
	thismenu += "\r\n  \x1b[1;35mSeth Able the Bard\x1b[0m\x1b[1;30m (A,R,Q) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	thisQuit = False
	while ( not thisQuit ):
		func_slowecho(connection, thismenu)
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'r' or data[0] == 'R' or data[0] == 'q' or data[0] == 'Q' ):
			connection.send('R')
			thisQuit = True
		if ( data[0] == 'a' or data[0] == 'A' ):
			rdi_hearbard(connection, user)

def rdi_hearbard(connection, user):
	""" Hear the bard sing"""
	if ( not user.didBard() ):
		func_slowecho(connection, "\r\n  \x1b[32mSeth thinks for a moment, picks up his lute, and begins...\r\n\r\n")
		songnum = random.randint(1, 10)
		for lyrics in thebard[songnum][0]:
			time.sleep(1)
			re.sub("\{(\d+)\}", "\x1b[" + r"\1" + "m" , text)
			lyrics = re.sub("\.\.\.\"", "\x1b[37m...\"\x1b[32m", lyrics)
			lyrics = re.sub("\"\.\.\.", "\x1b[37m\"...\x1b[0m", lyrics)
			lyrics = re.sub("XX", "\x1b[1m"+user.thisFullname+"\x1b[22m", lyrics)
			func_slowecho(connection, lyrics+"\r\n")
		func_slowecho(connection, "\r\n  \x1b[1;32m"+thebard[songnum][1][0]+"\x1b[0m\r\n")
		func_slowecho(connection, "\r\n  \x1b[1;34m"+thebard[songnum][1][1]+"\x1b[0m\r\n\r\n")
		thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"stats SET "+thebard[songnum][2]+" WHERE userid = "+str(user.thisUserID)
		user.db.execute(thisSQL)
		func_pauser(connection)
	else:
		func_slowecho(connection, func_casebold("\r\n  Seth says:  I'm a bit tired, maybe tommorow...\r\n", 2))

def rdi_flirt(connection, user):
	""" Flirt initiator.  Locked on viloet for now.
	@todo else should go to seth.  """
	func_slowecho(connection, rdi_menu_flirt(connection, user))
	func_slowecho(connection, "\n  \x1b[32mYour Choice? \x1b[1m: \x1b[0m ")
	if ( user.getSex() == 1 ):
		rdi_flirt_violet(connection, user)
	else:
		rdi_flirt_violet(connection, user) #rdi_flirt_seth(connection, user)

def rdi_flirt_violet(connection, user):
	"""Flirt with the barmaid"""
	thisTry = False
	thisScrew = False
	thisQuit = False
	while ( not thisQuit ):
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'w' or data[0] == 'W' ):
			connection.send('W')
			thisRun = 0
			thisQuit = True
			thisTry = True
		if ( data[0] == 'k' or data[0] == 'K' ):
			connection.send('K')
			thisRun = 1
			thisQuit = True
			thisTry = True
		if ( data[0] == 'p' or data[0] == 'P' ):
			connection.send('P')
			thisRun = 2
			thisQuit = True
			thisTry = True
		if ( data[0] == 's' or data[0] == 'S' ):
			connection.send('S')
			thisRun = 3
			thisQuit = True
			thisTry = True
		if ( data[0] == 'g' or data[0] == 'G' ):
			connection.send('G')
			thisRun = 4
			thisQuit = True
			thisTry = True
		if ( data[0] == 'c' or data[0] == 'C' ):
			connection.send('C')
			thisRun = 5
			thisQuit = True
			thisTry = True
			thisScrew = True
		if ( data[0] == 'r' or data[0] == 'R' or data[0] == 'n' or data[0] == 'N' or data[0] == 'q' or data[0] == 'Q' ):
			connection.send('N')
			thisQuit = True
	if ( thisTry ):
		func_slowecho(connection, "\r\n  \x1b[32m"+violet[thisRun][2]+"\x1b[0m\r\n")
		time.sleep(1)
		func_slowecho(connection, "\r\n  \x1b[1;37m...")
		time.sleep(1)
		func_slowecho(connection, "\x1b[31mAND\x1b[37m")
		time.sleep(1)
		func_slowecho(connection, "...\x1b[0m")
		if ( user.getCharm() > violet[thisRun][0] ):
			thisExp = user.getLevel() * violet[thisRun][1]
			user.updateExperience(thisExp)
			user.setFlirt()
			func_slowecho(connection, "\r\n  \x1b[1;34m"+violet[thisRun][3]+"\x1b[0m\r\n  \x1b[32mYou gain \x1b[1m"+str(thisExp)+"\x1b[22m experience.\x1b[0m\r\n")
		else:
			thisScrew = False
			func_slowecho(connection, "\r\n  \x1b[1;31m"+violet[thisRun][4]+"\x1b[0m\r\n")

		if ( thisScrew ):
			vd = ['herpes', 'crabs', 'ghonnereah']
			vdc = random.randint(0, 2)
			thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"daily ( `data` ) VALUES ( '{32}{1}"+user.thisFullname+"{0}{32} got a little somethin somethin today.  {34}And "+vd[vdc]+".')"
			user.db.execute(thisSQL)

def rdi_menu_flirt(connection, user):
	thismenu = ""
	for saying in flirts[user.getSex()]:
		thismenu += func_normmenu(saying[1])
	return thismenu

def inn_bartend(connection, art, user):
	""" Bartender Logic
	@todo Bribe System """
	thisQuit = False
	if ( user.getLevel() < 2 ):
		func_slowecho(connection, "\r\n  \x1b[32mNever heard of ya...  Come back when you've done something.\x1b[0m\r\n")
		thisQuit = True
	while ( not thisQuit ):
		func_slowecho(connection, rdi_menu_bartend(connection, art, user))
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'r' or data[0] == 'R' or data[0] == 'q' or data[0] == 'Q' ):
			connection.send('R')
			thisQuit = True
		if ( data[0] == 'v' or data[0] == 'V' ):
			connection.send('V')
			func_slowecho(connection, "\r\n  \x1b[35m\"Ya want to know about \x1b[1mViolet\x1b[22m do ya?  She is every warrior's\x1b[0m")
			func_slowecho(connection, "\r\n  \x1b[35mwet dream...But forget it, Lad, she only goes for the type\x1b[0m")
			func_slowecho(connection, "\r\n  \x1b[35mof guy who would help old peple...\"\x1b[0m\r\n")
			func_pauser(connection)
		if ( data[0] == 'c' or data[0] == 'C' ):
			connection.send('C')
			func_slowecho(connection, "\r\n  \x1b[35m\"Ya wanna change your name, eh?  Yeah..\x1b[0m")
			if ( user.getClass() == 1 ):
				thisTitle = "the Death Knight"
			elif ( user.getClass() == 2 ):
				thisTitle = "the Magiciain"
			else:
				thisTitle = "the Thief"
			thisPrice = user.getLevel() * 500
			func_slowecho(connection, "\r\n  \x1b[35m"+user.thisFullname+" "+thisTitle+" does sound kinda funny..\x1b[0m")
			func_slowecho(connection, "\r\n  \x1b[35mit would cost ya "+str(thisPrice)+" gold... Deal?\"\x1b[0m")
			func_slowecho(connection, "\r\n  \x1b[32mChange your name? [\x1b[1mN\x1b[22m]\x1b[0m ")
			yesno = connection.recv(2)
			if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
				connection.send('Y')
				if ( user.getGold() < thisPrice ):
					func_slowecho("\r\n  \x1b[35m\"Then I suggest you go find some more gold...\"\x1b[0m\r\n")
				else:
					thisGoodName = False;
					func_slowecho(connection, "\r\n  \x1b[32mWhat'll it be? \x1b[1m: \x1b[0m")
					ann = func_getLine(connection)
					if ( not ann.isalnum() ):
						thisGoodName = False
					elif ( ann.rfind('barak') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mNaw, the real Barak would decapitate you if he found out. \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('seth able') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mYou are not God! \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('red dragon') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mOh go plague some other land! \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('seth') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mYou are not Seth Able!  Don't take his name in vain! \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('turgon') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mHaw.  Hardly - Turgon has muscles. \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('violet') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mHaw.  Hardly - Violet has breasts. \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('dragon') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mYou ain't Bruce Lee, so get out! \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('bartender') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mNah, the bartender is smarter than you! \x1b[31m**\x1b[0m\r\n")
					elif ( ann.rfind('chance') >= 0 ):
						func_slowecho(connection, "\r\n  \x1b[31m** \x1b[35mWhy not go take a chance with a rattlesnake? \x1b[31m**\x1b[0m\r\n")
					else:
						func_slowecho(connection, "\r\n  \x1b[32mName Changed.\x1b[0m\r\n")
						thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"users SET fullname = '"+user.dbc.escape_string(ann)+"' WHERE userid = "+str(user.thisUserID)
						user.db.execute(thisSQL)
						user.updateGold(thisPrice * -1)
			else:
				func_slowecho(connection, "\r\n  \x1b[35m\"Fine...Keep your stupid name...See if I care...\"\x1b[0m\r\n")
			func_pauser(connection)
		if ( data[0] == 'd' or data[0] == 'D' ):
			if ( user.getLevel() == 12 ):
				connection.send('D')
				func_slowecho(connection, "\r\n  \x1b[32mA \x1b[1;31mRed Dragon\x1b[0m\x1b[32m eh?  Have you tried to \x1b[1mS\x1b[22mearch?\r\n")
		if ( data[0] == 'g' or data[0] == 'G' ):
			connection.send('G')
			func_slowecho(connection, "\r\n  \x1b[35m\"You have \x1b[1;37mGems\x1b[0m\x1b[35m, eh?  I'll give ya a pint of magic elixer for two.\"\x1b[0m\r\n")
			func_slowecho(connection, "  \x1b[32mBuy how many elixers? : ")
			number = int(func_getLine(connection, True))
			if ( number > 0 ):
				if ( number * 2 > user.getGems() ):
					func_slowecho(connection, "\r\n  \x1b[31mYou don't have that many gems!\x1b[0m\r\n")
				else: # /*sell and process elixer */
					func_slowecho(connection, "\r\n  \x1b[32mIncrease which stat?\x1b[0m\r\n")
					func_slowecho(connection, func_normmenu("(H)itpoints"))
					func_slowecho(connection, func_normmenu("(S)trength"))
					func_slowecho(connection, func_normmenu("(V)itality"))
					func_slowecho(connection, func_normmenu("(N)evermind"))
					tinyQuit = False
					while( not tinyQuit ):
						func_slowecho(connection, "  \x1b[32mChoose : \x1b[0m")
						thisType = connection.recv(2)
						if ( thisType[0] == 'n' or thisType[0] == 'N' or thisType[0] == 'q' or thisType[0] == 'Q' or thisType[0] == 'r' or thisType[0] == 'R' ):
							connection.send('N')
							tinyQuit = True
						if ( thisType[0] == 'H' or thisType[0] == 'h' ):
							user.updateHPMax(number)
							user.updateHP(number)
							user.updateGems(number * -2)
							func_slowecho(connection, "\r\n  \x1b[32mYou feel as if your stamina is greater\r\n")
							tinyQuit = True
						if ( thisType[0] == 'S' or thisType[0] == 's' ):
							user.updateStrength(number)
							user.updateGems(number * -2)
							func_slowecho(connection, "\r\n  \x1b[32mYou feel as if your strength is greater\r\n")
							tinyQuit = True
						if ( thisType[0] == 'v' or thisType[0] == 'V' ):
							user.updateDefense(number)
							user.updateGems(number * -2)
							func_slowecho(connection, "\r\n  \x1b[32mYou feel as if your vitality is greater\r\n")
							tinyQuit = True
					func_slowecho(connection, "\r\n  \x1b[32mPleasure doing business with you\x1b[0m\r\n")

def rdi_menu_bartend(connection, art, user):
	""" Show bartender menu """
	ptime = func_maketime(user)
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mBartender\x1b[0m\r\n"
	thismenu += art.blueline()
	thismenu += "  \x1b[32mThe bartender escorts you into a back\x1b[0m\r\n"
	thismenu += "  \x1b[32mroom.  \x1b[35m\"I have heard yer name before kid...\x1b[0m\r\n"
	thismenu += "  \x1b[35mwhat do ya want to talk about?\"\x1b[0m\r\n\r\n"
	thismenu += func_normmenu("(V)iolet")
	thismenu += func_normmenu("(G)ems")
	#thismenu += func_normmenu("(B)ribe")
	thismenu += func_normmenu("(C)hange your name")
	thismenu += func_normmenu("(R)eturn to Bar")
	thismenu += "\r\n  \x1b[35m\"Well?\" \x1b[32mThe bartender inquires. \x1b[1;30m(V,G,B,C,R) (? for menu)\x1b[0m\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

