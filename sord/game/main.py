#!/usr/bin/python
"""
 * Contains main game loops
 *
"""
import random
from ..base import func
from ..base import peditor
from . import util
from . import data
from . import menu
from . import rdi
from . import forest
from ..sord import igm

class other():
	def __init__(self, user):
		self.user = user
	def run(self):
		""" Main Menu Logic """
		quitfull = False
		skipDisp = False
		while ( not quitfull ):
			if ( not skipDisp ):
				ptime = func.maketime(self.user)
				optionslist = ""
				self.user.write("\r\n\r\n\x1b[1;37m  Saga of the Red Dragon - \x1b[0m\x1b[32mOther Places\x1b[0m\r\n")
				self.user.write(self.user.art.line())
				self.user.write("\x1b[32m  You see some odd places to go...\r\n\r\n")
				for item in igm.igmlist:
					optionslist += item[0] + ","
					self.user.write(func.normmenu("("+item[0]+") "+item[2]))
				self.user.write("\r\n  \x1b[1;35mOther Places\x1b[0m \x1b[1;30m("+optionslist+"Q)\x1b[0m\x1b[1;30m (? for menu)\x1b[0m\r\n")
				self.user.write("  \x1b[32mYour command, \x1b[1m" + self.user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m")
			skipDisp = False
			key = self.user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == "?" ):
				skipDisp = False
			elif ( key[0] == "q" or key[0] == "Q" ):
				self.user.ntcon.send('Q')
				quitfull = True
			else:
				skipDisp = True
				for item in igm.igmlist:
					if ( key[0] == item[0] or key[0] == item[0].lower() ):
						self.user.write(key[0].upper())
						thismod = item[1]
						thismod.run(self.user)
						del thismod
						skipDisp = False
						
				
					

class mainmenu():
	def __init__(self, user):
		self.user = user
	def run(self):
		""" Main Menu Logic """
		quitfull = False
		skipDisp = False
		while ( not quitfull ):
			if ( not skipDisp ):
				if ( not self.user.expert ):
					self.user.write(menu.mainlong(self.user))
				self.user.write(menu.mainshort(self.user))
			skipDisp = False
			key = self.user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == "q" or key[0] == "Q" ):
				self.user.ntcon.send('Q')
				quitfull = True
			elif ( key[0] == "x" or key[0] == "X" ):
				self.user.ntcon.send('X')
				self.user.jennielevel = 0
				self.user.toggleXprt()
			elif ( key[0] == "v" or key[0] == "V" ):
				self.user.ntcon.send('V')
				self.user.jennielevel = 0
				self.user.write(util.viewstats(self.user))
				self.user.pause()
			elif ( key[0] == "d" or key[0] == "D" ):
				self.user.ntcon.send('D')
				self.user.jennielevel = 0
				self.user.write(util.dailyhappen(True, self.user))
				self.user.pause()
			elif ( key[0] == "?" ):
				self.user.ntcon.send('?')
				self.user.jennielevel = 0
				if ( self.user.expert ):
					self.user.write(menu.mainlong(self.user))
			elif ( key[0] == "p" or key[0] == "P" ):
				self.user.ntcon.send('P')
				self.user.jennielevel = 0
				self.user.write(util.who(self.user))
				self.user.pause()
			elif ( key[0] == "l" or key[0] == "L" ):
				self.user.ntcon.send('L')
				self.user.jennielevel = 0
				self.user.write(util.list(self.user.art, self.user.sqcon))
				self.user.pause()
			elif ( key[0] == "o" or key[0] == "O" ):
				self.user.ntcon.send('O')
				self.user.jennielevel = 0
				thismod = other(self.user)
				thismod.run()
				del thismod
			elif ( key[0] == "a" or key[0] == "A" ):
				self.user.ntcon.send('A')
				self.user.jennielevel = 0
				thismod = abduls(self.user)
				thismod.run()
				del thismod
			elif ( key[0] == "k" or key[0] == "K" ):
				self.user.ntcon.send('K')
				self.user.jennielevel = 0
				thismod = arthurs(self.user)
				thismod.run()
				del thismod
			elif ( key[0] == "y" or key[0] == "Y" ):
				self.user.ntcon.send('Y')
				self.user.jennielevel = 0
				thismod = bank(self.user)
				thismod.run()
				del thismod
			elif ( key[0] == "h" or key[0] == "H" ):
				ntcon.send('H')
				self.user.jennielevel = 0
				thismod = heal(self.user)
				thismod.run()
				del thismod
			elif ( key[0] == "m" or key[0] == "M" ): 
				self.user.ntcon.send('M')
				self.user.jennielevel = 0
				util.announce(user)
			elif ( key[0] == "w" or key[0] == "W" ): 
				self.user.ntcon.send('W')
				self.user.jennielevel = 0
				util.sendmail(user)
			elif ( key[0] == "i" or key[0] == "I" ):
				self.user.ntcon.send('I')
				thismod = rdi.rdi(self.user)
				thismod.run()
				del thismod
			elif ( key[0] == "f" or key[0] == "F" ):
				self.user.ntcon.send('F')
				self.user.jennielevel = 0
				thismod = forest.ffight(self.user, heal(self.user))
				thismod.run()
				del thismod
			elif ( key[0] == 't' or key[0] == 'T' ): #"""RIGHT HERE"""
				self.user.ntcon.send('T')
				self.user.jennielevel = 0
				module_turgon(user)
			elif ( key[0] == "1" ): 				#"""RIGHT HERE"""
				self.user.ntcon.send("1\r\n")
				self.user.jennielevel = 0
				self.user.write(artwork.info(user))
				self.user.pause()
			elif ( key[0] == 's' or key[0] == 'S' ): #"""RIGHT HERE"""
				self.user.ntcon.send('S')
				self.user.jennielevel = 0
				module_killer(user)
			elif ( key[0] == 'j' or key[0] == 'J' ):
				skipDisp = True
				if self.user.jennielevel == 0 :
					self.user.jennielevel = 1
				else:
					self.user.jennielevel = 0
			elif ( key[0] == 'e' or key[0] == 'E' ):
				skipDisp = True
				if self.user.jennielevel == 1:
					self.user.jennielevel = 2
				else:
					self.user.jennielevel = 0
			elif ( key[0] == 'n' or key[0] == 'N' ):
				skipDisp = True
				if self.user.jennielevel == 2:
					self.user.jennielevel = 3
				elif self.user.jennielevel == 3:
					self.user.jennielevel = 4
				else:
					self.user.jennielevel = 0
			elif ( key[0] == "!" ):	
				if (self.user.thisUserID == 1):
					self.user.log.add(" !!! ENTERING USER EDITOR !!!")
					thismod = peditor.editor(self.user)
					thismod.run()
					del thismod
					self.user.log.add(" !!! EXITING USER EDITOR !!!")
				else:
					skipDisp = True
			elif ( key[0] == "@" ):
				self.user.toggleQuick()
				self.user.write('@')
			else:
				skipDisp = True
				self.user.jennielevel = 0

class intro():
	def __init__(self, connection, config, art, log, sqc, lineconfig):
		self.config = config
		self.art = art
		self.sqc = sqc
		self.lineconfig = lineconfig
		self.connection = connection
		self.log = log
		
	def run(self):
		quitter = False
		skipDisp = False
		while ( not quitter ):
			if ( not skipDisp ):
				func.slowecho(self.connection, self.art.banner(), self.lineconfig[0], self.lineconfig[1])
			skipDisp = False
			key = self.connection.recv(2)
			if not key: break
			elif ( key == "Q" or key == "q" ):
				self.connection.send('Q')
				self.connection.send("NO CARRIER\r\n\r\n")
				raise Exception('normal', "User quit at intro menu.")
				quitter = True
			elif ( key == "L" or key == "l" ):
				self.connection.send('L')
				func.slowecho(self.connection, util.list(self.art, self.sqc), self.lineconfig[0], self.lineconfig[1])
				func.pauser(self.connection)
			elif ( key == "E" or key == "e" ):
				self.connection.send('E')
				self.log.add('   ** User Logging In::' + str(self.connection.getpeername()))
				quitter = True
			elif ( key == 'S' or key == 's' ):
				func.slowecho(self.connection, "S\r\n")
				for storyitem in data.story:
					func.slowecho(self.connection, func.casebold("  \x1b[37m" + storyitem + "\r\n", 7), self.lineconfig[0], self.lineconfig[1])
				func.pauser(self.connection)
			else:
				skipDisp = True

class abduls():
	def __init__(self, user):
		self.user = user
	def run(self):
		""" Abdul's Armor"""
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp):
				if ( not self.user.expert ):
					self.user.write(self.user.art.abdul())
			self.user.write(menu.abdul(self.user))
			skipDisp = False
			key = self.user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'b' or key[0] == 'B' ):
				self.user.write('B')
				self.user.write(self.user.art.armbuy())
				self.user.write("\r\n\r\n\x1b[32mYour choice? \x1b[1m:\x1b[22m-\x1b[1m:\x1b[0m ")
				try:
					number = int(func.getLine(self.user.ntcon, True))
				except ValueError:
					number = 0
				if ( number > 0 and number < 16 ):
					if ( self.user.armor > 0 ):
						self.user.write(func.casebold("\r\nYou cannot hold 2 sets of Armor!\r\n", 1))
						self.user.pause()
					else:
						if ( self.user.gold < data.armorprice[number] ):
							self.user.write(func.casebold("\r\nYou do NOT have enough Gold!\n", 1))
							self.user.pause()
						else:
							if ( self.user.defence < data.armorndef[number] ):
								self.user.write(func.casebold("\r\nYou are NOT strong enough for that!\r\n", 1))
								self.user.pause()
							else:
								self.user.write(func.casebold("\r\nI'll sell you my Best "+data.armor[number]+" for "+str(data.armorprice[number])+" gold.  OK? ", 2)) 
								yesno = self.user.ntcon.recv(2)
								if not yesno: break
								if ( yesno[0] == "Y" or yesno[0] == "y" ):
									self.user.write('Y')
									self.user.armor = number
									self.user.gold -= data.armorprice[number]
									self.user.defence += data.armordef[number]
									self.user.write(func_casebold("\r\nPleasure doing business with you!\r\n", 2))
									self.user.pause()
								else:
									self.user.write(func_casebold("\r\nFine then...\r\n", 2))
									self.user.pause()
			elif ( key[0] == 's' or key[0] == 'S' ):
				self.user.write('S')
				sellpercent = 50 + random.randint(1, 10)
				sellarmor = self.user.armor
				if ( sellarmor > 0 ):
					sellprice = ((sellpercent * data.armorprice[sellarmor]) // 100 )
					self.user.write(func.casebold("\r\nHmm...  I'll buy that "+data.armor[sellarmor]+" for "+str(sellprice)+" gold.  OK? ", 2))
					yesno = self.user.ntcon.recv(2)
					if not yesno: break
					if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
						self.user.write('Y')
						self.user.armor = 0
						self.user.gold += sellprice
						self.user.defence -= ((60 * data.armordef[sellarmor]) // 100)
						self.user.write(func.casebold("\r\nPleasure doing business with you!\r\n", 2))
						self.user.pause()
					else:
						self.user.write(func.casebold("\r\nFine then...\r\n", 2))
						self.user.pause()
				else:
					self.user.write(func.casebold("\r\nYou have nothing I want!\r\n", 1))
					self.user.pause()
			elif ( key[0] == "?" ):
				self.user.write('?')
				if ( self.user.expert ):
					self.user.write(self.user.art.abdul())
			elif ( key[0] == 'Y' or key[0] == 'y' ):
				self.user.write('Y')
				self.user.write(util.viewstats(self.user))
				self.user.pause()
			elif ( key[0] == 'Q' or key[0] == 'q' or key[0] == 'R' or key[0] == 'r' ):
				self.user.write('R')
				thisQuit = True
			else:
				skipDisp = True

class heal():
	def __init__(self, user):
		self.user = user
	def run(self):
		""" Healers Hut Logic """
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				user.write(menu.heal(user))
			skipDisp = False
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( data[0] == 'h' or data[0] == 'H' ):
				user.write('H')
				hptoheal = user.hpmax - user.hp
				if ( hptoheal < 1 ):
					user.write(func.casebold("\r\n  You do NOT need healing!\r\n", 2))
				else:
					perhpgold = user.level * 5
					if ( user.gold < perhpgold ):
						user.write(func.casebold("\r\n  You are too poor to heal anything!\r\n)", 2))
					else:
						fullcosttoheal = hptoheal * perhpgold
						canaffordtoheal =  ( user.gold - ( user.gold % perhpgold ) ) / perhpgold
						if ( canaffordtoheal >= hptoheal ):
							canaffordtoheal = hptoheal
						user.gold -= (canaffordtoheal * perhpgold)
						user.hp += canaffordtoheal
						user.write("\r\n  \x1b[32m\x1b[1m"+str(canaffordtoheal)+" \x1b[22mHitPoints are healed and you feel much better!\x1b[0m\r\n")
						user.pause()
			elif ( data[0] == 'c' or data[0] == 'C' ):
				user.write('C')
				hptoheal = user.hpmax - user.hp
				if ( hptoheal < 1 ):
					user.write(func.casebold("\r\n  You do NOT need healing!\r\n", 2))
				else:
					user.write("\r\n  \x1b[32mHow much to heal warror? \x1b[1m: \x1b[0m")
					try:
						number = int(func.getLine(user.ntcon, True))
					except ValueError:
						number = 0
					if ( number > hptoheal ):
						number = hptoheal
					if ( number > 0 ):
						perhpgold = user.level * 5
						costforaction = perhpgold * number
						if ( costforaction > user.gold ):
							user.write(func.casebold("\r\n  You do not have enough gold for that!\r\n", 1))
						else:
							user.gold -= costforaction
							user.hp += number
							user.write("\r\n  \x1b[32m\x1b[1m"+str(number)+" \x1b[22mHitPoints are healed and you feel much better!\x1b[0m\r\n")
							user.pause()
			else:
				skipDisp = True
			
class arthurs():
	def __init__(self, user):
		self.user = user
	def run(self):
		"""King Arthur's Weapons"""
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if ( not user.expert ):
					user.write(user.art.arthur())
				user.write(menu.arthur(user))
			skipDisp = False
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 'b' or data[0] == 'B' ):
				user.write('B')
				user.write(user.art.wepbuy())
				user.write("\r\n\r\n\x1b[32mYour choice? \x1b[1m:\x1b[22m-\x1b[1m:\x1b[0m ")
				try:
					number = int(func.getLine(user.ntcon, True))
				except ValueError:
					number = 0
				if ( number > 0 and number < 16 ):
					if ( user.weapon > 0 ):
						user.write(func.casebold("\r\nYou cannot hold 2 Weapons!\r\n", 1))
						user.pause()
					else:
						if ( user.gold < data.weaponprice[number] ):
							user.write(func.casebold("\r\nYou do NOT have enough Gold!\n", 1))
							user.pause
						else:
							if ( user.str < data.weaponnstr[number] ):
								user.write(func.casebold("\r\nYou are NOT strong enough for that!\r\n", 1))
								user.pause()
							else:
								user.write(func.casebold("\r\nI'll sell you my Favorite "+data.weapon[number]+" for "+str(data.weaponprice[number])+" gold.  OK? ", 2)) 
								yesno = user.ntcon.recv(2)
								if not yesno: break
								if ( yesno[0] == "Y" or yesno[0] == "y" ):
									user.write('Y')
									user.weapon = number
									user.gold -= data.weaponprice[number]
									user.str += data.weaponstr[number]
									user.write(func.casebold("\r\nPleasure doing business with you!\r\n", 2))
									user.pause()
								else:
									user.write(func.casebold("\r\nFine then...\r\n", 2))
									user.pause()
			elif ( data[0] == 's' or data[0] == 'S' ):
				user.write('S')
				sellpercent = 50 + random.randint(1, 10)
				sellweapon = user.weapon
				if ( sellweapon > 0 ):
					sellprice = ((sellpercent * data.weaponprice[sellweapon]) // 100 )
					user.write(func.casebold("\r\nHmm...  I'll buy that "+data.weapon[sellweapon]+" for "+str(sellprice)+" gold.  OK? ", 2))
					yesno = user.ntcon.recv(2)
					if not yesno: break
					if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
						user.write('Y')
						user.weapon = 0
						user.gold += sellprice
						user.str -= ((60 * data.weaponstr[sellweapon]) // 100)
						user.write(func.casebold("\r\nPleasure doing business with you!\r\n", 2))
						user.pause()
					else:
						user.write(func.casebold("\r\nFine then...\r\n", 2))
						user.pause()
				else:
					user.write(func.casebold("\r\nYou have nothing I want!\r\n", 1))
					user.pause()
			elif ( data[0] == "?" ):
				user.write('?')
				if ( user.expert ):
					user.write(user.art.arthur())
			elif ( data[0] == 'Y' or data[0] == 'y' ):
				user.write('Y')
				user.write(util.viewstats(user))
				user.pause()
			elif ( data[0] == 'Q' or data[0] == 'q' or data[0] == 'R' or data[0] == 'r' ):
				user.write('R')
				thisQuit = True
			else:
				skipDisp = True
			
class bank():
	def __init__(self, user):
		self.user = user
	def run(self):
		""" Ye Olde Bank """
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if ( not user.expert ):
					user.write(user.art.bank())
				user.write(menu.bank(user))
			skipDisp = False
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
				user.write('Q')
				thisQuit = True
			elif ( data[0] == 'd' or data[0] == 'D' ):
				user.write('D')
				user.write("\r\n  \x1b[32mDeposit how much? \x1b[1;30m(1 for all) \x1b[1;32m:\x1b[0m ")
				try:
					number = int(func.getLine(user.ntcon, True))
				except ValueError:
					number = 0
				if ( number > user.gold ):
					user.write(func.casebold("\r\n  You don't have that much gold!\r\n", 1))
					user.pause()
				elif ( number > 0 ):
					if ( number == 1 ):
						number = user.gold
					user.bank += number
					user.gold -= number
					user.write(func.casebold("\r\n  Gold deposited\r\n", 2))
					user.pause()
				else:
					pass
			elif ( data[0] == 'w' or data[0] == 'W' ):
				user.write('W')
				user.write("\r\n  \x1b[32mWithdraw how much? \x1b[1;30m(1 for all) \x1b[1;32m:\x1b[0m ")
				try:
					number = int(func.getLine(user.ntcon, True))
				except ValueError:
					number = 0
				if ( number > user.bank ):
					user.write(func.casebold("\r\n  You don't have that much gold in the bank!\r\n", 1))
					user.pause()
				elif ( number > 0 ):
					if ( number == 1 ):
						number = user.bank
					user.gold += number
					user.bank -= number
					user.write(func.casebold("\r\n  Gold widthdrawn\r\n", 2))
					user.pause()
				else:
					pass
			elif ( data[0] == 't' or data[0] == 'T' ):
				user.write('T')
				touser = module_finduser(user, "\r\n  \x1b[32mTransfer to which player? \x1b[1;32m:\x1b[0m ")
				if ( touser > 0 ):
					user.write("\r\n  \x1b[32mTransfer how much? \x1b[1;32m:\x1b[0m ")
					try:
						number = int(func.getLine(user.ntcon, True))
					except ValueError:
						number = 0
					if ( number > user.gold ):
						user.write(func.casebold("\r\n  You don't have that much gold!\r\n", 1))
						user.pause()
					elif ( number > 0 ):
						user.dbcon.execute("UPDATE stats SET gold = (gold + ?) WHERE userid = ?", (number, touser))
						user.dbcon.commit()
						user.gold -= number
						user.write(func.casebold("\r\n  Gold transfered\r\n", 2))
						user.pause()
					else:
						user.write(func.casebold("\r\n Cheap Ass!\r\n", 2))
				else:
					user.write(func.casebold("\r\n  No user by that name found!\r\n", 1))
					user.pause()
			else:
				skipDisp = True

