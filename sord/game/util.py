#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains basic player in-game utility displays / functions

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"
from ..base import func
from . import data

def readmail(user):
	""" Read waiting in-game e-mail. Very simple. """
	db = user.dbcon.cursor()
	db.execute("SELECT `id`, `from`, `message`, `sent` FROM mail WHERE `to` = ?", (user.thisUserID,))
	try:
		for (id, sender, message, sent) in db.fetchall():
			thismail  = "\r\n  \x1b[1;37mNew Mail...\x1b[0m\r\n"
			thismail += "\x1b[32m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\x1b[0m\r\n"
			thismail += "\x1b[32m  From: \x1b[1m" + user.userGetName(sender) + "\x1b[0m\r\n"
			thismail += "\x1b[32m  Date: \x1b[1m" + sent + "\x1b[0m\r\n"
			thismail += "\x1b[32m  Message: " + func.colorcode(message) + "\x1b[0m\r\n\r\n"
			#if ( not isinstance(thismail, None) ):
			user.write(thismail)
			user.pause()
	except TypeError:
		pass
	db.close()
	user.dbcon.execute("DELETE FROM mail WHERE `to` = ?", (user.thisUserID,))
	user.dbcon.commit()

def announce(user):
	""" Make announcment """
	user.write(func.casebold("\r\n  Your announcment? :-: ", 2))
	ann = func.getLine(user.ntcon, True)
	user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (ann, ))
	user.dbcon.commit()
	user.write(func.casebold("\r\n  Announcment Made!\r\n", 2))
	user.pause()

def sendmail(user):
	""" Send in game mail to a user """
	toid = finduser(user, "\r\n  \x1b[32mSend mail to which user?")
	if ( toid == 0 ):
		return False
	else:
		user.write("\r\n  \x1b[32mYour message \x1b[1m:\x1b[0m ")
		msg = func.getLine(user.ntcon, True)
		user.dbcon.execute("INSERT INTO mail (`to`, `from`, `message`) VALUES ( ?, ?, ? )", (toid, user.thisUserID, msg))
		user.dbcon.commit()
		user.write(func.casebold("\r\n  Message Sent\r\n", 2))
		user.pause()

def finduser(user, prompter):
	"""Find a user"""
	user.write(prompter + " \x1b[1;32m:\x1b[0;32m-\x1b[1;32m:\x1b[0m ")
	name = func.getLine(user.ntcon, True)
	returnID = user.userExist(name)
	if ( returnID > 0 ) :
		if ( returnID == user.thisUserID ):
			user.write(func.casebold("\r\n  Masturbation is gross...\r\n", 1))
			return 0
		else:
			user.write("\r\n  \x1b[32mDid you mean \x1b[1m" + user.userGetName(returnID) +"\x1b[0m \x1b[1;30m(Y/N)\x1b[0m\x1b[32m ?\x1b[0m ")
			yesno = user.ntcon.recv(2)
			if ( yesno[0] == "Y" or yesno[0] == "y" ):
				return returnID
			else:
				return 0
	else:
		return 0

def viewstats(user):
	""" View Player Stats """
	output  = "\r\n\r\n\x1b[1m\x1b[37m"+user.thisFullname+"\x1b[0m\x1b[32m's Stats...\r\n"
	output += user.art.line()
	output += "\x1b[32m Experience    : \x1b[1m"+str(user.exp)+"\x1b[0m\r\n"
	output += "\x1b[32m Level         : \x1b[1m"+str(user.level)+"\x1b[0m" + func.padnumcol(str(user.level), 20) + "\x1b[32mHitPoints          : \x1b[1m"+str(user.hp)+" \x1b[22mof\x1b[1m "+str(user.hpmax)+"\x1b[0m\r\n"
	output += "\x1b[32m Forest Fights : \x1b[1m"+str(user.ffight)+"\x1b[0m" + func.padnumcol(str(user.ffight), 20) + "\x1b[32mPlayer Fights Left : \x1b[1m"+str(user.pfight)+"\x1b[0m\r\n"
	output += "\x1b[32m Gold In Hand  : \x1b[1m"+str(user.gold)+"\x1b[0m" + func.padnumcol(str(user.gold), 20) + "\x1b[32mGold In Bank       : \x1b[1m"+str(user.bank)+"\x1b[0m\r\n"
	output += "\x1b[32m Weapon        : \x1b[1m"+data.weapon[user.weapon]+"\x1b[0m" + func.padnumcol(data.weapon[user.weapon], 20) + "\x1b[32mAttack Strength    : \x1b[1m"+str(user.str)+"\x1b[0m\r\n"
	output += "\x1b[32m Armor         : \x1b[1m"+data.armor[user.armor]+"\x1b[0m" + func.padnumcol(data.armor[user.armor], 20) + "\x1b[32mDefensive Strength : \x1b[1m"+str(user.defence)+"\x1b[0m\r\n"
	output += "\x1b[32m Charm         : \x1b[1m"+str(user.charm)+"\x1b[0m" + func.padnumcol(str(user.charm), 20) + "\x1b[32mGems               : \x1b[1m"+str(user.gems)+"\x1b[0m\r\n\r\n"
	for skillnum in [1,2,3]:
		if ( user.cls == skillnum or user.getSkillPoint(skillnum) > 0 ):
			output += "\x1b[32m The "+data.classes[skillnum]+" Skills: \x1b[1m"
			if ( user.getSkillPoint(skillnum) > 0 ):
				output +=  str(user.getSkillPoint(skillnum)) + func.padnumcol(str(user.getSkillPoint(skillnum)), 11)
			else:
				output += "NONE     "
			output += func.padnumcol(data.classes[skillnum], 12)
			output += "\x1b[0m\x1b[32mUses Today: (\x1b[1m"+str(user.getSkillUse(skillnum))+"\x1b[22m)\x1b[0m\r\n"
	output += "\r\n \x1b[1;32mYou are currently interested in \x1b[37mThe "+data.classes[user.cls]+" \x1b[32mskills.\r\n\r\n";
	return output
	
def who(user):
	""" Who's Online """
	db = user.dbcon.cursor()
	db.execute("SELECT o.userid, fullname, whence FROM users u, online o WHERE o.userid = u.userid ORDER BY whence ASC")
	output  = "\r\n\r\n\x1b[1;37m                     Warriors In The Realm Now\x1b[22;32m\x1b[0m\r\n"
	output += user.art.line()
	for line in db.fetchall():
		output += "  \x1b[1;32m" + line[1] + func.padnumcol(line[1], 28)
		output += "\x1b[0m\x1b[32mArrived At             \x1b[1;37m" + str(line[2]) + "\x1b[0m\r\n"
	db.close()
	return output + "\r\n"

def dailyhappen(noprmpt, user):
	""" View Daily Happenings
	
	* @param bool $noprmpt Do not prompt for additions. """
	db = user.dbcon.cursor()
	db.execute("SELECT data FROM (SELECT * FROM daily ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id")
	output  = "\r\n\r\n\x1b[1;37mRecent Happenings\033[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	for line in db.fetchall():
		output += "    " + func.colorcode(line[0])
		output += "\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	if ( not noprmpt ) :
		output +=  "\n\x1b[32m(\x1b[1;35mC\x1b[22;32m)ontinue  \x1b[32m(\x1b[1;35mT\x1b[22;32m)odays happenings again  \x1b[1;32m[\x1b[35mC\x1b[32m] \x1b[22m:-: "
	db.close()
	return output

def list(art, dbc):
	""" Player List """
	db = dbc.cursor()
	db.execute("SELECT userid, fullname, exp, level, cls, spclm, spcld, spclt, sex, alive FROM users WHERE 1 ORDER BY exp DESC")
	output = "\r\n\r\n\x1b[32m    Name                    Experience    Level    Mastered    Status\x1b[0m\r\n";
	output += art.line()
	for line in db.fetchall():
		if ( line[8] == 2 ):
			lineSex = "\x1b[1;35mF\x1b[0m "
		else:
			lineSex = "  "
			
		if ( line[4] == 1 ):
			lineClass = "\x1b[1;31mD \x1b[0m"
		elif ( line[4] == 2 ):
			lineClass = "\x1b[1;31mM \x1b[0m"
		else:
			lineClass = "\x1b[1;31mT \x1b[0m"
		
		lineMaster = ""
		if ( line[6] > 19 ):
			if ( line[6] > 39 ):
				lineMaster += "\x1b[1;37mD \x1b[0m"
			else:
				lineMaster += "\x1b[37mD \x1b[0m"
		else:
			lineMaster += "  "
			
		if ( line[5] > 19 ):
			if ( line[5] > 39 ):
				lineMaster += "\x1b[1;37mM \x1b[0m"
			else:
				lineMaster += "\x1b[37mM \x1b[0m"
		else:
			lineMaster += "  "
						
		if ( line[7] > 19 ):
			if ( line[7] > 39 ):
				lineMaster += "\x1b[1;37mT \x1b[0m"
			else:
				lineMaster += "\x1b[37mT \x1b[0m"
		else:
			lineMaster += "  "
									
		
		if ( line[9] == 1 ):
			lineStatus = "\x1b[1;32mAlive\x1b[0m"
		else:
			lineStatus = "\x1b[31m Dead\x1b[0m"
			
		output += lineSex + lineClass + "\x1b[32m" + line[1] + func.padnumcol(str(line[1]), 24) + func.padright(str(line[2]), 10)
		output += func.padright(str(line[3]), 9) + "       " + lineMaster + "    " + lineStatus + "\r\n"
	db.close()
	return output + "\r\n"
	
def flowers(user):
	""" The forest flowers """
	output  = "\r\n\r\n  \x1b[1;37mStudy the forest flowers\x1b[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	db = user.dbcon.cursor()
	db.execute("SELECT data, nombre FROM (SELECT * FROM flowers ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
	for (data, nombre) in db.fetchall():
		output += "    \x1b[32m"+nombre+" \x1b[1;37msays... \x1b[0m\x1b[32m" + func.colorcode(data)
		output += "\x1b[0m\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	output += "\r\n  \x1b[32mAdd to the conversation? (Y/N) \x1b[1m: \x1b[0m"
	db.close()
	user.write(output)
	yesno = user.ntcon.recv(2)
	if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
		user.write(func.casebold("Y\r\n  What!? What do you want? :-: ", 2))
		ann = func.getLine(user.ntcon, True)
		user.dbcon.execute("INSERT INTO flowers ( `data`, `nombre` ) VALUES ( ?, ? )", (safeann, user.thisFullname))
		user.dbcon.commit()
		user.write(func.casebold("\r\n  Idiocy added!\r\n", 2))
		user.pause()
	else:
		user.write('N\r\n')

def dirt(user):
	""" The slaughter dirt """
	output  = "\r\n\r\n  \x1b[1;37mExamine the dirt\x1b[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	db = user.dbcon.cursor()
	db.execute("SELECT data, nombre FROM (SELECT * FROM dirt ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
	for (data, nombre) in db.fetchall():
		output += "    \x1b[32m"+nombre+" \x1b[1;37msays... \x1b[0m\x1b[32m" + func.colorcode(data)
		output += "\x1b[0m\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	user.write(output)
	user.pause()

def newuser(user):
	""" Create a user """
	user.write(func.casebold("\r\nCreating a New Character...\r\n", 2))
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nPlease Choose a Username (12 characters MAX) :-: ", 2))
		newname = func.getLine(user.ntcon, True)
		newname = newname[:12]
		if ( user.userLoginExist(newname) ):
			user.write(func.casebold("\r\nName In Use!\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nAnd, how will you be addressed? (a Handle) (40 characters MAX) :-: ", 2))
		newfname = func.getLine(user.ntcon, True)
		newfname = newfname[:40]
		if ( newfname == "" ):
			user.write(func.casebold("\r\nHEY! No Anonymous Players!\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nPick a Password (12 characters MAX) :-: ", 2))
		newpass = func.getLine(user.ntcon, True)
		newpass = newpass[:12]
		if ( newpass == "" ):
			user.write(func.casebold("\r\nPassword MUST Not Be Empty\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nYour Sex (M/F) :-: ", 2))
		key = user.ntcon.recv(2)
		if not key: break
		if ( key[0] == 'm' or key[0] == 'M' ):
			user.write('M')
			newsexnum = 1
			thisLooper = True
			user.write(func.casebold("\r\nMy, what a girly man you are...\r\n", 2))
		if ( key[0] == 'f' or key[0] == 'F' ):
			user.write('F')
			newsexnum = 2
			thisLooper = True
			user.write(func.casebold("\r\nGee sweetheart, hope you don't break a nail...\r\n", 2))
	user.write(func.casebold("\r\nPick that which best describes your childhood.\r\nFrom an early age, you remember:\r\n\r\n", 2))
	user.write(func.normmenu("(D)abbling in the mystical forces"))
	user.write(func.normmenu("(K)illing a lot of woodland creatures"))
	user.write(func.normmenu("(L)ying, cheating, and stealing from the blind"))
	thisLooper = False
	while ( not thisLooper ):
		user.write(func.casebold("\r\nYour Choice (D/K/L) :-: ", 2))
		key = user.ntcon.recv(2)
		if not key: break
		if ( key[0] == 'k' or key[0] == 'K' ):
			user.write('K')
			newclassnum = 1
			thisLooper = True
			user.write(func.casebold("\r\nWelcome warrior to the ranks of the Death Knights!\n", 2))
		if ( key[0] == 'd' or key[0] == 'D' ):
			user.write('D')
			newclassnum = 2
			thisLooper = True
			user.write(func.casebold("\r\nFeel the force young jedi.!\n", 2))
		if ( key[0] == 'l' or key[0] == 'L' ):
			user.write('L')
			newclassnum = 3
			thisLooper = True
			user.write(func.casebold("\r\nYou're a real shitheel, you know that?\n", 2))
	user.dbcon.execute("INSERT INTO users (`username`, `password`, `fullname`, `sex`, `cls`) VALUES ( ?, ?, ?, ?, ?)", (newname, newpass, newfname, newsexnum, newclassnum))
	user.dbcon.commit()
	return newname
