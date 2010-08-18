#!/usr/bin/python
""" Saga of the Red Dragon - Player Editor

  * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
  * All attempts were made to be as close to the original as possible, 
  * including some original artwork, the original fight equations, and 
  * most especially the original spelling and punctuation mistakes.  Enjoy.

  * @author J.T.Sage
  * @copyright 2009-2011
  * @license http://sord.jtsage.com/LICENSE Disclaimer's License
  * @version 2.0"""

from . import func
from . import user
from ..game import data

class editor():

	def __init__(self, user):
		self.user = user
	
	def main_menu(self):
		user = self.user
		if ( user.sex == 1 ):
			sexo = "Male"
		else:
			sexo = "Female"
		thismsg =  "\r\n" + self.makecenter("** Saga Of The Red Dragon - User Editor v."+user.config.version+" **", 1) + "\r\n"
		thismsg += self.makecenter("Account Number: "+str(user.thisUserID), 7) + "\r\n\r\n"
		thismsg += self.makeentry(1, 'Name', 1, user.thisFullname) + self.makeentry(2, 'Level', 2, user.level) + "\r\n"
		thismsg += self.makeentry(3, 'Login Name', 1, user.thisUserName) + self.makeentry(4, 'Hit Points', 2, user.hp) + "\r\n"
		thismsg += self.makeentry(5, 'Experience', 1, user.exp) + self.makeentry(6, 'Hit Max', 2, user.hpmax) + "\r\n"
		thismsg += self.makeentry(7, 'Weapon', 1, data.weapon[user.weapon], False) + self.makeentry(8, 'Weapon Number', 2, user.weapon) + "\r\n"
		thismsg += self.makeentry(9, 'Armor', 1, data.armor[user.armor], False) + self.makeentry(0, 'Armor Number', 2, user.armor) + "\r\n"
		thismsg += self.makeentry('A', 'Seen Master', 1, user.master) + self.makeentry('B', 'Forest Fights', 2, user.ffight) + "\r\n"
		thismsg += self.makeentry('C', 'Player Fights', 1, user.pfight) + self.makeentry('D', 'Sex', 2, sexo) + "\r\n"
		thismsg += self.makeentry('E', 'Defence', 1, user.defence) + self.makeentry('F', 'Gems', 2, user.gems) + "\r\n"
		thismsg += self.makeentry('G', 'Strength', 1, user.str) + self.makeentry('H', 'Charm', 2, user.charm) + "\r\n"
		thismsg += self.makeentry('I', 'Seen Flirt', 1, user.flirt) + self.makeentry('J', 'Seen Bard', 2, user.sung) + "\r\n"
		thismsg += self.makeentry('K', 'Class', 1, '('+str(user.cls)+') '+data.classes[user.cls]) + self.makeentry('L', 'Dragon Kills', 2, user.dragon) + "\r\n"
		thismsg += self.makeentry('M', 'Gold in Hand', 1, user.gold) + self.makeentry('N', 'Player Kills', 2, user.pkill) + "\r\n"
		thismsg += self.makeentry('O', 'Gold in Bank', 1, user.bank) + self.makeentry('P', 'At The Inn', 2, user.atinn) + "\r\n"
		thismsg += self.makeentry('R', 'Has Horse', 1, user.horse) + self.makeentry('S', 'Has Fairy', 2, user.fairy) + "\r\n"
		thismsg += self.makeentry('T', 'Player Alive', 1, user.alive) + self.makeentry('U', 'Times Laid', 2, user.fuck) + "\r\n"
		thismsg += "\r\n  \x1b[32m(\x1b[1;35m$\x1b[0;32m) Edit Skills   \x1b[32m(\x1b[1;35m[\x1b[0;32m) Previous Player   \x1b[32m(\x1b[1;35m]\x1b[0;32m) Next Player   \x1b[32m(\x1b[1;35m#\x1b[0;32m) Jump to Player\r\n"
		thismsg += self.makecenter("Input key to change / toggle, 'Q' to Quit", 7) + "\r\n"
		return thismsg

	def skill_menu(self):
		user = self.user
		thismsg  = "\r\n" + self.makecenter("** Saga Of The Red Dragon - Skills Editor v."+user.config.version+" **", 1) + "\r\n"
		thismsg += self.makecenter("Account Number: "+str(user.thisUserID)+" / "+user.thisFullname, 7) + "\r\n\r\n"
		thismsg += self.makecenter("*** Death Knight Skills ***", 2) + "\r\n"
		thismsg += self.makeentry(1, 'Skill Points', 1, user.getSkillPoint(1)) + self.makeentry('A', 'Uses Today', 2, user.getSkillUse(1)) + "\r\n\r\n"
		thismsg += self.makecenter("*** Magical Skills ***", 2) + "\r\n"
		thismsg += self.makeentry(2, 'Skill Points', 1, user.getSkillPoint(2)) + self.makeentry('B', 'Uses Today', 2, user.getSkillUse(2)) + "\r\n\r\n"
		thismsg += self.makecenter("*** Thief Skills ***", 2) + "\r\n"
		thismsg += self.makeentry(3, 'Skill Points', 1, user.getSkillPoint(3)) + self.makeentry('C', 'Uses Today', 2, user.getSkillUse(3)) + "\r\n\r\n"
		thismsg += self.makecenter("Input key to change, 'R' to Return to main", 7) + "\r\n"
		return thismsg

	def skill_logic(self):
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit):
			if ( not skipDisp ):
				user.write(self.skill_menu())
			skipDisp = False
			choice = user.ntcon.recv(2)
			if not choice: break
			elif ( choice[0] == 'r' or choice[0] == 'R' or choice[0] == 'q' or choice[0] == 'Q' ):
				thisQuit = True
			elif ( choice[0] == '1' ):
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Skill Points :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - user.getSkillPoint(1)
						user.updateSkillPoint(1,hptoadd)
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == '2' ):
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Skill Points :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - user.getSkillPoint(2)
						user.updateSkillPoint(2,hptoadd)
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == '3' ):
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Skill Points :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - user.getSkillPoint(3)
						user.updateSkillPoint(3,hptoadd)
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'a' or choice[0] == 'A' ):
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Uses Today :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - user.getSkillUse(1)
						user.updateSkillUse(1,hptoadd)
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'b' or choice[0] == 'B' ):
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Uses Today :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - user.getSkillUse(2)
						user.updateSkillUse(2,hptoadd)
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'c' or choice[0] == 'C' ):
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Uses Today :-:", 2)))
					if ( thisIn >= 0 ):
						hptoadd = thisIn - user.getSkillUse(3)
						user.updateSkillUse(3,hptoadd)
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			else:
				skipDisp = True

	def run(self):
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit):
			if ( not skipDisp ):
				user.write(self.main_menu())
			skipDisp = False
			choice = user.ntcon.recv(2)
			if not choice: break
			elif ( choice[0] == 'q' or choice[0] == 'Q' ): # Quit
				thisQuit = True
			elif ( choice[0] == '1' ): # Full Name
				thisIn = func.getLine(user.ntcon, True, func.casebold("New Full Name :-:", 2))
				if not thisIn: break
				else:
					user.dbcon.execute("UPDATE users SET fullname = ? WHERE userid = ?", (thisIn, user.thisUserID))
					user.dbcon.commit()
					user.thisFullname = thisIn
			elif ( choice[0] == '2' ): # Level
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Level :-:", 2)))
					if ( thisIn > 0 and thisIn < 13 ):
						user.level = thisIn
					else:
						user.write(func.casebold("\r\nNot a valid level!", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid level", 1))
					user.pause()
			elif ( choice[0] == '3' ): # Login Name
				thisIn = func.getLine(user.ntcon, True, func.casebold("New Login Name :-:", 2))
				if not thisIn: break
				else:
					user.dbcon.execute("UPDATE users SET username = ? WHERE userid = ?", (thisIn, user.thisUserID))
					user.dbcon.commit()
					user.thisUserName = thisIn
			elif ( choice[0] == '4' ): # HP
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Hit Points :-:", 2)))
					if ( thisIn >= 0 ):
						user.hp = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == '5' ): # Experience
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Experience Points :-:", 2)))
					if ( thisIn >= 0 ):
						user.exp = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == '6' ): # Max HP
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Max Hit Points :-:", 2)))
					if ( thisIn > 0 ):
						user.hpmax = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == '8' or choice[0] == '7' ): # Weapon
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Weapon Number :-:", 2)))
					if ( thisIn >= 0 and thisIn < 16 ):
						user.weapon = thisIn
					else:
						user.write(func.casebold("\r\nNot a valid choice", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == '0' or choice[0] == '9' ): # Armor
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Armor Number :-:", 2)))
					if ( thisIn >= 0 and thisIn < 16 ):
						user.armor = thisIn
					else:
						user.write(func.casebold("\r\nNot a valid choice", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'a' or choice[0] == 'A' ): # Seen Master
				if ( user.master ):
					user.master = 0
				else:
					user.master = 1
			elif ( choice[0] == 'b' or choice[0] == 'B' ): # Forest Fights
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Forest Fights :-:", 2)))
					if ( thisIn >= 0 ):
						user.ffight = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'c' or choice[0] == 'C' ): # Player Fights
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Player Fights :-:", 2)))
					if ( thisIn >= 0 ):
						user.pfight = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'd' or choice[0] == 'D' ): # Sex
				if ( user.sex == 1 ):
					user.sex = 2
				else:
					user.sex = 1
			elif ( choice[0] == 'e' or choice[0] == 'E' ): # Defense
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Defence :-:", 2)))
					if ( thisIn >= 0 ):
						user.defence = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'f' or choice[0] == 'F' ): # Gems
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Gems :-:", 2)))
					if ( thisIn >= 0 ):
						user.gems = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'g' or choice[0] == 'G' ): # Strength
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Strength :-:", 2)))
					if ( thisIn >= 0 ):
						user.str = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'h' or choice[0] == 'H' ): # Charm
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Charm :-:", 2)))
					if ( thisIn >= 0 ):
						user.charm = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'i' or choice[0] == 'I' ): # Flirt
				if ( user.flirt ):
					user.flirt = 0
				else:
					user.flirt = 1
			elif ( choice[0] == 'j' or choice[0] == 'J' ): # Bard
				if ( user.sung ):
					user.sung = 0
				else:
					user.sung = 1
			elif ( choice[0] == 'k' or choice[0] == 'K' ): # Class
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Class Number :-:", 2)))
					if ( thisIn > 0 and thisIn < 4 ):
						user.cls = thisIn
					else:
						user.write(func.casebold("\r\nMust be 1, 2, or 3", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'l' or choice[0] == 'L' ): # Dragon
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Dragon Kills :-:", 2)))
					if ( thisIn >= 0 ):
						user.dkill = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'm' or choice[0] == 'M' ): # Gold
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Gold in Hand :-:", 2)))
					if ( thisIn >= 0 ):
						user.gold = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'n' or choice[0] == 'N' ): # Player Kills
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Player Kills :-:", 2)))
					if ( thisIn >= 0 ):
						user.pkill = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'o' or choice[0] == 'O' ): # Bank
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Gold in Bank :-:", 2)))
					if ( thisIn >= 0 ):
						user.bank = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == 'p' or choice[0] == 'P' ): # Inn
				if ( user.atinn ):
					user.atinn = 0
				else:
					user.atinn = 1
			elif ( choice[0] == 'r' or choice[0] == 'R' ): # Horse
				if ( user.horse ):
					user.horse = 0
				else:
					user.horse = 1
			elif ( choice[0] == 's' or choice[0] == 'S' ): # Fairy
				if ( user.fairy ):
					user.fairy = 0
				else:
					user.fairy = 1
			elif ( choice[0] == 't' or choice[0] == 'T' ): # Dead
				if ( user.alive ):
					user.alive = 0
				else:
					user.alive = 1
			elif ( choice[0] == 'u' or choice[0] == 'U' ): # Fucks
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("New Times Laid :-:", 2)))
					if ( thisIn >= 0 ):
						user.fuck = thisIn
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == ']' ): # Next
				newLogin = user.userGetLogin(user.thisUserID + 1)
				try:
					if ( newLogin == 0 ):
						user.write(func.casebold("\r\nLast Record Reached", 1))
						user.pause()
					else:
						user = user.sorduser(newLogin, user.dbcon, user.ntcon, user.art, user.log, user.linespeed, user.noise)
				except ValueError:
					user = user.sorduser(newLogin, user.dbcon, user.ntcon, user.art, user.log, user.linespeed, user.noise)
			elif ( choice[0] == '[' ): # Prev
				newLogin = user.userGetLogin(user.thisUserID - 1)
				try:
					if ( newLogin == 0 ):
						user.write(func.casebold("\r\nFirst Record Reached", 1))
						user.pause()
					else:
						user = user.sorduser(newLogin, user.dbcon, user.ntcon, user.art, user.log, user.linespeed, user.noise)
				except ValueError:
					user = user.sorduser(newLogin, user.dbcon, user.ntcon, user.art, user.log, user.linespeed, user.noise)
			elif ( choice[0] == '#' ): # By Rec Num
				try:
					thisIn = int(func.getLine(user.ntcon, True, func.casebold("Jump to User Number :-:", 2)))
					if ( thisIn >= 0 ):
						newLogin = user.userGetLogin(thisIn)
						try:
							if ( newLogin == 0 ):
								user.write(func.casebold("\r\nNon-valid Record", 1))
								user.pause()
							else:
								user = user.sorduser(newLogin, user.dbcon, user.ntcon, user.art, user.log, user.linespeed, user.noise)
						except ValueError:
							user = user.sorduser(newLogin, user.dbcon, user.ntcon, user.art, user.log, user.linespeed, user.noise)
					else:
						user.write(func.casebold("\r\nMust be positive", 1))
						user.pause()
				except ValueError:
					user.write(func.casebold("\r\nNot a valid number", 1))
					user.pause()
			elif ( choice[0] == '$' ): # Edit Skills
				self.skill_logic()
			else:
				skipDisp = True

	def makecenter(self, text, color):
		col = 40 - (len(text) / 2)
		ittr = 0
		retval = ""
		while ( ittr < col ):
			retval += " "
			ittr += 1
		return retval + func.casebold(text, color)
	
	def makeentry(self, option, text, col, value, editable = True):
		thisentry = ""
		if ( col == 1 ):
			thisentry += "  "
		fcol = 14 - len(text)
		ittr = 0
		retval = ""
		while ( ittr < fcol ):
			retval += " "
			ittr += 1
		thisentry += "\x1b[32m(\x1b[1;35m"+str(option)+"\x1b[0;32m) "+text+retval+":\x1b[1"
		if ( not editable ):
			thisentry += ";30"
		thisentry += "m"+str(value)
		if ( col == 1 ):
			xcol = 25 - len(str(value))
			ittr = 0
			while ( ittr < xcol ):
				thisentry += " "
				ittr += 1
		return thisentry + "\x1b[0m"