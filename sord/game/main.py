#!/usr/bin/python
"""
 * Contains main game loops
 *
"""
import random
from ..base import func
from . import util
from . import data
from . import menu

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
			elif ( key[0] == "a" or key[0] == "A" ):
				self.user.ntcon.send('A')
				self.user.jennielevel = 0
				thismod = abduls(self.user)
				thismod.run()
				del thismod
			elif ( key[0] == "k" or key[0] == "K" ):
				self.user.ntcon.send('K')
				self.user.jennielevel = 0
				module_arthurs(user)
			elif ( key[0] == "y" or key[0] == "Y" ):
				self.user.ntcon.send('Y')
				self.user.jennielevel = 0
				module_bank(user)
			elif ( key[0] == "h" or key[0] == "H" ):
				ntcon.send('H')
				self.user.jennielevel = 0
				module_heal(user)
			elif ( key[0] == "m" or key[0] == "M" ):
				self.user.ntcon.send('M')
				self.user.jennielevel = 0
				msg_announce(user)
			elif ( key[0] == "w" or key[0] == "W" ):
				self.user.ntcon.send('W')
				self.user.jennielevel = 0
				msg_sendmail(user)
			elif ( key[0] == "i" or key[0] == "I" ):
				ntcon.send('I')
				rdi_logic(user)
			elif ( key[0] == "f" or key[0] == "F" ):
				self.user.ntcon.send('F')
				self.user.jennielevel = 0
				module_forest(user)
			elif ( key[0] == 't' or key[0] == 'T' ):
				self.user.ntcon.send('T')
				self.user.jennielevel = 0
				module_turgon(user)
			elif ( key[0] == "1" ):
				self.user.ntcon.send("1\r\n")
				self.user.jennielevel = 0
				self.user.write(artwork.info(user))
				self.user.pause()
			elif ( key[0] == 's' or key[0] == 'S' ):
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
					log.add(" !!! ENTERING USER EDITOR !!!")
					editor_main_logic(user)
					log.add(" !!! EXITING USER EDITOR !!!")
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
	
