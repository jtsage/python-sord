#!/usr/bin/python
""" Saga of the Red Dragon - Player Editor

  * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
  * All attempts were made to be as close to the original as possible, 
  * including some original artwork, the original fight equations, and 
  * most especially the original spelling and punctuation mistakes.  Enjoy.

  * @author J.T.Sage
  * @copyright 2009-2011
  * @license http://sord.jtsage.com/LICENSE Disclaimer's License
  * @version 0.9.9"""
import MySQLdb
from sord.functions import *
from sord.user import *
from sord.data import *
from sord.art import *
from config import sord

mySord = sord()
myArt = art()

mySQLconn = MySQLdb.connect(host=str(mySord.sqlServer()), db=str(mySord.sqlDatabase()), user=str(mySord.sqlUser()), passwd=str(mySord.sqlPass()))
mySQLcurs = mySQLconn.cursor()

user = sordUser('1', mySQLconn, mySQLcurs, 'aa', myArt)
firstName = user.userGetLogin(1)
user = sordUser(firstName, mySQLconn, mySQLcurs, 'aa', myArt)

def editskills(user):
	thisQuit = False
	while ( not thisQuit):
		print makecenter("** Saga Of The Red Dragon - Skills Editor v."+mySord.version()+" **", 1)
		print makecenter("Account Number: "+str(user.thisUserID)+" / "+user.thisFullname, 7) + "\n"
		print makecenter("*** Death Knight Skills ***", 2)
		print makeentry(1, 'Skill Points', 1, user.getSkillPoint(1)) + makeentry('A', 'Uses Today', 2, user.getSkillUse(1)) + "\n"
		print makecenter("*** Magical Skills ***", 2)
		print makeentry(2, 'Skill Points', 1, user.getSkillPoint(2)) + makeentry('B', 'Uses Today', 2, user.getSkillUse(2)) + "\n"
		print makecenter("*** Thief Skills ***", 2)
		print makeentry(3, 'Skill Points', 1, user.getSkillPoint(3)) + makeentry('C', 'Uses Today', 2, user.getSkillUse(3)) + "\n"
		print makecenter("Input key to change, 'R' to Return to main", 7)
		choice = raw_input()
		if not choice: 
			choice = " "
		if ( choice[0] == 'r' or choice[0] == 'R' or choice[0] == 'q' or choice[0] == 'Q' ):
			thisQuit = True
		elif ( choice[0] == '1' ):
			try:
				thisIn = int(raw_input(func_casebold("New Skill Points :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getSkillPoint(1)
					user.updateSkillPoint(1,hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == '2' ):
			try:
				thisIn = int(raw_input(func_casebold("New Skill Points :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getSkillPoint(2)
					user.updateSkillPoint(2,hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == '3' ):
			try:
				thisIn = int(raw_input(func_casebold("New Skill Points :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getSkillPoint(3)
					user.updateSkillPoint(3,hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'a' or choice[0] == 'A' ):
			try:
				thisIn = int(raw_input(func_casebold("New Uses Today :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getSkillUse(1)
					user.updateSkillUse(1,hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'b' or choice[0] == 'B' ):
			try:
				thisIn = int(raw_input(func_casebold("New Uses Today :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getSkillUse(2)
					user.updateSkillUse(2,hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'c' or choice[0] == 'C' ):
			try:
				thisIn = int(raw_input(func_casebold("New Uses Today :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getSkillUse(3)
					user.updateSkillUse(3,hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"

def editloop():
	global user
	thisQuit = False
	while ( not thisQuit):
		print makecenter("** Saga Of The Red Dragon - User Editor v."+mySord.version()+" **", 1)
		print makecenter("Account Number: "+str(user.thisUserID), 7) + "\n"
		print makeentry(1, 'Name', 1, user.thisFullname) + makeentry(2, 'Level', 2, user.getLevel())
		print makeentry(3, 'Login Name', 1, user.thisUserName) + makeentry(4, 'Hit Points', 2, user.getHP())
		print makeentry(5, 'Experience', 1, user.getExperience()) + makeentry(6, 'Hit Max', 2, user.getHPMax())
		print makeentry(7, 'Weapon', 1, weapon[user.getWeapon()], False) + makeentry(8, 'Weapon Number', 2, user.getWeapon())
		print makeentry(9, 'Armor', 1, armor[user.getArmor()], False) + makeentry(0, 'Armor Number', 2, user.getArmor())
		print makeentry('A', 'Seen Master', 1, user.didMaster()) + makeentry('B', 'Forest Fights', 2, user.getForestFight())
		if ( user.getSex() == 1 ):
			sexo = "Male"
		else:
			sexo = "Female"
		print makeentry('C', 'Player Fights', 1, user.getPlayerFight()) + makeentry('D', 'Sex', 2, sexo)
		print makeentry('E', 'Defence', 1, user.getDefense()) + makeentry('F', 'Gems', 2, user.getGems())
		print makeentry('G', 'Strength', 1, user.getStrength()) + makeentry('H', 'Charm', 2, user.getCharm())
		print makeentry('I', 'Seen Flirt', 1, user.didFlirt()) + makeentry('J', 'Seen Bard', 2, user.didBard())
		print makeentry('K', 'Class', 1, '('+str(user.getClass())+') '+classes[user.getClass()]) + makeentry('L', 'Dragon Kills', 2, user.getDragon())
		print makeentry('M', 'Gold in Hand', 1, user.getGold()) + makeentry('N', 'Player Kills', 2, user.getKiller())
		print makeentry('O', 'Gold in Bank', 1, user.getBank()) + makeentry('P', 'At The Inn', 2, user.didInn())
		print makeentry('R', 'Has Horse', 1, user.didHorse()) + makeentry('S', 'Has Fairy', 2, user.didFairy())
		print makeentry('T', 'Player Dead', 1, user.isDead()) + makeentry('U', 'Times Laid', 2, user.getFuck())
		print "\n  \x1b[32m(\x1b[1;35m$\x1b[0;32m) Edit Skills   \x1b[32m(\x1b[1;35m[\x1b[0;32m) Previous Player   \x1b[32m(\x1b[1;35m]\x1b[0;32m) Next Player   \x1b[32m(\x1b[1;35m#\x1b[0;32m) Jump to Player"
		print makecenter("Input key to change / toggle, 'Q' to Quit", 7)
		choice = raw_input()
		if not choice: 
			choice = " "
		if ( choice[0] == 'q' or choice[0] == 'Q' ):
			thisQuit = True
		elif ( choice[0] == '1' ):
			thisIn = raw_input(func_casebold("New Full Name :-:", 2))
			if not thisIn: break
			else:
				thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"users SET fullname = '"+str(thisIn)+"' WHERE userid = "+str(user.thisUserID)
				user.db.execute(thisSQL)
				user.thisFullname = thisIn
		elif ( choice[0] == '2' ):
			try:
				thisIn = int(raw_input(func_casebold("New Level :-:", 2)))
				if ( thisIn > 0 and thisIn < 13 ):
					user.setLevel(thisIn)
				else:
					print "Not a valid level!"
			except ValueError:
				print "Not a valid level"
		elif ( choice[0] == '3' ):
			thisIn = raw_input(func_casebold("New Login Name :-:", 2))
			if not thisIn: break
			else:
				thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"users SET username = '"+str(thisIn)+"' WHERE userid = "+str(user.thisUserID)
				user.db.execute(thisSQL)
				user.thisUserName = thisIn
		elif ( choice[0] == '4' ):
			try:
				thisIn = int(raw_input(func_casebold("New Hit Points :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getHP()
					user.updateHP(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == '5' ):
			try:
				thisIn = int(raw_input(func_casebold("New Experience Points :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getExperience()
					user.updateExperience(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == '6' ):
			try:
				thisIn = int(raw_input(func_casebold("New Max Hit Points :-:", 2)))
				if ( thisIn > 0 ):
					hptoadd = thisIn - user.getHPMax()
					user.updateHPMax(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == '8' or choice[0] == '7' ):
			try:
				thisIn = int(raw_input(func_casebold("New Weapon Number :-:", 2)))
				if ( thisIn >= 0 and thisIn < 16 ):
					user.setWeapon(thisIn)
				else:
					print "Not a valid choice"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == '0' or choice[0] == '9' ):
			try:
				thisIn = int(raw_input(func_casebold("New Armor Number :-:", 2)))
				if ( thisIn >= 0 and thisIn < 16 ):
					user.setArmor(thisIn)
				else:
					print "Not a valid choice"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'a' or choice[0] == 'A' ):
			if ( user.didMaster() ):
				user.setMaster(0)
			else:
				user.setMaster()
		elif ( choice[0] == 'b' or choice[0] == 'B' ):
			try:
				thisIn = int(raw_input(func_casebold("New Forest Fights :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getForestFight()
					user.updateForestFight(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'c' or choice[0] == 'C' ):
			try:
				thisIn = int(raw_input(func_casebold("New Player Fights :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getPlayerFight()
					user.updatePlayerFight(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'd' or choice[0] == 'D' ):
			if ( user.getSex() == 1 ):
				user.setSex(2)
			else:
				user.setSex(1)
		elif ( choice[0] == 'e' or choice[0] == 'E' ):
			try:
				thisIn = int(raw_input(func_casebold("New Defence :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getDefense()
					user.updateDefense(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'f' or choice[0] == 'F' ):
			try:
				thisIn = int(raw_input(func_casebold("New Gems :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getGems()
					user.updateGems(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'g' or choice[0] == 'G' ):
			try:
				thisIn = int(raw_input(func_casebold("New Strength :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getStrength()
					user.updateStrength(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'h' or choice[0] == 'H' ):
			try:
				thisIn = int(raw_input(func_casebold("New Charm :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getCharm()
					user.updateCharm(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'i' or choice[0] == 'I' ):
			if ( user.didFlirt() ):
				user.setFlirt(0)
			else:
				user.setFlirt()
		elif ( choice[0] == 'j' or choice[0] == 'J' ):
			if ( user.didBard() ):
				user.setBard(0)
			else:
				user.setBard()
		elif ( choice[0] == 'k' or choice[0] == 'K' ):
			try:
				thisIn = int(raw_input(func_casebold("New Class Number :-:", 2)))
				if ( thisIn > 0 and thisIn < 4 ):
					user.setClass(thisIn)
				else:
					print "Must be 1, 2, or 3"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'l' or choice[0] == 'L' ):
			try:
				thisIn = int(raw_input(func_casebold("New Dragon Kills :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getDragon()
					user.setDragon(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'm' or choice[0] == 'M' ):
			try:
				thisIn = int(raw_input(func_casebold("New Gold in Hand :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getGold()
					user.updateGold(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif( choice[0] == 'n' or choice[0] == 'N' ):
			try:
				thisIn = int(raw_input(func_casebold("New Player Kills :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getKiller()
					user.setKiller(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'o' or choice[0] == 'O' ):
			try:
				thisIn = int(raw_input(func_casebold("New Gold in Bank :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getBank()
					user.updateBank(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == 'p' or choice[0] == 'P' ):
			if ( user.didInn() ):
				user.setInn(0)
			else:
				user.setInn(1)
		elif ( choice[0] == 'r' or choice[0] == 'R' ):
			if ( user.didHorse() ):
				user.setHorse(0)
			else:
				user.setHorse(1)
		elif ( choice[0] == 's' or choice[0] == 'S' ):
			if ( user.didFairy() ):
				user.setFairy(0)
			else:
				user.setFairy(1)
		elif ( choice[0] == 't' or choice[0] == 'T' ):
			if ( user.isDead() ):
				user.setDead(1)
			else:
				user.setDead()
		elif ( choice[0] == 'u' or choice[0] == 'U' ):
			try:
				thisIn = int(raw_input(func_casebold("New Times Laid :-:", 2)))
				if ( thisIn >= 0 ):
					hptoadd = thisIn - user.getFuck()
					user.updateFuck(hptoadd)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == ']' ):
			newLogin = user.userGetLogin(user.thisUserID + 1)
			try:
				if ( newLogin == 0 ):
					print "Last Record Reached"
				else:
					user = sordUser(newLogin, mySQLconn, mySQLcurs, 'aa', myArt)
			except ValueError:
				user = sordUser(newLogin, mySQLconn, mySQLcurs, 'aa', myArt)
		elif ( choice[0] == '[' ):
			newLogin = user.userGetLogin(user.thisUserID - 1)
			try:
				if ( newLogin == 0 ):
					print "First Record Reached"
				else:
					user = sordUser(newLogin, mySQLconn, mySQLcurs, 'aa', myArt)
			except ValueError:
				user = sordUser(newLogin, mySQLconn, mySQLcurs, 'aa', myArt)
		elif ( choice[0] == '#' ):
			try:
				thisIn = int(raw_input(func_casebold("Jump to User Number :-:", 2)))
				if ( thisIn >= 0 ):
					newLogin = user.userGetLogin(thisIn)
					try:
						if ( newLogin == 0 ):
							print "Non-valid Record"
						else:
							user = sordUser(newLogin, mySQLconn, mySQLcurs, 'aa', myArt)
					except ValueError:
						user = sordUser(newLogin, mySQLconn, mySQLcurs, 'aa', myArt)
				else:
					print "Must be positive"
			except ValueError:
				print "Not a valid number"
		elif ( choice[0] == '$' ):
			editskills(user)

def makecenter(text, color):
	col = 40 - (len(text) / 2)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
		
	return retval + func_casebold(text, color)
	
def makeentry(option, text, col, value, editable = True):
	thisentry = ""
	if ( col == 1 ):
		thisentry += "  "
		col = 14
		extra = True
	else:
		col = 14
		extra = False
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	thisentry += "\x1b[32m(\x1b[1;35m"+str(option)+"\x1b[0;32m) "
	thisentry += text + retval
	if ( editable ):
		thisentry += ":\x1b[1m"
	else:
		thisentry += ":\x1b[1;30m"
	thisentry += str(value)
	if ( extra ):
		xcol = 25 - len(str(value))
		ittr = 0
		xtxt = ""
		while ( ittr < xcol ):
			xtxt += " "
			ittr += 1
		thisentry += xtxt + "\x1b[0m"
	else:
		thisentry += "\x1b[0m"
	return thisentry
	

editloop()
